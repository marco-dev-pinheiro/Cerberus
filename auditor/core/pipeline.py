"""
auditor/core/pipeline.py
━━━━━━━━━━━━━━━━━━━━━━━━
Motor central do Cerberus.

Este módulo é o único lugar onde o pipeline de auditoria é implementado.
Tanto a CLI (main.py) quanto a interface gráfica (app.py) o consomem
sem duplicar nenhuma lógica.

Contrato público:
    executar_auditoria(alvo, callback) -> ResultadoAuditoria | None
"""

import logging
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from auditor.scanners.semgrep_scanner import executar_semgrep
from auditor.scanners.gitleaks_scanner import executar_gitleaks
from auditor.scanners.dependency_scanner import auditoria_dependencias
from auditor.models.findings import (
    Finding,
    normalizar_semgrep,
    normalizar_gitleaks,
    normalizar_dependencias,
)
from auditor.analyzers.score_de_risco import calcular_score_risco
from auditor.llm.llm_analyzer import analisar_findings_com_ia
from auditor.reports.markdown_report import gerar_relatorio_markdown

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------

# Callback chamado a cada etapa: callback(etapa: str, detalhe: str)
ProgressCallback = Callable[[str, str], None]


@dataclass
class ResultadoAuditoria:
    """Resultado completo de uma auditoria. Retornado por executar_auditoria()."""

    alvo: Path
    findings: list[Finding]
    resultado_risco: dict
    analise_ia: str
    caminho_relatorio: Path
    ferramentas_usadas: list[str] = field(default_factory=list)

    # Atalhos de conveniência
    @property
    def score(self) -> int:
        return self.resultado_risco["score_total"]

    @property
    def nivel_risco(self) -> str:
        return self.resultado_risco["nivel_risco"]

    @property
    def contagem_por_severidade(self) -> dict[str, int]:
        return self.resultado_risco["detalhes"]

    @property
    def total_findings(self) -> int:
        return len(self.findings)


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _ferramenta_disponivel(nome: str) -> bool:
    """Verifica se uma ferramenta externa está no PATH."""
    disponivel = shutil.which(nome) is not None
    if disponivel:
        logger.info("✅ %s disponível", nome)
    else:
        logger.warning("⚠️  %s não encontrado — etapa ignorada", nome)
    return disponivel


def _noop(_etapa: str, _detalhe: str) -> None:
    """Callback vazio padrão — não faz nada."""


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

def ferramentas_status() -> dict[str, bool]:
    """
    Retorna o status de disponibilidade de cada ferramenta externa.

    Útil para a UI exibir os scanners ativos antes de iniciar a auditoria.
    """
    return {
        "semgrep": _ferramenta_disponivel("semgrep"),
        "gitleaks": _ferramenta_disponivel("gitleaks"),
        "dependencias": True,   # pip-audit/npm audit: verificados em tempo de execução
        "ia": True,             # Ollama: opcional, falha graciosamente
    }


def executar_auditoria(
    alvo: str | Path,
    callback: ProgressCallback = _noop,
) -> ResultadoAuditoria | None:
    """
    Executa o pipeline completo de auditoria de segurança.

    Parâmetros
    ----------
    alvo:
        Caminho do projeto a auditar. Aceita str ou Path.
    callback:
        Função opcional chamada a cada etapa do pipeline com
        (etapa: str, detalhe: str). Usada pela UI para atualizar
        a barra de progresso sem acoplar a lógica de negócio ao Streamlit.

    Retorna
    -------
    ResultadoAuditoria ou None se o alvo não existir.
    """
    alvo_path = Path(alvo).expanduser().resolve()
    logger.info("Iniciando auditoria em: %s", alvo_path)

    if not alvo_path.exists():
        logger.error("Caminho não encontrado: %s", alvo_path)
        return None

    todos_findings: list[Finding] = []
    ferramentas_usadas: list[str] = []

    # ── Semgrep ──────────────────────────────────────────────────────────────
    callback("semgrep", "Executando análise estática...")
    if _ferramenta_disponivel("semgrep"):
        logger.info("🔬 Semgrep iniciado")
        dados = executar_semgrep(str(alvo_path))
        achados = normalizar_semgrep(dados)
        todos_findings.extend(achados)
        ferramentas_usadas.append("semgrep")
        logger.info("   Semgrep: %d achado(s)", len(achados))
        callback("semgrep", f"{len(achados)} achado(s) encontrado(s)")
    else:
        callback("semgrep", "Não disponível — ignorado")

    # ── Gitleaks ─────────────────────────────────────────────────────────────
    callback("gitleaks", "Detectando segredos expostos...")
    if _ferramenta_disponivel("gitleaks"):
        logger.info("🔑 Gitleaks iniciado")
        dados = executar_gitleaks(str(alvo_path))
        achados = normalizar_gitleaks(dados)
        todos_findings.extend(achados)
        ferramentas_usadas.append("gitleaks")
        logger.info("   Gitleaks: %d achado(s)", len(achados))
        callback("gitleaks", f"{len(achados)} achado(s) encontrado(s)")
    else:
        callback("gitleaks", "Não disponível — ignorado")

    # ── Dependências ─────────────────────────────────────────────────────────
    callback("dependencias", "Auditando dependências...")
    logger.info("📦 Scanner de dependências iniciado")
    dados = auditoria_dependencias(str(alvo_path))
    achados = normalizar_dependencias(dados)
    todos_findings.extend(achados)
    ferramentas_usadas.append("dependencias")
    logger.info("   Dependências: %d achado(s)", len(achados))
    callback("dependencias", f"{len(achados)} achado(s) encontrado(s)")

    # ── Score ─────────────────────────────────────────────────────────────────
    callback("score", "Calculando score de risco...")
    logger.info("📊 Calculando score")
    resultado_risco = calcular_score_risco(todos_findings)
    callback("score", f"Score: {resultado_risco['score_total']} — {resultado_risco['nivel_risco']}")

    # ── IA ────────────────────────────────────────────────────────────────────
    callback("ia", "Enviando para análise da IA...")
    logger.info("🤖 Análise por IA iniciada")
    analise_ia = analisar_findings_com_ia(todos_findings)
    ferramentas_usadas.append("ia")
    callback("ia", "Análise concluída")

    # ── Relatório ─────────────────────────────────────────────────────────────
    callback("relatorio", "Gerando relatório Markdown...")
    logger.info("📄 Gerando relatório")
    caminho_relatorio = gerar_relatorio_markdown(
        projeto=str(alvo_path),
        findings=todos_findings,
        resultado_risco=resultado_risco,
        analise_ia=analise_ia,
    )
    callback("relatorio", f"Salvo em: {caminho_relatorio}")
    logger.info("Auditoria concluída. Relatório: %s", caminho_relatorio)

    return ResultadoAuditoria(
        alvo=alvo_path,
        findings=todos_findings,
        resultado_risco=resultado_risco,
        analise_ia=analise_ia,
        caminho_relatorio=caminho_relatorio,
        ferramentas_usadas=ferramentas_usadas,
    )
