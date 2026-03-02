import streamlit as st
from agente_personaje import crear_agente, PERSONAJE_TEMPLATES
from personajes_data import (
    PERSONAJES_PREDEFINIDOS,
    obtener_personaje,
    obtener_personajes_por_faccion,
    listar_facciones,
    buscar_personaje_por_nombre,
)
import random

st.set_page_config(
    page_title="NEXUS // Character Creator",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Rajdhani', sans-serif;
    }
    
    .stApp {
        background: 
            radial-gradient(ellipse at 50% 0%, rgba(0, 255, 255, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 100% 100%, rgba(138, 43, 226, 0.06) 0%, transparent 40%),
            linear-gradient(180deg, #0a0a0f 0%, #0d0d14 50%, #0a0a0f 100%);
        color: #e0e0e0;
    }
    
    .title {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        text-align: center;
        font-size: 2.8rem;
        letter-spacing: 8px;
        text-shadow: 
            0 0 10px rgba(0, 240, 255, 0.8),
            0 0 30px rgba(0, 240, 255, 0.4),
            0 0 60px rgba(0, 240, 255, 0.2);
        margin-bottom: 0.5rem;
        animation: flicker 4s infinite;
    }
    
    @keyframes flicker {
        0%, 100% { opacity: 1; }
        92% { opacity: 1; }
        93% { opacity: 0.8; }
        94% { opacity: 1; }
        96% { opacity: 0.9; }
        97% { opacity: 1; }
    }
    
    .subtitle {
        font-family: 'Orbitron', sans-serif;
        color: #8a2be2;
        text-align: center;
        font-size: 0.9rem;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        text-shadow: 0 0 15px rgba(138, 43, 226, 0.6);
    }
    
    .panel {
        background: 
            linear-gradient(135deg, rgba(20, 20, 30, 0.9) 0%, rgba(10, 10, 15, 0.95) 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 8px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .panel::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f0ff, transparent);
        animation: scan 2s linear infinite;
    }
    
    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .panel::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #8a2be2, transparent);
        opacity: 0.5;
    }
    
    .panel-title {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        font-size: 0.85rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .panel-title::before {
        content: '//';
        color: #8a2be2;
    }
    
    .hud-corner {
        position: absolute;
        width: 20px;
        height: 20px;
        border: 2px solid #00f0ff;
    }
    
    .hud-corner.tl { top: -1px; left: -1px; border-right: none; border-bottom: none; }
    .hud-corner.tr { top: -1px; right: -1px; border-left: none; border-bottom: none; }
    .hud-corner.bl { bottom: -1px; left: -1px; border-right: none; border-top: none; }
    .hud-corner.br { bottom: -1px; right: -1px; border-left: none; border-top: none; }
    
    .glow-btn {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15) 0%, rgba(138, 43, 226, 0.15) 100%);
        border: 1px solid #00f0ff;
        color: #00f0ff;
        padding: 0.8rem 2rem;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 2px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .glow-btn:hover {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.3) 0%, rgba(138, 43, 226, 0.3) 100%);
        box-shadow: 
            0 0 20px rgba(0, 240, 255, 0.4),
            0 0 40px rgba(138, 43, 226, 0.2),
            inset 0 0 20px rgba(0, 240, 255, 0.1);
        transform: translateY(-2px);
        text-shadow: 0 0 10px #00f0ff;
    }
    
    .glow-btn:active {
        transform: translateY(0);
    }
    
    .data-label {
        color: #8a2be2;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    
    .data-value {
        color: #00f0ff;
        font-size: 1.1rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    .neon-input {
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 4px;
        color: #00f0ff;
        padding: 0.8rem 1rem;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .neon-input:focus {
        outline: none;
        border-color: #00f0ff;
        box-shadow: 
            0 0 15px rgba(0, 240, 255, 0.3),
            inset 0 0 10px rgba(0, 240, 255, 0.1);
    }
    
    .neon-input::placeholder {
        color: rgba(0, 240, 255, 0.4);
    }
    
    .slider-container {
        position: relative;
        padding: 0.5rem 0;
    }
    
    .slider-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .slider-value {
        color: #00f0ff;
        font-weight: 600;
    }
    
    .stSlider > div > div > div[role="slider"] {
        background: linear-gradient(90deg, #8a2be2, #00f0ff);
        border: none;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    .stSlider > div > div > div > div {
        background: rgba(0, 240, 255, 0.2) !important;
    }
    
    .color-swatch {
        width: 40px;
        height: 40px;
        border-radius: 4px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .color-swatch:hover {
        transform: scale(1.1);
        border-color: #00f0ff;
        box-shadow: 0 0 15px currentColor;
    }
    
    .color-swatch.selected {
        border-color: #00f0ff;
        box-shadow: 0 0 20px currentColor;
    }
    
    .stat-bar {
        height: 8px;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .stat-fill {
        height: 100%;
        background: linear-gradient(90deg, #8a2be2, #00f0ff);
        border-radius: 4px;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    .template-chip {
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid rgba(0, 240, 255, 0.3);
        color: #00f0ff;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        margin: 0.2rem;
    }
    
    .template-chip:hover {
        background: rgba(0, 240, 255, 0.2);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
    }
    
    .template-chip.selected {
        background: rgba(138, 43, 226, 0.3);
        border-color: #8a2be2;
        color: #8a2be2;
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
    }
    
    .character-viewer {
        background: 
            radial-gradient(ellipse at center, rgba(0, 240, 255, 0.05) 0%, transparent 70%),
            linear-gradient(180deg, #0a0a12 0%, #0d0d18 100%);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 8px;
        height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .character-viewer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 240, 255, 0.03) 2px,
                rgba(0, 240, 255, 0.03) 4px
            );
        pointer-events: none;
    }
    
    .character-grid {
        position: absolute;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
    }
    
    @keyframes gridMove {
        0% { transform: perspective(500px) rotateX(60deg) translateY(0); }
        100% { transform: perspective(500px) rotateX(60deg) translateY(50px); }
    }
    
    .character-silhouette {
        width: 200px;
        height: 400px;
        position: relative;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }
    
    .silhouette-body {
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(138, 43, 226, 0.3) 0%, rgba(0, 240, 255, 0.2) 100%);
        clip-path: polygon(
            50% 0%, 65% 5%, 70% 15%, 68% 25%, 75% 30%,
            80% 40%, 85% 50%, 80% 60%, 85% 70%, 75% 80%,
            70% 85%, 60% 90%, 50% 95%, 40% 90%, 30% 85%,
            25% 80%, 15% 70%, 20% 60%, 15% 50%, 20% 40%,
            25% 30%, 32% 25%, 30% 15%, 35% 5%
        );
        filter: blur(1px);
    }
    
    .glow-ring {
        position: absolute;
        width: 300px;
        height: 300px;
        border: 2px solid rgba(0, 240, 255, 0.3);
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: translate(-50%, -50%) scale(1);
            opacity: 0.3;
        }
        50% { 
            transform: translate(-50%, -50%) scale(1.1);
            opacity: 0.6;
        }
    }
    
    .hud-text {
        font-family: 'Orbitron', sans-serif;
        color: rgba(0, 240, 255, 0.6);
        font-size: 0.7rem;
        letter-spacing: 2px;
    }
    
    .loading-bar {
        width: 100%;
        height: 2px;
        background: rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .loading-fill {
        height: 100%;
        background: linear-gradient(90deg, #8a2be2, #00f0ff);
        animation: loading 1.5s ease-in-out infinite;
    }
    
    @keyframes loading {
        0% { width: 0%; left: 0; }
        50% { width: 100%; left: 0; }
        100% { width: 0%; left: 100%; }
    }
    
    .expander-header {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #00f0ff !important;
    }
    
    .stExpander > div > div {
        background: transparent !important;
    }
    
    .glow-text {
        text-shadow: 
            0 0 10px rgba(0, 240, 255, 0.8),
            0 0 20px rgba(0, 240, 255, 0.4);
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.5), transparent);
        margin: 1rem 0;
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        background: #00f0ff;
        border-radius: 50%;
        display: inline-block;
        animation: pulseDot 1.5s ease-in-out infinite;
        margin-right: 8px;
    }
    
    @keyframes pulseDot {
        0%, 100% { opacity: 1; box-shadow: 0 0 5px #00f0ff; }
        50% { opacity: 0.5; box-shadow: 0 0 15px #00f0ff; }
    }
    
    .status-text {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        color: rgba(0, 240, 255, 0.7);
    }
</style>
""",
    unsafe_allow_html=True,
)

if "customization" not in st.session_state:
    st.session_state.customization = {
        "race": "Humano",
        "class": "Guerrero",
        "age": 30,
        "strength": 70,
        "agility": 60,
        "intelligence": 50,
        "charisma": 65,
        "armor_color": "#00f0ff",
        "accent_color": "#8a2be2",
        "energy_color": "#00ff88",
    }


def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha})"


def render_character_preview():
    armor = st.session_state.customization["armor_color"]
    accent = st.session_state.customization["accent_color"]
    energy = st.session_state.customization["energy_color"]

    return f"""
    <div class="character-viewer">
        <div class="character-grid"></div>
        <div class="glow-ring"></div>
        <div class="character-silhouette">
            <div class="silhouette-body" style="
                background: linear-gradient(180deg, 
                    {hex_to_rgba(accent, 0.4)} 0%, 
                    {hex_to_rgba(armor, 0.3)} 50%,
                    {hex_to_rgba(accent, 0.3)} 100%);
                box-shadow: 
                    0 0 30px {hex_to_rgba(armor, 0.3)},
                    0 0 60px {hex_to_rgba(accent, 0.2)},
                    inset 0 0 30px {hex_to_rgba(energy, 0.1)};
            "></div>
        </div>
        <div style="position: absolute; bottom: 20px; left: 20px;" class="hud-text">
            <span class="pulse-dot"></span>SCANNING...
        </div>
        <div style="position: absolute; top: 20px; right: 20px; text-align: right;" class="hud-text">
            RENDER: ACTIVE<br>
            POLYS: 24,568<br>
            FPS: 60
        </div>
    </div>
    """


st.markdown('<h1 class="title">NEXUS</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Character Creator v2.077</div>', unsafe_allow_html=True
)

top_bar_col1, top_bar_col2, top_bar_col3 = st.columns([1, 2, 1])
with top_bar_col1:
    st.markdown(
        f"""
    <div class="status-text">
        <span class="pulse-dot"></span>
        SYSTEM: ONLINE
    </div>
    """,
        unsafe_allow_html=True,
    )
with top_bar_col2:
    pass
with top_bar_col3:
    st.markdown(
        f"""
    <div style="text-align: right;" class="hud-text">
        SECTOR 7-G<br>
        {random.randint(1000, 9999)}-{random.randint(100, 999)}
    </div>
    """,
        unsafe_allow_html=True,
    )

main_col_left, main_col_center, main_col_right = st.columns([1, 2, 1])

with main_col_left:
    st.markdown(
        """
    <div class="panel" style="margin-bottom: 1rem;">
        <div class="hud-corner tl"></div>
        <div class="hud-corner tr"></div>
        <div class="hud-corner bl"></div>
        <div class="hud-corner br"></div>
        <div class="panel-title">Parameters</div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="data-label">Raza</div>', unsafe_allow_html=True)
    race = st.selectbox(
        "raza",
        options=["Humano", "Ciborg", "Mutante", "Alienígena", "Androide", "Híbrido"],
        index=[
            "Humano",
            "Ciborg",
            "Mutante",
            "Alienígena",
            "Androide",
            "Híbrido",
        ].index(st.session_state.customization["race"]),
        label_visibility="collapsed",
    )
    st.session_state.customization["race"] = race

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="data-label">Clase</div>', unsafe_allow_html=True)
    char_class = st.selectbox(
        "clase",
        options=[
            "Guerrero",
            "Asesino",
            "Mago",
            "Ingeniero",
            "Médico",
            "Piloto",
            "Hacker",
        ],
        index=[
            "Guerrero",
            "Asesino",
            "Mago",
            "Ingeniero",
            "Médico",
            "Piloto",
            "Hacker",
        ].index(st.session_state.customization["class"]),
        label_visibility="collapsed",
    )
    st.session_state.customization["class"] = char_class

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="data-label">Edad</div>', unsafe_allow_html=True)
    age = st.slider(
        "edad",
        18,
        150,
        st.session_state.customization["age"],
        label_visibility="collapsed",
    )
    st.session_state.customization["age"] = age

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
    <div class="panel">
        <div class="hud-corner tl"></div>
        <div class="hud-corner tr"></div>
        <div class="hud-corner bl"></div>
        <div class="hud-corner br"></div>
        <div class="panel-title">Attributes</div>
    """,
        unsafe_allow_html=True,
    )

    def render_stat_slider(label, key, min_val=0, max_val=100):
        st.markdown(
            f'<div class="slider-label"><span class="data-label">{label}</span><span class="slider-value">{st.session_state.customization[key]}</span></div>',
            unsafe_allow_html=True,
        )
        val = st.slider(
            f"slider_{key}",
            min_val,
            max_val,
            st.session_state.customization[key],
            label_visibility="collapsed",
            key=f"slider_{key}",
        )
        st.session_state.customization[key] = val
        st.markdown(
            f"""
        <div class="stat-bar">
            <div class="stat-fill" style="width: {val}%;"></div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    render_stat_slider("Strength", "strength")
    render_stat_slider("Agility", "agility")
    render_stat_slider("Intelligence", "intelligence")
    render_stat_slider("Charisma", "charisma")

    st.markdown("</div>", unsafe_allow_html=True)

with main_col_center:
    st.markdown(render_character_preview(), unsafe_allow_html=True)

    st.markdown(
        """
    <div style="display: flex; gap: 1rem; margin-top: 1rem;">
    """,
        unsafe_allow_html=True,
    )

    desc_col1, desc_col2 = st.columns([3, 1])
    with desc_col1:
        descripcion = st.text_input(
            "DESCRIPCION DEL PERSONAJE",
            placeholder="Ej: Un guerrero cyborg que lucha por la resistencia...",
            label_visibility="collapsed",
        )
    with desc_col2:
        st.markdown(
            '<button class="glow-btn" style="width: 100%;">Generar</button>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

with main_col_right:
    st.markdown(
        """
    <div class="panel" style="margin-bottom: 1rem;">
        <div class="hud-corner tl"></div>
        <div class="hud-corner tr"></div>
        <div class="hud-corner bl"></div>
        <div class="hud-corner br"></div>
        <div class="panel-title">Color Scheme</div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="data-label">Armor Primary</div>', unsafe_allow_html=True)
    armor_colors = [
        "#00f0ff",
        "#8a2be2",
        "#ff0080",
        "#00ff88",
        "#ffaa00",
        "#ffffff",
        "#1a1a2e",
    ]
    armor_cols = st.columns([1] * len(armor_colors))
    selected_armor = st.session_state.customization["armor_color"]

    for i, color in enumerate(armor_colors):
        with armor_cols[i]:
            if st.button(" ", key=f"armor_{i}", help=color):
                st.session_state.customization["armor_color"] = color
                st.rerun()

    st.markdown(
        '<div class="data-label" style="margin-top: 1rem;">Accent</div>',
        unsafe_allow_html=True,
    )
    accent_colors = ["#8a2be2", "#00f0ff", "#ff0080", "#00ff88", "#ffaa00"]
    accent_cols = st.columns([1] * len(accent_colors))
    for i, color in enumerate(accent_colors):
        with accent_cols[i]:
            if st.button(" ", key=f"accent_{i}", help=color):
                st.session_state.customization["accent_color"] = color
                st.rerun()

    st.markdown(
        '<div class="data-label" style="margin-top: 1rem;">Energy Glow</div>',
        unsafe_allow_html=True,
    )
    energy_colors = ["#00ff88", "#00f0ff", "#ff0080", "#8a2be2", "#ffaa00"]
    energy_cols = st.columns([1] * len(energy_colors))
    for i, color in enumerate(energy_colors):
        with energy_cols[i]:
            if st.button(" ", key=f"energy_{i}", help=color):
                st.session_state.customization["energy_color"] = color
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    opciones_personajes = ["-- Seleccionar --"] + [
        f"{p['nombre']} ({p['clase']})" for p in PERSONAJES_PREDEFINIDOS
    ]
    personaje_seleccionado = st.selectbox(
        "PERSONAJES PREDEFINIDOS",
        options=opciones_personajes,
        label_visibility="collapsed",
    )

    if personaje_seleccionado != "-- Seleccionar --":
        nombre_buscar = personaje_seleccionado.split(" (")[0]
        personaje_data = buscar_personaje_por_nombre(nombre_buscar)
        if personaje_data:
            st.session_state.selected_character = personaje_data

    st.markdown(
        """
    <div class="panel" style="margin-top: 1rem;">
        <div class="hud-corner tl"></div>
        <div class="hud-corner tr"></div>
        <div class="hud-corner bl"></div>
        <div class="hud-corner br"></div>
        <div class="panel-title">Quick Clases</div>
    """,
        unsafe_allow_html=True,
    )

    templates = [
        "Guerrero",
        "Asesino",
        "Mago",
        "Ingeniero",
        "Médico",
        "Piloto",
        "Hacker",
    ]
    for template in templates:
        is_selected = st.session_state.customization["class"] == template
        btn_class = "template-chip selected" if is_selected else "template-chip"
        st.markdown(
            f'<div class="{btn_class}">{template}</div>', unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---", unsafe_allow_html=True)

footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col1:
    st.markdown(
        """
    <div class="hud-text">
        MEM: 87.4 TB<br>
        CPU: 34%<br>
        GPU: 67%
    </div>
    """,
        unsafe_allow_html=True,
    )
with footer_col2:
    if descripcion:
        if st.button("✦ CREAR PERSONAJE ✦", use_container_width=True, type="primary"):
            with st.spinner(""):
                st.markdown(
                    """
                <div style="text-align: center; padding: 2rem;">
                    <div class="loading-bar">
                        <div class="loading-fill"></div>
                    </div>
                    <br>
                    <span class="hud-text">GENERATING NEURAL PATTERN...</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            try:
                agente = crear_agente()
                resultado = agente.crear_personaje(descripcion)
                personaje = resultado["personaje_obj"]

                st.markdown(
                    f"""
                <div class="panel" style="margin-top: 1rem;">
                    <div class="hud-corner tl"></div>
                    <div class="hud-corner tr"></div>
                    <div class="hud-corner bl"></div>
                    <div class="hud-corner br"></div>
                    <div class="panel-title">PERSONAJE CREADO // {personaje.nombre}</div>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        <div>
                            <div class="data-label">Edad</div>
                            <div class="data-value">{personaje.edad}</div>
                        </div>
                        <div>
                            <div class="data-label">Raza</div>
                            <div class="data-value">{st.session_state.customization["race"]}</div>
                        </div>
                        <div>
                            <div class="data-label">Clase</div>
                            <div class="data-value">{st.session_state.customization["class"]}</div>
                        </div>
                    </div>
                    
                    <div class="divider"></div>
                    
                    <div class="data-label">Historia</div>
                    <div>{personaje.historia}</div>
                    
                    <div class="divider"></div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div>
                            <div class="data-label">Poderes</div>
                            {"".join([f"• {p}<br>" for p in personaje.poderes])}
                        </div>
                        <div>
                            <div class="data-label">Enemigos</div>
                            {"".join([f"• {e}<br>" for e in personaje.enemigos])}
                        </div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
with footer_col3:
    st.markdown(
        """
    <div style="text-align: right;" class="hud-text">
        BUILD: 2077.03<br>
        NEXUS ENGINE<br>
        V2.077
    </div>
    """,
        unsafe_allow_html=True,
    )
