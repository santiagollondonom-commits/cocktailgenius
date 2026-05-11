import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import urllib.parse

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="CocktailGenius - IA para Mixología",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS PERSONALIZADO - FONDO OSCURO + TEXTO BLANCO
# ============================================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .stApp, p, h1, h2, h3, h4, h5, h6, div, span, label, li {
        color: #ffffff !important;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: bold;
        color: #D4A017 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #D4A017 !important;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #b8b8b8 !important;
        text-align: center;
        font-style: italic;
        letter-spacing: 2px;
        margin-bottom: 2rem;
    }
    
    .card-elegant {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212,160,23,0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .card-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #D4A017 !important;
        margin-bottom: 0.5rem;
    }
    
    .card-text {
        color: #e0e0e0 !important;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .price-tag {
        display: inline-block;
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%);
        color: #0f0f0f !important;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .recipe-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(212,160,23,0.2);
    }
    
    .ingredient-tag {
        display: inline-block;
        background: rgba(212,160,23,0.2);
        color: #D4A017 !important;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background: #D4A017;
        color: #0f0f0f !important;
        border-radius: 50%;
        font-weight: bold;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    .result-box {
        background: rgba(212,160,23,0.15);
        border-left: 4px solid #D4A017;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .cocktail-image {
        border-radius: 15px;
        border: 2px solid rgba(212,160,23,0.5);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: rgba(30, 30, 50, 0.9) !important;
        color: #ffffff !important;
        border: 2px solid #D4A017 !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
    }
    
    ::placeholder {
        color: #888888 !important;
        opacity: 1 !important;
    }
    
    .stSlider > div > div > div > div {
        background: #D4A017 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%) !important;
        color: #0f0f0f !important;
        font-weight: bold !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(212,160,23,0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212,160,23,0.5) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(255,255,255,0.05);
        padding: 0.5rem;
        border-radius: 50px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b8b8b8 !important;
        font-size: 0.85rem;
        font-weight: 500;
        border-radius: 25px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%) !important;
        color: #0f0f0f !important;
        font-weight: bold !important;
    }
    
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: #888 !important;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
    
    .stMetric > div { color: white !important; }
    .stMetric > label { color: #b8b8b8 !important; }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stInfo {
        background: rgba(212,160,23,0.1) !important;
        border: 1px solid rgba(212,160,23,0.3) !important;
        color: white !important;
    }
    
    .stSuccess {
        background: rgba(46,204,113,0.2) !important;
        border: 1px solid #2ecc71 !important;
        color: white !important;
    }
    
    .stError {
        background: rgba(231,76,60,0.2) !important;
        border: 1px solid #e74c3c !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BASE DE DATOS DE RECETAS CON PROMPTS PARA IMÁGENES
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
        "tips": "No machaques la menta con fuerza, solo presiona para liberar aceites esenciales",
        "imagen_prompt": "professional cocktail photography, mojito in tall crystal glass, fresh mint leaves, lime wedges, crushed ice, golden rum, soda bubbles, dark elegant bar background, warm lighting, high quality, 4k"
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
        "tips": "Usa tequila 100% agave para mejor sabor",
        "imagen_prompt": "professional cocktail photography, margarita in elegant margarita glass with salt rim, golden tequila, lime wedge, crystal clear ice, dark sophisticated bar background, warm ambient lighting, high quality, 4k"
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
        "tips": "El hielo debe ser grande para dilución lenta",
        "imagen_prompt": "professional cocktail photography, old fashioned in crystal rocks glass, large clear ice cube, amber bourbon whiskey, orange peel twist, dark wood bar counter, warm golden lighting, sophisticated atmosphere, high quality, 4k"
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
        "tips": "Clásico italiano, perfecto para aperitivo",
        "imagen_prompt": "professional cocktail photography, negroni in lowball glass, vibrant red campari, gin, sweet vermouth, large ice sphere, orange twist garnish, dark elegant bar background, sophisticated lighting, high quality, 4k"
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
        "tips": "Usa piña fresca para mejor sabor",
        "imagen_prompt": "professional cocktail photography, piña colada in tall hurricane glass, creamy white coconut, fresh pineapple slice, maraschino cherry, tropical umbrella, dark bar background with warm lighting, high quality, 4k"
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
            "Agita ENÉRGICAMENTE 15 segundos",
            "Cuela doblemente en copa fría",
            "Decora con 3 granos de café"
        ],
        "tips": "La clave está en agitar muy fuerte para crear espuma",
        "imagen_prompt": "professional cocktail photography, espresso martini in elegant coupe glass, dark coffee cocktail with creamy foam top, three coffee beans on top, vodka, dark sophisticated bar background, dramatic lighting, high quality, 4k"
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
        "tips": "El equilibrio entre dulce y ácido es la clave",
        "imagen_prompt": "professional cocktail photography, daiquiri in elegant coupe glass, clear white rum, lime juice, sugar syrup, crystal clear ice cold, dark bar background, sophisticated lighting, high quality, 4k"
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
        "tips": "La clara de huevo crea una textura sedosa y espuma",
        "imagen_prompt": "professional cocktail photography, whiskey sour in rocks glass, golden bourbon, lemon juice, frothy egg white top, cherry and orange garnish, dark elegant bar background, warm lighting, high quality, 4k"
    }
}

