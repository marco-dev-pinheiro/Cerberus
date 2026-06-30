"""
ui/theme.py
━━━━━━━━━━━
Design system do Cerberus UI: paleta, tipografia, espaçamento e CSS global.

Centralizar aqui evita valores mágicos espalhados pelos componentes.
Todas as constantes públicas originais (CORES_SEVERIDADE, ICONES_SEVERIDADE,
CORES_NIVEL, ICONES_NIVEL, CSS_GLOBAL) são preservadas — apenas o conteúdo
visual foi reformulado.
"""

# ---------------------------------------------------------------------------
# Identidade do produto (usado pelo header e pela sidebar)
# ---------------------------------------------------------------------------
APP_NOME = "CERBERUS"
APP_TAGLINE = "AI Security Auditor"
APP_VERSAO = "v1.0"
APP_STATUS = "Operacional"
APP_DESCRICAO = (
    "Auditoria automatizada de segurança combinando análise estática, "
    "varredura de segredos, dependências vulneráveis e parecer de IA."
)

# ---------------------------------------------------------------------------
# Cores por severidade
# ---------------------------------------------------------------------------
CORES_SEVERIDADE: dict[str, str] = {
    "CRITICAL": "#F85149",
    "HIGH":     "#FF8C42",
    "MEDIUM":   "#F2C744",
    "LOW":      "#58A6FF",
    "INFO":     "#8B949E",
}

ICONES_SEVERIDADE: dict[str, str] = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🔵",
    "INFO":     "⚪",
}

# Nível de risco → cor e ícone
CORES_NIVEL: dict[str, str] = {
    "CRÍTICO": "#F85149",
    "ALTO":    "#FF8C42",
    "MÉDIO":   "#F2C744",
    "BAIXO":   "#3FB950",
}

ICONES_NIVEL: dict[str, str] = {
    "CRÍTICO": "🚨",
    "ALTO":    "🔴",
    "MÉDIO":   "🟡",
    "BAIXO":   "🟢",
}

