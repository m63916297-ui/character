import streamlit as st
from personajes_data import PERSONAJES_PREDEFINIDOS, buscar_personaje_por_nombre
import random

st.set_page_config(
    page_title="NEXUS // Character Creator",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    * { box-sizing: border-box; }
    
    html, body, .stApp {
        font-family: 'Rajdhani', sans-serif;
        background: #050508;
        color: #c0c0c0;
        margin: 0;
        padding: 0;
    }
    
    .stApp {
        background: 
            linear-gradient(180deg, #080810 0%, #0a0a12 50%, #06060a 100%);
        min-height: 100vh;
    }
    
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid rgba(0, 255, 242, 0.15);
        margin-bottom: 1.5rem;
    }
    
    .logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #00fff2;
        text-shadow: 0 0 30px rgba(0, 255, 242, 0.5);
        letter-spacing: 20px;
        margin: 0;
    }
    
    .tagline {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.75rem;
        color: #8b5cf6;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Layout Grid */
    .content-grid {
        display: grid;
        grid-template-columns: 280px 1fr 280px;
        gap: 1.5rem;
        align-items: start;
    }
    
    @media (max-width: 1200px) {
        .content-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Panels */
    .panel {
        background: linear-gradient(180deg, rgba(15, 15, 25, 0.95) 0%, rgba(8, 8, 15, 0.98) 100%);
        border: 1px solid rgba(0, 255, 242, 0.12);
        border-radius: 4px;
        padding: 1.25rem;
        position: relative;
    }
    
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.7rem;
        color: #00fff2;
        letter-spacing: 3px;
        text-transform: uppercase;
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 255, 242, 0.1);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .panel-header::before {
        content: '◆';
        color: #8b5cf6;
        font-size: 0.5rem;
    }
    
    /* Form Elements */
    .form-group {
        margin-bottom: 1rem;
    }
    
    .form-label {
        font-size: 0.7rem;
        color: #8b5cf6;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
        display: block;
    }
    
    .neon-input, .neon-select {
        width: 100%;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(0, 255, 242, 0.2);
        border-radius: 3px;
        color: #00fff2;
        padding: 0.6rem 0.8rem;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem;
        transition: all 0.2s;
    }
    
    .neon-input:focus, .neon-select:focus {
        outline: none;
        border-color: #00fff2;
        box-shadow: 0 0 15px rgba(0, 255, 242, 0.15);
    }
    
    .neon-input::placeholder {
        color: rgba(0, 255, 242, 0.3);
    }
    
    /* Sliders */
    .slider-group {
        margin-bottom: 0.8rem;
    }
    
    .slider-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.3rem;
    }
    
    .slider-value {
        color: #00fff2;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .stat-bar {
        height: 6px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 3px;
        overflow: hidden;
    }
    
    .stat-fill {
        height: 100%;
        background: linear-gradient(90deg, #8b5cf6, #00fff2);
        border-radius: 3px;
        transition: width 0.3s;
    }
    
    /* Buttons */
    .btn-primary {
        width: 100%;
        background: linear-gradient(180deg, rgba(0, 255, 242, 0.15) 0%, rgba(0, 255, 242, 0.05) 100%);
        border: 1px solid rgba(0, 255, 242, 0.4);
        color: #00fff2;
        padding: 0.8rem 1.5rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 2px;
        cursor: pointer;
        transition: all 0.2s;
        text-transform: uppercase;
    }
    
    .btn-primary:hover {
        background: linear-gradient(180deg, rgba(0, 255, 242, 0.25) 0%, rgba(0, 255, 242, 0.1) 100%);
        box-shadow: 0 0 25px rgba(0, 255, 242, 0.2);
    }
    
    .btn-secondary {
        background: transparent;
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #8b5cf6;
        padding: 0.5rem 1rem;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .btn-secondary:hover {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.1);
    }
    
    /* Character Viewer */
    .viewer {
        background: radial-gradient(ellipse at center bottom, rgba(0, 255, 242, 0.03) 0%, transparent 60%),
                    linear-gradient(180deg, #0a0a12 0%, #050508 100%);
        border: 1px solid rgba(0, 255, 242, 0.1);
        border-radius: 4px;
        height: 420px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .viewer-grid {
        position: absolute;
        width: 200%;
        height: 200%;
        bottom: -50%;
        background-image: 
            linear-gradient(rgba(0, 255, 242, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 242, 0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        transform: perspective(500px) rotateX(60deg);
        animation: gridScroll 15s linear infinite;
    }
    
    @keyframes gridScroll {
        0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
        100% { transform: perspective(500px) rotateX(60deg) translateY(40px); }
    }
    
    .character-model {
        width: 140px;
        height: 320px;
        position: relative;
        animation: float 4s ease-in-out infinite;
        z-index: 1;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .model-body {
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, 
            rgba(139, 92, 246, 0.25) 0%, 
            rgba(0, 255, 242, 0.15) 50%,
            rgba(139, 92, 246, 0.2) 100%);
        clip-path: polygon(
            50% 0%, 62% 4%, 68% 12%, 66% 22%, 72% 28%,
            78% 38%, 82% 48%, 78% 58%, 82% 68%, 74% 78%,
            68% 84%, 58% 90%, 42% 90%, 32% 84%, 26% 78%,
            18% 68%, 22% 58%, 18% 48%, 22% 38%, 34% 28%,
            38% 22%, 32% 12%, 38% 4%
        );
    }
    
    .viewer-hud {
        position: absolute;
        padding: 0.75rem;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.6rem;
        letter-spacing: 1px;
        color: rgba(0, 255, 242, 0.5);
    }
    
    .viewer-hud.top-left { top: 0; left: 0; }
    .viewer-hud.top-right { top: 0; right: 0; text-align: right; }
    .viewer-hud.bottom-left { bottom: 0; left: 0; }
    .viewer-hud.bottom-right { bottom: 0; right: 0; text-align: right; }
    
    /* Character Info */
    .char-name {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        color: #00fff2;
        text-shadow: 0 0 20px rgba(0, 255, 242, 0.4);
        margin: 0 0 0.5rem 0;
    }
    
    .char-subtitle {
        font-size: 0.8rem;
        color: #8b5cf6;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    
    .info-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .info-item {
        background: rgba(0, 0, 0, 0.3);
        padding: 0.5rem 0.75rem;
        border-radius: 3px;
        border-left: 2px solid rgba(0, 255, 242, 0.3);
    }
    
    .info-label {
        font-size: 0.65rem;
        color: #8b5cf6;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .info-value {
        color: #00fff2;
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    .section-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.65rem;
        color: #00fff2;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
        padding-bottom: 0.3rem;
        border-bottom: 1px solid rgba(0, 255, 242, 0.1);
    }
    
    .list-item {
        font-size: 0.85rem;
        color: #a0a0a0;
        padding: 0.2rem 0;
        padding-left: 1rem;
        position: relative;
    }
    
    .list-item::before {
        content: '›';
        position: absolute;
        left: 0;
        color: #8b5cf6;
    }
    
    /* Color Swatches */
    .color-row {
        display: flex;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
    }
    
    .color-swatch {
        width: 28px;
        height: 28px;
        border-radius: 3px;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.2s;
    }
    
    .color-swatch:hover {
        transform: scale(1.1);
        border-color: #00fff2;
    }
    
    .color-swatch.active {
        border-color: #00fff2;
        box-shadow: 0 0 10px currentColor;
    }
    
    /* Quick Stats */
    .quick-stats {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
        text-align: center;
    }
    
    .quick-stat {
        background: rgba(0, 0, 0, 0.3);
        padding: 0.5rem;
        border-radius: 3px;
    }
    
    .quick-stat-value {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.1rem;
        color: #00fff2;
    }
    
    .quick-stat-label {
        font-size: 0.55rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Character List */
    .char-list {
        max-height: 200px;
        overflow-y: auto;
    }
    
    .char-list::-webkit-scrollbar {
        width: 4px;
    }
    
    .char-list::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    .char-list::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 242, 0.3);
        border-radius: 2px;
    }
    
    .char-list-item {
        padding: 0.5rem 0.75rem;
        cursor: pointer;
        transition: all 0.15s;
        border-left: 2px solid transparent;
        font-size: 0.85rem;
    }
    
    .char-list-item:hover {
        background: rgba(0, 255, 242, 0.05);
        border-left-color: rgba(0, 255, 242, 0.3);
    }
    
    .char-list-item.active {
        background: rgba(139, 92, 246, 0.1);
        border-left-color: #8b5cf6;
        color: #00fff2;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 242, 0.1), transparent);
        margin: 1rem 0;
    }
    
    /* Hidden elements */
    .stSelectbox > div > div { background: transparent !important; }
    .stSlider > div > div > div[role="slider"] {
        background: linear-gradient(90deg, #8b5cf6, #00fff2) !important;
        border: none !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 1.5rem;
        border-top: 1px solid rgba(0, 255, 242, 0.1);
        font-size: 0.7rem;
        color: rgba(0, 255, 242, 0.3);
    }
</style>
""",
    unsafe_allow_html=True,
)

if "customization" not in st.session_state:
    st.session_state.customization = {
        "race": "Humano",
        "class": "Guerrero",
        "age": 25,
        "strength": 65,
        "agility": 55,
        "intelligence": 50,
        "charisma": 60,
        "armor_color": "#00fff2",
        "accent_color": "#8b5cf6",
    }

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    """
<div class="header">
    <h1 class="logo">NEXUS</h1>
    <div class="tagline">Character Creation System v2.0</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="content-grid">', unsafe_allow_html=True)

# ===== LEFT PANEL =====
with st.container():
    st.markdown(
        """
    <div class="panel">
        <div class="panel-header">Personaje</div>
    """,
        unsafe_allow_html=True,
    )

    races = ["Humano", "Ciborg", "Mutante", "Alienígena", "Androide", "Híbrido"]
    classes = ["Guerrero", "Asesino", "Mago", "Ingeniero", "Médico", "Piloto", "Hacker"]

    race_idx = (
        races.index(st.session_state.customization["race"])
        if st.session_state.customization["race"] in races
        else 0
    )
    class_idx = (
        classes.index(st.session_state.customization["class"])
        if st.session_state.customization["class"] in classes
        else 0
    )

    race = st.selectbox(
        "RAZA",
        options=races,
        index=race_idx,
        label_visibility="collapsed",
        key="race_select",
    )
    st.session_state.customization["race"] = race

    char_class = st.selectbox(
        "CLASE",
        options=classes,
        index=class_idx,
        label_visibility="collapsed",
        key="class_select",
    )
    st.session_state.customization["class"] = char_class

    age = st.slider(
        "EDAD",
        15,
        120,
        st.session_state.customization["age"],
        label_visibility="collapsed",
        key="age_slider",
    )
    st.session_state.customization["age"] = age

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="panel" style="margin-top: 1rem;">
        <div class="panel-header">Atributos</div>
    """,
        unsafe_allow_html=True,
    )

    def render_stat(name, key):
        val = st.session_state.customization[key]
        st.markdown(
            f"""
        <div class="slider-group">
            <div class="slider-header">
                <span class="form-label">{name}</span>
                <span class="slider-value">{val}</span>
            </div>
            <div class="stat-bar">
                <div class="stat-fill" style="width: {val}%;"></div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        new_val = st.slider(
            f"_{key}", 0, 100, val, label_visibility="collapsed", key=f"slider_{key}"
        )
        st.session_state.customization[key] = new_val

    render_stat("FUERZA", "strength")
    render_stat("AGILIDAD", "agility")
    render_stat("INTELIGENCIA", "intelligence")
    render_stat("CARISMA", "charisma")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="panel" style="margin-top: 1rem;">
        <div class="panel-header">Colores</div>
    """,
        unsafe_allow_html=True,
    )

    armor_colors = ["#00fff2", "#8b5cf6", "#ff0080", "#00ff88", "#ffaa00"]
    accent_colors = ["#8b5cf6", "#00fff2", "#ff0080", "#00ff88"]

    st.markdown('<div class="form-label">ARMADURA</div>', unsafe_allow_html=True)
    armor_cols = st.columns([1] * len(armor_colors))
    for i, color in enumerate(armor_colors):
        with armor_cols[i]:
            is_active = st.session_state.customization["armor_color"] == color
            if st.button(" ", key=f"armor_{i}", help=color):
                st.session_state.customization["armor_color"] = color
                st.rerun()

    st.markdown(
        '<div class="form-label" style="margin-top: 0.75rem;">ACENTO</div>',
        unsafe_allow_html=True,
    )
    accent_cols = st.columns([1] * len(accent_colors))
    for i, color in enumerate(accent_colors):
        with accent_cols[i]:
            is_active = st.session_state.customization["accent_color"] == color
            if st.button(" ", key=f"accent_{i}", help=color):
                st.session_state.customization["accent_color"] = color
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ===== CENTER PANEL =====
with st.container():
    armor = st.session_state.customization["armor_color"]
    accent = st.session_state.customization["accent_color"]

    char_name = (
        st.session_state.selected_character["nombre"]
        if st.session_state.selected_character
        else "NEXUS-7"
    )
    char_class = (
        st.session_state.selected_character["clase"]
        if st.session_state.selected_character
        else st.session_state.customization["class"]
    )
    char_planet = (
        st.session_state.selected_character["planeta"]
        if st.session_state.selected_character
        else "Unknown"
    )
    char_edad = (
        st.session_state.selected_character["edad"]
        if st.session_state.selected_character
        else str(st.session_state.customization["age"])
    )
    char_raza = (
        st.session_state.selected_character["raza"]
        if st.session_state.selected_character
        else st.session_state.customization["race"]
    )

    st.markdown(
        f"""
    <div class="viewer">
        <div class="viewer-grid"></div>
        <div class="character-model">
            <div class="model-body" style="
                background: linear-gradient(180deg, 
                    {hex_to_rgba(accent, 0.3)} 0%, 
                    {hex_to_rgba(armor, 0.2)} 50%,
                    {hex_to_rgba(accent, 0.25)} 100%);
                box-shadow: 
                    0 0 40px {hex_to_rgba(armor, 0.2)},
                    0 0 80px {hex_to_rgba(accent, 0.1)};
            "></div>
        </div>
        <div class="viewer-hud top-left">
            <span style="color: {accent};">◈</span> RENDER: ACTIVE
        </div>
        <div class="viewer-hud top-right">
            CLASE: {char_class}<br>
            ORIGEN: {char_planet}
        </div>
        <div class="viewer-hud bottom-left">
            ID: {random.randint(1000, 9999)}
        </div>
        <div class="viewer-hud bottom-right">
            POLYS: 18,432
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
    <div class="quick-stats" style="margin: 1rem 0;">
        <div class="quick-stat">
            <div class="quick-stat-value">{st.session_state.customization["strength"]}</div>
            <div class="quick-stat-label">STR</div>
        </div>
        <div class="quick-stat">
            <div class="quick-stat-value">{st.session_state.customization["agility"]}</div>
            <div class="quick-stat-label">AGI</div>
        </div>
        <div class="quick-stat">
            <div class="quick-stat-value">{st.session_state.customization["intelligence"]}</div>
            <div class="quick-stat-label">INT</div>
        </div>
        <div class="quick-stat">
            <div class="quick-stat-value">{st.session_state.customization["charisma"]}</div>
            <div class="quick-stat-label">CHA</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if st.session_state.selected_character:
        char = st.session_state.selected_character
        st.markdown(
            f"""
        <div class="panel" style="margin-top: 1rem;">
            <div class="panel-header">{char["nombre"]}</div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">EDAD</div>
                    <div class="info-value">{char["edad"]}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">RAZA</div>
                    <div class="info-value">{char["raza"]}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">CLASE</div>
                    <div class="info-value">{char["clase"]}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">PLANETA</div>
                    <div class="info-value">{char["planeta"]}</div>
                </div>
            </div>
            
            <div class="section-title">HISTORIA</div>
            <div style="color: #909090; font-size: 0.9rem; line-height: 1.5;">{char["historia"]}</div>
            
            <div class="section-title">PODERES</div>
            {"".join([f'<div class="list-item">{p}</div>' for p in char["poderes"]])}
            
            <div class="section-title">ARMAS</div>
            {"".join([f'<div class="list-item">{a}</div>' for a in char["armas"]])}
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        descripcion = st.text_area(
            "DESCRIPCION",
            placeholder="Describe tu personaje o selecciona uno predefinido...",
            label_visibility="collapsed",
            height=80,
        )

        if st.button("CREAR PERSONAJE", use_container_width=True):
            if descripcion:
                st.success(f"Personaje creado: {descripcion[:30]}...")

# ===== RIGHT PANEL =====
with st.container():
    st.markdown(
        """
    <div class="panel">
        <div class="panel-header">Base de Datos</div>
    """,
        unsafe_allow_html=True,
    )

    opciones = ["-- Seleccionar --"] + [
        f"{p['nombre']}" for p in PERSONAJES_PREDEFINIDOS
    ]
    seleccion = st.selectbox(
        "PERSONAJES", options=opciones, label_visibility="collapsed", key="char_select"
    )

    if seleccion != "-- Seleccionar --":
        personaje = buscar_personaje_por_nombre(seleccion)
        if personaje:
            st.session_state.selected_character = personaje

    if st.button("LIMPIAR SELECCION"):
        st.session_state.selected_character = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="panel" style="margin-top: 1rem;">
        <div class="panel-header">Lista</div>
    """,
        unsafe_allow_html=True,
    )

    for p in PERSONAJES_PREDEFINIDOS[:15]:
        is_active = (
            st.session_state.selected_character
            and st.session_state.selected_character["nombre"] == p["nombre"]
        )
        cls = "active" if is_active else ""
        if st.button(
            f"{p['nombre']} ({p['clase']})",
            key=f"btn_{p['id']}",
            help=f"{p['raza']} - {p['planeta']}",
        ):
            st.session_state.selected_character = p
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
<div class="footer">
    NEXUS ENGINE v2.0 | SISTEMA DE CREACION DE PERSONAJES | TODOS LOS DERECHOS RESERVADOS
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