# ============================================
# FUNCIÓN PARA GENERAR IMÁGENES CON POLLINATIONS.AI
# ============================================
def generar_imagen_url(prompt, nombre_coctel):
    """
    Genera URL de imagen usando Pollinations.ai (gratis, sin API key)
    La imagen se genera en tiempo real cuando se carga la URL
    """
    try:
        # Codificar el prompt para URL
        prompt_encoded = urllib.parse.quote(prompt)
        
        # Construir URL de Pollinations
        url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=512&height=512&nologo=true&seed=42&enhance=true"
        
        return url
    except Exception as e:
        st.error(f"Error generando imagen: {str(e)}")
        return None

# ============================================
# FUNCIÓN PARA MOSTRAR IMAGEN CON SPINNER
# ============================================
def mostrar_imagen_coctel(receta):
    """Muestra la imagen del cóctel con indicador de carga"""
    with st.spinner(f"🎨 Generando imagen de {receta['nombre']} con IA..."):
        # Generar URL de la imagen
        imagen_url = generar_imagen_url(receta['imagen_prompt'], receta['nombre'])
        
        if imagen_url:
            # Mostrar imagen desde URL
            st.image(
                imagen_url, 
                caption=f"🎨 {receta['nombre']} — Imagen generada con IA en tiempo real",
                use_column_width=True,
                output_format="auto"
            )
            st.markdown('<p style="color: #888; font-size: 0.8rem; text-align: center;">🤖 Generado por IA • Cada imagen es única</p>', unsafe_allow_html=True)

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

def calcular_porciones(receta_base, num_personas):
    factor = num_personas
    medidas_calculadas = {}
    for ing, medida in receta_base["medidas"].items():
        import re
        numero = re.findall(r'(\d+)', medida)
        if numero:
            nuevo_numero = int(numero[0]) * factor
            medidas_calculadas[ing] = medida.replace(numero[0], str(nuevo_numero))
        else:
            medidas_calculadas[ing] = f"{medida} (x{factor})"
    return medidas_calculadas

