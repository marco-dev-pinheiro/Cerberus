import json
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def _executar_comando(cmd: list[str], cwd: str | None = None) -> str | None:
    """Executa um subprocesso e retorna stdout, ou None em caso de erro."""
    try:
        resultado = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=180,
        )
        # Tanto 0 (sem vulns) quanto 1 (vulns encontradas) são saídas esperadas
        if resultado.returncode not in (0, 1):
            logger.warning(
                "Comando %s terminou com código %d: %s",
                cmd[0],
                resultado.returncode,
                resultado.stderr.strip()[:300],
            )
            return None
        return resultado.stdout.strip() or None
    except FileNotFoundError:
        logger.warning("Ferramenta '%s' não encontrada no PATH.", cmd[0])
        return None
    except subprocess.TimeoutExpired:
        logger.error("Comando '%s' excedeu o tempo limite.", cmd[0])
        return None


def _parse_json(raw: str, ferramenta: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        logger.error("Falha ao decodificar JSON de '%s': %s", ferramenta, exc)
        return None


def auditoria_dependencias(alvo: str):
    """
    Detecta o tipo de projeto e executa o scanner de dependências adequado.

    - Python (requirements.txt)  → pip-audit
    - Node.js (package.json)     → npm audit

    Retorna os dados brutos (dict ou list) para normalização posterior,
    ou um dict com chave "erro" em caso de falha.
    """
    alvo_path = Path(alvo).resolve()

    req_txt = alvo_path / "requirements.txt"
    pkg_json = alvo_path / "package.json"

    if req_txt.exists():
        logger.info("Detectado projeto Python — executando pip-audit...")
        saida = _executar_comando(
            ["pip-audit", "-r", str(req_txt), "-f", "json"]
        )
        if saida is None:
            return {"erro": "pip-audit falhou ou não está instalado."}
        dados = _parse_json(saida, "pip-audit")
        return dados if dados is not None else {"erro": "JSON inválido do pip-audit"}

    if pkg_json.exists():
        logger.info("Detectado projeto Node.js — executando npm audit...")
        saida = _executar_comando(["npm", "audit", "--json"], cwd=str(alvo_path))
        if saida is None:
            return {"erro": "npm audit falhou ou não está disponível."}
        dados = _parse_json(saida, "npm audit")
        return dados if dados is not None else {"erro": "JSON inválido do npm audit"}

    return {"erro": "Nenhum arquivo de dependências encontrado (requirements.txt ou package.json)."}
