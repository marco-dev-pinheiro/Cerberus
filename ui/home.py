import time
import streamlit as st
from pathlib import Path
from auditor.core.pipeline import executar_auditoria
from ui import components

# Mapeamento estético etapa → (cor, rótulo) usado apenas para o Console.
ROTULOS_CONSOLE = {
    "semgrep":     ("red",    "Cabeça 1 · Análise Estática"),
    "gitleaks":    ("orange", "Cabeça 1 · Varredura de Segredos"),
    "dependencias": ("blue",   "Cabeça 2 · Dependências"),
    "score":        ("cyan",   "Métricas · Cálculo de Risco"),
    "ia":           ("gold",   "Cabeça 3 · Análise do Agente Ollama"),
    "relatorio":    ("green",  "Gerador · Relatórios"),
}

def render_pagina():
    # Caminho seguro para o asset no Windows/Linux usando Path
    caminho_banner = Path("assets") / "cerberus_banner.png"
    st.image(str(caminho_banner), width="stretch")
      
    components.render_hero_header()

    # ─── Painel de configuração ────────────────────────────────────────
    components.render_section_eyebrow("⚙️", "Início da varredura de segurança")
    with st.container(border=True):
        caminho_alvo = st.text_input(
            "📂 Diretório do projeto para auditar",
            value=".",
            placeholder="/caminho/do/projeto",
        )
        st.caption(
            "Caminho absoluto ou relativo à raiz a partir de onde o Cerberus está sendo executado."
        )
        iniciar = st.button("🐺 Iniciar Auditoria", type="primary", width="stretch")

    if not iniciar:
        return

    # ─── Painel de execução: pipeline em tempo real ────────────────────
    components.render_section_eyebrow("📡", "Execução da varredura de Cerberus")
    with st.status("🐺 Cerberus está farejando os módulos...", expanded=True) as status:
        col_etapas, col_console = st.columns([1, 1.4])

        with col_etapas:
            st.caption("Etapas")
            barra_progresso = components.BarraProgresso(col_etapas)

        with col_console:
            st.caption("Console")
            console = components.Console(col_console)

        # Callback do pipeline em tempo real
        def atualizar_interface_cerberus(etapa: str, detalhe: str):
            cor, rotulo = ROTULOS_CONSOLE.get(etapa, ("white", etapa.upper()))
            console.registrar(cor, rotulo, detalhe)
            barra_progresso.atualizar(etapa, detalhe)

        resultado = executar_auditoria(alvo=caminho_alvo, callback=atualizar_interface_cerberus)

        if resultado:
            barra_progresso.concluir()
            status.update(label="🔒 Sistema Auditado pelo Cerberus!", state="complete", expanded=False)
        else:
            status.update(label="❌ Falha na Auditoria", state="error", expanded=True)

    # ─── Painel de resultado ────────────────────────────────────────────
    if not resultado:
        st.error("Não foi possível realizar a varredura no caminho indicado.")
        return

    components.render_section_eyebrow("📜", "Resultado da Auditoria")
    components.render_score_card(resultado.nivel_risco, resultado.score)

    components.render_section_eyebrow("🤖", "Parecer do Agente Cerberus")
    with st.container(border=True):
        components.render_ia_report_header()
        st.markdown(resultado.analise_ia)