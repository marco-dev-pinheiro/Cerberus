import logging
from datetime import datetime
from pathlib import Path
from auditor.models.findings import Finding

logger = logging.getLogger(__name__)

_PASTA_RELATORIOS = Path("reports_resultado")

_ICONES_SEVERIDADE: dict[str, str] = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🔵",
    "INFO": "⚪",
}


def _icone_risco(nivel: str) -> str:
    mapa = {"CRÍTICO": "🚨", "ALTO": "🔴", "MÉDIO": "🟡", "BAIXO": "🟢"}
    return mapa.get(nivel, "❓")


def gerar_relatorio_markdown(
    projeto: str,
    findings: list[Finding],
    resultado_risco: dict,
    analise_ia: str,
) -> Path:
    """
    Gera o relatório de auditoria em Markdown e o salva em reports_resultado/.

    Retorna o caminho do arquivo gerado.
    """
    _PASTA_RELATORIOS.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    arquivo = _PASTA_RELATORIOS / f"{timestamp}-auditoria.md"

    nivel = resultado_risco["nivel_risco"]
    score = resultado_risco["score_total"]
    detalhes = resultado_risco["detalhes"]

    linhas: list[str] = [
        "# 🛡️ Relatório de Auditoria de Segurança — Cerberus\n",
        f"**Projeto:** `{projeto}`  ",
        f"**Data:** {timestamp}  ",
        f"**Nível de Risco:** {_icone_risco(nivel)} {nivel}  ",
        f"**Score Total:** {score}  \n",
        "---\n",
        "## 📊 Resumo por Severidade\n",
        "| Severidade | Quantidade |",
        "| :--- | :---: |",
    ]

    for sev, qtd in detalhes.items():
        icone = _ICONES_SEVERIDADE.get(sev, "")
        linhas.append(f"| {icone} {sev} | {qtd} |")

    linhas += [
        "\n---\n",
        "## 🔍 Achados Detalhados\n",
    ]

    if findings:
        for idx, f in enumerate(findings, 1):
            icone = _ICONES_SEVERIDADE.get(f.severity.upper(), "")
            linhas += [
                f"### {idx}. {icone} `{f.severity}` — {f.title}\n",
                f"- **Arquivo:** `{f.file}`",
                f"- **Origem:** {f.source}",
            ]
            if f.description:
                linhas.append(f"- **Detalhes:** {f.description}")
            linhas.append("")
    else:
        linhas.append("✅ Nenhuma vulnerabilidade encontrada.\n")

    linhas += [
        "---\n",
        "## 🤖 Análise da IA\n",
        analise_ia,
    ]

    arquivo.write_text("\n".join(linhas), encoding="utf-8")
    logger.info("Relatório salvo em: %s", arquivo)
    return arquivo
