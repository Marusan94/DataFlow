"""Proyectos / Datasets / Explorador / IA / Settings — agnósticos."""
import io, os
from datetime import date
import pandas as pd
import streamlit as st
from modules.design import go
from modules.home import render_sidebar
from modules.generic_analyzer import _read_csv_bytes, render_generic_analysis

TYPES = ["Análisis tabular", "Mapa", "Chat IA", "Lab"]

def _ensure():
    st.session_state.setdefault("projects", [])
    st.session_state.setdefault("df_active", None)
    st.session_state.setdefault("df_name", "")

def render_projects():
    from modules.home import render_sidebar
    render_sidebar("Proyectos")
    _ensure()
    st.markdown("## Proyectos")
    st.caption("4 tipos agnósticos: Analizar → Evaluar → Asistir → Actuar.")
    with st.container(border=True):
        t = st.text_input("Título", placeholder="Mi análisis Q3")
        tipo = st.selectbox("Tipo", TYPES)
        if st.button("Crear proyecto", type="primary"):
            if not t.strip():
                st.error("Ponle un título.")
            else:
                st.session_state.projects.append({"titulo": t.strip(), "tipo": tipo, "fecha": str(date.today())})
                st.success(f"Proyecto “{t.strip()}” creado (demo).")
    for i, p in enumerate(st.session_state.projects):
        c1, c2 = st.columns([4, 1])
        c1.markdown(f"**{p['titulo']}** · {p['tipo']} · {p['fecha']}")
        if c2.button("Abrir", key=f"p_{i}"):
            go("datasets" if p["tipo"] == "Análisis tabular" else "ai")

def _load_example():
    base = os.path.dirname(os.path.dirname(__file__))
    for cand in [os.path.join(base, "datos_ejemplo.csv"), "datos_ejemplo.csv", os.path.join(base, "datos_educativos.csv")]:
        if os.path.exists(cand):
            return pd.read_csv(cand), os.path.basename(cand)
    return None, ""

def render_datasets():
    from modules.home import render_sidebar
    render_sidebar("Datasets")
    _ensure()
    st.markdown("## Datasets")
    up = st.file_uploader("Sube cualquier CSV", type=None)
    if up is not None:
        try:
            df = _read_csv_bytes(up.getvalue())
            st.session_state.df_active = df
            st.session_state.df_name = up.name
            st.success(f"{up.name}: {len(df)} filas, {len(df.columns)} columnas.")
        except Exception as e:
            st.error(f"No se pudo leer: {e}")
    if st.button("▶️ Usar datos de ejemplo"):
        df, name = _load_example()
        if df is None:
            st.error("No hay ejemplo disponible.")
        else:
            st.session_state.df_active = df
            st.session_state.df_name = name
            st.success(f"Ejemplo {name}: {len(df)} filas.")
    if st.session_state.df_active is not None:
        st.caption(f"Activo: {st.session_state.df_name}")
        render_generic_analysis(st.session_state.df_active)
    else:
        st.info("Sube un CSV o usa el ejemplo para ver el análisis agnóstico.")

def render_explorer():
    from modules.home import render_sidebar
    render_sidebar("Explorador")
    _ensure()
    st.markdown("## Explorador")
    df = st.session_state.df_active
    if df is None:
        st.info("Primero carga un dataset en Datasets.")
        if st.button("Ir a Datasets"):
            go("datasets")
        return
    st.caption(f"Explorando {st.session_state.df_name} ({len(df)} filas)")
    cols = st.multiselect("Columnas", list(df.columns), default=list(df.columns)[:5])
    q = st.text_input("Filtro texto (contiene)", placeholder="ej. 2024")
    view = df[cols] if cols else df
    if q:
        mask = pd.Series(False, index=view.index)
        for c in view.columns:
            mask = mask | view[c].astype(str).str.contains(q, case=False, na=False)
        view = view[mask]
    st.dataframe(view.head(100), use_container_width=True)
    st.download_button("Descargar vista (CSV)", view.to_csv(index=False).encode("utf-8-sig"), "vista.csv", "text/csv")

def render_ai():
    from modules.home import render_sidebar
    render_sidebar("IA")
    _ensure()
    st.markdown("## Analizar con IA")
    df = st.session_state.df_active
    if df is not None:
        st.caption(f"Contexto: {st.session_state.df_name} · {len(df)} filas · {list(df.columns)[:6]}")
    q = st.text_input("Pregunta", placeholder="¿Qué patrones ves en mis datos?")
    if st.button("Preguntar", type="primary"):
        if not q.strip():
            st.error("Escribe una pregunta.")
        else:
            key = None
            try:
                key = st.secrets.get("OPENROUTER_API_KEY", None)
            except Exception:
                key = os.getenv("OPENROUTER_API_KEY")
            if key and df is not None:
                try:
                    from openai import OpenAI
                    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)
                    sample = df.head(10).to_csv(index=False)
                    r = client.chat.completions.create(
                        model="openai/gpt-4o-mini",
                        messages=[{"role": "user", "content": f"Datos:\n{sample}\n\nPregunta: {q}\nResponde breve y accionable."}],
                    )
                    st.write(r.choices[0].message.content)
                except Exception as e:
                    st.warning(f"IA remota falló ({e}). Respuesta local demo abajo.")
                    _local_answer(q, df)
            else:
                _local_answer(q, df)

def _local_answer(q, df):
    st.info("Demo sin API key: respuesta local basada en perfilado.")
    if df is None:
        st.write("Carga un dataset y podré describir columnas, nulos y correlaciones. Tu pregunta fue: " + q)
        return
    from modules.generic_analyzer import profile_csv
    info = profile_csv(df)
    st.write(f"Tienes {info['rows']} filas y {len(info['cols'])} columnas. Nulos: {info['nulls_total']}. "
             f"Columnas: {', '.join(info['cols'][:8])}. Afina tu pregunta (ej. correlación, top valores, tendencia).")

def render_settings():
    from modules.home import render_sidebar
    render_sidebar("Configuración")
    st.markdown("## Configuración")
    u = st.session_state.get("user") or {"name": "Santiago", "role": "Analista de datos", "email": "demo@dataflow.app"}
    st.json(u)
    new_role = st.selectbox("Rol", ["Analista de datos", "Desarrollador", "Estudiante", "Investigador"],
                            index=0 if not u.get("role") else ["Analista de datos", "Desarrollador", "Estudiante", "Investigador"].index(u.get("role")) if u.get("role") in ["Analista de datos", "Desarrollador", "Estudiante", "Investigador"] else 0)
    if st.button("Guardar rol"):
        st.session_state.user = {**u, "role": new_role}
        st.success(f"Rol: {new_role}")
    if st.button("Reiniciar demo"):
        for k in ["projects", "df_active", "df_name", "role_pick", "user", "pending_email"]:
            st.session_state.pop(k, None)
        go("landing")
