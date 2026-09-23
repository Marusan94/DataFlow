"""Auth simulada DataFlow: 7 pantallas solo UI, sin backend. Verify demo: 123456."""
import streamlit as st
from modules.design import show_logo, go

DEMO_CODE = "123456"
ROLES = [
    ("Analista de datos", "Explora y visualiza datos", "📊"),
    ("Desarrollador", "Construye y automatiza", "💻"),
    ("Estudiante", "Aprende y practica", "📦"),
    ("Investigador", "Analiza y descubre", "🔍"),
]

def _init():
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("pending_email", "")

def skip_auth():
    """Auth opcional: entra al Home con usuario demo sin registrarse."""
    st.session_state.user = {"name": "Santiago", "email": "demo@dataflow.app",
                             "role": "Analista de datos", "verified": True, "guest": True}
    go("home")

def _skip_button(label="Omitir por ahora →", key="skip"):
    st.caption("El registro es opcional en esta demo.")
    if st.button(label, key=key, use_container_width=True):
        skip_auth()

def render_landing():
    _init()
    show_logo()
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown("<div class='df-title'>Convierte<br>tus datos en<br>decisiones.</div>", unsafe_allow_html=True)
        st.markdown("<div class='df-sub'>Analiza. Visualiza. Explora.<br>Todo en un solo lugar.</div>", unsafe_allow_html=True)
        st.write("")
        for icon, label in [("📈", "Análisis de datos"), ("🤖", "Machine Learning"), ("📊", "Visualización"), ("👥", "Colaboración")]:
            st.markdown(f"{icon} &nbsp; <span class='small-muted'>{label}</span>", unsafe_allow_html=True)
        st.write("")
        if st.button("Iniciar sesión", type="primary", use_container_width=True):
            go("login")
        if st.button("Crear cuenta", use_container_width=True):
            go("register")
        st.write("")
        _skip_button("Explorar sin cuenta →", key="skip_landing")
    with c2:
        st.markdown(
            "<div class='df-hero'>"
            "<div class='df-hero-title'>DataFlow</div>"
            "<div class='df-hero-sub'>Datos. Análisis. Decisiones.</div>"
            "</div>", unsafe_allow_html=True)

def render_login():
    _init()
    show_logo(small=True)
    st.markdown("<div class='df-auth-center'>", unsafe_allow_html=True)
    st.markdown("### Bienvenido de nuevo")
    st.caption("Inicia sesión en tu espacio de trabajo")
    st.button("Continuar con GitHub (demo)", use_container_width=True, on_click=skip_auth)
    st.button("Continuar con Google (demo)", use_container_width=True, on_click=skip_auth)
    st.caption("o")
    email = st.text_input("Correo electrónico", placeholder="tu@ejemplo.com", value=st.session_state.pending_email)
    pwd = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Recordarme", value=True)
    with c2:
        if st.button("¿Olvidaste tu contraseña?", key="forgot"):
            go("recover")
    if st.button("Iniciar sesión", type="primary", use_container_width=True):
        if "@" not in email:
            st.error("Ingresa un correo válido (demo: cualquiera con @).")
        elif len(pwd) < 8:
            st.error("La contraseña debe tener al menos 8 caracteres (demo).")
        else:
            st.session_state.user = {"name": email.split("@")[0].title(), "email": email, "role": "Analista de datos", "verified": True}
            go("home")
    cc1, cc2 = st.columns([2, 1])
    with cc1:
        st.caption("¿No tienes una cuenta?")
    with cc2:
        if st.button("Crear cuenta"):
            go("register")
    st.write("")
    _skip_button(key="skip_login")
    st.markdown("</div>", unsafe_allow_html=True)

