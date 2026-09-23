# DataFlow Remake — Design Spec (2026-09-23)

## Contexto
Remake de `Marusan94/Eduanalytics` (Streamlit, EduAnalytics HUB) hacia estética `DataFlow` de la imagen de referencia.
Decisiones del usuario: mantener Streamlit, auth solo UI simulada, rescatar solo estructura agnóstica (Analizar→Evaluar→Asistir→Actuar), mismo repo renombrado, deploy en Render con token del usuario.

## Objetivo
Reemplazar la app educativa acoplada (14 análisis fijos, dashboard Medellín, STEAM Lab educativo) por un HUB genérico estilo DataFlow:
`Convierte tus datos en decisiones. Analiza. Visualiza. Explora.`

## Alcance
### Incluye
- Router custom `app.py` con `session_state.page`: `landing, login, register, verify, recover, reset, twofa, role, home, projects, datasets, explorer, ai, settings`.
- Auth simulada: cualquier email + password >=8 chars pasa; verify acepta `123456` en demo; recover/reset/2FA solo UI; rol guarda en session (Analista / Desarrollador / Estudiante / Investigador).
- Home `Hola, Santiago`: buscador + 3 cards (Explorar datos / Analizar con IA / Nuevo proyecto).
- Analizador genérico `generic_analyzer.py`: perfila CUALQUIER CSV (shape, dtypes, describe, nulos, correlación numérica, top valores categóricos, histogramas Plotly). Nada de `nota/asistencia/grupo_id` hardcodeado.
- 4 tipos de proyecto agnósticos: Análisis tabular, Mapa, Chat IA (opcional OpenRouter si hay key, si no mock), Lab genérico.
- Tema DataFlow: `background #111110, surface #191918, borders #2A2A28, accent #B9B091, text #F2F1EC`, font Inter/SF Pro, botón primario beige texto negro, inputs `#1E1E1C` radius 8px.
- Rebrand: `app.py title DataFlow`, `render.yaml name: dataflow`, `README.md` nuevo, `requirements.txt` mínimo.
- Mobile 390px OK.

### No incluye
- Auth real (Supabase/Auth0/OAuth Google/GitHub, emails reales, 2FA real).
- Migración de lógica educativa (se borra `analytics.py` 14 queries, `dashboard_geo` Medellín, `steam_lab` educativo).
- DB persistente (solo session_state + SQLite existente si acaso, no bloqueante).
- Tests E2E (solo `py_compile` + smoke manual).

## Arquitectura
```
repo/
  app.py                  # router + page_config DataFlow + CSS tokens
  modules/
    design.py             # tokens, CSS, helpers UI
    auth_ui.py            # 7 pantallas auth simulada
    home.py               # Hola Santiago + search + cards
    projects.py           # CRUD session_state proyectos
    generic_analyzer.py   # perfilado agnóstico CSV
    datasets.py           # upload/list datasets session
    explorer.py           # tabla + filtros genéricos
    ai_basic.py           # chat mock + OpenRouter opcional
    settings.py           # rol, tema, reset demo
  .streamlit/config.toml  # dark DataFlow
  render.yaml             # name dataflow, mismo startCommand
  requirements.txt        # streamlit, pandas, plotly, numpy
  datos_ejemplo.csv       # CSV genérico (no educativo)
```

## Data flow
Landing → login simulado → verify (`123456`) → role (1 de 4) → home. `session_state.user={name,email,role,verified}`. `session_state.projects=[{id,tipo,titulo,fecha}]`. `session_state.datasets` en memoria. Sin secretos requeridos para demo.

## Riesgos
- Streamlit no logra pixel-perfect 100% de la imagen (topbar/sidebar nativos). Mitigación: `collapsed sidebar`, CSS `stApp` full-bleed, cards con `st.container(border=True)`.
- Rename del repo en GitHub lo debe hacer el usuario en Settings (no se hace por código). Yo actualizo contenido + remote.
- Deploy Render requiere `RENDER_API_KEY` + serviceId que el usuario prometió. Sin eso, dejo repo listo + instrucciones.

## Verificación
1. `python -m py_compile app.py modules/*.py`
2. `streamlit run app.py --server.headless true` smoke 30s
3. Checklist visual 9 pantallas imagen vs app
4. Mobile 390px

## Spec self-review
- Sin TBD/TODO: auth simulada explícita, código verify `123456` explícito.
- Consistencia: agnóstico en todos los módulos, no quedan columnas educativas.
- Scope: un solo ciclo spec→plan→build, no sub-proyectos.
- Ambigüedad: nombre final `DataFlow`, repo mismo, deploy mismo servicio renombrado.
