import json
import subprocess
import logging

logger = logging.getLogger(__name__)


def executar_semgrep(alvo: str) -> dict:
    """
    Executa o Semgrep no diretório alvo e retorna o resultado como dict.

    Retorna um dict vazio em caso de falha de parsing ou execução.
    """
    cmd = ["semgrep", "--config=auto", alvo, "--json", "--quiet"]

    try:
        resultado = subprocess.run(
            cmd,
            capture_output=True,
            encoding="utf-8",
            text=True,
            timeout=300,
        )
    except FileNotFoundError:
        logger.error("Semgrep não encontrado no PATH.")
        return {}
    except subprocess.TimeoutExpired:
        logger.error("Semgrep excedeu o tempo limite de execução.")
        return {}

    if resultado.stderr:
        logger.debug("Semgrep stderr: %s", resultado.stderr[:500])

    if not resultado.stdout.strip():
        logger.warning("Semgrep retornou saída vazia.")
        return {}

    try:
        return json.loads(resultado.stdout)
    except json.JSONDecodeError as exc:
        logger.error("Falha ao decodificar JSON do Semgrep: %s", exc)
        return {}