def render_register():
    _init()
    if st.button("← Volver"):
        go("landing")
    show_logo(small=True)
    st.markdown("<div class='df-auth-center'>", unsafe_allow_html=True)
    st.markdown("### Crea tu cuenta")
    st.caption("Únete a DataFlow y empieza a explorar tus datos.")
    name = st.text_input("Nombre completo", placeholder="Tu nombre")
    email = st.text_input("Correo electrónico", placeholder="tu@ejemplo.com")
    pwd = st.text_input("Contraseña", type="password", placeholder="Mínimo 8 caracteres")
    ok = st.checkbox("Acepto los Términos y Condiciones y la Política de Privacidad")
    if st.button("Crear cuenta", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Ingresa tu nombre.")
        elif "@" not in email:
            st.error("Correo inválido.")
        elif len(pwd) < 8:
            st.error("Mínimo 8 caracteres.")
        elif not ok:
            st.error("Debes aceptar los términos (demo).")
        else:
            st.session_state.pending_email = email
            st.session_state.user = {"name": name.strip(), "email": email, "role": None, "verified": False}
            go("verify")
    if st.button("¿Ya tienes una cuenta? Inicia sesión"):
        go("login")
    st.write("")
    _skip_button(key="skip_register")
    st.markdown("</div>", unsafe_allow_html=True)

def _code_boxes(prefix="code", n=6):
    """6 casillas como en la imagen DataFlow. Retorna el código unido."""
    cols = st.columns(n, gap="small")
    digits = []
    for i in range(n):
        with cols[i]:
            d = st.text_input(f"{prefix}{i}", value=st.session_state.get(f"{prefix}{i}", ""),
                              max_chars=1, key=f"{prefix}_{i}", label_visibility="collapsed",
                              placeholder=str(i + 1))
            digits.append(d.strip())
    return "".join(digits)

def render_verify():
    _init()
    if st.button("← Volver"):
        go("register")
    show_logo(small=True)
    st.markdown("<div class='df-auth-center'>", unsafe_allow_html=True)
    st.markdown("### Verifica tu correo")
    email = (st.session_state.user or {}).get("email", st.session_state.pending_email) or "tu@ejemplo.com"
    st.caption(f"Te enviamos un código de 6 dígitos a {email} (demo: {DEMO_CODE}).")
    code = _code_boxes(prefix="verify", n=6)
    if st.button("Verificar", type="primary", use_container_width=True):
        if code == DEMO_CODE:
            if st.session_state.user:
                st.session_state.user["verified"] = True
            go("role")
        else:
            st.error(f"Código demo incorrecto. Usa {DEMO_CODE}.")
    st.write("")
    _skip_button("Saltar verificación →", key="skip_verify")
    st.markdown("</div>", unsafe_allow_html=True)

def render_recover():
    if st.button("← Volver"):
        go("login")
    show_logo(small=True)
    st.markdown("### Recupera tu contraseña")
    st.caption("Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.")
    email = st.text_input("Correo electrónico", placeholder="tu@ejemplo.com")
    if st.button("Enviar enlace", type="primary", use_container_width=True):
        if "@" not in email:
            st.error("Correo inválido.")
        else:
            st.success("Enlace enviado (demo). Revisa tu bandeja y usa la pantalla de nueva contraseña.")
            go("reset")
    if st.button("¿Recordaste tu contraseña? Inicia sesión"):
        go("login")

def render_reset():
    if st.button("← Volver"):
        go("login")
    show_logo(small=True)
    st.markdown("### Establece una nueva contraseña")
    st.caption("Debe tener al menos 8 caracteres.")
    p1 = st.text_input("Nueva contraseña", type="password", placeholder="Mínimo 8 caracteres")
    p2 = st.text_input("Confirmar contraseña", type="password", placeholder="Repite tu contraseña")
    if st.button("Restablecer contraseña", type="primary", use_container_width=True):
        if len(p1) < 8:
            st.error("Mínimo 8 caracteres.")
        elif p1 != p2:
            st.error("No coinciden.")
        else:
            st.success("Contraseña actualizada (demo).")
            go("login")

def render_twofa():
    if st.button("← Volver"):
        go("login")
    show_logo(small=True)
    st.markdown("### Autenticación de dos factores")
    st.caption("Ingresa el código de 6 dígitos de tu app de autenticación (demo: 123456).")
    code = st.text_input("Código 2FA", placeholder="123456", max_chars=6)
    if st.button("Verificar", type="primary", use_container_width=True):
        if code.strip() == DEMO_CODE:
            go("home")
        else:
            st.error("Usa 123456 en demo.")

def render_role():
    show_logo(small=True)
    st.progress(0.25, text="1 de 4")
    st.markdown("<div class='df-auth-center'>", unsafe_allow_html=True)
    st.markdown("### ¿Cuál es tu rol?")
    st.caption("Nos ayudará a personalizar tu experiencia.")
    cols = st.columns(2)
    selected = st.session_state.get("role_pick", ROLES[0][0])
    for i, (title, desc, icon) in enumerate(ROLES):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"{icon} **{title}**<br><span class='small-muted'>{desc}</span>", unsafe_allow_html=True)
                if st.button(f"Elegir {title}", key=f"role_{i}", use_container_width=True):
                    st.session_state.role_pick = title
                    selected = title
    st.caption(f"Seleccionado: **{selected}**")
    if st.button("Siguiente →", type="primary", use_container_width=True):
        u = st.session_state.user or {"name": "Santiago", "email": "demo@dataflow.app", "verified": True}
        u["role"] = st.session_state.get("role_pick", ROLES[0][0])
        u["verified"] = True
        st.session_state.user = u
        go("home")
    st.write("")
    _skip_button("Elegir después →", key="skip_role")
    st.markdown("</div>", unsafe_allow_html=True)
