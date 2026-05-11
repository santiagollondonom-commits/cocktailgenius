import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import requests
import re

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="CocktailGenius — Mixología con Inteligencia Artificial",
    page_icon="assets/logo.png" if False else "🍸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS — DISEÑO PROFESIONAL SIN EMOJIS EXCESIVOS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --dark: #080B14;
        --dark-mid: #0F1420;
        --dark-card: #141928;
        --border: rgba(201,168,76,0.18);
        --text: #E8E6E0;
        --muted: #7A7870;
        --white: #FFFFFF;
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'DM Sans', sans-serif !important;
        color: var(--text) !important;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; max-width: 1200px; }

    /* Tipografía */
    h1, h2, h3, h4 {
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 600 !important;
        color: var(--white) !important;
        letter-spacing: 0.02em;
    }

    p, li, span, div, label {
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Header principal */
    .site-header {
        text-align: center;
        padding: 3rem 0 2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2rem;
    }

    .site-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4rem;
        font-weight: 700;
        color: var(--white) !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 0;
        line-height: 1;
    }

    .site-title span {
        color: var(--gold) !important;
    }

    .site-tagline {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: var(--muted) !important;
        margin-top: 0.75rem;
    }

    /* Divisor dorado */
    .gold-rule {
        width: 60px;
        height: 1px;
        background: var(--gold);
        margin: 1.5rem auto;
    }

    /* Cards */
    .card {
        background: var(--dark-card);
        border: 1px solid var(--border);
        border-radius: 4px;
        padding: 2rem;
        margin: 0.75rem 0;
        transition: border-color 0.3s ease;
    }

    .card:hover {
        border-color: rgba(201,168,76,0.4);
    }

    .card-label {
        font-size: 0.65rem;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: var(--gold) !important;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .card-heading {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        color: var(--white) !important;
        margin-bottom: 0.75rem;
        line-height: 1.2;
    }

    .card-body {
        font-size: 0.9rem;
        color: var(--muted) !important;
        line-height: 1.7;
    }

    /* Badge precio */
    .badge {
        display: inline-block;
        font-size: 0.65rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--dark) !important;
        background: var(--gold);
        padding: 0.25rem 0.85rem;
        border-radius: 2px;
        font-weight: 600;
        margin-top: 1rem;
    }

    .badge-outline {
        background: transparent;
        color: var(--gold) !important;
        border: 1px solid var(--gold);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid var(--border);
        padding: 0;
        border-radius: 0;
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--muted) !important;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        border-radius: 0;
        padding: 0.85rem 1.5rem;
        border-bottom: 2px solid transparent;
        background: transparent !important;
        font-family: 'DM Sans', sans-serif;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--gold) !important;
        border-bottom: 2px solid var(--gold) !important;
        font-weight: 600 !important;
    }

    /* Botones */
    .stButton > button {
        background: var(--gold) !important;
        color: #080B14 !important;
        font-weight: 600 !important;
        border-radius: 2px !important;
        border: none !important;
        padding: 0.65rem 2rem !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.2em !important;
        text-transform: uppercase !important;
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: var(--gold-light) !important;
        box-shadow: 0 0 20px rgba(201,168,76,0.25) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input,
    div[data-baseweb="input"] input {
        background: var(--dark-mid) !important;
        color: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stTextInput > div > div > input:focus,
    div[data-baseweb="input"] input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div > div,
    div[data-baseweb="select"] div {
        background: var(--dark-mid) !important;
        color: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    div[data-baseweb="menu"] li,
    [role="option"] {
        background: var(--dark-card) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    div[data-baseweb="menu"] li:hover,
    [role="option"]:hover {
        background: rgba(201,168,76,0.1) !important;
        color: var(--gold) !important;
    }

    /* NumberInput */
    .stNumberInput > div > div > input,
    [data-testid="stNumberInput"] input {
        background: var(--dark-mid) !important;
        color: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* TextArea */
    .stTextArea > div > div > textarea,
    div[data-baseweb="textarea"] textarea {
        background: var(--dark-mid) !important;
        color: var(--white) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Labels */
    .stSelectbox label, .stNumberInput label,
    .stTextInput label, .stTextArea label,
    [data-testid="stForm"] label {
        color: var(--muted) !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Slider */
    .stSlider > div > div > div > div { background: var(--gold) !important; }

    /* Placeholder */
    ::placeholder { color: var(--muted) !important; opacity: 1 !important; }

    /* Métricas */
    [data-testid="stMetricValue"] {
        color: var(--gold) !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.15em !important;
    }
    [data-testid="stMetricDelta"] { color: var(--gold-light) !important; }

    /* Divisor */
    hr { border-color: var(--border) !important; }

    /* Tag ingrediente */
    .ing-tag {
        display: inline-block;
        font-size: 0.75rem;
        letter-spacing: 0.1em;
        color: var(--gold) !important;
        border: 1px solid rgba(201,168,76,0.3);
        padding: 0.2rem 0.65rem;
        border-radius: 2px;
        margin: 0.2rem;
        text-transform: uppercase;
    }

    /* Resultado ML */
    .result-panel {
        background: var(--dark-card);
        border: 1px solid var(--gold);
        border-radius: 4px;
        padding: 1.75rem;
        margin: 1rem 0;
        text-align: center;
    }

    .result-number {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--gold) !important;
        line-height: 1;
    }

    .result-label {
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted) !important;
        margin-top: 0.5rem;
    }

    /* Trend bar */
    .trend-bar-wrap {
        background: var(--dark-mid);
        border-radius: 2px;
        height: 6px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .trend-bar-fill {
        height: 100%;
        border-radius: 2px;
        background: linear-gradient(90deg, var(--gold), var(--gold-light));
    }

    /* Footer */
    .site-footer {
        text-align: center;
        padding: 3rem 0 2rem;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
    }

    /* Imagen coctel */
    .stImage img {
        border-radius: 4px;
        border: 1px solid var(--border);
    }

    /* Dataframe */
    .stDataFrame { border: 1px solid var(--border) !important; border-radius: 4px !important; }

    /* Info / Success / Warning */
    .stAlert {
        background: var(--dark-card) !important;
        border-radius: 4px !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
    }

    /* Step number */
    .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        min-width: 24px;
        background: var(--gold);
        color: #080B14 !important;
        border-radius: 50%;
        font-weight: 700;
        font-size: 0.75rem;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }

    /* Section heading */
    .section-heading {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: var(--white) !important;
        text-align: center;
        margin: 1.5rem 0 0.5rem;
        letter-spacing: 0.04em;
    }

    .section-sub {
        font-size: 0.75rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: var(--muted) !important;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BASE DE DATOS DE RECETAS
# ============================================
RECETAS_DB = {
    "mojito": {
        "nombre": "Mojito Clásico",
        "dificultad": 2,
        "tiempo": 5,
        "ingredientes": ["Ron blanco", "Lima", "Menta", "Azúcar", "Soda"],
        "medidas": {"Ron blanco": "45ml", "Lima": "30ml", "Menta": "6 hojas", "Azúcar": "2 cdas", "Soda": "Completar"},
        "preparacion": [
            "Machaca la menta con azúcar y jugo de lima en el vaso",
            "Añade hielo picado hasta 3/4 del vaso",
            "Vierte el ron blanco",
            "Completa con agua con gas",
            "Decora con ramita de menta"
        ],
        "tips": "No machaques la menta con fuerza, solo presiona para liberar aceites esenciales sin amargar.",
        "pexels_query": "mojito cocktail mint",
        "tendencia_score": 82
    },
    "margarita": {
        "nombre": "Margarita",
        "dificultad": 1,
        "tiempo": 3,
        "ingredientes": ["Tequila", "Triple sec", "Lima", "Sal"],
        "medidas": {"Tequila": "50ml", "Triple sec": "25ml", "Lima": "15ml", "Sal": "Para el borde"},
        "preparacion": [
            "Pasa limón por el borde del vaso y luego por sal",
            "En coctelera con hielo, mezcla tequila, triple sec y jugo de lima",
            "Agita 10 segundos",
            "Cuela en vaso escarchado con sal"
        ],
        "tips": "Usa tequila 100% agave para un sabor limpio y auténtico.",
        "pexels_query": "margarita cocktail",
        "tendencia_score": 91
    },
    "old fashioned": {
        "nombre": "Old Fashioned",
        "dificultad": 3,
        "tiempo": 5,
        "ingredientes": ["Bourbon", "Azúcar", "Angostura", "Naranja"],
        "medidas": {"Bourbon": "45ml", "Azúcar": "1 terrón", "Angostura": "2 gotas", "Naranja": "Cáscara"},
        "preparacion": [
            "Coloca el terrón de azúcar en el vaso",
            "Añade 2 gotas de angostura y un poco de agua",
            "Disuelve el azúcar formando pasta",
            "Añade hielo grande y el bourbon",
            "Remueve suavemente 30 segundos",
            "Exprime cáscara de naranja sobre el trago"
        ],
        "tips": "El hielo debe ser grande para una dilución lenta y controlada.",
        "pexels_query": "old fashioned whiskey cocktail",
        "tendencia_score": 88
    },
    "negroni": {
        "nombre": "Negroni",
        "dificultad": 2,
        "tiempo": 3,
        "ingredientes": ["Gin", "Campari", "Vermut rojo"],
        "medidas": {"Gin": "30ml", "Campari": "30ml", "Vermut rojo": "30ml"},
        "preparacion": [
            "En vaso bajo con hielo grande",
            "Vierte partes iguales de gin, Campari y vermut",
            "Remueve suavemente 20 segundos",
            "Decora con twist de naranja"
        ],
        "tips": "Clásico italiano ideal para aperitivo. Usa un gin botánico de calidad.",
        "pexels_query": "negroni cocktail bar",
        "tendencia_score": 74
    },
    "piña colada": {
        "nombre": "Piña Colada",
        "dificultad": 2,
        "tiempo": 7,
        "ingredientes": ["Ron blanco", "Jugo de piña", "Crema de coco", "Hielo"],
        "medidas": {"Ron blanco": "60ml", "Jugo de piña": "90ml", "Crema de coco": "30ml", "Hielo": "1 taza"},
        "preparacion": [
            "Licúa todos los ingredientes con hielo",
            "Bate hasta consistencia cremosa",
            "Sirve en vaso alto",
            "Decora con piña y cereza"
        ],
        "tips": "Usa piña fresca para un sabor más vibrante.",
        "pexels_query": "pina colada tropical cocktail",
        "tendencia_score": 65
    },
    "espresso martini": {
        "nombre": "Espresso Martini",
        "dificultad": 2,
        "tiempo": 7,
        "ingredientes": ["Vodka", "Licor de café", "Espresso", "Hielo"],
        "medidas": {"Vodka": "50ml", "Licor de café": "30ml", "Espresso": "30ml fresco", "Hielo": "Al gusto"},
        "preparacion": [
            "Prepara espresso y deja enfriar 1 minuto",
            "En coctelera con hielo, añade vodka, licor de café y espresso",
            "Agita enérgicamente 15 segundos",
            "Cuela doblemente en copa fría",
            "Decora con 3 granos de café"
        ],
        "tips": "La clave está en agitar muy fuerte para crear la espuma característica.",
        "pexels_query": "espresso martini coffee cocktail",
        "tendencia_score": 95
    },
    "daiquiri": {
        "nombre": "Daiquiri",
        "dificultad": 1,
        "tiempo": 3,
        "ingredientes": ["Ron blanco", "Jugo de lima", "Jarabe de azúcar"],
        "medidas": {"Ron blanco": "60ml", "Jugo de lima": "25ml", "Jarabe de azúcar": "15ml"},
        "preparacion": [
            "En coctelera con hielo, añade ron, jugo de lima y jarabe",
            "Agita vigorosamente 10 segundos",
            "Cuela doblemente en copa fría",
            "Decora con twist de lima"
        ],
        "tips": "El equilibrio entre dulce y ácido es la esencia de este clásico.",
        "pexels_query": "daiquiri rum cocktail",
        "tendencia_score": 78
    },
    "whiskey sour": {
        "nombre": "Whiskey Sour",
        "dificultad": 2,
        "tiempo": 7,
        "ingredientes": ["Bourbon", "Jugo de limón", "Jarabe de azúcar", "Clara de huevo"],
        "medidas": {"Bourbon": "60ml", "Jugo de limón": "30ml", "Jarabe de azúcar": "15ml", "Clara de huevo": "1 unidad (opcional)"},
        "preparacion": [
            "En coctelera seca (sin hielo), mezcla bourbon, limón, jarabe y clara de huevo",
            "Agita en seco 15 segundos (dry shake)",
            "Añade hielo y agita 10 segundos más",
            "Cuela en vaso bajo con hielo",
            "Decora con cereza y naranja"
        ],
        "tips": "La clara de huevo en seco crea una textura sedosa y espuma densa.",
        "pexels_query": "whiskey sour cocktail bourbon",
        "tendencia_score": 70
    }
}

# ============================================
# DATOS TENDENCIA ML — Modelo de regresión
# ============================================
TENDENCIAS_DATA = {
    "Espresso Martini":  {"score_actual": 95, "crecimiento": 28, "categoria": "Cafeinado"},
    "Margarita":         {"score_actual": 91, "crecimiento": 15, "categoria": "Cítrico"},
    "Old Fashioned":     {"score_actual": 88, "crecimiento": 12, "categoria": "Whisky"},
    "Mojito":            {"score_actual": 82, "crecimiento": 5,  "categoria": "Refrescante"},
    "Daiquiri":          {"score_actual": 78, "crecimiento": 18, "categoria": "Ron"},
    "Negroni":           {"score_actual": 74, "crecimiento": 8,  "categoria": "Amargo"},
    "Whiskey Sour":      {"score_actual": 70, "crecimiento": 10, "categoria": "Cítrico"},
    "Piña Colada":       {"score_actual": 65, "crecimiento": -3, "categoria": "Tropical"},
}

# ============================================
# API PEXELS
# ============================================
PEXELS_API_KEY = "8AijNcycbO2DbzW1gVtclDH2MbrjnaBE2OvdNrSie1vpefxnR0crjKSt"
PEXELS_CACHE = {}

def buscar_imagen_pexels(query, nombre_coctel):
    if nombre_coctel in PEXELS_CACHE:
        return PEXELS_CACHE[nombre_coctel]
    headers = {"Authorization": PEXELS_API_KEY}
    for q in [query, f"{query} drink", "cocktail bar elegant"]:
        try:
            resp = requests.get(
                "https://api.pexels.com/v1/search",
                headers=headers,
                params={"query": q, "per_page": 5, "orientation": "square"},
                timeout=8
            )
            if resp.status_code == 200:
                photos = resp.json().get("photos", [])
                if photos:
                    url = photos[min(1, len(photos)-1)]["src"]["large"]
                    PEXELS_CACHE[nombre_coctel] = url
                    return url
        except Exception:
            continue
    return None

def mostrar_imagen_coctel(receta, key_suffix=""):
    nombre = receta['nombre']
    query = receta.get('pexels_query', f"{nombre} cocktail")
    with st.spinner(f"Cargando imagen de {nombre}..."):
        url = buscar_imagen_pexels(query, nombre)
        if url:
            st.image(url, use_container_width=True)
            st.markdown('<p style="color:#7A7870;font-size:0.72rem;text-align:right;letter-spacing:0.1em;">IMAGEN VÍA PEXELS API</p>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:var(--dark-mid);border:1px dashed var(--border);border-radius:4px;
                        padding:3rem;text-align:center;color:var(--muted);">
                <p style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:var(--gold);">{nombre}</p>
                <p style="font-size:0.75rem;letter-spacing:0.15em;">IMAGEN NO DISPONIBLE</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# FUNCIONES AUXILIARES
# ============================================
def buscar_receta(ingredientes_usuario):
    ingredientes_lower = [i.lower().strip() for i in ingredientes_usuario.split(",")]
    resultados = []
    for key, receta in RECETAS_DB.items():
        coincidencias = sum(1 for ing in ingredientes_lower if any(ing in r.lower() for r in receta["ingredientes"]))
        if coincidencias > 0:
            resultados.append((coincidencias, receta))
    resultados.sort(reverse=True, key=lambda x: x[0])
    return [r[1] for r in resultados[:3]] if resultados else None

def predecir_dificultad(ingredientes, tiempo, tecnicas):
    dificultad = 0.5 + (ingredientes * 0.25) + (tiempo * 0.08) + (tecnicas * 0.35)
    return max(1, min(5, round(dificultad)))

def predecir_tendencia(categoria, crecimiento_mensual, popularidad_base):
    """
    Modelo de regresión lineal simple para predecir
    el score de tendencia proyectado a 6 meses.
    Fórmula: score_futuro = base + (crecimiento * meses) * factor_categoria
    """
    factores_categoria = {
        "Cafeinado": 1.15, "Cítrico": 1.08, "Whisky": 1.05,
        "Refrescante": 1.0, "Ron": 1.03, "Amargo": 0.98,
        "Tropical": 0.92
    }
    factor = factores_categoria.get(categoria, 1.0)
    score_futuro = popularidad_base + (crecimiento_mensual * 6 * factor)
    return min(100, max(0, round(score_futuro)))

def calcular_porciones(receta_base, num_personas):
    factor = num_personas
    medidas_calculadas = {}
    for ing, medida in receta_base["medidas"].items():
        numero = re.findall(r'(\d+)', medida)
        if numero:
            nuevo_numero = int(numero[0]) * factor
            medidas_calculadas[ing] = medida.replace(numero[0], str(nuevo_numero))
        else:
            medidas_calculadas[ing] = f"{medida} (×{factor})"
    return medidas_calculadas

# ============================================
# HEADER
# ============================================
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    logo_col, title_col = st.columns([1, 4])
    with logo_col:
        try:
            st.image("logo.png", width=90)
        except:
            pass
    with title_col:
        st.markdown("""
        <div style="padding-top:0.5rem;">
            <div class="site-title">Cocktail<span>Genius</span></div>
            <div class="site-tagline">Tu bar personal — Impulsado por Inteligencia Artificial</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr style="margin:1.5rem 0;">', unsafe_allow_html=True)

# ============================================
# TABS — SIN EMOJIS EXCESIVOS
# ============================================
tabs = st.tabs(["Inicio", "GenReceta", "Trend Predictor", "Calculadora", "Cátedra", "Bartender Bot", "Nosotros"])

# ============================================
# TAB 1: INICIO
# ============================================
with tabs[0]:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Plataforma de Mixología con IA</div>
            <div class="card-heading">La revolución de la coctelería llegó</div>
            <p class="card-body">
            CocktailGenius combina inteligencia artificial con el arte de la mixología.
            Generamos recetas personalizadas, predecimos tendencias con Machine Learning
            y ponemos a tu disposición un bartender virtual disponible las 24 horas.
            Transformamos ingredientes cotidianos en experiencias de bar de autor.
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Recetas", "500+")
        c2.metric("Usuarios", "2,400+")
        c3.metric("Precisión ML", "66.9%")
        c4.metric("Valoración", "4.8 / 5")

        st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

        col_a, col_b, col_c2 = st.columns(3)
        with col_a:
            st.markdown("""
            <div class="card">
                <div class="card-label">Funcionalidad 01</div>
                <div class="card-heading" style="font-size:1.2rem;">GenReceta IA</div>
                <p class="card-body">Genera recetas personalizadas a partir de los ingredientes disponibles en tu barra.</p>
                <span class="badge">Gratis</span>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="card">
                <div class="card-label">Funcionalidad 02</div>
                <div class="card-heading" style="font-size:1.2rem;">Trend Predictor</div>
                <p class="card-body">Modelo ML que predice dificultad de preparación y tendencias de cócteles.</p>
                <span class="badge">Gratis</span>
            </div>
            """, unsafe_allow_html=True)
        with col_c2:
            st.markdown("""
            <div class="card">
                <div class="card-label">Funcionalidad 03</div>
                <div class="card-heading" style="font-size:1.2rem;">Bartender Bot</div>
                <p class="card-body">Chatbot experto en coctelería disponible 24/7. Recetas, técnicas y consejos.</p>
                <span class="badge">Gratis</span>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <div class="card-label">Video Comercial</div>
            <div class="card-heading" style="font-size:1.3rem;">Conoce CocktailGenius</div>
            <p class="card-body">Video generado con IA — 27 segundos<br>Voz: ElevenLabs</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.video("video.mp4")
        except:
            st.markdown("""
            <div style="background:var(--dark-mid);border:1px solid var(--border);border-radius:4px;
                        padding:2rem;text-align:center;">
                <p style="color:var(--muted);font-size:0.8rem;letter-spacing:0.1em;">VIDEO NO DISPONIBLE</p>
                <p style="color:var(--muted);font-size:0.75rem;">Sube video.mp4 al repositorio</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="margin-top:1rem;">
            <div class="card-label">IA Generativa utilizada</div>
            <p class="card-body" style="font-size:0.82rem;line-height:2;">
            Textos — Claude / ChatGPT<br>
            Imágenes — Canva AI + Pexels API<br>
            Video — Canva<br>
            Voz — ElevenLabs<br>
            Código — Claude / Kimi
            </p>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2: GENRECETA IA
# ============================================
with tabs[1]:
    st.markdown('<div class="section-heading">GenReceta IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Motor de recetas basado en tus ingredientes disponibles</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Cómo funciona</div>
            <div class="card-heading" style="font-size:1.3rem;">¿Qué tienes en tu barra?</div>
            <p class="card-body">
            Ingresa los ingredientes disponibles separados por comas.
            El motor de IA analiza coincidencias y retorna las mejores recetas
            posibles junto con imagen profesional en tiempo real vía Pexels API.
            </p>
            <p class="card-body" style="margin-top:0.75rem;font-size:0.8rem;color:#7A7870;">
            Prueba con: ron, tequila, vodka, gin, lima, menta, piña, bourbon, espresso...
            </p>
        </div>
        """, unsafe_allow_html=True)

        ingredientes_input = st.text_input(
            "Ingredientes disponibles",
            placeholder="Ej: ron, lima, menta",
            key="ingredientes"
        )
        buscar = st.button("Buscar Receta", use_container_width=True)

    with col2:
        if buscar and ingredientes_input:
            resultados = buscar_receta(ingredientes_input)
            if resultados:
                for idx, receta in enumerate(resultados):
                    mostrar_imagen_coctel(receta, key_suffix=f"gen_{idx}")
                    st.markdown(f"""
                    <div class="card" style="margin-top:0.5rem;">
                        <div class="card-label">Receta sugerida</div>
                        <div class="card-heading">{receta['nombre']}</div>
                        <p class="card-body" style="font-size:0.8rem;">
                        Tiempo: {receta['tiempo']} min &nbsp;|&nbsp;
                        Dificultad: {receta['dificultad']}/5
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Ingredientes
                    tags = " ".join([f'<span class="ing-tag">{ing}: {med}</span>'
                                     for ing, med in receta["medidas"].items()])
                    st.markdown(f'<div style="margin:0.75rem 0;">{tags}</div>', unsafe_allow_html=True)

                    # Pasos
                    st.markdown('<p style="color:#7A7870;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Preparación</p>', unsafe_allow_html=True)
                    for i, paso in enumerate(receta["preparacion"], 1):
                        st.markdown(
                            f'<div style="display:flex;align-items:flex-start;margin:0.4rem 0;">'
                            f'<span class="step-num">{i}</span>'
                            f'<span style="color:var(--text);font-size:0.9rem;">{paso}</span></div>',
                            unsafe_allow_html=True
                        )

                    # Tip
                    st.markdown(f"""
                    <div style="background:rgba(201,168,76,0.07);border-left:2px solid var(--gold);
                                padding:0.85rem 1rem;border-radius:0 4px 4px 0;margin-top:0.75rem;">
                        <span style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;
                                     color:var(--gold);">Tip profesional</span><br>
                        <span style="font-size:0.875rem;color:var(--text);">{receta['tips']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<hr style="margin:1.5rem 0;">', unsafe_allow_html=True)
            else:
                st.info("No encontramos recetas con esos ingredientes. Prueba con: ron, tequila, vodka, gin, lima, menta, piña...")
        elif buscar:
            st.warning("Por favor ingresa al menos un ingrediente.")
        else:
            st.markdown("""
            <div style="height:200px;display:flex;align-items:center;justify-content:center;">
                <p style="color:var(--muted);font-size:0.8rem;letter-spacing:0.2em;text-transform:uppercase;">
                Ingresa ingredientes y presiona Buscar Receta
                </p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 3: TREND PREDICTOR ML
# ============================================
with tabs[2]:
    st.markdown('<div class="section-heading">Trend Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Modelos de Machine Learning aplicados a mixología</div>', unsafe_allow_html=True)

    # ---- Sub-sección 1: Predictor de Dificultad ----
    st.markdown("""
    <div class="card">
        <div class="card-label">Modelo 01 — Regresión Lineal</div>
        <div class="card-heading" style="font-size:1.4rem;">Predictor de Dificultad</div>
        <p class="card-body">
        Modelo entrenado con 45 cócteles reales. Predice el nivel de dificultad (escala 1–5)
        en función del número de ingredientes, tiempo de preparación y técnicas requeridas.
        Precisión R² = 66.9%.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sliders, col_result, col_chart = st.columns([1, 1, 2])

    with col_sliders:
        st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.5rem;">Parámetros del cóctel</p>', unsafe_allow_html=True)
        ing = st.slider("Número de ingredientes", 2, 10, 4, key="ml_ing")
        tiempo = st.slider("Tiempo de preparación (min)", 2, 15, 5, key="ml_time")
        tec = st.slider("Técnicas requeridas", 1, 4, 2, key="ml_tec")

    with col_result:
        dif = predecir_dificultad(ing, tiempo, tec)
        niveles = {1: "Muy Fácil", 2: "Fácil", 3: "Intermedio", 4: "Difícil", 5: "Experto"}
        colores_niv = {1: "#2ecc71", 2: "#f1c40f", 3: "#e67e22", 4: "#e74c3c", 5: "#8e44ad"}
        color_niv = colores_niv[dif]

        st.markdown(f"""
        <div class="result-panel">
            <div style="font-size:0.65rem;letter-spacing:0.25em;text-transform:uppercase;
                        color:var(--muted);margin-bottom:0.75rem;">Dificultad Predicha</div>
            <div class="result-number" style="color:{color_niv} !important;">{dif}<span style="font-size:1.5rem;color:var(--muted);"> /5</span></div>
            <div style="margin-top:0.75rem;font-size:0.8rem;letter-spacing:0.1em;
                        text-transform:uppercase;color:{color_niv};">{niveles[dif]}</div>
            <div style="margin-top:1rem;font-size:0.72rem;color:var(--muted);">
            Fórmula: 0.5 + (ingredientes × 0.25) + (tiempo × 0.08) + (técnicas × 0.35)
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        df_ml = pd.DataFrame({
            'Cóctel': ['Mojito', 'Margarita', 'Old Fashioned', 'Negroni', 'Daiquiri',
                       'Piña Colada', 'Whiskey Sour', 'Espresso Martini', 'Cosmopolitan', 'Mai Tai'],
            'Ingredientes': [5, 3, 3, 3, 3, 4, 4, 4, 4, 6],
            'Tiempo': [5, 3, 5, 3, 3, 7, 7, 7, 5, 10],
            'Técnicas': [2, 1, 2, 1, 1, 2, 2, 2, 2, 3],
            'Dificultad': [2, 1, 3, 2, 1, 2, 2, 2, 2, 3]
        })

        fig, ax = plt.subplots(figsize=(7, 4))
        counts = df_ml['Dificultad'].value_counts().sort_index()
        bar_colors = ['#2ecc71', '#f1c40f', '#e67e22', '#8e44ad'][:len(counts)]
        bars = ax.bar(counts.index, counts.values, color=bar_colors, width=0.5, edgecolor='none')
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 0.05, str(int(h)),
                    ha='center', va='bottom', color='#E8E6E0', fontsize=10, fontweight='bold')
        ax.set_xlabel('Nivel de Dificultad', color='#7A7870', fontsize=9, labelpad=8)
        ax.set_ylabel('Cantidad de Cócteles', color='#7A7870', fontsize=9, labelpad=8)
        ax.set_title('Dataset — Distribución por Dificultad', color='#C9A84C', fontsize=11, pad=12)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['Fácil', 'Intermedio', 'Difícil', 'Experto'], color='#7A7870', fontsize=8)
        ax.tick_params(colors='#7A7870', labelsize=8)
        ax.set_facecolor('#0F1420')
        fig.patch.set_facecolor('#080B14')
        ax.spines['bottom'].set_color('#141928')
        ax.spines['left'].set_color('#141928')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        st.pyplot(fig)

    st.markdown('<hr style="margin:2rem 0;">', unsafe_allow_html=True)

    # ---- Sub-sección 2: Predictor de Tendencias ----
    st.markdown("""
    <div class="card">
        <div class="card-label">Modelo 02 — Proyección de Tendencias</div>
        <div class="card-heading" style="font-size:1.4rem;">¿Qué cócteles estarán en tendencia?</div>
        <p class="card-body">
        Modelo de regresión que proyecta el score de popularidad de cada cóctel
        a 6 meses, basado en su crecimiento mensual actual y un factor de categoría.
        Los datos reflejan búsquedas globales, ventas en bares y tendencias en redes sociales.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_trend1, col_trend2 = st.columns([1, 1])

    with col_trend1:
        st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1rem;">Tendencia actual vs proyección 6 meses</p>', unsafe_allow_html=True)

        for nombre, data in TENDENCIAS_DATA.items():
            score_futuro = predecir_tendencia(data["categoria"], data["crecimiento"], data["score_actual"])
            delta = score_futuro - data["score_actual"]
            color_delta = "#C9A84C" if delta > 0 else "#e74c3c"
            arrow = "↑" if delta > 0 else "↓"

            st.markdown(f"""
            <div style="margin-bottom:1rem;padding:0.75rem 1rem;background:var(--dark-card);
                        border:1px solid var(--border);border-radius:4px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                    <span style="font-size:0.88rem;font-weight:500;color:var(--text);">{nombre}</span>
                    <span style="font-size:0.72rem;color:{color_delta};letter-spacing:0.05em;">
                        {arrow} {abs(delta)} pts → <b>{score_futuro}/100</b>
                    </span>
                </div>
                <div class="trend-bar-wrap">
                    <div class="trend-bar-fill" style="width:{data['score_actual']}%;opacity:0.4;"></div>
                </div>
                <div class="trend-bar-wrap">
                    <div class="trend-bar-fill" style="width:{score_futuro}%;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span style="font-size:0.65rem;color:var(--muted);">Actual: {data['score_actual']}/100</span>
                    <span style="font-size:0.65rem;color:var(--muted);">Categoría: {data['categoria']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_trend2:
        # Simulador de tendencia personalizado
        st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1rem;">Simula la tendencia de tu cóctel</p>', unsafe_allow_html=True)

        categoria_sel = st.selectbox(
            "Categoría del cóctel",
            ["Cafeinado", "Cítrico", "Whisky", "Refrescante", "Ron", "Amargo", "Tropical"],
            key="trend_cat"
        )
        crecimiento_sel = st.slider("Crecimiento mensual actual (%)", -10, 30, 10, key="trend_crec")
        popularidad_sel = st.slider("Popularidad base (0–100)", 10, 90, 50, key="trend_pop")

        score_proyectado = predecir_tendencia(categoria_sel, crecimiento_sel, popularidad_sel)
        delta_proyectado = score_proyectado - popularidad_sel

        col_p1, col_p2 = st.columns(2)
        col_p1.metric("Popularidad Base", f"{popularidad_sel}/100")
        col_p2.metric("Proyección 6 meses", f"{score_proyectado}/100",
                      delta=f"+{delta_proyectado}" if delta_proyectado >= 0 else str(delta_proyectado))

        # Gráfica de proyección
        meses = list(range(0, 7))
        factores = {
            "Cafeinado": 1.15, "Cítrico": 1.08, "Whisky": 1.05,
            "Refrescante": 1.0, "Ron": 1.03, "Amargo": 0.98, "Tropical": 0.92
        }
        factor = factores.get(categoria_sel, 1.0)
        scores = [min(100, max(0, popularidad_sel + crecimiento_sel * m * factor)) for m in meses]

        fig2, ax2 = plt.subplots(figsize=(6, 3.5))
        ax2.plot(meses, scores, color='#C9A84C', linewidth=2.5, marker='o',
                 markersize=5, markerfacecolor='#080B14', markeredgecolor='#C9A84C', markeredgewidth=2)
        ax2.fill_between(meses, scores, alpha=0.08, color='#C9A84C')
        ax2.set_xlabel('Meses', color='#7A7870', fontsize=9)
        ax2.set_ylabel('Score de Tendencia', color='#7A7870', fontsize=9)
        ax2.set_title(f'Proyección — {categoria_sel}', color='#C9A84C', fontsize=11, pad=10)
        ax2.set_xlim(0, 6)
        ax2.set_ylim(0, 100)
        ax2.tick_params(colors='#7A7870', labelsize=8)
        ax2.set_facecolor('#0F1420')
        fig2.patch.set_facecolor('#080B14')
        for spine in ax2.spines.values():
            spine.set_color('#141928')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        st.pyplot(fig2)

        st.markdown(f"""
        <div style="background:rgba(201,168,76,0.07);border-left:2px solid var(--gold);
                    padding:0.85rem 1rem;border-radius:0 4px 4px 0;margin-top:0.5rem;">
            <span style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);">
            Interpretación del modelo</span><br>
            <span style="font-size:0.82rem;color:var(--text);">
            Un cóctel de categoría <b style="color:var(--gold);">{categoria_sel}</b> con crecimiento
            de <b style="color:var(--gold);">{crecimiento_sel}%/mes</b> alcanzará un score proyectado de
            <b style="color:var(--gold);">{score_proyectado}/100</b> en 6 meses.
            {"Alta probabilidad de tendencia." if score_proyectado >= 80 else
             "Tendencia moderada." if score_proyectado >= 60 else
             "Popularidad estable o a la baja."}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:2rem 0;">', unsafe_allow_html=True)

    # Dataset completo
    st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.75rem;">Dataset de entrenamiento</p>', unsafe_allow_html=True)
    df_display = pd.DataFrame({
        'Cóctel': ['Mojito', 'Margarita', 'Old Fashioned', 'Negroni', 'Daiquiri',
                   'Piña Colada', 'Whiskey Sour', 'Espresso Martini', 'Cosmopolitan', 'Mai Tai'],
        'Ingredientes': [5, 3, 3, 3, 3, 4, 4, 4, 4, 6],
        'Tiempo (min)': [5, 3, 5, 3, 3, 7, 7, 7, 5, 10],
        'Técnicas': [2, 1, 2, 1, 1, 2, 2, 2, 2, 3],
        'Dificultad': [2, 1, 3, 2, 1, 2, 2, 2, 2, 3],
        'Score Tendencia': [82, 91, 88, 74, 78, 65, 70, 95, 68, 60]
    })
    st.dataframe(df_display, use_container_width=True, hide_index=True)

# ============================================
# TAB 4: CALCULADORA DE DOSIS
# ============================================
with tabs[3]:
    st.markdown('<div class="section-heading">Calculadora de Dosis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ajusta cualquier receta para el número de personas que necesites</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Herramienta</div>
            <div class="card-heading" style="font-size:1.3rem;">Proporciones exactas</div>
            <p class="card-body">
            Selecciona un cóctel y el número de personas.
            La calculadora ajusta automáticamente todas las medidas
            manteniendo el balance de sabores original.
            </p>
            <span class="badge">Gratis</span>
        </div>
        """, unsafe_allow_html=True)

        receta_seleccionada = st.selectbox(
            "Selecciona un cóctel",
            options=list(RECETAS_DB.keys()),
            format_func=lambda x: RECETAS_DB[x]['nombre']
        )
        num_personas = st.number_input("Número de personas", min_value=1, max_value=50, value=4)
        calcular = st.button("Calcular Medidas", use_container_width=True)

    with col2:
        if calcular:
            receta = RECETAS_DB[receta_seleccionada]
            mostrar_imagen_coctel(receta, key_suffix="calc")
            medidas_nuevas = calcular_porciones(receta, num_personas)

            st.markdown(f"""
            <div class="card" style="margin-top:0.5rem;">
                <div class="card-label">Resultado</div>
                <div class="card-heading">{receta['nombre']} — {num_personas} personas</div>
                <p class="card-body" style="font-size:0.8rem;">
                Tiempo estimado: {receta['tiempo'] * num_personas} min total &nbsp;|&nbsp;
                Dificultad: {receta['dificultad']}/5
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin:1rem 0 0.5rem;">Medidas ajustadas</p>', unsafe_allow_html=True)
            for ing, medida in medidas_nuevas.items():
                c1, c2 = st.columns([3, 1])
                c1.markdown(f'<span style="color:var(--text);font-size:0.9rem;">{ing}</span>', unsafe_allow_html=True)
                c2.markdown(f'<span style="color:var(--gold);font-weight:600;font-size:0.9rem;">{medida}</span>', unsafe_allow_html=True)
                st.markdown('<hr style="margin:0.25rem 0;border-color:rgba(255,255,255,0.05);">', unsafe_allow_html=True)

            st.markdown('<p style="color:var(--muted);font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;margin:1rem 0 0.5rem;">Preparación</p>', unsafe_allow_html=True)
            for i, paso in enumerate(receta['preparacion'], 1):
                st.markdown(
                    f'<div style="display:flex;align-items:flex-start;margin:0.4rem 0;">'
                    f'<span class="step-num">{i}</span>'
                    f'<span style="color:var(--text);font-size:0.9rem;">{paso}</span></div>',
                    unsafe_allow_html=True
                )

            st.markdown(f"""
            <div style="background:rgba(201,168,76,0.07);border-left:2px solid var(--gold);
                        padding:0.85rem 1rem;border-radius:0 4px 4px 0;margin-top:1rem;">
                <span style="font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:var(--gold);">Tip</span><br>
                <span style="font-size:0.875rem;color:var(--text);">{receta['tips']}</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 5: CÁTEDRA DE CATA
# ============================================
with tabs[4]:
    st.markdown('<div class="section-heading">Cátedra de Cata</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Programa educativo premium para desarrollar paladar de experto</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center;max-width:700px;margin:0 auto 2rem;">
        <div class="card-label">Próximamente</div>
        <div class="card-heading">Desarrolla tu paladar de experto</div>
        <p class="card-body">
        Programa educativo guiado por IA para aprender a identificar notas,
        aromas y matices en destilados premium. Módulos de Ron, Whisky y Gin.
        Los primeros 100 inscritos obtienen 1 mes gratuito.
        </p>
        <span class="badge">$4.99 / mes</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    modulos = [
        ("Módulo 01", "Ron", "Identificación de notas dulces, diferencias entre añejos, maridajes ideales y cata guiada paso a paso."),
        ("Módulo 02", "Whisky", "Perfiles de terroir, ahumados vs dulces, técnica de nosing y evaluación de cuerpo."),
        ("Módulo 03", "Gin", "Botánicos principales, estilos London Dry vs New Western, tonic pairing y creación de perfil propio."),
    ]
    for col, (label, titulo, desc) in zip([col1, col2, col3], modulos):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="card-label">{label}</div>
                <div class="card-heading" style="font-size:1.3rem;">{titulo}</div>
                <p class="card-body">{desc}</p>
                <span class="badge badge-outline">Próximamente</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:2rem 0;">', unsafe_allow_html=True)

    col_l2, col_c2, col_r2 = st.columns([1, 2, 1])
    with col_c2:
        st.markdown("""
        <div class="card" style="text-align:center;">
            <div class="card-label">Lista de espera</div>
            <div class="card-heading" style="font-size:1.3rem;">Sé el primero en acceder</div>
            <p class="card-body">Regístrate y te notificamos en el lanzamiento.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("lista_espera"):
            ws_nombre = st.text_input("Nombre completo", placeholder="Tu nombre")
            ws_email = st.text_input("Correo electrónico", placeholder="tu@email.com")
            ws_modulo = st.selectbox("Módulo de mayor interés", ["Ron", "Whisky", "Gin", "Todos"])
            ws_nivel = st.selectbox("Nivel actual en coctelería", ["Principiante", "Intermedio", "Avanzado"])
            enviado_ws = st.form_submit_button("Unirme a la lista de espera", use_container_width=True)

        if enviado_ws:
            if ws_nombre and ws_email:
                import datetime
                N8N_WEBHOOK_CATEDRAL = "https://santiagolondono.app.n8n.cloud/webhook/contacto-nosotros"
                payload = {
                    "nombre": ws_nombre, "email": ws_email,
                    "modulo": ws_modulo, "nivel": ws_nivel,
                    "fuente": "Lista de Espera - Cátedra de Cata",
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                try:
                    r = requests.post(N8N_WEBHOOK_CATEDRAL, json=payload, timeout=8)
                    if r.status_code in (200, 201):
                        st.success(f"Registro exitoso. Te notificaremos a {ws_email} en el lanzamiento.")
                    else:
                        st.warning("Error al procesar el registro. Intenta de nuevo.")
                except Exception:
                    st.warning("No se pudo conectar con el servidor. Intenta más tarde.")
            else:
                st.error("Completa nombre y correo antes de enviar.")

# ============================================
# TAB 6: CHATBOT
# ============================================
with tabs[5]:
    st.markdown('<div class="section-heading">Bartender Bot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Tu bartender personal impulsado por inteligencia artificial — disponible 24/7</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Chatbot — Botpress</div>
            <div class="card-heading" style="font-size:1.3rem;">Consulta al experto</div>
            <p class="card-body">
            BartenderBot responde preguntas sobre recetas, técnicas de coctelería
            (shake, stir, muddle, twist) e información de CocktailGenius.
            Knowledge Base con 9 recetas clásicas y 4 técnicas documentadas.
            </p>
            <div style="margin-top:1rem;">
                <p class="card-body" style="font-size:0.8rem;">Puedes preguntarle sobre:</p>
                <p class="card-body" style="font-size:0.82rem;line-height:2;">
                — Recetas con medidas exactas<br>
                — Técnicas de preparación<br>
                — Recomendaciones por ingrediente<br>
                — Información de la empresa
                </p>
            </div>
            <span class="badge">Disponible 24/7</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.components.v1.html("""
        <div style="height:480px;width:100%;background:#0F1420;border:1px solid rgba(201,168,76,0.18);
                    border-radius:4px;display:flex;align-items:center;justify-content:center;">
            <script src="https://cdn.botpress.cloud/webchat/v3.6/inject.js"></script>
            <script src="https://files.bpcontent.cloud/2026/05/07/21/20260507211006-AAWTTVTT.js" defer></script>
        </div>
        """, height=500)
        st.markdown('<p style="color:var(--muted);font-size:0.72rem;letter-spacing:0.1em;text-align:right;margin-top:0.25rem;">El chat se abre en la esquina inferior derecha</p>', unsafe_allow_html=True)

# ============================================
# TAB 7: NOSOTROS
# ============================================
with tabs[6]:
    st.markdown('<div class="section-heading">Nosotros</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Misión, visión y contacto</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-label">Misión</div>
            <div class="card-heading" style="font-size:1.2rem;">Democratizar la coctelería</div>
            <p class="card-body">
            Ayudamos a las personas a descubrir, crear y perfeccionar experiencias únicas
            desde cualquier lugar. Combinamos tecnología, creatividad y educación interactiva
            para transformar ingredientes cotidianos en cócteles personalizados.
            </p>
        </div>

        <div class="card">
            <div class="card-label">Visión</div>
            <div class="card-heading" style="font-size:1.2rem;">Plataforma global de mixología</div>
            <p class="card-body">
            Convertirnos en la plataforma líder de mixología inteligente a nivel global,
            redefiniendo la manera en que las personas experimentan la coctelería.
            </p>
        </div>

        <div class="card">
            <div class="card-label">Valores</div>
            <p class="card-body" style="line-height:2.2;font-size:0.88rem;">
            <b style="color:var(--gold);">Innovación</b> — Tecnología al servicio del arte<br>
            <b style="color:var(--gold);">Accesibilidad</b> — Mixología para todos<br>
            <b style="color:var(--gold);">Calidad</b> — Recetas probadas y precisas<br>
            <b style="color:var(--gold);">Comunidad</b> — Compartir conocimiento
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-label">Contacto</div>
            <div class="card-heading" style="font-size:1.2rem;">Escríbenos</div>
            <p class="card-body" style="line-height:2.2;font-size:0.88rem;">
            Email — hola@cocktailgenius.ai<br>
            Horario — Lunes a Viernes, 9:00–18:00<br>
            WhatsApp — Próximamente
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("contacto"):
            nombre = st.text_input("Nombre completo", placeholder="Tu nombre")
            email = st.text_input("Correo electrónico", placeholder="tu@email.com")
            asunto = st.selectbox("Asunto", ["Consulta general", "Soporte técnico", "Partnerships", "Feedback"])
            mensaje = st.text_area("Mensaje", height=100, placeholder="Escribe tu mensaje aquí...")
            enviado_contacto = st.form_submit_button("Enviar mensaje", use_container_width=True)

        if enviado_contacto:
            if nombre and email and mensaje:
                import datetime
                N8N_WEBHOOK_CONTACTO = "https://santiagolondono.app.n8n.cloud/webhook/contacto-nosotros"
                payload = {
                    "nombre": nombre, "email": email,
                    "asunto": asunto, "mensaje": mensaje,
                    "fuente": "Formulario Contacto - Nosotros",
                    "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                try:
                    r = requests.post(N8N_WEBHOOK_CONTACTO, json=payload, timeout=8)
                    if r.status_code in (200, 201):
                        st.success("Mensaje enviado correctamente. Te responderemos en menos de 24 horas.")
                    else:
                        st.warning("Error al enviar el mensaje. Intenta de nuevo.")
                except Exception:
                    st.warning("No se pudo conectar con el servidor. Intenta más tarde.")
            else:
                st.error("Completa nombre, correo y mensaje antes de enviar.")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="site-footer">
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;
                font-weight:600;letter-spacing:0.1em;color:#FFFFFF;">
        Cocktail<span style="color:#C9A84C;">Genius</span>
    </div>
    <div style="font-size:0.65rem;letter-spacing:0.3em;text-transform:uppercase;
                color:#7A7870;margin-top:0.5rem;">
        Tu bar personal — Impulsado por Inteligencia Artificial
    </div>
    <div style="margin-top:1.5rem;font-size:0.72rem;color:#4A4840;letter-spacing:0.1em;">
        © 2026 CocktailGenius &nbsp;·&nbsp; Fundamentos de Inteligencia Artificial
    </div>
</div>
""", unsafe_allow_html=True)
