"""DataFlow design tokens + CSS helpers. Agnóstico, sin lógica educativa."""
import streamlit as st

ACCENT = "#B9B091"
BG = "#111110"
SURFACE = "#191918"
SURFACE2 = "#1E1E1C"
BORDER = "#2A2A28"
TEXT = "#F2F1EC"
MUTED = "#9C9C94"

DATAFLOW_CSS = f"""
<style>
.stApp {{ background:{BG}; color:{TEXT}; font-family:'Inter','SF Pro',system-ui,sans-serif; }}
section[data-testid="stSidebar"] {{ background:{SURFACE}; border-right:1px solid {BORDER}; }}
div[data-testid="stVerticalBlockBorderWrapper"] {{
  background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
}}
.stTextInput input, .stTextArea textarea, .stNumberInput input {{
  background:{SURFACE2} !important; color:{TEXT} !important;
  border:1px solid {BORDER} !important; border-radius:8px !important;
}}
.stButton > button[kind="primary"], .stButton > button[data-testid="baseButton-primary"] {{
  background:{ACCENT} !important; color:#111110 !important;
  border:none !important; border-radius:8px !important; font-weight:600 !important;
}}
.stButton > button[kind="secondary"] {{
  background:transparent !important; color:{TEXT} !important;
  border:1px solid {BORDER} !important; border-radius:8px !important;
}}
/* Hero landing */
.df-hero {{ display:flex; flex-direction:column; align-items:center; justify-content:center;
  height:65vh; text-align:center; padding:24px; }}
.df-hero-title {{ font-size:56px; font-weight:700; letter-spacing:-0.03em; line-height:1.05; }}
.df-hero-sub {{ color:{MUTED}; font-size:18px; margin-top:12px; }}
/* 6 casillas código */
.df-code-row {{ display:flex; gap:8px; justify-content:center; margin:16px 0; }}
.df-code-box {{ width:56px; height:56px; text-align:center; font-size:24px; font-weight:600;
  background:{SURFACE2}; border:2px solid {BORDER}; border-radius:12px; color:{TEXT};
  -webkit-text-security:none; }}
@media (prefers-color-scheme: dark) {{
  .df-code-box {{ background:{SURFACE2}; border-color:{BORDER}; }}
}}
/* Reducir altura inputs código Streamlit para alinear */
div[data-testid="stTextInput"]:has(input[maxlength="1"]) {{ width:56px !important; }}
div[data-testid="stTextInput"]:has(input[maxlength="1"]) input {{
  height:56px !important; font-size:24px !important; text-align:center !important;
  padding:0 !important; }}
/* Centrar auth forms */
.df-auth-center {{ max-width:420px; margin:0 auto; padding:24px 0; }}
.df-auth-center .stButton > button {{ width:100%; }}
.small-muted {{ color:{MUTED}; font-size:13px; }}
.df-title {{ font-size:28px; font-weight:700; letter-spacing:-0.02em; }}
.df-sub {{ color:{MUTED}; font-size:14px; margin-top:4px; }}
.df-card {{ padding:16px; }}
a {{ color:{ACCENT} !important; }}
</style>
"""

def apply_theme():
    st.markdown(DATAFLOW_CSS, unsafe_allow_html=True)

def show_logo(small=False):
    size = "16px" if small else "20px"
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;font-weight:700;font-size:{size}'>"
        f"<span style='letter-spacing:-0.05em'>▮▮▮</span><span>DataFlow</span></div>",
        unsafe_allow_html=True,
    )

def go(page: str):
    st.session_state.page = page
    st.rerun()
