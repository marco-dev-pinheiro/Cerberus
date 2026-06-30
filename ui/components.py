"""
ui/components.py
━━━━━━━━━━━━━━━━
Componentes reutilizáveis da interface Cerberus.

Cada função recebe dados puros (sem lógica de negócio) e renderiza HTML
via st.markdown(). Nenhum import de auditor/ aqui — apenas Streamlit, theme
e biblioteca padrão (time/pathlib/subprocess, usados só para apresentação).
"""

import time
import streamlit as st
from pathlib import Path
from ui.theme import (
    CORES_SEVERIDADE,
    ICONES_SEVERIDADE,
    CORES_NIVEL,
    ICONES_NIVEL,
    APP_NOME,
    APP_TAGLINE,
    APP_VERSAO,
    APP_STATUS,
    APP_DESCRICAO,
)


# ---------------------------------------------------------------------------
# Hero header — topo da página
# ---------------------------------------------------------------------------

def render_hero_header() -> None:
    """Cabeçalho principal: nome, tagline, descrição, status e versão."""
    st.markdown(
        f"""
        <div class="cerberus-hero">
            <div class="hero-left">
                <div class="hero-title-row">
                    <h1>🐕 <span class="mark">{APP_NOME}</span></h1>
                </div>
                <div class="hero-tagline">{APP_TAGLINE}</div>
                <div class="hero-desc">{APP_DESCRICAO}</div>
            </div>
            <div class="hero-meta">
                <span class="status-pill"><span class="dot"></span>{APP_STATUS}</span>
                <span class="version-tag">{APP_VERSAO}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_eyebrow(icone: str, titulo: str) -> None:
    """Rótulo de seção pequeno e em caixa alta, usado para separar painéis."""
    st.markdown(
        f'<div class="section-eyebrow">{icone} {titulo}</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar — Marca
# ---------------------------------------------------------------------------

def render_brand() -> None:
    """Logo e subtítulo do Cerberus na sidebar."""
    st.sidebar.markdown(
        f"""
        <div class="cerberus-brand">
            <h1>🛡️ Cerberus</h1>
            <p>AI Security Auditor</p>
        </div>
        <hr class="cerberus-divider"/>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar — Status dos scanners
# ---------------------------------------------------------------------------

def render_scanner_status(status: dict[str, bool]) -> None:
    """Exibe os scanners disponíveis como badges na sidebar."""
    labels = {
        "semgrep":      ("Semgrep",       "🔬"),
        "gitleaks":     ("Gitleaks",      "🔑"),
        "dependencias": ("Dependências",  "📦"),
        "ia":           ("IA (Ollama)",   "🤖"),
    }
    st.sidebar.markdown('<div class="sidebar-section-label">Scanners</div>', unsafe_allow_html=True)
    for chave, (nome, icone) in labels.items():
        disponivel = status.get(chave, False)
        badge_cls = "badge-ok" if disponivel else "badge-off"
        badge_txt = "ativo" if disponivel else "indisponível"
        st.sidebar.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:0.5rem;
                        padding:0.3rem 0;font-size:0.85rem;">
                <span>{icone}</span>
                <span style="flex:1;color:var(--text-primary)">{nome}</span>
                <span class="badge {badge_cls}">{badge_txt}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.sidebar.markdown('<hr class="cerberus-divider"/>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Score card
# ---------------------------------------------------------------------------

def render_score_card(nivel: str, score: int, total_findings: int | None = None) -> None:
    """Card central com score, nível de risco e total de achados.

    `total_findings` é opcional: quando não informado, exibe um rótulo
    genérico em vez do contador de achados (evita depender de dados que
    a página chamadora pode não ter disponíveis).
    """
    cor = CORES_NIVEL.get(nivel, "#8B949E")
    icone = ICONES_NIVEL.get(nivel, "❓")
    rotulo = (
        f"{total_findings} achado(s) · score de risco"
        if total_findings is not None
        else "score de risco calculado pela auditoria"
    )
    st.markdown(
        f"""
        <div class="score-card">
            <div class="score-number" style="color:{cor}">{score}</div>
            <div class="score-nivel" style="color:{cor}">{icone} {nivel}</div>
            <div class="score-label">{rotulo}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Cards de severidade
# ---------------------------------------------------------------------------

def render_severity_cards(contagem: dict[str, int]) -> None:
    """
    Renderiza uma linha de cards com a contagem por severidade.
    Ordem fixa: CRITICAL → HIGH → MEDIUM → LOW → INFO.
    """
    ordem = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    cols = st.columns(len(ordem))
    for col, sev in zip(cols, ordem):
        qtd = contagem.get(sev, 0)
        cor = CORES_SEVERIDADE.get(sev, "#8B949E")
        icone = ICONES_SEVERIDADE.get(sev, "")
        with col:
            st.markdown(
                f"""
                <div class="sev-card" style="border-left-color:{cor}">
                    <div class="sev-label">{icone} {sev}</div>
                    <div class="sev-count" style="color:{cor}">{qtd}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Lista de findings
# ---------------------------------------------------------------------------

def render_findings(findings: list) -> None:
    """
    Lista os achados agrupados por severidade (CRITICAL primeiro).
    `findings` é uma lista de Finding (auditor/models/findings.py).
    """
    if not findings:
        st.info("✅ Nenhuma vulnerabilidade encontrada.")
        return

    ordem = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
    por_sev: dict[str, list] = {s: [] for s in ordem}
    for f in findings:
        sev = f.severity.upper()
        bucket = por_sev.get(sev, por_sev["INFO"])
        bucket.append(f)

    for sev in ordem:
        grupo = por_sev[sev]
        if not grupo:
            continue
        cor = CORES_SEVERIDADE.get(sev, "#8B949E")
        icone = ICONES_SEVERIDADE.get(sev, "")
        with st.expander(f"{icone} {sev} — {len(grupo)} achado(s)", expanded=(sev in ("CRITICAL", "HIGH"))):
            for f in grupo:
                st.markdown(
                    f"""
                    <div class="finding-row" style="border-left-color:{cor}">
                        <div class="finding-title">{f.title}</div>
                        <div class="finding-meta">
                            📁 {f.file} &nbsp;·&nbsp; 🔧 {f.source}
                            {"&nbsp;·&nbsp; " + f.description if f.description else ""}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ---------------------------------------------------------------------------
# Relatório IA — cabeçalho de relatório executivo
# ---------------------------------------------------------------------------

def render_ia_report_header(gerado_em: str | None = None) -> None:
    """
    Cabeçalho estilizado para o parecer da IA, dando a ele aparência de
    relatório executivo. O conteúdo do parecer (markdown vindo do backend)
    deve ser renderizado logo depois, via st.markdown(texto) — sem
    encapsular o texto em HTML, para preservar tabelas/blocos de código.
    """
    gerado_em = gerado_em or time.strftime("%d/%m/%Y às %H:%M")
    st.markdown(
        f"""
        <div class="ia-report-header">
            <div>
                <div class="ia-title">🤖 Parecer do Agente Cerberus</div>
                <div class="ia-subtitle">Relatório executivo gerado por IA (Ollama)</div>
            </div>
            <span class="ia-timestamp">gerado em {gerado_em}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Relatório — localização e botão de abrir pasta
# ---------------------------------------------------------------------------

def render_report_location(caminho: Path) -> None:
    """Exibe o caminho do relatório gerado e um botão para abrir a pasta."""
    st.markdown(
        f"""
        <div style="background:var(--bg-surface);border-radius:var(--radius-md);padding:1rem 1.25rem;
                    border:1px solid var(--border);margin-bottom:0.75rem;">
            <div style="font-size:0.68rem;color:var(--text-secondary);text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:0.3rem;">📄 Relatório gerado</div>
            <div style="font-size:0.85rem;color:var(--accent-strong, #79C0FF);word-break:break-all;
                        font-family:var(--font-mono);">
                {caminho}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("📂 Abrir pasta de relatórios", use_container_width=True):
        _abrir_pasta(caminho.parent)


def _abrir_pasta(pasta: Path) -> None:
    """Abre o gerenciador de arquivos do SO na pasta informada."""
    import subprocess, sys, os
    try:
        if sys.platform == "win32":
            os.startfile(str(pasta))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(pasta)])
        else:
            subprocess.Popen(["xdg-open", str(pasta)])
    except Exception as exc:
        st.warning(f"Não foi possível abrir a pasta automaticamente: {exc}")


# ---------------------------------------------------------------------------
# Histórico de relatórios
# ---------------------------------------------------------------------------

def render_historico(pasta_relatorios: Path) -> None:
    """Lista os relatórios existentes, do mais recente para o mais antigo."""
    relatorios = sorted(
        pasta_relatorios.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not relatorios:
        st.caption("Nenhum relatório anterior encontrado.")
        return

    for rel in relatorios:
        tamanho_kb = rel.stat().st_size / 1024
        st.markdown(
            f"""
            <div class="hist-item">
                <span>📄 {rel.name}</span>
                <span>{tamanho_kb:.1f} KB</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Barra de progresso por etapas
# ---------------------------------------------------------------------------

class BarraProgresso:
    """
    Gerencia a exibição das etapas do pipeline no Streamlit, em formato
    de stepper vertical (etapa concluída / ativa / pendente).

    Uso:
        barra = BarraProgresso(placeholder)
        barra.atualizar("semgrep", "Executando análise estática...")
        ...
        barra.concluir()
    """

    ETAPAS = [
        ("semgrep",      "🔬", "Semgrep"),
        ("gitleaks",     "🔑", "Gitleaks"),
        ("dependencias", "📦", "Dependências"),
        ("score",        "📊", "Score de Risco"),
        ("ia",           "🤖", "Análise IA"),
        ("relatorio",    "📄", "Relatório"),
    ]

    def __init__(self, container) -> None:
        self._container = container
        self._concluidas: set[str] = set()
        self._atual: str = ""
        self._detalhe: str = ""
        self._barra = container.progress(0)
        self._texto = container.empty()
        self._renderizar()

    def atualizar(self, etapa: str, detalhe: str) -> None:
        """Marca a etapa anterior como concluída e define a atual."""
        if self._atual:
            self._concluidas.add(self._atual)
        self._atual = etapa
        self._detalhe = detalhe
        self._renderizar()

    def concluir(self) -> None:
        """Marca todas as etapas como concluídas."""
        self._concluidas = {e[0] for e in self.ETAPAS}
        self._atual = ""
        self._barra.progress(1.0)
        self._renderizar()

    def _renderizar(self) -> None:
        total = len(self.ETAPAS)
        concluidas = len(self._concluidas)
        self._barra.progress(concluidas / total)

        linhas = ['<div class="progress-steps">']
        for chave, icone, nome in self.ETAPAS:
            if chave in self._concluidas:
                linhas.append(f'<div class="step-row done">✅ {nome}</div>')
            elif chave == self._atual:
                linhas.append(
                    f'<div class="step-row active">'
                    f'{icone} {nome} <span class="step-detail">— {self._detalhe}</span></div>'
                )
            else:
                linhas.append(f'<div class="step-row">{icone} {nome}</div>')
        linhas.append("</div>")

        self._texto.markdown("\n".join(linhas), unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Console — log de execução em estilo terminal
# ---------------------------------------------------------------------------

class Console:
    """
    Exibe um log de eventos do pipeline em estilo terminal, atualizado em
    tempo real conforme o callback do pipeline é chamado.

    Uso:
        console = Console(placeholder)
        console.registrar("blue", "Cabeça 2 · Dependências", "Verificando requirements.txt")
    """

    MAX_LINHAS = 8

    def __init__(self, container) -> None:
        self._placeholder = container.empty()
        self._linhas: list[dict] = []
        self._renderizar()

    def registrar(self, cor: str, rotulo: str, detalhe: str) -> None:
        """Adiciona uma nova linha ao console com timestamp automático."""
        self._linhas.append(
            {
                "hora": time.strftime("%H:%M:%S"),
                "cor": cor,
                "rotulo": rotulo,
                "detalhe": detalhe,
            }
        )
        self._renderizar()

    def _renderizar(self) -> None:
        ultimas = self._linhas[-self.MAX_LINHAS:]
        if not ultimas:
            html = '<div class="console"><span class="console-empty">Aguardando início da auditoria…</span></div>'
        else:
            linhas_html = "\n".join(
                f'<div class="console-line console-{l["cor"]}">'
                f'<span class="console-time">[{l["hora"]}]</span>'
                f'<span class="console-label">{l["rotulo"]}</span>'
                f'<span class="console-arrow">➔</span>{l["detalhe"]}</div>'
                for l in ultimas
            )
            html = f'<div class="console">{linhas_html}</div>'
        self._placeholder.markdown(html, unsafe_allow_html=True)
