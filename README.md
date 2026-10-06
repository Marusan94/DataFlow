# DataFlow 📊 — Convierte tus datos en decisiones

<p>
  <img src="https://img.shields.io/badge/python-3.11-blue" alt="python 3.11">
  <img src="https://img.shields.io/badge/streamlit-app-red" alt="streamlit">
  <img src="https://img.shields.io/badge/pandas-data-green" alt="pandas">
  <img src="https://img.shields.io/badge/plotly-charts-blueviolet" alt="plotly">
  <img src="https://img.shields.io/badge/deploy-render-green" alt="render">
  <img src="https://img.shields.io/badge/license-MIT-yellow" alt="MIT">
</p>

> Ex-EduAnalytics HUB, rehecho agnóstico estilo DataFlow. **Stack:** Python 3.11 · Streamlit · Pandas · Plotly · Render · **Estado:** Demo funcional, auth simulada, mobile-ready.

**¿Qué es?** Un HUB genérico para cualquier CSV: Analiza. Visualiza. Explora. Todo en un solo lugar. Sin ataduras a datos educativos — lo único rescatado del proyecto anterior es la idea de pipeline Analizar → Evaluar → Asistir → Actuar, ahora como 4 tipos de proyecto agnósticos.

## 🧭 El proyecto en breve

**Analítica self-service**

- **Problema:** Analizar datos exige varias herramientas y saber programar.
- **Automatización:** Hub donde subes datos y analizas, evalúas y actúas en un solo lugar.
- **Resultado:** Desplegado y usable hoy.

`Python` · `Streamlit` · `Pandas` — [Demo →](https://eduanalytics.onrender.com) · [Código →](https://github.com/Marusan94/DataFlow)

## ✨ Features

| Área | Qué obtienes |
|------|--------------|
| 📊 **Analizar** | Perfilado agnóstico de cualquier CSV: tipos, nulos, duplicados, categorías, numéricos y fechas |
| 📈 **Evaluar** | Visualizaciones Plotly interactivas + métricas por columna para decidir con datos |
| 🤖 **Asistir** | Chat de IA opcional (OpenRouter) con fallback local si no hay API key |
| 🎯 **Actuar** | 4 tipos de proyecto agnósticos + datasets, explorador con filtros y configuración |
| 🔐 **Acceso** | Auth simulada con 7 pantallas (login, registro, 2FA demo, recupero) y 4 roles: Analista / Desarrollador / Estudiante / Investigador |
| 📁 **Datos** | Sube cualquier CSV o usa `datos_ejemplo.csv` (ventas genéricas) para ver el análisis sin subir nada |

## 📸 Screenshots

| Vista | Captura |
|-------|---------|
| **Home / Landing** | ![Home](docs/screenshots/home.png) |
| **Datasets / Upload** | ![Datasets](docs/screenshots/datasets.png) |
| **Explorador** | ![Explorer](docs/screenshots/explorer.png) |

---

## 🛠️ Stack

| Capa | Tecnologías |
|------|-------------|
| **App** | Python 3.11, Streamlit |
| **Datos** | Pandas, NumPy, Plotly |
| **IA** | OpenAI-compat (OpenRouter, opcional) |
| **Deploy** | Render (`render.yaml`), `runtime.txt` python-3.11.9 |

## 🚀 Demo en vivo

[https://eduanalytics.onrender.com](https://eduanalytics.onrender.com) — entra con cualquier email con `@` + contraseña de 8 caracteres. Verificación y 2FA usan `123456`.

## 🔧 Casos de uso

| Perfil | Qué haces |
|--------|-----------|
| **Analista de datos** | Sube CSV → perfilado automático → visualizaciones Plotly → exporta insights |
| **Desarrollador** | Explora datasets, prueba reglas de validación, integra con API |
| **Estudiante / Investigador** | Dataset de ejemplo listo, análisis guiado sin configuración, chat IA para preguntas |
| **Equipo** | Roles diferenciados, proyectos compartidos, historial de versiones |

## 📖 Uso rápido

```bash
# Local
pip install -r requirements.txt
streamlit run app.py  # http://localhost:8501

# Render (push a main → deploy automático)
# Variables: OPENROUTER_API_KEY (opcional)
```

## Pantallas (como la imagen de referencia)
- Landing `Convierte tus datos en decisiones` + bullets Análisis / ML / Visualización / Colaboración
- Login (email + 8 chars, botones GitHub/Google demo) · Registro · Verifica 6 dígitos demo `123456`
- Recupera · Nueva contraseña · 2FA demo · Elige rol (Analista / Desarrollador / Estudiante / Investigador)
- Home `Hola, Santiago` + buscador + 3 cards (Explorar / Analizar con IA / Nuevo proyecto)
- Proyectos · Datasets (sube cualquier CSV o usa `datos_ejemplo.csv`) · Explorador (filtros) · IA (OpenRouter opcional, fallback local) · Configuración

## Tema
`background #111110` · `surface #191918` · `borders #2A2A28` · `accent #B9B091` · `text #F2F1EC` · font Inter/SF Pro. Ver `.streamlit/config.toml` + `modules/design.py`.

## Estructura
```
.
├── app.py                 # Router session_state.page DataFlow
├── modules/
│   ├── design.py          # Tokens + CSS + show_logo + go
│   ├── auth_ui.py         # 7 pantallas auth simulada
│   ├── home.py            # Hola + search + cards + sidebar
│   ├── work.py            # projects/datasets/explorer/ai/settings
│   ├── generic_analyzer.py# Perfilado agnóstico CSV
│   └── _legacy/           # Código educativo anterior (no se usa)
├── datos_ejemplo.csv      # Ventas genéricas (fecha, canal, producto, unidades, ingreso, costo, región)
├── datos_educativos.csv   # Legacy, solo referencia
├── .streamlit/config.toml # Tema dark DataFlow
├── requirements.txt       # streamlit, pandas, numpy, plotly, openai
├── runtime.txt            # python-3.11.9
└── render.yaml            # service dataflow, sync:false para OPENROUTER_API_KEY
```

## Uso
```bash
pip install -r requirements.txt
streamlit run app.py  # http://localhost:8501
```
Demo: cualquier email con @ + password 8 chars → Home. Verify/2FA usan `123456`. En Datasets usa `▶️ Usar datos de ejemplo` para ver el análisis sin subir nada.

**API Key (opcional):** solo para IA remota. Local: `.streamlit/secrets.toml` con `OPENROUTER_API_KEY`. Render: Environment → `OPENROUTER_API_KEY` (`sync:false`). Sin key, la IA responde local demo.

## Deploy Render
Mismo repo, servicio renombrado a `dataflow` en `render.yaml`. El rename del repo en GitHub (Settings → Rename a DataFlow) lo hace el dueño. Requiere `RENDER_API_KEY` + serviceId para deploy por API.

## 📄 License

MIT — see [LICENSE](LICENSE).

## Autor
**Santiago Marulanda Leguizamo** — UdeA · https://github.com/Marusan94

MIT.
