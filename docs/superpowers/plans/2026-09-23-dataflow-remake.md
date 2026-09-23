# DataFlow Remake Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar EduAnalytics HUB por DataFlow estilo imagen en Streamlit en el mismo repo.

**Architecture:** Router custom `session_state.page` + módulos UI agnósticos + tema dark DataFlow vía config.toml + CSS.

**Tech Stack:** Streamlit>=1.28, Pandas 2.1, Plotly, Numpy

**Spec:** `docs/superpowers/specs/2026-09-23-dataflow-remake-design.md`

## Global Constraints
- background #111110, surface #191918, borders #2A2A28, accent #B9B091, text #F2F1EC
- Auth solo simulada, verify code `123456`
- Agnóstico: ningún análisis hardcodea nota/asistencia/grupo_id
- `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- Mobile 390px OK

---

### Task 1: Tema + router base

**Files:**
- Modify: `.streamlit/config.toml`
- Create: `modules/design.py`
- Create: `app.py` (overwrite)

**Interfaces:**
- Consumes: nada
- Produces: `design.DATAFLOW_CSS: str`, `design.show_logo(): None`, `app.py` router con `st.session_state.page`

- [ ] **Step 1: config.toml DataFlow**
```toml
[theme]
base="dark"
primaryColor="#B9B091"
backgroundColor="#111110"
secondaryBackgroundColor="#191918"
textColor="#F2F1EC"
font="sans serif"
[server]
headless=true
```
Run: `cat .streamlit/config.toml`
Expected: valores exactos

- [ ] **Step 2: modules/design.py tokens + CSS**
```python
ACCENT="#B9B091"; BG="#111110"; SURFACE="#191918"; BORDER="#2A2A28"; TEXT="#F2F1EC"
DATAFLOW_CSS="""<style>.stApp{background:#111110;color:#F2F1EC}...</style>"""
def show_logo(): ...
def card(title, desc): ...
```
Run: `python -m py_compile modules/design.py`
Expected: PASS

- [ ] **Step 3: app.py router mínimo**
```python
import streamlit as st
st.set_page_config(page_title="DataFlow", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
if "page" not in st.session_state: st.session_state.page="landing"
# router: landing, login, register, verify, recover, reset, twofa, role, home, projects, datasets, explorer, ai, settings
```
Run: `python -m py_compile app.py`
Expected: PASS

### Task 2: Auth simulada 7 pantallas

**Files:**
- Create: `modules/auth_ui.py`

**Interfaces:**
- Consumes: `design.DATAFLOW_CSS`
- Produces: `render_landing(), render_login(), render_register(), render_verify(), render_recover(), render_reset(), render_twofa(), render_role()`

- [ ] **Step 1: landing + login + register**
Landing: logo + "Convierte tus datos en decisiones." + "Analiza. Visualiza. Explora." + bullets Análisis/Machine Learning/Visualización/Colaboración + botón Iniciar sesión.
Login: GitHub/Google (mock) + email + password>=8 + Recordarme + link registro. Si OK → page=home (demo simplificada, verify opcional).
- [ ] **Step 2: verify + recover + reset + 2fa + role**
Verify: 6 inputs, acepta `123456`. Recover: email → enlace. Reset: 2 passwords >=8 iguales. 2FA: 6 dígitos mock. Role: 4 cards Analista/Desarrollador/Estudiante/Investigador + Siguiente → home.
Run: `python -m py_compile modules/auth_ui.py`

### Task 3: Home + proyectos agnósticos

**Files:**
- Create: `modules/home.py`, `modules/projects.py`, `modules/generic_analyzer.py`, `modules/datasets.py`, `modules/explorer.py`, `modules/ai_basic.py`, `modules/settings.py`
- Create: `datos_ejemplo.csv`

**Interfaces:**
- Consumes: `session_state.user, session_state.projects`
- Produces: `home.render()`, `generic_analyzer.profile_csv(df)->dict`

- [ ] **Step 1: generic_analyzer agnóstico**
```python
def profile_csv(df):
    return {"rows":len(df),"cols":list(df.columns),"nulls":df.isnull().sum().to_dict(),"describe":df.describe(include="all").to_dict()}
```
Soporta cualquier CSV, sin columnas fijas. Plotly hist + correlación solo si hay numéricas.
- [ ] **Step 2: home Hola Santiago + search + 3 cards**
Sidebar: Inicio/Proyectos/Datasets/Explorador/IA/Config. Header "Hola, Santiago" + "Listo para analizar tus datos hoy?" + search + cards Explorar/Analizar con IA/Nuevo proyecto.
- [ ] **Step 3: datasets/explorer/ai/settings/projects**
Upload cualquier CSV, tabla con filtros, chat mock (si OPENROUTER_API_KEY hay streaming real, si no respuesta mock), settings con rol + reset demo.
Run: `python -m py_compile modules/*.py`

### Task 4: Rebrand + Render + smoke

**Files:**
- Modify: `render.yaml`, `requirements.txt`, `README.md`
- Delete: `modules/analytics.py, modules/dashboard_geo.py, modules/dashboard_academic.py, modules/steam_lab.py, modules/laboratory.py` (mover a `_legacy/` si existen)

**Interfaces:**
- Consumes: todo lo anterior
- Produces: repo DataFlow desplegable

- [ ] **Step 1: render.yaml**
```yaml
services:
  - type: web
    name: dataflow
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
    envVars:
      - key: OPENROUTER_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.9
```
- [ ] **Step 2: requirements mínimo**
```
streamlit>=1.28.0
pandas==2.1.0
numpy==1.24.0
plotly
```
- [ ] **Step 3: smoke**
Run: `python -m py_compile app.py modules/*.py`
Run: `streamlit run app.py --server.headless true --server.port 8502` 15s, curl localhost:8502, matar proceso.
Expected: HTTP 200, sin traceback.