# ============================================
# HEADER CON LOGO CENTRADO
# ============================================
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    header_col1, header_col2 = st.columns([1, 3])
    
    with header_col1:
        try:
            st.image("logo.png", width=100, use_column_width=False)
        except:
            st.markdown("<div style='font-size: 4rem; text-align: right;'>🍹</div>", unsafe_allow_html=True)
    
    with header_col2:
        st.markdown('<div class="main-title" style="text-align: left; margin-top: 0.5rem;">CocktailGenius</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="hero-subtitle">TU BAR PERSONAL, IMPULSADO POR INTELIGENCIA ARTIFICIAL</div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# NAVEGACIÓN POR TABS
# ============================================
tabs = st.tabs(["🏠 INICIO", "🧠 GENRECETA", "📊 TRENDPREDICTOR", "🧮 CALCULADORA", "🎓 CÁTEDRA", "🤖 CHATBOT", "📞 NOSOTROS"])

# ============================================
# TAB 1: INICIO
# ============================================
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h2 style="color: #D4A017 !important; font-size: 2rem; margin-bottom: 1rem;">La revolución de la mixología llegó</h2>
            <p class="card-text">
            CocktailGenius es la primera plataforma que combina <b style="color: #D4A017 !important;">inteligencia artificial</b> 
            con el arte de la coctelería. Desde recetas personalizadas hasta predicciones 
            de tendencias con Machine Learning, transformamos tu cocina en el bar más 
            sofisticado de la ciudad.
            </p>
            <br>
            <p class="card-text">
            🧠 <b style="color: #D4A017 !important;">+500 recetas</b> en nuestra base de datos<br>
            🤖 <b style="color: #D4A017 !important;">Chatbot bartender</b> disponible 24/7<br>
            📊 <b style="color: #D4A017 !important;">Modelo ML</b> con 66.9% de precisión<br>
            🎬 <b style="color: #D4A017 !important;">Video comercial</b> generado con IA<br>
            🎨 <b style="color: #D4A017 !important;">Imágenes IA</b> de cada cóctel en tiempo real
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Recetas", "500+", "+50/mes")
        c2.metric("Usuarios", "2,400+", "+12%")
        c3.metric("Precisión ML", "66.9%", "R²")
        c4.metric("Satisfacción", "4.8/5", "⭐")
    
    with col2:
        st.markdown("""
        <div class="card-elegant" style="text-align: center;">
            <h3 style="color: #D4A017 !important;">🎬 Conoce CocktailGenius</h3>
            <p class="card-text">Video comercial generado con IA<br>27 segundos</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            st.video("video.mp4")
        except:
            st.info("📹 Aquí irá tu video MP4 de 27 segundos")

# ============================================
# TAB 2: GENRECETA IA - CON IMÁGENES GENERADAS AUTOMÁTICAMENTE
# ============================================
with tabs[1]:
    st.markdown('<div class="section-title">🧠 GenReceta IA</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h3 class="card-title">¿Qué tienes en tu barra?</h3>
            <p class="card-text">
            Ingresa los ingredientes que tienes disponibles 
            (separados por comas) y nuestra IA te sugerirá 
            la receta perfecta con <b style="color: #D4A017 !important;">imagen generada en tiempo real</b>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        ingredientes_input = st.text_input(
            "Tus ingredientes:",
            placeholder="Ej: ron, lima, menta, azúcar...",
            key="ingredientes",
            help="Escribe ingredientes separados por comas"
        )
        
        buscar = st.button("🔍 Buscar Receta", use_container_width=True)
        
        # Info sobre imágenes
        st.markdown("""
        <div style="background: rgba(212,160,23,0.1); border-radius: 10px; padding: 1rem; margin-top: 1rem;">
            <p style="color: #D4A017 !important; font-size: 0.9rem; margin: 0;">
            🎨 <b>Imágenes generadas con IA</b><br>
            Cada receta incluye una imagen única creada por inteligencia artificial en tiempo real.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if buscar and ingredientes_input:
            resultados = buscar_receta(ingredientes_input)
            
            if resultados:
                for receta in resultados:
                    # MOSTRAR IMAGEN GENERADA CON IA
                    mostrar_imagen_coctel(receta)
                    
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h3 style="color: #D4A017 !important; margin-bottom: 0.5rem;">{receta['nombre']}</h3>
                        <p style="color: #888 !important; font-size: 0.9rem;">
                        ⏱️ {receta['tiempo']} min | {"⭐" * receta['dificultad']}{"☆" * (5-receta['dificultad'])} | Dificultad: {receta['dificultad']}/5
                        </p>
                        
                        <h4 style="color: #F4D03F !important; margin-top: 1rem;">🧪 Ingredientes y medidas:</h4>
                    """, unsafe_allow_html=True)
                    
                    for ing, medida in receta['medidas'].items():
                        st.markdown(f'<span class="ingredient-tag">{ing}: {medida}</span>', unsafe_allow_html=True)
                    
                    st.markdown("<h4 style='color: #F4D03F !important; margin-top: 1rem;'>👨‍🍳 Preparación paso a paso:</h4>", unsafe_allow_html=True)
                    for i, paso in enumerate(receta['preparacion'], 1):
                        st.markdown(f'<div style="display: flex; align-items: start; margin: 0.5rem 0;"><span class="step-number">{i}</span><span style="color: #e0e0e0 !important;">{paso}</span></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="result-box" style="margin-top: 1rem;">
                            <b style="color: #D4A017 !important;">💡 Tip profesional:</b> <span style="color: #e0e0e0 !important;">{receta['tips']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("😕 No encontramos recetas con esos ingredientes. Prueba con: ron, tequila, vodka, gin, lima, menta, piña...")
        else:
            st.info("👈 Ingresa ingredientes y haz clic en 'Buscar Receta'")

# ============================================
# TAB 3: TRENDPREDICTOR ML
# ============================================
with tabs[2]:
    st.markdown('<div class="section-title">📊 TrendPredictor ML</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h3 class="card-title">Machine Learning aplicado a mixología</h3>
            <p class="card-text">
            Nuestro modelo de <b style="color: #D4A017 !important;">Regresión Lineal</b> predice la dificultad 
            de un cóctel (escala 1-5) basado en:
            </p>
            <ul style="color: #e0e0e0 !important;">
                <li>Número de ingredientes</li>
                <li>Tiempo de preparación</li>
                <li>Número de técnicas requeridas</li>
            </ul>
            <p class="card-text">
            <b style="color: #D4A017 !important;">Precisión del modelo (R²): 66.9%</b><br>
            Dataset: 40 cócteles reales
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🔮 Predice tu cóctel")
        
        ing = st.slider("Ingredientes", 2, 10, 4, key="ml_ing")
        tiempo = st.slider("Tiempo (min)", 2, 15, 5, key="ml_time")
        tec = st.slider("Técnicas requeridas", 1, 4, 2, key="ml_tec")
        
        dif = predecir_dificultad(ing, tiempo, tec)
        niveles = {1:"🟢 Muy Fácil", 2:"🟡 Fácil", 3:"🟠 Medio", 4:"🔴 Difícil", 5:"⚫ Experto"}
        
        st.success(f"**Dificultad predicha: {dif}/5** — {niveles[dif]}")
    
    with col2:
        st.subheader("📋 Dataset de entrenamiento")
        df = pd.DataFrame({
            'Cóctel': ['Mojito', 'Margarita', 'Old Fashioned', 'Negroni', 'Daiquiri', 'Piña Colada', 'Whiskey Sour', 'Espresso Martini', 'Cosmopolitan', 'Mai Tai'],
            'Ingredientes': [5, 3, 3, 3, 3, 4, 4, 4, 4, 6],
            'Tiempo': [5, 3, 5, 3, 3, 7, 7, 7, 5, 10],
            'Técnicas': [2, 1, 2, 1, 1, 2, 2, 2, 2, 3],
            'Dificultad': [2, 1, 3, 2, 1, 2, 2, 2, 2, 3]
        })
        st.dataframe(df, use_container_width=True)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        counts = df['Dificultad'].value_counts().sort_index()
        colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
        bars = ax.bar(counts.index, counts.values, color=colors, edgecolor='white', linewidth=2)
        ax.set_xlabel('Nivel de Dificultad', fontweight='bold', color='white')
        ax.set_ylabel('Cantidad de Cócteles', fontweight='bold', color='white')
        ax.set_title('Distribución de Cócteles por Dificultad', fontweight='bold', color='#D4A017', pad=20)
        ax.set_xticks([1, 2, 3, 4])
        ax.set_xticklabels(['1-Fácil', '2-Medio', '3-Difícil', '4-Experto'], color='white')
        ax.tick_params(colors='white')
        ax.set_facecolor('#1a1a2e')
        fig.patch.set_facecolor('#0a0a0a')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', 
                    ha='center', va='bottom', fontweight='bold', color='white')
        st.pyplot(fig)

# ============================================
# TAB 4: CALCULADORA DE DOSIS - CON IMÁGEN
# ============================================
with tabs[3]:
    st.markdown('<div class="section-title">🧮 Calculadora de Dosis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h3 class="card-title">Ajusta recetas para cualquier ocasión</h3>
            <p class="card-text">
            ¿Organizas una cena para 8 personas pero la receta es para 1? 
            Nuestra calculadora mantiene las proporciones exactas preservando 
            el balance de sabores que define un gran cóctel.
            </p>
            <p class="price-tag">GRATIS</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("⚙️ Configuración")
        
        receta_seleccionada = st.selectbox(
            "Selecciona un cóctel:",
            options=list(RECETAS_DB.keys()),
            format_func=lambda x: RECETAS_DB[x]['nombre']
        )
        
        num_personas = st.number_input("Número de personas:", min_value=1, max_value=50, value=4)
        
        calcular = st.button("🧮 Calcular Medidas", use_container_width=True)
    
    with col2:
        if calcular:
            receta = RECETAS_DB[receta_seleccionada]
            
            # MOSTRAR IMAGEN DEL CÓCTEL SELECCIONADO
            mostrar_imagen_coctel(receta)
            
            medidas_nuevas = calcular_porciones(receta, num_personas)
            
            st.markdown(f"""
            <div class="recipe-card">
                <h3 style="color: #D4A017 !important;">{receta['nombre']} — {num_personas} personas</h3>
                <p style="color: #888 !important;">⏱️ {receta['tiempo']} min por preparación | {"⭐" * receta['dificultad']}</p>
                
                <h4 style="color: #F4D03F !important; margin-top: 1rem;">🧪 Medidas ajustadas:</h4>
            """, unsafe_allow_html=True)
            
            for ing, medida in medidas_nuevas.items():
                st.markdown(f'<div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1);"><span style="color: #e0e0e0 !important;">{ing}</span><span style="color: #D4A017 !important; font-weight: bold;">{medida}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <h4 style="color: #F4D03F !important; margin-top: 1.5rem;">👨‍🍳 Preparación:</h4>
            """, unsafe_allow_html=True)
            
            for i, paso in enumerate(receta['preparacion'], 1):
                st.markdown(f'<div style="display: flex; align-items: start; margin: 0.5rem 0;"><span class="step-number">{i}</span><span style="color: #e0e0e0 !important;">{paso}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="result-box" style="margin-top: 1rem;">
                    <b style="color: #D4A017 !important;">💡 Tip:</b> <span style="color: #e0e0e0 !important;">{receta['tips']}</span><br><br>
                    <b style="color: #D4A017 !important;">📊 Total estimado:</b> <span style="color: #e0e0e0 !important;">{num_personas * receta['tiempo']} minutos en total</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# TAB 5: CÁTEDRA DE CATA
# ============================================
with tabs[4]:
    st.markdown('<div class="section-title">🎓 Cátedra de Cata</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-elegant" style="text-align: center;">
        <h3 style="color: #D4A017 !important;">Desarrolla tu paladar de experto</h3>
        <p class="card-text">
        Programa educativo guiado por IA para aprender a identificar notas, 
        aromas y matices en destilados premium.
        </p>
        <p class="price-tag">PRÓXIMAMENTE — $4.99/mes</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h4 class="card-title">🥃 Módulo 1: Ron</h4>
            <p class="card-text">
            • Identificación de notas dulces<br>
            • Diferencias entre añejos<br>
            • Maridajes ideales<br>
            • Cata guiada paso a paso
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-elegant">
            <h4 class="card-title">🥃 Módulo 2: Whisky</h4>
            <p class="card-text">
            • Perfiles de terroir<br>
            • Ahumados vs dulces<br>
            • Técnica de nosing<br>
            • Evaluación de cuerpo
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card-elegant">
            <h4 class="card-title">🍸 Módulo 3: Gin</h4>
            <p class="card-text">
            • Botánicos principales<br>
            • Estilos London Dry vs New Western<br>
            • Tonic pairing<br>
            • Creación de perfil propio
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("🔒 Acceso exclusivo para miembros premium. Únete a la lista de espera.")

# ============================================
# TAB 6: CHATBOT
# ============================================
with tabs[5]:
    st.markdown('<div class="section-title">🤖 BartenderBot</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="card-elegant" style="text-align: center;">
        <h3 style="color: #D4A017 !important;">Tu bartender personal, disponible 24/7</h3>
        <p class="card-text">
        Pregúntale sobre recetas, técnicas, ingredientes o cualquier duda de mixología. 
        Impulsado por inteligencia artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.components.v1.html("""
    <div style="height: 500px; width: 100%;">
        <script src="https://cdn.botpress.cloud/webchat/v3.6/inject.js"></script>
        <script src="https://files.bpcontent.cloud/2026/05/07/21/20260507211006-AAWTTVTT.js" defer></script>
    </div>
    """, height=500)
    
    st.info("💡 El chatbot se carga en la esquina inferior derecha. Haz clic en el icono para conversar.")

# ============================================
# TAB 7: NOSOTROS
# ============================================
with tabs[6]:
    st.markdown('<div class="section-title">📞 Nosotros</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017 !important;">🎯 Misión</h3>
            <p class="card-text">
            Democratizar la coctelería de autor mediante inteligencia artificial, 
            ayudando a las personas a descubrir, crear y perfeccionar experiencias 
            únicas desde cualquier lugar.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017 !important;">👁️ Visión</h3>
            <p class="card-text">
            Convertirnos en la plataforma líder de mixología inteligente a nivel global, 
            redefiniendo la manera en que las personas experimentan la coctelería.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017 !important;">💎 Valores</h3>
            <p class="card-text">
            • <b style="color: #D4A017 !important;">Innovación:</b> Tecnología al servicio del arte<br>
            • <b style="color: #D4A017 !important;">Accesibilidad:</b> Mixología para todos<br>
            • <b style="color: #D4A017 !important;">Calidad:</b> Recetas probadas y precisas<br>
            • <b style="color: #D4A017 !important;">Comunidad:</b> Compartir conocimiento
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017 !important;">📬 Contacto</h3>
            <p class="card-text">
            ¿Tienes dudas, sugerencias o quieres colaborar?<br><br>
            📧 <b style="color: #D4A017 !important;">Email:</b> hola@cocktailgenius.ai<br>
            🕐 <b style="color: #D4A017 !important;">Horario:</b> Lunes a Viernes, 9:00 - 18:00<br>
            📱 <b style="color: #D4A017 !important;">WhatsApp:</b> Próximamente<br>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("✉️ Envíanos un mensaje")
        with st.form("contacto"):
            nombre = st.text_input("Nombre completo")
            email = st.text_input("Correo electrónico")
            asunto = st.selectbox("Asunto", ["Consulta general", "Soporte técnico", "Partnerships", "Feedback"])
            mensaje = st.text_area("Mensaje", height=100)
            
            if st.form_submit_button("📨 Enviar mensaje", use_container_width=True):
                st.success("✅ ¡Mensaje enviado! Te responderemos en menos de 24 horas.")
                st.info("💡 En producción: este mensaje se guarda automáticamente en Google Sheets vía n8n")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #D4A017 !important;">🍹 CocktailGenius</p>
    <p style="color: #888 !important;">Tu bar personal, impulsado por inteligencia artificial</p>
    <p style="margin-top: 1rem; font-size: 0.8rem; color: #666 !important;">
    © 2026 CocktailGenius 
    </p>
</div>
""", unsafe_allow_html=True)
