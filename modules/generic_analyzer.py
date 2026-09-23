"""Analizador genérico agnóstico: perfila CUALQUIER CSV, sin columnas fijas."""
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def _read_csv_bytes(data: bytes):
    import io
    try:
        return pd.read_csv(io.BytesIO(data), encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(io.BytesIO(data), encoding="latin-1")

def profile_csv(df: pd.DataFrame) -> dict:
    num = df.select_dtypes(include="number")
    return {
        "rows": int(len(df)),
        "cols": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "nulls": {c: int(v) for c, v in df.isnull().sum().items()},
        "nulls_total": int(df.isnull().sum().sum()),
        "numeric_corr": num.corr(numeric_only=True).round(3).to_dict() if num.shape[1] >= 2 else {},
    }

def render_generic_analysis(df: pd.DataFrame):
    info = profile_csv(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filas", info["rows"])
    c2.metric("Columnas", len(info["cols"]))
    c3.metric("Nulos", info["nulls_total"])
    c4.metric("Numéricas", len(df.select_dtypes(include="number").columns))
    with st.expander("Vista previa"):
        st.dataframe(df.head(20), use_container_width=True)
    with st.expander("Tipos y nulos"):
        st.json({"dtypes": info["dtypes"], "nulls": info["nulls"]})
    num = df.select_dtypes(include="number")
    if num.shape[1] >= 1:
        col = st.selectbox("Histograma", list(num.columns))
        try:
            import plotly.express as px
            st.plotly_chart(px.histogram(df, x=col), use_container_width=True)
        except Exception as e:
            st.warning(f"No se pudo graficar: {e}")
    if len(info["numeric_corr"]) >= 2:
        st.caption("Correlación numérica")
        st.dataframe(pd.DataFrame(info["numeric_corr"]), use_container_width=True)
    cat = df.select_dtypes(include="object")
    if cat.shape[1] >= 1:
        ccat = st.selectbox("Top valores", list(cat.columns))
        top = df[ccat].astype(str).value_counts().head(10).reset_index()
        top.columns = ["valor", "frecuencia"]
        st.dataframe(top, use_container_width=True)
