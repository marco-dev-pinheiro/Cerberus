"""
app.py
━━━━━━
Ponto de entrada da interface gráfica Cerberus (Streamlit).

Uso:
    streamlit run app.py

Este arquivo é intencionalmente mínimo.
Toda lógica de negócio vive em auditor/core/pipeline.py.
Toda lógica de UI vive em ui/home.py e ui/components.py.
"""

import streamlit as st
from ui.theme import CSS_GLOBAL
from ui.home import render_pagina


def _configurar_pagina() -> None:
    st.set_page_config(
        page_title="Cerberus — Farejador de vulnerabilidades",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CSS_GLOBAL, unsafe_allow_html=True)


def main() -> None:
    _configurar_pagina()
    render_pagina()


if __name__ == "__main__":
    main()
