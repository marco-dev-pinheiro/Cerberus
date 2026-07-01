"""
ui/theme.py
━━━━━━━━━━━
Design system do Cerberus UI: paleta, tipografia, espaçamento e CSS global.
"""

APP_NOME = "CERBERUS"
APP_TAGLINE = "⋆༺𓆩☠︎︎𓆪༻"
APP_VERSAO = "v1.0.1.7.26"
APP_STATUS = "Operacional"
APP_DESCRICAO = (
    "Auditoria automatizada de segurança combinando análise estática, "
    "varredura de segredos, dependências vulneráveis e parecer de IA."
)

# Cores calibradas com os neons e alertas do Banner
CORES_SEVERIDADE: dict[str, str] = {
    "CRITICAL": "#FF4B4B",  # Vermelho Vivo do Cerberus
    "HIGH":      "#FF8C42",  # Laranja Alerta
    "MEDIUM":    "#F2C744",  # Amarelo Cyber
    "LOW":       "#00F3FF",  # Cian Neon
    "INFO":      "#8B949E",
}

ICONES_SEVERIDADE: dict[str, str] = {
    "CRITICAL": "🔴",
    "HIGH":     "🟠",
    "MEDIUM":   "🟡",
    "LOW":      "🔵",
    "INFO":     "⚪",
}

CORES_NIVEL: dict[str, str] = {
    "CRÍTICO": "#FF4B4B",
    "ALTO":    "#FF8C42",
    "MÉDIO":   "#F2C744",
    "BAIXO":   "#00F3FF",
}

ICONES_NIVEL: dict[str, str] = {
    "CRÍTICO": "🚨",
    "ALTO":    "🔴",
    "MÉDIO":   "🟡",
    "BAIXO":   "🟢",
}

CSS_GLOBAL = """
<style>
/* ════════════════════════════════════════════════════════════════════
   1. DESIGN TOKENS (Alinhados com a paleta do Banner)
   ════════════════════════════════════════════════════════════════════ */
:root {
    --bg-canvas:    #0B0F17;  # Dark profundo do banner
    --bg-surface:   #121824;
    --bg-elevated:  #1A2336;
    --bg-sunken:    #06090F;

    --border:        #1E293B;
    --border-strong: #2E3E56;

    --text-primary:   #F1F5F9;
    --text-secondary: #94A3B8;
    --text-tertiary:  #64748B;

    /* Cores de Ação do Banner Cyber */
    --brand:       #FF4B4B;   /* Vermelho Olho do Cerberus / Crítico */
    --accent:      #00F3FF;   /* Cian HUD / Botões e Inputs Actives */
    --accent-soft: rgba(0, 243, 255, 0.1);
    --accent-strong: #70F9FF;
    --success:     #00F3FF;
    --success-soft: rgba(0, 243, 255, 0.08);

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;

    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;

    --font-sans: 'Inter', 'Segoe UI', system-ui, sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', ui-monospace, monospace;
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

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--border-strong);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

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
    text-shadow: 0 0 15px rgba(255, 75, 75, 0.3);
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
    padding: var(--space-4) var(--space-1) var(--space-5);
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
}
.cerberus-hero h1 .mark { color: var(--brand); text-shadow: 0 0 10px rgba(255, 75, 75, 0.4); }
.cerberus-hero .hero-tagline {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--accent);
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
    color: var(--accent);
    border: 1px solid rgba(0, 243, 255, 0.3);
    border-radius: 999px;
    padding: 0.25rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.status-pill .dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
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
   6. CONTAINERS COM BORDA
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--border) !important;
    border-radius: var(--radius-lg) !important;
    background-color: var(--bg-surface);
}

/* ════════════════════════════════════════════════════════════════════
   7. BOTÕES (Estilo HUD do Banner)
   ════════════════════════════════════════════════════════════════════ */
.stButton > button,
[data-testid^="stBaseButton"] {
    border-radius: var(--radius-md) !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    padding: 0.6rem 1.3rem !important;
    border: 1px solid var(--accent) !important;
    background-color: transparent !important;
    color: var(--accent) !important;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.1);
    transition: all 0.2s ease;
}
.stButton > button:hover,
[data-testid^="stBaseButton"]:hover {
    border-color: var(--brand) !important;
    color: #FFFFFF !important;
    background-color: var(--brand) !important;
    box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
}
.stButton > button:active { transform: scale(0.98); }

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #0E1117 !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
}
.stButton > button[kind="primary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background-color: var(--accent-strong) !important;
    border-color: var(--accent-strong) !important;
    color: #0E1117 !important;
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.5);
}

/* ════════════════════════════════════════════════════════════════════
   8. INPUTS
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stTextInput"] input {
    background-color: var(--bg-sunken) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: var(--radius-md) !important;
    color: var(--accent) !important;
    font-family: var(--font-mono);
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.2) !important;
}

/* ════════════════════════════════════════════════════════════════════
   9. EXPANDER / STATUS
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stExpander"], [data-testid="stStatusWidget"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    background-color: var(--bg-surface) !important;
}

/* ════════════════════════════════════════════════════════════════════
   10. PROGRESS NATIVA
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stProgress"] > div > div > div {
    background-color: var(--accent) !important;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
}

/* ════════════════════════════════════════════════════════════════════
   11. STEPPER DE ETAPAS
   ════════════════════════════════════════════════════════════════════ */
.step-row.active {
    border-left-color: var(--accent);
    background: var(--accent-soft);
    color: var(--text-primary);
}

/* ════════════════════════════════════════════════════════════════════
   12. CONSOLE HUD STYLE
   ════════════════════════════════════════════════════════════════════ */
.console {
    background: var(--bg-sunken);
    border: 1px solid var(--border-strong);
    border-radius: var(--radius-md);
    font-family: var(--font-mono);
}
.console-cyan   .console-label { color: var(--accent); }
.console-red    .console-label { color: var(--brand); }

/* ════════════════════════════════════════════════════════════════════
   14. CARD DE SCORE (Efeito Central do HUD)
   ════════════════════════════════════════════════════════════════════ */
.score-card {
    border-radius: var(--radius-lg);
    background: linear-gradient(180deg, var(--bg-elevated) 0%, var(--bg-canvas) 100%);
    border: 1px solid var(--border-strong);
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.05);
}
.score-card .score-number { 
    font-family: var(--font-mono);
    font-size: 3.5rem; 
    font-weight: 900; 
    color: var(--accent);
    text-shadow: 0 0 15px rgba(0, 243, 255, 0.4);
}

/* ════════════════════════════════════════════════════════════════════
   18. PARECER DA IA (Tabelas de Auditoria Limpas)
   ════════════════════════════════════════════════════════════════════ */
[data-testid="stMarkdown"] th {
    background: var(--bg-elevated);
    color: var(--accent);
    border-bottom: 2px solid var(--accent);
}
[data-testid="stMarkdown"] pre {
    background: var(--bg-sunken) !important;
    border: 1px solid var(--border-strong);
}
</style>
"""