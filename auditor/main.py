"""
auditor/main.py
━━━━━━━━━━━━━━━
CLI do Cerberus. Thin client — toda lógica vive em auditor/core/pipeline.py.

Uso:
    python -m auditor.main --target <caminho-do-projeto>
    python auditor/main.py --target <caminho-do-projeto>
"""

import argparse
import logging
import sys

from auditor.core.pipeline import executar_auditoria, ResultadoAuditoria

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _callback_cli(etapa: str, detalhe: str) -> None:
    """Exibe o progresso da auditoria no terminal."""
    icones = {
        "semgrep":      "🔬",
        "gitleaks":     "🔑",
        "dependencias": "📦",
        "score":        "📊",
        "ia":           "🤖",
        "relatorio":    "📄",
    }
    icone = icones.get(etapa, "→")
    print(f"  {icone}  {detalhe}")


def _imprimir_resumo(resultado: ResultadoAuditoria) -> None:
    nivel = resultado.nivel_risco
    score = resultado.score
    detalhes = resultado.contagem_por_severidade

    print("\n" + "=" * 54)
    print("  AUDITORIA CONCLUÍDA")
    print(f"  Total de achados : {resultado.total_findings}")
    print(f"  Nível de Risco   : {nivel}")
    print(f"  Score Total      : {score}")
    print("  Detalhes:")
    for sev, qtd in detalhes.items():
        if qtd:
            print(f"    {sev:<10} {qtd}")
    print("=" * 54)
    print(f"\n📄 Relatório: {resultado.caminho_relatorio}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cerberus",
        description="Cerberus — Auditor de segurança para repositórios de código.",
    )
    parser.add_argument(
        "--target",
        metavar="CAMINHO",
        help="Caminho do projeto a auditar (padrão: diretório atual).",
    )
    args = parser.parse_args()

    print("\n🛡️  Cerberus — AI Security Auditor\n")
    resultado = executar_auditoria(alvo=args.target, callback=_callback_cli)

    if resultado is None:
        logger.error("Auditoria não pôde ser concluída.")
        sys.exit(1)

    _imprimir_resumo(resultado)
    sys.exit(0)


if __name__ == "__main__":
    main()
