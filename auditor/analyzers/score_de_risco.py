from auditor.models.findings import Finding

# Mapeamento de aliases de severidade para o padrão interno
_ALIASES_SEVERIDADE: dict[str, str] = {
    "ERROR": "HIGH",
    "SEV-HIGH": "HIGH",
    "WARNING": "MEDIUM",
    "SEV-MEDIUM": "MEDIUM",
    "NOTE": "LOW",
    "SEV-LOW": "LOW",
}

_PESOS: dict[str, int] = {
    "CRITICAL": 10,
    "HIGH": 5,
    "MEDIUM": 3,
    "LOW": 1,
    "INFO": 0,
}

_NIVEIS: list[tuple[int, str]] = [
    (40, "CRÍTICO"),
    (20, "ALTO"),
    (5, "MÉDIO"),
    (0, "BAIXO"),
]


def _normalizar_severidade(severidade: str) -> str:
    """Converte aliases para o padrão interno e garante capitalização correta."""
    s = severidade.upper().strip()
    return _ALIASES_SEVERIDADE.get(s, s)


def calcular_score_risco(findings: list[Finding]) -> dict:
    """
    Calcula o score de risco a partir de uma lista de achados.

    Retorna um dict com:
        - score_total (int)
        - nivel_risco (str)
        - detalhes (dict com contagem por severidade)
    """
    contagem: dict[str, int] = {k: 0 for k in _PESOS}
    score_total = 0

    for finding in findings:
        severidade = _normalizar_severidade(finding.severity)
        peso = _PESOS.get(severidade, 1)
        score_total += peso

        if severidade in contagem:
            contagem[severidade] += 1

    nivel = "BAIXO"
    for limite, nome in _NIVEIS:
        if score_total > limite:
            nivel = nome
            break

    return {
        "score_total": score_total,
        "nivel_risco": nivel,
        "detalhes": contagem,
    }
