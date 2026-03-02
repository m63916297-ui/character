import streamlit as st
from personajes_data import PERSONAJES_PREDEFINIDOS
from agente_personaje import crear_agente, PERSONAJE_TEMPLATES
import random

st.set_page_config(
    page_title="NEXUS // Character Creator", page_icon="◈", layout="wide"
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    .stApp { 
        font-family: 'Rajdhani', sans-serif; 
        background: #06060a; 
        color: #b0b0b0;
    }
    
    /* Header */
    .header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(0, 255, 242, 0.1);
    }
    
    .logo { font-family: 'Orbitron'; font-size: 2.5rem; color: #00fff2; letter-spacing: 15px; }
    .tagline { font-size: 0.65rem; color: #666; letter-spacing: 6px; text-transform: uppercase; }
    
    /* Grid */
    .grid { display: grid; grid-template-columns: 250px 1fr 250px; gap: 1rem; }
    @media (max-width: 1100px) { .grid { grid-template-columns: 1fr; } }
    
    /* Panel */
    .panel {
        background: #0a0a10;
        border: 1px solid rgba(0, 255, 242, 0.1);
        border-radius: 4px;
        padding: 1rem;
    }
    
    .panel-title {
        font-family: 'Orbitron'; font-size: 0.6rem; color: #00fff2; 
        letter-spacing: 2px; text-transform: uppercase;
        padding-bottom: 0.5rem; margin-bottom: 1rem;
        border-bottom: 1px solid rgba(0, 255, 242, 0.1);
    }
    
    /* Inputs */
    .stSelectbox > div > div { background: #0a0a10 !important; border-color: rgba(0,255,242,0.2) !important; }
    .stTextInput > div > div { background: #0a0a10 !important; border-color: rgba(0,255,242,0.2) !important; }
    .stTextArea > div > div { background: #0a0a10 !important; border-color: rgba(0,255,242,0.2) !important; }
    div[data-baseweb="select"] > div { background: #0a0a10 !important; }
    
    /* Viewer */
    .viewer {
        background: radial-gradient(ellipse at bottom, rgba(0,255,242,0.03) 0%, transparent 50%),
                    linear-gradient(180deg, #0a0a12 0%, #050508 100%);
        border: 1px solid rgba(0,255,242,0.1);
        border-radius: 4px;
        height: 350px;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .model {
        width: 100px; height: 250px;
        animation: float 3s ease-in-out infinite;
    }
    
    .model-body {
        width: 100%; height: 100%;
        background: linear-gradient(180deg, rgba(139,92,246,0.3) 0%, rgba(0,255,242,0.15) 100%);
        clip-path: polygon(50% 0%, 62% 4%, 68% 12%, 66% 22%, 72% 28%, 78% 38%, 82% 48%, 78% 58%, 82% 68%, 74% 78%, 68% 84%, 58% 90%, 42% 90%, 32% 84%, 26% 78%, 18% 68%, 22% 58%, 18% 48%, 22% 38%, 34% 28%, 38% 22%, 32% 12%, 38% 4%);
    }
    
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    
    .hud { position: absolute; font-size: 0.55rem; color: rgba(0,255,242,0.4); font-family: 'Orbitron'; }
    .hud-tl { top: 10px; left: 10px; }
    .hud-tr { top: 10px; right: 10px; text-align: right; }
    .hud-bl { bottom: 10px; left: 10px; }
    .hud-br { bottom: 10px; right: 10px; text-align: right; }
    
    /* Stats */
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.5rem; margin: 1rem 0; }
    .stat { background: #0a0a10; padding: 0.5rem; text-align: center; border-radius: 3px; }
    .stat-val { font-family: 'Orbitron'; font-size: 1rem; color: #00fff2; }
    .stat-lbl { font-size: 0.5rem; color: #555; text-transform: uppercase; }
    
    /* Character Info */
    .char-name { font-family: 'Orbitron'; font-size: 1.5rem; color: #00fff2; }
    .char-sub { font-size: 0.75rem; color: #666; letter-spacing: 2px; }
    
    .info-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.75rem 0; }
    .info-box { background: #0a0a10; padding: 0.5rem; border-radius: 3px; border-left: 2px solid rgba(0,255,242,0.3); }
    .info-lbl { font-size: 0.55rem; color: #666; text-transform: uppercase; }
    .info-val { color: #00fff2; font-size: 0.85rem; }
    
    .sec-title {
        font-family: 'Orbitron'; font-size: 0.55rem; color: #8b5cf6;
        letter-spacing: 2px; text-transform: uppercase;
        margin: 1rem 0 0.5rem 0;
    }
    
    .list-item { font-size: 0.8rem; color: #888; padding: 0.2rem 0 0.2rem 0.8rem; position: relative; }
    .list-item::before { content: '›'; position: absolute; left: 0; color: #8b5cf6; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(180deg, rgba(0,255,242,0.1) 0%, rgba(0,255,242,0.02) 100%);
        border: 1px solid rgba(0,255,242,0.3); color: #00fff2;
        font-family: 'Orbitron'; font-size: 0.7rem; letter-spacing: 2px;
        padding: 0.6rem 1rem; border-radius: 3px;
    }
    .stButton > button:hover { background: rgba(0,255,242,0.15); border-color: #00fff2; }
    
    /* Slider */
    .stSlider > div > div > div[role="slider"] {
        background: linear-gradient(90deg, #8b5cf6, #00fff2) !important;
    }
    
    /* Character List */
    .char-list { max-height: 280px; overflow-y: auto; }
    .char-list::-webkit-scrollbar { width: 4px; }
    .char-list::-webkit-scrollbar-track { background: #0a0a10; }
    .char-list::-webkit-scrollbar-thumb { background: rgba(0,255,242,0.2); border-radius: 2px; }
    
    .char-item {
        padding: 0.4rem 0.6rem; cursor: pointer;
        border-left: 2px solid transparent;
        font-size: 0.75rem; transition: all 0.15s;
    }
    .char-item:hover { background: rgba(0,255,242,0.05); border-left-color: rgba(0,255,242,0.3); }
    .char-item.active { background: rgba(139,92,246,0.1); border-left-color: #8b5cf6; color: #00fff2; }
    
    .stTextArea textarea { color: #00fff2 !important; }
    .stTextInput input { color: #00fff2 !important; }
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

# Header
st.markdown(
    '<div class="header"><h1 class="logo">NEXUS</h1><div class="tagline">Character Creator v2.0</div></div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="grid">', unsafe_allow_html=True)

# ===== LEFT PANEL =====
with st.container():
    st.markdown(
        '<div class="panel"><div class="panel-title">Personaje</div>',
        unsafe_allow_html=True,
    )

    races = ["Humano", "Ciborg", "Mutante", "Alienígena", "Androide", "Híbrido"]
    classes = ["Guerrero", "Asesino", "Mago", "Ingeniero", "Médico", "Piloto", "Hacker"]

    race = st.selectbox(
        "Raza",
        races,
        index=races.index(st.session_state.customization["race"]),
        label_visibility="collapsed",
    )
    st.session_state.customization["race"] = race

    char_class = st.selectbox(
        "Clase",
        classes,
        index=classes.index(st.session_state.customization["class"]),
        label_visibility="collapsed",
    )
    st.session_state.customization["class"] = char_class

    age = st.slider(
        "Edad",
        15,
        120,
        st.session_state.customization["age"],
        label_visibility="collapsed",
    )
    st.session_state.customization["age"] = age

    st.markdown("</div>", unsafe_allow_html=True)

    # Atributos
    st.markdown(
        '<div class="panel" style="margin-top:1rem"><div class="panel-title">Atributos</div>',
        unsafe_allow_html=True,
    )

    for attr, key in [
        ("FUERZA", "strength"),
        ("AGILIDAD", "agility"),
        ("INTELIGENCIA", "intelligence"),
        ("CARISMA", "charisma"),
    ]:
        val = st.session_state.customization[key]
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;margin-bottom:0.2rem;"><span style="font-size:0.65rem;color:#666;text-transform:uppercase;">{attr}</span><span style="color:#00fff2;font-size:0.8rem;">{val}</span></div>',
            unsafe_allow_html=True,
        )
        new_val = st.slider(
            f"_{key}", 0, 100, val, label_visibility="collapsed", key=f"sl_{key}"
        )
        st.session_state.customization[key] = new_val

    st.markdown("</div>", unsafe_allow_html=True)

    # Colores
    st.markdown(
        '<div class="panel" style="margin-top:1rem"><div class="panel-title">Colores</div>',
        unsafe_allow_html=True,
    )

    for color_name, color_key in [
        ("Armadura", "armor_color"),
        ("Acento", "accent_color"),
    ]:
        colors = ["#00fff2", "#8b5cf6", "#ff0080", "#00ff88", "#ffaa00"]
        cols = st.columns([1] * len(colors))
        for i, c in enumerate(colors):
            with cols[i]:
                if st.button(" ", key=f"{color_key}_{i}", help=c):
                    st.session_state.customization[color_key] = c
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ===== CENTER PANEL =====
with st.container():
    armor = st.session_state.customization["armor_color"]
    accent = st.session_state.customization["accent_color"]

    # Viewer
    char_display = st.session_state.selected_character
    nombre = char_display["nombre"] if char_display else "NEXUS-7"
    clase = (
        char_display["clase"]
        if char_display
        else st.session_state.customization["class"]
    )
    planeta = char_display["planeta"] if char_display else "Unknown"

    st.markdown(
        f"""
    <div class="viewer">
        <div class="model">
            <div class="model-body" style="background:linear-gradient(180deg,{accent}40 0%,{armor}25 100%);box-shadow:0 0 40px {armor}30,0 0 80px {accent}15;"></div>
        </div>
        <div class="hud hud-tl">◈ RENDER</div>
        <div class="hud hud-tr">CLASE: {clase}<br>ORIGEN: {planeta}</div>
        <div class="hud hud-bl">ID: {random.randint(1000, 9999)}</div>
        <div class="hud hud-br">POLYS: 18K</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Quick Stats
    st.markdown(
        f"""
    <div class="stats">
        <div class="stat"><div class="stat-val">{st.session_state.customization["strength"]}</div><div class="stat-lbl">STR</div></div>
        <div class="stat"><div class="stat-val">{st.session_state.customization["agility"]}</div><div class="stat-lbl">AGI</div></div>
        <div class="stat"><div class="stat-val">{st.session_state.customization["intelligence"]}</div><div class="stat-lbl">INT</div></div>
        <div class="stat"><div class="stat-val">{st.session_state.customization["charisma"]}</div><div class="stat-lbl">CHA</div></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Character Info
    if char_display:
        st.markdown(
            f"""
        <div class="panel" style="margin-top:1rem">
            <div class="char-name">{char_display["nombre"]}</div>
            <div class="char-sub">{char_display["clase"]} | {char_display["raza"]}</div>
            
            <div class="info-row">
                <div class="info-box"><div class="info-lbl">Edad</div><div class="info-val">{char_display["edad"]}</div></div>
                <div class="info-box"><div class="info-lbl">Planeta</div><div class="info-val">{char_display["planeta"]}</div></div>
            </div>
            
            <div class="sec-title">Historia</div>
            <div style="color:#777;font-size:0.85rem;line-height:1.5;">{char_display["historia"]}</div>
            
            <div class="sec-title">Poderes</div>
            {"".join([f'<div class="list-item">{p}</div>' for p in char_display["poderes"]])}
            
            <div class="sec-title">Armas</div>
            {"".join([f'<div class="list-item">{a}</div>' for a in char_display["armas"]])}
            
            <div class="sec-title">Enemigos</div>
            {"".join([f'<div class="list-item">{e}</div>' for e in char_display["enemigos"]])}
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        # Generator
        desc = st.text_area(
            "Descripcion",
            placeholder="Ej: Crea un heroe llamado Valerius...",
            label_visibility="collapsed",
            height=60,
        )

        if st.button("◈ GENERAR ◈", use_container_width=True):
            if desc:
                with st.spinner("Generando..."):
                    try:
                        agente = crear_agente()
                        result = agente.crear_personaje(desc)
                        p = result["personaje_obj"]

                        st.session_state.generated = {
                            "nombre": p.nombre,
                            "edad": p.edad,
                            "raza": st.session_state.customization["race"],
                            "clase": st.session_state.customization["class"],
                            "planeta": "Planeta Generado",
                            "historia": p.historia,
                            "poderes": p.poderes,
                            "armas": ["Arma Custom"],
                            "enemigos": p.enemigos,
                            "personalidad": p.personalidad,
                        }
                    except Exception as e:
                        st.error(f"Error: {e}")

        if "generated" in st.session_state:
            g = st.session_state.generated
            st.markdown(
                f"""
            <div class="panel" style="margin-top:1rem;border-color:rgba(0,255,242,0.3)">
                <div class="char-name">{g["nombre"]}</div>
                <div class="char-sub">{g["clase"]} | {g["raza"]}</div>
                
                <div class="info-row">
                    <div class="info-box"><div class="info-lbl">Edad</div><div class="info-val">{g["edad"]}</div></div>
                    <div class="info-box"><div class="info-lbl">Planeta</div><div class="info-val">{g["planeta"]}</div></div>
                </div>
                
                <div class="sec-title">Historia</div>
                <div style="color:#777;font-size:0.85rem;line-height:1.5;">{g["historia"]}</div>
                
                <div class="sec-title">Personalidad</div>
                <div style="color:#00fff2;font-size:0.85rem;">{g["personalidad"]}</div>
                
                <div class="sec-title">Poderes</div>
                {"".join([f'<div class="list-item">{p}</div>' for p in g["poderes"]])}
                
                <div class="sec-title">Enemigos</div>
                {"".join([f'<div class="list-item">{e}</div>' for e in g["enemigos"]])}
            </div>
            """,
                unsafe_allow_html=True,
            )

            if st.button("Limpiar", key="clr_gen"):
                del st.session_state.generated
                st.rerun()


# ===== RIGHT PANEL =====
with st.container():
    st.markdown(
        '<div class="panel"><div class="panel-title">Base de Datos</div>',
        unsafe_allow_html=True,
    )

    opciones = ["-- Seleccionar --"] + [p["nombre"] for p in PERSONAJES_PREDEFINIDOS]
    sel = st.selectbox("Personajes", opciones, label_visibility="collapsed")

    if sel != "-- Seleccionar --":
        for p in PERSONAJES_PREDEFINIDOS:
            if p["nombre"] == sel:
                st.session_state.selected_character = p
                break

    if st.session_state.selected_character:
        if st.button("Limpiar Seleccion"):
            st.session_state.selected_character = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Lista
    st.markdown(
        '<div class="panel" style="margin-top:1rem"><div class="panel-title">Personajes</div>',
        unsafe_allow_html=True,
    )

    for p in PERSONAJES_PREDEFINIDOS[:20]:
        active = (
            "active"
            if st.session_state.selected_character
            and st.session_state.selected_character["nombre"] == p["nombre"]
            else ""
        )
        if st.button(f"{p['nombre']} ({p['clase'][:1]})", key=f"btn_{p['id']}"):
            st.session_state.selected_character = p
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
