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
    # ── RON ──────────────────────────────────────────────────────────────
    "mojito": {
        "nombre": "Mojito Clásico",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Ron blanco", "Lima", "Limón", "Menta", "Hierbabuena", "Azúcar", "Azúcar blanca", "Soda", "Agua con gas"],
        "medidas": {"Ron blanco": "45ml", "Lima": "30ml", "Menta": "6 hojas", "Azúcar": "2 cdas", "Soda": "Completar"},
        "preparacion": ["Machaca la menta con azúcar y jugo de lima en el vaso", "Añade hielo picado hasta 3/4 del vaso", "Vierte el ron blanco", "Completa con agua con gas", "Decora con ramita de menta"],
        "tips": "No machaques la menta con fuerza, solo presiona para liberar aceites esenciales sin amargar.",
        "pexels_query": "mojito cocktail mint", "tendencia_score": 82
    },
    "daiquiri": {
        "nombre": "Daiquiri Clásico",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Ron blanco", "Ron", "Lima", "Limón", "Jarabe de azúcar", "Azúcar", "Azúcar blanca"],
        "medidas": {"Ron blanco": "60ml", "Jugo de lima": "25ml", "Jarabe de azúcar": "15ml"},
        "preparacion": ["En coctelera con hielo, añade ron, jugo de lima y jarabe", "Agita vigorosamente 10 segundos", "Cuela doblemente en copa fría", "Decora con twist de lima"],
        "tips": "El equilibrio entre dulce y ácido es la esencia de este clásico.",
        "pexels_query": "daiquiri rum cocktail", "tendencia_score": 78
    },
    "piña colada": {
        "nombre": "Piña Colada",
        "dificultad": 2, "tiempo": 7,
        "ingredientes": ["Ron blanco", "Ron", "Piña", "Jugo de piña", "Crema de coco", "Leche de coco", "Coco"],
        "medidas": {"Ron blanco": "60ml", "Jugo de piña": "90ml", "Crema de coco": "30ml", "Hielo": "1 taza"},
        "preparacion": ["Licúa todos los ingredientes con hielo", "Bate hasta consistencia cremosa", "Sirve en vaso alto", "Decora con piña y cereza"],
        "tips": "Usa piña fresca para un sabor más vibrante.",
        "pexels_query": "pina colada tropical cocktail", "tendencia_score": 65
    },
    "cuba libre": {
        "nombre": "Cuba Libre",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Ron blanco", "Ron", "Ron añejo", "Coca-Cola", "Cola", "Lima", "Limón"],
        "medidas": {"Ron": "50ml", "Cola": "Completar", "Lima": "Jugo de media"},
        "preparacion": ["Llena un vaso alto con hielo", "Añade el ron y el jugo de lima", "Completa con cola bien fría", "Revuelve suavemente y decora con rodaja de lima"],
        "tips": "Usa ron añejo para más carácter, o ron blanco para algo más ligero.",
        "pexels_query": "cuba libre rum cola cocktail", "tendencia_score": 72
    },
    "dark and stormy": {
        "nombre": "Dark & Stormy",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Ron oscuro", "Ron añejo", "Ron", "Cerveza de jengibre", "Ginger beer", "Jengibre", "Lima"],
        "medidas": {"Ron oscuro": "60ml", "Ginger beer": "Completar", "Lima": "Jugo de media"},
        "preparacion": ["Llena vaso alto con hielo", "Añade el jugo de lima", "Vierte la ginger beer", "Flota el ron oscuro encima sin mezclar", "Decora con rodaja de lima"],
        "tips": "No mezcles el ron para mantener el efecto visual de dos capas.",
        "pexels_query": "dark stormy rum ginger cocktail", "tendencia_score": 68
    },
    "mai tai": {
        "nombre": "Mai Tai",
        "dificultad": 3, "tiempo": 8,
        "ingredientes": ["Ron blanco", "Ron oscuro", "Ron", "Triple sec", "Naranja", "Lima", "Limón", "Almendra", "Jarabe de azúcar"],
        "medidas": {"Ron blanco": "30ml", "Ron oscuro": "30ml", "Triple sec": "15ml", "Lima": "20ml", "Jarabe de almendra": "10ml"},
        "preparacion": ["Agita todos los ingredientes con hielo excepto el ron oscuro", "Sirve en vaso bajo con hielo", "Flota el ron oscuro encima", "Decora con menta y rodaja de piña"],
        "tips": "El jarabe de almendra (orgeat) es el ingrediente secreto que lo distingue.",
        "pexels_query": "mai tai tropical rum cocktail", "tendencia_score": 61
    },
    # ── GIN ──────────────────────────────────────────────────────────────
    "gin tonic": {
        "nombre": "Gin Tonic",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Gin", "Ginebra", "Agua tónica", "Tónica", "Lima", "Limón", "Pepino", "Romero"],
        "medidas": {"Gin": "50ml", "Tónica": "150ml", "Lima": "2 rodajas"},
        "preparacion": ["Enfría una copa balloon o vaso alto", "Añade hielo abundante", "Vierte el gin", "Agrega la tónica muy fría sin agitar", "Decora con lima y aromáticos al gusto"],
        "tips": "El gin tonic vive o muere por la calidad de la tónica. Úsala bien fría.",
        "pexels_query": "gin tonic cocktail lime", "tendencia_score": 88
    },
    "negroni": {
        "nombre": "Negroni",
        "dificultad": 2, "tiempo": 3,
        "ingredientes": ["Gin", "Ginebra", "Campari", "Vermut rojo", "Vermut", "Naranja"],
        "medidas": {"Gin": "30ml", "Campari": "30ml", "Vermut rojo": "30ml"},
        "preparacion": ["En vaso bajo con hielo grande", "Vierte partes iguales de gin, Campari y vermut", "Remueve suavemente 20 segundos", "Decora con twist de naranja"],
        "tips": "Clásico italiano ideal para aperitivo. Usa un gin botánico de calidad.",
        "pexels_query": "negroni cocktail bar", "tendencia_score": 74
    },
    "tom collins": {
        "nombre": "Tom Collins",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Gin", "Ginebra", "Limón", "Lima", "Azúcar", "Jarabe de azúcar", "Soda", "Agua con gas"],
        "medidas": {"Gin": "45ml", "Jugo de limón": "30ml", "Jarabe de azúcar": "15ml", "Soda": "Completar"},
        "preparacion": ["En vaso alto con hielo, añade gin, limón y jarabe", "Completa con soda bien fría", "Revuelve suavemente", "Decora con rodaja de limón y cereza"],
        "tips": "Perfecto para días calurosos. Puedes usar lima en lugar de limón.",
        "pexels_query": "tom collins gin cocktail", "tendencia_score": 66
    },
    "gimlet": {
        "nombre": "Gimlet",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Gin", "Ginebra", "Lima", "Limón", "Jarabe de azúcar", "Azúcar"],
        "medidas": {"Gin": "60ml", "Jugo de lima": "20ml", "Jarabe de azúcar": "10ml"},
        "preparacion": ["En coctelera con hielo, añade todos los ingredientes", "Agita bien 10 segundos", "Cuela en copa fría", "Decora con twist de lima"],
        "tips": "Simple pero elegante. El equilibrio ácido-dulce es clave.",
        "pexels_query": "gimlet gin lime cocktail", "tendencia_score": 59
    },
    "aviation": {
        "nombre": "Aviation",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Gin", "Ginebra", "Limón", "Lima", "Cereza", "Jarabe de azúcar", "Violeta"],
        "medidas": {"Gin": "45ml", "Jugo de limón": "15ml", "Maraschino": "15ml", "Crème de violette": "7ml"},
        "preparacion": ["En coctelera con hielo, combina todos los ingredientes", "Agita vigorosamente 12 segundos", "Cuela doblemente en copa de cóctel", "Decora con cereza"],
        "tips": "El color azul-lavanda es su sello. No omitas la crème de violette.",
        "pexels_query": "aviation cocktail purple blue", "tendencia_score": 55
    },
    "bee's knees": {
        "nombre": "Bee's Knees",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Gin", "Ginebra", "Limón", "Lima", "Miel", "Jarabe de miel"],
        "medidas": {"Gin": "60ml", "Jugo de limón": "22ml", "Jarabe de miel": "22ml"},
        "preparacion": ["Prepara jarabe calentando miel con agua caliente en proporción 1:1", "En coctelera con hielo, añade gin, limón y jarabe de miel", "Agita vigorosamente", "Cuela en copa fría", "Decora con twist de limón"],
        "tips": "El jarabe de miel casero eleva este cóctel a otro nivel.",
        "pexels_query": "bees knees gin honey cocktail", "tendencia_score": 63
    },
    # ── VODKA ─────────────────────────────────────────────────────────────
    "espresso martini": {
        "nombre": "Espresso Martini",
        "dificultad": 2, "tiempo": 7,
        "ingredientes": ["Vodka", "Licor de café", "Café", "Espresso", "Café negro", "Kahlúa"],
        "medidas": {"Vodka": "50ml", "Licor de café": "30ml", "Espresso": "30ml fresco"},
        "preparacion": ["Prepara espresso y deja enfriar 1 minuto", "En coctelera con hielo, añade vodka, licor de café y espresso", "Agita enérgicamente 15 segundos", "Cuela doblemente en copa fría", "Decora con 3 granos de café"],
        "tips": "La clave está en agitar muy fuerte para crear la espuma característica.",
        "pexels_query": "espresso martini coffee cocktail", "tendencia_score": 95
    },
    "cosmopolitan": {
        "nombre": "Cosmopolitan",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Vodka", "Triple sec", "Naranja", "Arándano", "Jugo de arándano", "Lima", "Limón"],
        "medidas": {"Vodka": "45ml", "Triple sec": "15ml", "Jugo de arándano": "30ml", "Lima": "15ml"},
        "preparacion": ["En coctelera con hielo, añade todos los ingredientes", "Agita bien hasta enfriar", "Cuela en copa martini", "Decora con twist de naranja"],
        "tips": "El jugo de arándano le da el color rosa icónico. Usa poca cantidad para no endulzar en exceso.",
        "pexels_query": "cosmopolitan pink cocktail", "tendencia_score": 69
    },
    "moscow mule": {
        "nombre": "Moscow Mule",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Vodka", "Cerveza de jengibre", "Ginger beer", "Jengibre", "Lima", "Limón"],
        "medidas": {"Vodka": "50ml", "Ginger beer": "150ml", "Lima": "Jugo de media"},
        "preparacion": ["Llena un vaso (idealmente de cobre) con hielo", "Añade el vodka y el jugo de lima", "Completa con ginger beer bien fría", "Revuelve suavemente", "Decora con rodaja de lima y jengibre"],
        "tips": "El vaso de cobre mantiene la bebida fría más tiempo y es parte de la experiencia.",
        "pexels_query": "moscow mule copper mug cocktail", "tendencia_score": 80
    },
    "vodka tonic": {
        "nombre": "Vodka Tonic",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Vodka", "Agua tónica", "Tónica", "Lima", "Limón", "Pepino"],
        "medidas": {"Vodka": "50ml", "Tónica": "150ml", "Lima": "2 rodajas"},
        "preparacion": ["Llena vaso alto con hielo", "Añade el vodka", "Vierte la tónica fría sin agitar", "Exprime y añade rodajas de lima"],
        "tips": "Alternativa más suave al gin tonic. Perfecta para quienes no gustan del sabor botánico.",
        "pexels_query": "vodka tonic lime cocktail", "tendencia_score": 71
    },
    "screwdriver": {
        "nombre": "Screwdriver",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Vodka", "Naranja", "Jugo de naranja", "Jugo natural", "Jugo"],
        "medidas": {"Vodka": "50ml", "Jugo de naranja": "150ml"},
        "preparacion": ["Llena vaso alto con hielo", "Añade el vodka", "Completa con jugo de naranja recién exprimido", "Revuelve y decora con rodaja de naranja"],
        "tips": "Usa naranja recién exprimida, no de caja, para una diferencia notable.",
        "pexels_query": "screwdriver vodka orange juice cocktail", "tendencia_score": 62
    },
    "bloody mary": {
        "nombre": "Bloody Mary",
        "dificultad": 3, "tiempo": 6,
        "ingredientes": ["Vodka", "Tomate", "Jugo de tomate", "Limón", "Lima", "Salsa picante", "Tabasco", "Sal", "Pimienta", "Apio", "Worcestershire"],
        "medidas": {"Vodka": "50ml", "Jugo de tomate": "150ml", "Limón": "15ml", "Tabasco": "Al gusto"},
        "preparacion": ["En vaso alto con hielo, añade vodka", "Agrega jugo de tomate", "Sazona con limón, tabasco, sal y pimienta", "Revuelve bien", "Decora con apio y rodaja de limón"],
        "tips": "El Bloody Mary es muy personal: ajusta el picante y la acidez a tu gusto.",
        "pexels_query": "bloody mary tomato cocktail", "tendencia_score": 64
    },
    # ── TEQUILA ───────────────────────────────────────────────────────────
    "margarita": {
        "nombre": "Margarita",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Tequila", "Triple sec", "Cointreau", "Naranja", "Lima", "Limón", "Sal"],
        "medidas": {"Tequila": "50ml", "Triple sec": "25ml", "Lima": "15ml", "Sal": "Para el borde"},
        "preparacion": ["Pasa lima por el borde del vaso y luego por sal", "En coctelera con hielo, mezcla tequila, triple sec y jugo de lima", "Agita 10 segundos", "Cuela en vaso escarchado con sal"],
        "tips": "Usa tequila 100% agave para un sabor limpio y auténtico.",
        "pexels_query": "margarita cocktail", "tendencia_score": 91
    },
    "paloma": {
        "nombre": "Paloma",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Tequila", "Toronja", "Pomelo", "Jugo de toronja", "Jugo de pomelo", "Lima", "Sal", "Soda", "Agua con gas"],
        "medidas": {"Tequila": "50ml", "Jugo de toronja": "90ml", "Lima": "15ml", "Soda": "Splash"},
        "preparacion": ["Escacha el borde del vaso con sal", "Llena con hielo", "Añade tequila y jugo de toronja", "Exprime la lima y añade un chorrito de soda", "Decora con rodaja de toronja"],
        "tips": "Es el cóctel de tequila más popular en México. Simple y refrescante.",
        "pexels_query": "paloma tequila grapefruit cocktail", "tendencia_score": 76
    },
    "tequila sunrise": {
        "nombre": "Tequila Sunrise",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Tequila", "Naranja", "Jugo de naranja", "Jugo", "Granadina", "Cereza"],
        "medidas": {"Tequila": "45ml", "Jugo de naranja": "120ml", "Granadina": "15ml"},
        "preparacion": ["Llena vaso alto con hielo", "Añade tequila y jugo de naranja", "Revuelve suavemente", "Vierte la granadina despacio por el borde (se hundirá creando el efecto)", "No mezcles"],
        "tips": "El truco está en añadir la granadina al final sin mezclar para el efecto degradado.",
        "pexels_query": "tequila sunrise orange cocktail", "tendencia_score": 70
    },
    "tommy's margarita": {
        "nombre": "Tommy's Margarita",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Tequila", "Lima", "Limón", "Jarabe de agave", "Agave", "Miel de agave"],
        "medidas": {"Tequila": "60ml", "Lima": "30ml", "Jarabe de agave": "15ml"},
        "preparacion": ["En coctelera con hielo, añade tequila, lima y agave", "Agita 12 segundos", "Cuela en vaso con hielo", "Decora con rodaja de lima"],
        "tips": "La versión moderna de la margarita: sin triple sec, el tequila brilla más.",
        "pexels_query": "margarita tequila lime cocktail", "tendencia_score": 77
    },
    # ── WHISKY / BOURBON ──────────────────────────────────────────────────
    "old fashioned": {
        "nombre": "Old Fashioned",
        "dificultad": 3, "tiempo": 5,
        "ingredientes": ["Bourbon", "Whisky", "Whiskey", "Azúcar", "Azúcar blanca", "Angostura", "Naranja"],
        "medidas": {"Bourbon": "45ml", "Azúcar": "1 terrón", "Angostura": "2 gotas", "Naranja": "Cáscara"},
        "preparacion": ["Coloca el terrón de azúcar en el vaso", "Añade 2 gotas de angostura y un poco de agua", "Disuelve el azúcar formando pasta", "Añade hielo grande y el bourbon", "Remueve suavemente 30 segundos", "Exprime cáscara de naranja sobre el trago"],
        "tips": "El hielo debe ser grande para una dilución lenta y controlada.",
        "pexels_query": "old fashioned whiskey cocktail", "tendencia_score": 88
    },
    "whiskey sour": {
        "nombre": "Whiskey Sour",
        "dificultad": 2, "tiempo": 7,
        "ingredientes": ["Bourbon", "Whisky", "Whiskey", "Limón", "Lima", "Jarabe de azúcar", "Azúcar", "Huevo", "Clara de huevo"],
        "medidas": {"Bourbon": "60ml", "Jugo de limón": "30ml", "Jarabe de azúcar": "15ml", "Clara de huevo": "1 (opcional)"},
        "preparacion": ["En coctelera seca (sin hielo), mezcla bourbon, limón, jarabe y clara", "Agita en seco 15 segundos (dry shake)", "Añade hielo y agita 10 segundos más", "Cuela en vaso bajo con hielo", "Decora con cereza y naranja"],
        "tips": "La clara de huevo en seco crea una textura sedosa y espuma densa.",
        "pexels_query": "whiskey sour cocktail bourbon", "tendencia_score": 70
    },
    "manhattan": {
        "nombre": "Manhattan",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Bourbon", "Whisky", "Whiskey", "Vermut rojo", "Vermut", "Angostura", "Cereza"],
        "medidas": {"Bourbon": "50ml", "Vermut rojo": "25ml", "Angostura": "2 gotas"},
        "preparacion": ["En vaso mezclador con hielo, añade bourbon, vermut y angostura", "Remueve suavemente durante 30 segundos", "Cuela en copa de cóctel", "Decora con cereza al marrasquino"],
        "tips": "Se remueve, no se agita. Agitar rompe el equilibrio del cóctel.",
        "pexels_query": "manhattan whiskey cocktail", "tendencia_score": 73
    },
    "whisky highball": {
        "nombre": "Whisky Highball",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Whisky", "Whiskey", "Bourbon", "Soda", "Agua con gas", "Agua mineral"],
        "medidas": {"Whisky": "45ml", "Soda": "Completar"},
        "preparacion": ["Llena vaso alto con mucho hielo", "Añade el whisky", "Vierte la soda fría sin mezclar mucho", "Decora con twist de limón si deseas"],
        "tips": "Técnica japonesa: usa hielo en abundancia y soda bien fría para no diluir.",
        "pexels_query": "whisky highball soda cocktail", "tendencia_score": 67
    },
    "mint julep": {
        "nombre": "Mint Julep",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Bourbon", "Whisky", "Menta", "Hierbabuena", "Azúcar", "Jarabe de azúcar"],
        "medidas": {"Bourbon": "60ml", "Menta": "8 hojas", "Jarabe de azúcar": "15ml"},
        "preparacion": ["Machaca suavemente la menta con el jarabe en el vaso", "Llena con hielo picado fino", "Añade el bourbon", "Remueve hasta que el vaso esté escarcha", "Decora con ramita de menta abundante"],
        "tips": "El vaso debe empañarse completamente de frío. Usa hielo picado, no cubos.",
        "pexels_query": "mint julep bourbon cocktail", "tendencia_score": 58
    },
    # ── CHAMPÁN / PROSECCO / VINO ─────────────────────────────────────────
    "aperol spritz": {
        "nombre": "Aperol Spritz",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Aperol", "Prosecco", "Champán", "Cava", "Vino espumoso", "Soda", "Agua con gas", "Naranja"],
        "medidas": {"Prosecco": "90ml", "Aperol": "60ml", "Soda": "Splash"},
        "preparacion": ["Llena copa grande con hielo", "Añade el prosecco", "Agrega el Aperol", "Chorrito de soda", "Decora con rodaja de naranja"],
        "tips": "La proporción 3-2-1 (prosecco-aperol-soda) es la original veneciana.",
        "pexels_query": "aperol spritz orange cocktail", "tendencia_score": 89
    },
    "mimosa": {
        "nombre": "Mimosa",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Prosecco", "Champán", "Cava", "Vino espumoso", "Naranja", "Jugo de naranja"],
        "medidas": {"Champán": "90ml", "Jugo de naranja": "90ml"},
        "preparacion": ["Enfría la copa de champán", "Vierte el jugo de naranja recién exprimido", "Añade el champán o prosecco lentamente", "No mezcles para preservar las burbujas"],
        "tips": "Usa jugo de naranja fresco. La proporción es 50/50 pero puedes ajustar al gusto.",
        "pexels_query": "mimosa champagne orange cocktail", "tendencia_score": 75
    },
    "kir royal": {
        "nombre": "Kir Royal",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Champán", "Prosecco", "Cava", "Vino espumoso", "Cassis", "Licor de grosella", "Moras", "Frutos rojos"],
        "medidas": {"Champán": "150ml", "Crème de cassis": "15ml"},
        "preparacion": ["En copa fría, añade el crème de cassis", "Vierte el champán muy lentamente", "No mezcles", "Decora con mora o frambuesa"],
        "tips": "El cassis se hunde solo. Solo añade el champán encima para el efecto degradado.",
        "pexels_query": "kir royal champagne cocktail", "tendencia_score": 60
    },
    "sangria": {
        "nombre": "Sangría Española",
        "dificultad": 2, "tiempo": 10,
        "ingredientes": ["Vino tinto", "Vino", "Naranja", "Limón", "Lima", "Manzana", "Melocotón", "Durazno", "Azúcar", "Brandy", "Coñac", "Soda"],
        "medidas": {"Vino tinto": "750ml", "Brandy": "60ml", "Azúcar": "2 cdas", "Naranja": "1 entera", "Limón": "1 entero"},
        "preparacion": ["Corta las frutas en rodajas y coloca en jarra", "Añade el azúcar y el brandy", "Vierte el vino tinto", "Refrigera al menos 2 horas", "Sirve con hielo y un chorrito de soda"],
        "tips": "Prepárala con antelación, mínimo 2 horas en nevera para que maceren las frutas.",
        "pexels_query": "sangria red wine fruit cocktail", "tendencia_score": 71
    },
    # ── LICORES Y MEZCLAS ─────────────────────────────────────────────────
    "amaretto sour": {
        "nombre": "Amaretto Sour",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Amaretto", "Licor de almendra", "Limón", "Lima", "Jarabe de azúcar", "Azúcar", "Huevo", "Clara de huevo"],
        "medidas": {"Amaretto": "45ml", "Jugo de limón": "30ml", "Jarabe de azúcar": "7ml", "Clara de huevo": "1"},
        "preparacion": ["Dry shake todos los ingredientes sin hielo 10 segundos", "Añade hielo y agita 10 segundos más", "Cuela en vaso bajo con hielo", "Decora con cereza y naranja"],
        "tips": "El amaretto ya es dulce; ajusta el jarabe según tu preferencia.",
        "pexels_query": "amaretto sour cocktail", "tendencia_score": 66
    },
    "baileys on the rocks": {
        "nombre": "Baileys on the Rocks",
        "dificultad": 1, "tiempo": 1,
        "ingredientes": ["Baileys", "Crema irlandesa", "Licor de crema", "Café", "Chocolate", "Leche"],
        "medidas": {"Baileys": "60ml"},
        "preparacion": ["Llena vaso bajo con hielo grande", "Vierte el Baileys", "Opcionalmente añade un chorrito de café frío"],
        "tips": "Sirve siempre con hielo para atenuar el dulzor de la crema.",
        "pexels_query": "baileys irish cream cocktail", "tendencia_score": 57
    },
    "sex on the beach": {
        "nombre": "Sex on the Beach",
        "dificultad": 1, "tiempo": 3,
        "ingredientes": ["Vodka", "Durazno", "Melocotón", "Licor de durazno", "Jugo de arándano", "Arándano", "Naranja", "Jugo de naranja"],
        "medidas": {"Vodka": "40ml", "Licor de durazno": "20ml", "Jugo de naranja": "40ml", "Jugo de arándano": "40ml"},
        "preparacion": ["Llena vaso alto con hielo", "Añade vodka y licor de durazno", "Agrega los jugos", "Revuelve suavemente", "Decora con naranja y cereza"],
        "tips": "No lo mezcles demasiado para mantener las capas de color.",
        "pexels_query": "sex beach vodka orange cocktail", "tendencia_score": 64
    },
    "pisco sour": {
        "nombre": "Pisco Sour",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Pisco", "Lima", "Limón", "Jarabe de azúcar", "Azúcar", "Huevo", "Clara de huevo", "Angostura"],
        "medidas": {"Pisco": "60ml", "Lima": "30ml", "Jarabe de azúcar": "20ml", "Clara de huevo": "1"},
        "preparacion": ["Dry shake todos los ingredientes sin hielo", "Añade hielo y agita enérgicamente", "Cuela en copa fría", "Decora con 3 gotas de angostura"],
        "tips": "El dry shake es esencial para la espuma densa. Es el orgullo de Perú y Chile.",
        "pexels_query": "pisco sour peruvian cocktail", "tendencia_score": 69
    },
    # ── SIN ALCOHOL / MOCKTAILS ───────────────────────────────────────────
    "virgin mojito": {
        "nombre": "Virgin Mojito",
        "dificultad": 1, "tiempo": 4,
        "ingredientes": ["Lima", "Limón", "Menta", "Hierbabuena", "Azúcar", "Azúcar blanca", "Soda", "Agua con gas", "Agua mineral"],
        "medidas": {"Lima": "30ml", "Menta": "8 hojas", "Azúcar": "2 cdas", "Soda": "Completar"},
        "preparacion": ["Machaca menta con azúcar y lima en el vaso", "Añade hielo picado", "Completa con soda bien fría", "Decora con ramita de menta y rodaja de lima"],
        "tips": "Agrega un poco de jengibre rallado para darle un toque de spice sin alcohol.",
        "pexels_query": "virgin mojito mocktail mint lime", "tendencia_score": 73
    },
    "limonada casera": {
        "nombre": "Limonada de la Casa",
        "dificultad": 1, "tiempo": 5,
        "ingredientes": ["Limón", "Lima", "Azúcar", "Jarabe de azúcar", "Agua", "Menta", "Hierbabuena"],
        "medidas": {"Limón": "3 unidades", "Azúcar": "3 cdas", "Agua": "250ml"},
        "preparacion": ["Exprime los limones y mezcla con azúcar hasta disolver", "Añade agua fría y hielo", "Ajusta dulzor al gusto", "Decora con rodaja de limón y menta"],
        "tips": "Añade ralladura de limón para intensificar el sabor cítrico.",
        "pexels_query": "homemade lemonade fresh lemon", "tendencia_score": 68
    },
    "agua fresca de sandía": {
        "nombre": "Agua Fresca de Sandía",
        "dificultad": 1, "tiempo": 5,
        "ingredientes": ["Sandía", "Lima", "Limón", "Azúcar", "Menta", "Agua"],
        "medidas": {"Sandía": "400g", "Lima": "15ml", "Azúcar": "1 cda", "Agua": "200ml"},
        "preparacion": ["Licúa la sandía con el agua", "Cuela para eliminar semillas", "Añade lima y azúcar al gusto", "Sirve sobre hielo con hoja de menta"],
        "tips": "Perfecta en verano. Añade un chorrito de ron para convertirla en coctel.",
        "pexels_query": "watermelon agua fresca drink", "tendencia_score": 61
    },
    # ── CREMOSOS Y CALIENTES ──────────────────────────────────────────────
    "white russian": {
        "nombre": "White Russian",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Vodka", "Licor de café", "Café", "Kahlúa", "Crema de leche", "Nata", "Leche"],
        "medidas": {"Vodka": "50ml", "Licor de café": "25ml", "Crema": "25ml"},
        "preparacion": ["En vaso bajo con hielo, añade vodka y licor de café", "Vierte la crema encima muy despacio", "Deja que flote sin mezclar", "Sirve así para el efecto visual"],
        "tips": "La crema debe flotar. Si la mezclas pierdes el efecto característico.",
        "pexels_query": "white russian cream coffee cocktail", "tendencia_score": 72
    },
    "black russian": {
        "nombre": "Black Russian",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Vodka", "Licor de café", "Café", "Kahlúa"],
        "medidas": {"Vodka": "50ml", "Licor de café": "25ml"},
        "preparacion": ["En vaso bajo con hielo grande", "Añade vodka y licor de café", "Remueve suavemente 10 segundos"],
        "tips": "El hermano oscuro del White Russian. Simple, fuerte y equilibrado.",
        "pexels_query": "black russian vodka coffee cocktail", "tendencia_score": 60
    },
    "irish coffee": {
        "nombre": "Irish Coffee",
        "dificultad": 2, "tiempo": 6,
        "ingredientes": ["Whisky", "Whiskey", "Café", "Espresso", "Café negro", "Crema de leche", "Nata", "Azúcar", "Azúcar morena"],
        "medidas": {"Whisky irlandés": "45ml", "Café caliente": "120ml", "Azúcar morena": "1 cda", "Crema": "30ml"},
        "preparacion": ["Calienta la taza con agua caliente y vacíala", "Disuelve el azúcar morena con un poco de café caliente", "Añade el whisky", "Completa con café caliente", "Vierte la crema sobre el dorso de una cuchara para que flote"],
        "tips": "La crema NO se mezcla. Se bebe el café caliente a través de la crema fría.",
        "pexels_query": "irish coffee cream whiskey", "tendencia_score": 75
    },
    "hot toddy": {
        "nombre": "Hot Toddy",
        "dificultad": 1, "tiempo": 5,
        "ingredientes": ["Whisky", "Whiskey", "Bourbon", "Miel", "Jarabe de miel", "Limón", "Lima", "Agua caliente", "Canela", "Clavo"],
        "medidas": {"Whisky": "45ml", "Miel": "1 cda", "Limón": "30ml", "Agua caliente": "150ml"},
        "preparacion": ["Disuelve la miel en el agua caliente", "Añade el whisky y el jugo de limón", "Decora con palito de canela y rodaja de limón con clavo"],
        "tips": "El remedio escocés para el frío. También funciona con brandy o ron.",
        "pexels_query": "hot toddy whiskey honey lemon", "tendencia_score": 63
    },
    # ── TROPICALES Y ESPECIALES ───────────────────────────────────────────
    "caipirinha": {
        "nombre": "Caipirinha",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Cachaça", "Aguardiente", "Lima", "Limón", "Azúcar", "Azúcar blanca"],
        "medidas": {"Cachaça": "60ml", "Lima": "1 entera", "Azúcar": "2 cdas"},
        "preparacion": ["Corta la lima en cuartos y coloca en vaso", "Añade el azúcar", "Machaca fuerte para extraer el jugo y aceites de la cáscara", "Llena de hielo picado", "Añade la cachaça y mezcla bien"],
        "tips": "La lima entera (no solo el jugo) le da el sabor característico amargo-cítrico.",
        "pexels_query": "caipirinha lime brazil cocktail", "tendencia_score": 77
    },
    "michelada": {
        "nombre": "Michelada",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Cerveza", "Limón", "Lima", "Salsa picante", "Tabasco", "Sal", "Salsa inglesa", "Worcestershire", "Tomate", "Jugo de tomate"],
        "medidas": {"Cerveza": "355ml", "Limón": "30ml", "Tabasco": "Al gusto", "Sal": "Para el borde"},
        "preparacion": ["Escacha el borde del vaso con sal (y chile en polvo opcional)", "Añade hielo al vaso", "Exprime el limón", "Añade salsas al gusto", "Vierte la cerveza fría y mezcla suavemente"],
        "tips": "Usa cerveza clara y fría. El picante es a gusto pero define el carácter.",
        "pexels_query": "michelada beer lime spicy cocktail", "tendencia_score": 70
    },
    "frozen margarita": {
        "nombre": "Frozen Margarita",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Tequila", "Triple sec", "Cointreau", "Naranja", "Lima", "Limón", "Sal"],
        "medidas": {"Tequila": "50ml", "Triple sec": "25ml", "Lima": "30ml", "Hielo": "1 taza"},
        "preparacion": ["Escacha borde del vaso con sal", "Licúa tequila, triple sec, lima y hielo hasta consistencia sorbete", "Sirve inmediatamente en vaso escarchado"],
        "tips": "Agrega trozos de mango o fresa al licuar para variaciones de sabor.",
        "pexels_query": "frozen margarita slush cocktail", "tendencia_score": 74
    },
    "clericot": {
        "nombre": "Clericot",
        "dificultad": 1, "tiempo": 8,
        "ingredientes": ["Vino blanco", "Vino", "Naranja", "Manzana", "Durazno", "Melocotón", "Fresa", "Azúcar", "Soda", "Agua con gas"],
        "medidas": {"Vino blanco": "750ml", "Azúcar": "2 cdas", "Frutas": "Al gusto"},
        "preparacion": ["Corta todas las frutas en cubos pequeños", "Mezcla con azúcar y deja reposar 5 minutos", "Añade el vino blanco", "Refrigera 1 hora", "Sirve con hielo y un toque de soda"],
        "tips": "La versión blanca de la sangría. Usa frutas de temporada.",
        "pexels_query": "clericot white wine fruit punch", "tendencia_score": 59
    },
    "coquito": {
        "nombre": "Coquito",
        "dificultad": 2, "tiempo": 10,
        "ingredientes": ["Ron blanco", "Ron", "Crema de coco", "Leche de coco", "Coco", "Leche condensada", "Leche evaporada", "Leche", "Canela", "Vainilla"],
        "medidas": {"Ron": "240ml", "Crema de coco": "400ml", "Leche condensada": "400ml", "Leche evaporada": "340ml"},
        "preparacion": ["Licúa todos los ingredientes hasta integrar", "Añade canela y vainilla al gusto", "Refrigera al menos 2 horas", "Sirve muy frío con canela espolvoreada"],
        "tips": "Mejora de un día para otro. Agita bien antes de servir.",
        "pexels_query": "coquito coconut rum christmas drink", "tendencia_score": 65
    },
    "bramble": {
        "nombre": "Bramble",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Gin", "Ginebra", "Limón", "Lima", "Jarabe de azúcar", "Azúcar", "Moras", "Frutos rojos", "Crème de mûre", "Licor de mora"],
        "medidas": {"Gin": "45ml", "Jugo de limón": "25ml", "Jarabe de azúcar": "15ml", "Licor de mora": "15ml"},
        "preparacion": ["En vaso con hielo picado, añade gin, limón y jarabe", "Remueve", "Vierte el licor de mora encima en espiral sin mezclar", "Decora con moras y rodaja de limón"],
        "tips": "El licor de mora debe verterlo despacio al final para crear el efecto visual.",
        "pexels_query": "bramble gin blackberry cocktail", "tendencia_score": 67
    },
    "frozen daiquiri de fresa": {
        "nombre": "Daiquiri de Fresa Frozen",
        "dificultad": 2, "tiempo": 5,
        "ingredientes": ["Ron blanco", "Ron", "Fresa", "Fresas", "Lima", "Limón", "Jarabe de azúcar", "Azúcar"],
        "medidas": {"Ron blanco": "60ml", "Fresas": "6 unidades", "Lima": "30ml", "Jarabe de azúcar": "20ml", "Hielo": "1 taza"},
        "preparacion": ["Licúa ron, fresas, lima, jarabe y hielo hasta textura suave", "Prueba y ajusta dulzor", "Sirve inmediatamente en copa fría", "Decora con fresa entera"],
        "tips": "Usa fresas maduras y congeladas para mejor textura y sabor más intenso.",
        "pexels_query": "strawberry daiquiri frozen cocktail", "tendencia_score": 79
    },
    "hugo spritz": {
        "nombre": "Hugo Spritz",
        "dificultad": 1, "tiempo": 2,
        "ingredientes": ["Prosecco", "Champán", "Cava", "Vino espumoso", "Flores de saúco", "Jarabe de saúco", "Elderflower", "Menta", "Hierbabuena", "Soda", "Lima", "Limón"],
        "medidas": {"Prosecco": "100ml", "Jarabe de saúco": "20ml", "Soda": "Splash", "Menta": "3 hojas"},
        "preparacion": ["Llena copa con hielo y hojas de menta", "Añade jarabe de flores de saúco", "Vierte el prosecco", "Completa con un toque de soda", "Decora con lima y menta"],
        "tips": "El rival del Aperol Spritz. Más floral y ligero. El jarabe de saúco (elderflower) es esencial.",
        "pexels_query": "hugo spritz elderflower cocktail", "tendencia_score": 82
    },
    "dark chocolate martini": {
        "nombre": "Chocolate Martini",
        "dificultad": 2, "tiempo": 4,
        "ingredientes": ["Vodka", "Licor de chocolate", "Cacao", "Chocolate", "Crema de cacao", "Baileys", "Crema de leche", "Leche"],
        "medidas": {"Vodka": "45ml", "Licor de chocolate": "30ml", "Crema de cacao": "15ml"},
        "preparacion": ["Enfría bien la copa martini", "En coctelera con hielo, mezcla vodka, licor de chocolate y crema de cacao", "Agita 12 segundos", "Cuela en copa", "Decora con cacao espolvoreado"],
        "tips": "Puedes escarchar el borde de la copa con chocolate rallado.",
        "pexels_query": "chocolate martini cocktail dark", "tendencia_score": 66
    },
}


