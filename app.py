import streamlit as st
from agente_personaje import crear_agente, PERSONAJE_TEMPLATES

st.set_page_config(page_title="Creador de Personajes", page_icon="⚔️", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


def get_css(theme):
    if theme == "dark":
        return """
        <style>
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
        }
        .title {
            color: #e94560;
            text-align: center;
            font-size: 3rem;
            text-shadow: 0 0 20px rgba(233, 69, 96, 0.5);
            margin-bottom: 2rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }
        .card-title {
            color: #e94560;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #e94560;
            padding-bottom: 0.5rem;
        }
        .btn-primary {
            background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
            border: none;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(233, 69, 96, 0.3);
        }
        .sidebar {
            background: rgba(0, 0, 0, 0.3);
            padding: 1rem;
            border-radius: 12px;
        }
        .template-btn {
            background: rgba(233, 69, 96, 0.2);
            border: 1px solid #e94560;
            color: #e94560;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin: 0.3rem 0;
        }
        .template-btn:hover {
            background: #e94560;
            color: white;
        }
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #e8e8e8;
        }
        .stSelectbox > div > div > div {
            background: rgba(255, 255, 255, 0.1);
            color: #e8e8e8;
        }
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #e8e8e8;
        }
        </style>
        """
    else:
        return """
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2d3436;
        }
        .title {
            color: #6c5ce7;
            text-align: center;
            font-size: 3rem;
            text-shadow: 0 0 20px rgba(108, 92, 231, 0.3);
            margin-bottom: 2rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(108, 92, 231, 0.2);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .card-title {
            color: #6c5ce7;
            font-size: 1.3rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid #6c5ce7;
            padding-bottom: 0.5rem;
        }
        .btn-primary {
            background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
            border: none;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(108, 92, 231, 0.3);
        }
        .sidebar {
            background: rgba(255, 255, 255, 0.5);
            padding: 1rem;
            border-radius: 12px;
        }
        .template-btn {
            background: rgba(108, 92, 231, 0.1);
            border: 1px solid #6c5ce7;
            color: #6c5ce7;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            margin: 0.3rem 0;
        }
        .template-btn:hover {
            background: #6c5ce7;
            color: white;
        }
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(108, 92, 231, 0.3);
            color: #2d3436;
        }
        .stSelectbox > div > div > div {
            background: rgba(255, 255, 255, 0.8);
            color: #2d3436;
        }
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(108, 92, 231, 0.3);
            color: #2d3436;
        }
        </style>
        """


st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
theme_label = "Modo Oscuro" if st.session_state.theme == "dark" else "Modo Claro"

col1, col2 = st.columns([6, 1])
with col1:
    st.markdown(
        '<h1 class="title">⚔️ Creador de Personajes ⚔️</h1>', unsafe_allow_html=True
    )
with col2:
    if st.button(f"{theme_icon} {theme_label}", key="theme_toggle"):
        toggle_theme()
        st.rerun()

col_main, col_sidebar = st.columns([3, 1])

with col_sidebar:
    st.markdown('<div class="sidebar">', unsafe_allow_html=True)
    st.markdown("### 📜 Templates")

    template_seleccionado = st.radio(
        "Selecciona un tipo:",
        options=list(PERSONAJE_TEMPLATES.keys()),
        format_func=lambda x: f"{x.title()}",
    )

    if template_seleccionado:
        template = PERSONAJE_TEMPLATES[template_seleccionado]
        st.markdown(
            f"""
        <div class="card" style="margin-top: 1rem; padding: 1rem;">
            <strong>Tipo:</strong> {template.tipo}<br>
            <strong>Edad:</strong> {template.edad_base}<br>
            <strong>Personalidad:</strong> {template.personalidad_base}
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with col_main:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🎭 Describe tu personaje")

    descripcion = st.text_area(
        "Describe a tu personaje:",
        placeholder="Ej: Crea un heroe llamado Valerius que lucha contra el mal, tiene poderes de luz y es un guerrero noble",
        height=120,
    )

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        nombre_manual = st.text_input(
            "O especifica un nombre:", placeholder="Ej: Valerius"
        )
    with col_btn2:
        edad_manual = st.text_input("Edad específica:", placeholder="Ej: 25 años")

    if st.button("✨ Crear Personaje", type="primary", use_container_width=True):
        if descripcion or nombre_manual:
            if nombre_manual:
                descripcion = f"Crea un personaje llamado {nombre_manual}. " + (
                    descripcion or ""
                )
            if edad_manual:
                descripcion += f" Tiene {edad_manual}."

            with st.spinner("🪄 Creando personaje..."):
                try:
                    agente = crear_agente()
                    resultado = agente.crear_personaje(descripcion)

                    personaje = resultado["personaje_obj"]

                    st.markdown("### 🎉 ¡Personaje Creado!")

                    cols = st.columns(3)
                    with cols[0]:
                        st.markdown(
                            f"""
                        <div class="card">
                            <div class="card-title">👤 Información</div>
                            <strong>Nombre:</strong> {personaje.nombre}<br>
                            <strong>Edad:</strong> {personaje.edad}<br>
                            <strong>Raza:</strong> {personaje.raza}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with cols[1]:
                        st.markdown(
                            f"""
                        <div class="card">
                            <div class="card-title">🎭 Personalidad</div>
                            {personaje.personalidad}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with cols[2]:
                        st.markdown(
                            f"""
                        <div class="card">
                            <div class="card-title">⚔️ Ropa</div>
                            {personaje.ropa}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        f"""
                    <div class="card">
                        <div class="card-title">📖 Historia</div>
                        {personaje.historia}
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        st.markdown(
                            f"""
                        <div class="card">
                            <div class="card-title">🔥 Poderes</div>
                            {"".join([f"• {p}<br>" for p in personaje.poderes])}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col_p2:
                        st.markdown(
                            f"""
                        <div class="card">
                            <div class="card-title">💀 Enemigos</div>
                            {"".join([f"• {e}<br>" for e in personaje.enemigos])}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with st.expander("📋 Ver personaje completo en Markdown"):
                        st.code(resultado["personaje"], language="markdown")

                except Exception as e:
                    st.error(f"Error al crear el personaje: {str(e)}")
        else:
            st.warning("Por favor describe tu personaje o ingresa un nombre")

    st.markdown("</div>", unsafe_allow_html=True)
