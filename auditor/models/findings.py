from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Finding:
    """Representa uma vulnerabilidade encontrada durante a auditoria."""

    title: str
    severity: str
    source: str
    file: str
    description: Optional[str] = field(default=None)

    def __post_init__(self):
        self.severity = self.severity.upper()

    def __str__(self) -> str:
        return f"[{self.source}] {self.severity} | {self.file} | {self.title}"


# ---------------------------------------------------------------------------
# Normalizadores — convertem a saída bruta de cada ferramenta para Finding
# ---------------------------------------------------------------------------

def normalizar_semgrep(dados_json: dict) -> list[Finding]:
    findings = []
    if not dados_json or "results" not in dados_json:
        return findings

    for item in dados_json.get("results", []):
        extra = item.get("extra", {})
        findings.append(
            Finding(
                title=extra.get("message", "Sem descrição"),
                severity=extra.get("severity", "INFO"),
                source="Semgrep",
                file=item.get("path", "desconhecido"),
            )
        )
    return findings


def normalizar_gitleaks(dados_json: list) -> list[Finding]:
    findings = []
    if not dados_json:
        return findings

    for item in dados_json:
        if not isinstance(item, dict):
            continue
        findings.append(
            Finding(
                title=f"Segredo exposto: {item.get('Description', 'Sem descrição')}",
                severity="CRITICAL",
                source="Gitleaks",
                file=item.get("File", "desconhecido"),
                description=item.get("RuleID"),
            )
        )
    return findings


def normalizar_dependencias(dados_json) -> list[Finding]:
    findings = []
    if not dados_json:
        return findings

    # Erros retornados pelos scanners
    if isinstance(dados_json, dict) and "erro" in dados_json:
        return findings

    # Formato npm audit (dict com chave "vulnerabilities")
    if isinstance(dados_json, dict):
        vulnerabilidades = dados_json.get("vulnerabilities", {})
        if isinstance(vulnerabilidades, dict):
            for nome, info in vulnerabilidades.items():
                detalhes = info.get("title") or info.get("name") or nome
                severidade = str(info.get("severity") or "HIGH").upper()
                findings.append(
                    Finding(
                        title=f"Dependência vulnerável: {detalhes}",
                        severity=severidade,
                        source="npm audit",
                        file="package.json",
                    )
                )
        return findings

    # Formato pip-audit (lista de dicts)
    if isinstance(dados_json, list):
        for item in dados_json:
            if not isinstance(item, dict):
                continue
            nome = item.get("name") or item.get("package") or "dependência"
            for vuln in item.get("vulns") or []:
                descricao = (
                    vuln.get("description")
                    or vuln.get("id")
                    or "Vulnerabilidade detectada"
                )
                severidade = str(vuln.get("severity") or "HIGH").upper()
                findings.append(
                    Finding(
                        title=f"{nome}: {descricao}",
                        severity=severidade,
                        source="pip-audit",
                        file="requirements.txt",
                    )
                )

    return findings