# ---------------------------------------------------------------------------
# CSS global injetado no Streamlit
# ---------------------------------------------------------------------------
CSS_GLOBAL = """
<style>

/* ════════════════════════════════════════════════════════════════════
   1. DESIGN TOKENS
   ════════════════════════════════════════════════════════════════════ */
:root {
    /* Superfícies */
    --bg-canvas:    #0E1117;
    --bg-surface:   #161B22;
    --bg-elevated:  #1C2230;
    --bg-sunken:    #0A0D12;

    /* Bordas */
    --border:        #21262D;
    --border-strong: #30363D;

    /* Texto */
    --text-primary:   #F0F3F6;
    --text-secondary: #8B949E;
    --text-tertiary:  #6E7681;

    /* Marca e ação */
    --brand:       #F85149;   /* vermelho Cerberus — reservado à marca e crítico */
    --accent:      #58A6FF;   /* azul de interação — botões, foco, links */
    --accent-soft: rgba(88, 166, 255, 0.12);
    --accent-strong: #79C0FF;
    --success:     #3FB950;
    --success-soft: rgba(63, 185, 80, 0.12);

    /* Forma */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;

    /* Espaçamento */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;

    /* Tipografia */
    --font-sans: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, SFMono-Regular,
                 Menlo, Consolas, monospace;
}

/* ════════════════════════════════════════════════════════════════════
   2. RESET E BASE
   ════════════════════════════════════════════════════════════════════ */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-canvas);
    color: var(--text-primary);
    font-family: var(--font-sans);
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}

h1, h2, h3, h4 { color: var(--text-primary); letter-spacing: -0.01em; }
p { color: var(--text-secondary); }

/* Esconde elementos padrão desnecessários do Streamlit */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar global discreta */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border-strong);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: var(--text-tertiary); }

/* ════════════════════════════════════════════════════════════════════
   3. SIDEBAR
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: var(--bg-surface);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding-top: 0; }

.cerberus-brand {
    text-align: center;
    padding: var(--space-5) 0 var(--space-4);
}
.cerberus-brand h1 {
    font-size: 1.7rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: var(--brand);
    margin: 0;
}
.cerberus-brand p {
    font-size: 0.72rem;
    color: var(--text-secondary);
    margin: 0.3rem 0 0;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

hr.cerberus-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: var(--space-5) 0;
}

.sidebar-section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    margin-bottom: var(--space-2);
}

/* ════════════════════════════════════════════════════════════════════
   4. HERO HEADER
   ════════════════════════════════════════════════════════════════════ */
.cerberus-hero {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-5);
    padding: var(--space-5) var(--space-1) var(--space-5);
    border-bottom: 1px solid var(--border);
    margin-bottom: var(--space-5);
    flex-wrap: wrap;
}
.cerberus-hero .hero-title-row {
    display: flex;
    align-items: baseline;
    gap: var(--space-3);
}
.cerberus-hero h1 {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    margin: 0;
    color: var(--text-primary);
}
.cerberus-hero h1 .mark { color: var(--brand); }
.cerberus-hero .hero-tagline {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.14em;
}
.cerberus-hero .hero-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    max-width: 46rem;
    margin-top: var(--space-2);
    line-height: 1.5;
}
.hero-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: var(--space-2);
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--success-soft);
    color: var(--success);
    border: 1px solid rgba(63, 185, 80, 0.3);
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.status-pill .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--success);
    box-shadow: 0 0 0 3px var(--success-soft);
}
.version-tag {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-tertiary);
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.15rem 0.5rem;
}

/* ════════════════════════════════════════════════════════════════════
   5. RÓTULOS DE SEÇÃO
   ════════════════════════════════════════════════════════════════════ */
.section-eyebrow {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-secondary);
    margin: var(--space-5) 0 var(--space-3);
}
.section-eyebrow:first-child { margin-top: 0; }

/* ════════════════════════════════════════════════════════════════════
   6. CONTAINERS COM BORDA (st.container(border=True))
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
    border-radius: var(--radius-lg) !important;
    background-color: var(--bg-surface);
}
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-radius: var(--radius-lg) !important;
}

/* ════════════════════════════════════════════════════════════════════
   7. BOTÕES
   ════════════════════════════════════════════════════════════════════ */
.stButton > button,
[data-testid^="stBaseButton"] {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    padding: 0.5rem 1.1rem !important;
    border: 1px solid var(--border-strong) !important;
    background-color: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    transition: border-color 0.15s ease, background-color 0.15s ease, transform 0.05s ease;
}
.stButton > button:hover,
[data-testid^="stBaseButton"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent-strong) !important;
}
.stButton > button:active,
[data-testid^="stBaseButton"]:active { transform: scale(0.98); }
.stButton > button:focus-visible,
[data-testid^="stBaseButton"]:focus-visible {
    outline: 2px solid var(--accent) !important;
    outline-offset: 2px;
}

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #0E1117 !important;
}
.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background-color: var(--accent-strong) !important;
    border-color: var(--accent-strong) !important;
    color: #0E1117 !important;
}

/* ════════════════════════════════════════════════════════════════════
   8. INPUTS
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stWidgetLabel"] p {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-secondary);
}
[data-testid="stTextInput"] input {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    padding: 0.55rem 0.85rem !important;
    font-family: var(--font-mono);
    font-size: 0.88rem;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-tertiary); }

/* ════════════════════════════════════════════════════════════════════
   9. STATUS / EXPANDER (st.status, st.expander)
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stExpander"], [data-testid="stStatusWidget"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    background-color: var(--bg-surface) !important;
}
[data-testid="stExpander"] summary { font-weight: 600; }

/* ════════════════════════════════════════════════════════════════════
   10. BARRA DE PROGRESSO NATIVA (st.progress)
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stProgress"] > div > div {
    background-color: var(--bg-elevated) !important;
    border-radius: 999px !important;
}
[data-testid="stProgress"] > div > div > div {
    background-color: var(--accent) !important;
    border-radius: 999px !important;
}

/* ════════════════════════════════════════════════════════════════════
   11. STEPPER DE ETAPAS (BarraProgresso)
   ════════════════════════════════════════════════════════════════════ */
.progress-steps { display: flex; flex-direction: column; gap: 0.3rem; }
.step-row {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.45rem 0.7rem;
    border-left: 3px solid var(--border);
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    font-size: 0.84rem;
    color: var(--text-tertiary);
    transition: all 0.15s ease;
}
.step-row.done {
    border-left-color: var(--success);
    color: var(--success);
}
.step-row.active {
    border-left-color: var(--accent);
    background: var(--accent-soft);
    color: var(--text-primary);
    font-weight: 600;
}
.step-row .step-detail { color: var(--text-secondary); font-weight: 400; }

/* ════════════════════════════════════════════════════════════════════
   12. CONSOLE (log em estilo terminal)
   ════════════════════════════════════════════════════════════════════ */
.console {
    background: var(--bg-sunken);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    font-family: var(--font-mono);
    font-size: 0.76rem;
    line-height: 1.7;
    max-height: 260px;
    overflow-y: auto;
}
.console-line { color: var(--text-secondary); white-space: pre-wrap; word-break: break-word; }
.console-time { color: var(--text-tertiary); margin-right: 0.4rem; }
.console-arrow { margin: 0 0.35rem; color: var(--text-tertiary); }
.console-label { font-weight: 700; }
.console-empty { color: var(--text-tertiary); font-style: italic; }

.console-red    .console-label { color: #F85149; }
.console-orange .console-label { color: #FF8C42; }
.console-blue   .console-label { color: #58A6FF; }
.console-cyan   .console-label { color: #56D4DD; }
.console-gold   .console-label { color: #F2C744; }
.console-green  .console-label { color: #3FB950; }
.console-white  .console-label { color: var(--text-primary); }

/* ════════════════════════════════════════════════════════════════════
   13. CARDS DE SEVERIDADE
   ════════════════════════════════════════════════════════════════════ */
.sev-card {
    border-radius: var(--radius-md);
    padding: 1rem 1.1rem;
    border-left: 3px solid;
    background-color: var(--bg-surface);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}
.sev-card .sev-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 0.3rem;
}
.sev-card .sev-count { font-size: 1.9rem; font-weight: 800; line-height: 1; }

/* ════════════════════════════════════════════════════════════════════
   14. CARD DE SCORE
   ════════════════════════════════════════════════════════════════════ */
.score-card {
    border-radius: var(--radius-lg);
    padding: 1.75rem 2rem;
    background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-surface) 100%);
    border: 1px solid var(--border);
    text-align: center;
}
.score-card .score-number { font-size: 3.2rem; font-weight: 900; line-height: 1; }
.score-card .score-nivel {
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}
.score-card .score-label {
    font-size: 0.7rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.8rem;
}

/* ════════════════════════════════════════════════════════════════════
   15. STATUS BADGE (scanners)
   ════════════════════════════════════════════════════════════════════ */
.badge {
    display: inline-block;
    border-radius: var(--radius-sm);
    padding: 0.15rem 0.55rem;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-ok   { background: var(--success-soft); color: var(--success); }
.badge-warn { background: rgba(242, 199, 68, 0.14); color: #F2C744; }
.badge-off  { background: var(--bg-elevated); color: var(--text-tertiary); }

/* ════════════════════════════════════════════════════════════════════
   16. FINDING ROW
   ════════════════════════════════════════════════════════════════════ */
.finding-row {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-left: 3px solid;
    border-radius: var(--radius-md);
    padding: 0.75rem 1rem;
    margin-bottom: 0.4rem;
    font-size: 0.85rem;
}
.finding-row .finding-title { font-weight: 600; color: var(--text-primary); }
.finding-row .finding-meta  { color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.25rem; }

/* ════════════════════════════════════════════════════════════════════
   17. HISTÓRICO
   ════════════════════════════════════════════════════════════════════ */
.hist-item {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.6rem 1rem;
    margin-bottom: 0.35rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    color: var(--text-secondary);
}
.hist-item span:first-child { color: var(--text-primary); font-weight: 500; }

/* ════════════════════════════════════════════════════════════════════
   18. RELATÓRIO IA — cabeçalho de relatório executivo
   ════════════════════════════════════════════════════════════════════ */
.ia-report-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding-bottom: var(--space-3);
    margin-bottom: var(--space-3);
    border-bottom: 1px solid var(--border);
}
.ia-report-header .ia-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-primary);
}
.ia-report-header .ia-subtitle {
    font-size: 0.72rem;
    color: var(--text-tertiary);
}
.ia-report-header .ia-timestamp {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-tertiary);
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.2rem 0.55rem;
}

/* Tabelas e blocos de código dentro do parecer da IA */
[data-testid="stMarkdown"] table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    margin: 0.5rem 0 1rem;
}
[data-testid="stMarkdown"] th {
    background: var(--bg-elevated);
    color: var(--text-primary);
    text-align: left;
    padding: 0.5rem 0.75rem;
    border-bottom: 2px solid var(--border-strong);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stMarkdown"] td {
    padding: 0.5rem 0.75rem;
    border-bottom: 1px solid var(--border);
    color: var(--text-secondary);
}
[data-testid="stMarkdown"] tr:hover td { background: rgba(255, 255, 255, 0.02); }
[data-testid="stMarkdown"] pre {
    background: var(--bg-sunken) !important;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
}
[data-testid="stMarkdown"] code {
    font-family: var(--font-mono);
    font-size: 0.82rem;
}

</style>
"""