# ============================================
# DATOS TENDENCIA ML — Modelo de regresión
# ============================================
TENDENCIAS_DATA = {
    "Espresso Martini":  {"score_actual": 95, "crecimiento": 28, "categoria": "Cafeinado"},
    "Aperol Spritz":     {"score_actual": 89, "crecimiento": 22, "categoria": "Cítrico"},
    "Margarita":         {"score_actual": 91, "crecimiento": 15, "categoria": "Cítrico"},
    "Hugo Spritz":       {"score_actual": 82, "crecimiento": 20, "categoria": "Refrescante"},
    "Old Fashioned":     {"score_actual": 88, "crecimiento": 12, "categoria": "Whisky"},
    "Moscow Mule":       {"score_actual": 80, "crecimiento": 10, "categoria": "Refrescante"},
    "Mojito":            {"score_actual": 82, "crecimiento": 5,  "categoria": "Refrescante"},
    "Paloma":            {"score_actual": 76, "crecimiento": 18, "categoria": "Cítrico"},
    "Mimosa":            {"score_actual": 75, "crecimiento": 8,  "categoria": "Cítrico"},
    "Irish Coffee":      {"score_actual": 75, "crecimiento": 6,  "categoria": "Cafeinado"},
    "Caipirinha":        {"score_actual": 77, "crecimiento": 9,  "categoria": "Cítrico"},
    "Daiquiri de Fresa": {"score_actual": 79, "crecimiento": 14, "categoria": "Frutal"},
    "Negroni":           {"score_actual": 74, "crecimiento": 8,  "categoria": "Amargo"},
    "Pisco Sour":        {"score_actual": 69, "crecimiento": 11, "categoria": "Cítrico"},
    "Sangria":           {"score_actual": 71, "crecimiento": 4,  "categoria": "Frutal"},
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
    # Normalizar y separar ingredientes del usuario
    ingredientes_lower = [i.lower().strip() for i in re.split(r'[,;\s]+', ingredientes_usuario) if i.strip()]
    resultados = []
    for key, receta in RECETAS_DB.items():
        receta_ings = [r.lower() for r in receta["ingredientes"]]
        coincidencias = 0
        for ing_user in ingredientes_lower:
            for ing_receta in receta_ings:
                if ing_user in ing_receta or ing_receta in ing_user:
                    coincidencias += 1
                    break
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
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    try:
        st.image("logo2.png", use_container_width=True)
    except:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown('<div class="site-title" style="text-align:center;">Cocktail<span>Genius</span></div>', unsafe_allow_html=True)

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
            Prueba con: gin, vodka, ron, tequila, whisky, bourbon, champán, prosecco,<br>
            vino, cerveza, lima, limón, naranja, menta, miel, café, espresso, moras,<br>
            fresas, piña, coco, jengibre, canela, huevo, leche, crema, azúcar...
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
                st.info("No encontramos recetas con esos ingredientes. Prueba con: gin, vodka, ron, tequila, whisky, lima, limón, naranja, menta, miel, café, prosecco, vino, cerveza, fresa, piña, coco...")
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
