"""Home DataFlow: Hola + buscador + 3 cards + sidebar."""
import streamlit as st
from modules.design import show_logo, go

NAV = ["Inicio", "Proyectos", "Datasets", "Explorador", "IA", "Configuración"]

def render_sidebar(active="Inicio"):
    with st.sidebar:
        show_logo(small=True)
        st.divider()
        for item in NAV:
            if st.button(("● " if item == active else "○ ") + item, key=f"nav_{item}", use_container_width=True):
                go({"Inicio": "home", "Proyectos": "projects", "Datasets": "datasets",
                    "Explorador": "explorer", "IA": "ai", "Configuración": "settings"}[item])
        st.divider()
        u = st.session_state.get("user") or {}
        st.caption(f"{u.get('name','Santiago')} · {u.get('role','Analista de datos')}")
        if st.button("Cerrar sesión (demo)"):
            st.session_state.user = None
            go("landing")

def render_home():
    render_sidebar("Inicio")
    u = st.session_state.get("user") or {"name": "Santiago"}
    st.markdown(f"## Hola, {u.get('name','Santiago')}")
    st.caption("Listo para analizar tus datos hoy?")
    q = st.text_input("Buscar", placeholder="Buscar datasets, proyectos, análisis...", label_visibility="collapsed")
    if q:
        st.caption(f"Resultados demo para “{q}”: usa Datasets o Explorador para ver datos reales.")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("📁 **Explorar datos**<br><span class='small-muted'>Sube o conecta tus datasets</span>", unsafe_allow_html=True)
            if st.button("Abrir", key="h_exp", use_container_width=True):
                go("datasets")
    with c2:
        with st.container(border=True):
            st.markdown("✨ **Analizar con IA**<br><span class='small-muted'>Haz preguntas a tus datos</span>", unsafe_allow_html=True)
            if st.button("Abrir", key="h_ai", use_container_width=True):
                go("ai")
    with c3:
        with st.container(border=True):
            st.markdown("📄 **Nuevo proyecto**<br><span class='small-muted'>Comienza un análisis</span>", unsafe_allow_html=True)
            if st.button("Crear", key="h_new", use_container_width=True):
                go("projects")
    st.divider()
    projs = st.session_state.get("projects", [])
    st.caption(f"Tienes {len(projs)} proyecto(s) en esta demo.")
    for p in projs[-3:]:
        st.markdown(f"- **{p['titulo']}** · {p['tipo']} · {p['fecha']}")
