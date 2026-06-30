import json
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


def executar_gitleaks(alvo: str) -> list:
    """
    Executa o Gitleaks no diretório alvo e retorna os achados como lista.

    Usa um arquivo temporário para receber o relatório JSON e o remove
    ao final, independente de erros.
    """
    with tempfile.NamedTemporaryFile(
        suffix=".json", delete=False, mode="w"
    ) as tmp:
        relatorio = Path(tmp.name)

    cmd = [
        "gitleaks",
        "detect",
        "--source", alvo,
        "--report-path", str(relatorio),
        "--report-format", "json",
        "--no-git",
        "--exit-code", "0",   # não falha se encontrar segredos
    ]

    dados = []
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
    except FileNotFoundError:
        logger.error("Gitleaks não encontrado no PATH.")
        return []
    except subprocess.TimeoutExpired:
        logger.error("Gitleaks excedeu o tempo limite de execução.")
        return []
    finally:
        # Garante que o arquivo temporário seja lido e removido
        if relatorio.exists():
            try:
                dados = json.loads(relatorio.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.error("Falha ao ler relatório do Gitleaks: %s", exc)
            finally:
                relatorio.unlink(missing_ok=True)

    return dados if isinstance(dados, list) else []
