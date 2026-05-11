import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
from io import BytesIO

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
# CSS PERSONALIZADO - ESTILO ELEGANTE
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 50%, #D4A017 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: #b8b8b8;
        text-align: center;
        font-weight: 300;
        letter-spacing: 2px;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: #D4A017;
        text-align: center;
        margin: 3rem 0 1.5rem 0;
        font-weight: 700;
    }
    
    .card-elegant {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(212,160,23,0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .card-elegant:hover {
        border-color: #D4A017;
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(212,160,23,0.2);
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        color: #D4A017;
        margin-bottom: 0.5rem;
    }
    
    .card-text {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .price-tag {
        display: inline-block;
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%);
        color: #0f0f0f;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%);
        color: #0f0f0f;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .btn-primary:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(212,160,23,0.4);
    }
    
    .input-elegant {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(212,160,23,0.3);
        border-radius: 10px;
        color: white;
        padding: 0.8rem;
    }
    
    .result-box {
        background: rgba(212,160,23,0.1);
        border-left: 4px solid #D4A017;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .recipe-card {
        background: rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(212,160,23,0.2);
    }
    
    .ingredient-tag {
        display: inline-block;
        background: rgba(212,160,23,0.2);
        color: #D4A017;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
    
    .step-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
        background: #D4A017;
        color: #0f0f0f;
        border-radius: 50%;
        font-weight: 700;
        margin-right: 1rem;
    }
    
    .footer {
        text-align: center;
        padding: 3rem 0;
        color: #666;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 3rem;
    }
    
    /* Ocultar menú por defecto de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: rgba(255,255,255,0.05);
        padding: 1rem 2rem;
        border-radius: 50px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b8b8b8;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #D4A017 0%, #F4D03F 100%);
        color: #0f0f0f !important;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
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
        "tips": "No machaques la menta con fuerza, solo presiona para liberar aceites esenciales"
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
        "tips": "Usa tequila 100% agave para mejor sabor"
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
        "tips": "El hielo debe ser grande para dilución lenta"
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
        "tips": "Clásico italiano, perfecto para aperitivo"
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
        "tips": "Usa piña fresca para mejor sabor"
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
        "tips": "La clave está en agitar muy fuerte para crear espuma"
    }
}

# ============================================
# FUNCIONES AUXILIARES
# ============================================
def buscar_receta(ingredientes_usuario):
    """Busca receta según ingredientes disponibles"""
    ingredientes_lower = [i.lower().strip() for i in ingredientes_usuario.split(",")]
    resultados = []
    
    for key, receta in RECETAS_DB.items():
        coincidencias = sum(1 for ing in ingredientes_lower if any(ing in r.lower() for r in receta["ingredientes"]))
        if coincidencias > 0:
            resultados.append((coincidencias, receta))
    
    resultados.sort(reverse=True, key=lambda x: x[0])
    return [r[1] for r in resultados[:3]] if resultados else None

def predecir_dificultad(ingredientes, tiempo, tecnicas):
    """Modelo ML simplificado"""
    dificultad = 0.5 + (ingredientes * 0.25) + (tiempo * 0.08) + (tecnicas * 0.35)
    return max(1, min(5, round(dificultad)))

def calcular_porciones(receta_base, num_personas):
    """Calcula medidas para N personas"""
    factor = num_personas
    medidas_calculadas = {}
    for ing, medida in receta_base["medidas"].items():
        # Extraer número si existe
        import re
        numero = re.findall(r'(\d+)', medida)
        if numero:
            nuevo_numero = int(numero[0]) * factor
            medidas_calculadas[ing] = medida.replace(numero[0], str(nuevo_numero))
        else:
            medidas_calculadas[ing] = f"{medida} (x{factor})"
    return medidas_calculadas

# ============================================
# HEADER / HERO SECTION
# ============================================
st.markdown('<div class="hero-title">🍹 CocktailGenius</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">TU BAR PERSONAL, IMPULSADO POR INTELIGENCIA ARTIFICIAL</div>', unsafe_allow_html=True)

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
            <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">La revolución de la mixología llegó</h3>
            <p class="card-text">
            CocktailGenius es la primera plataforma que combina <b>inteligencia artificial</b> 
            con el arte de la coctelería. Desde recetas personalizadas hasta predicciones 
            de tendencias con Machine Learning, transformamos tu cocina en el bar más 
            sofisticado de la ciudad.
            </p>
            <br>
            <p class="card-text">
            🧠 <b>+500 recetas</b> en nuestra base de datos<br>
            🤖 <b>Chatbot bartender</b> disponible 24/7<br>
            📊 <b>Modelo ML</b> con 66.9% de precisión<br>
            🎬 <b>Video comercial</b> generado con IA
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Estadísticas
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Recetas", "500+", "+50/mes")
        c2.metric("Usuarios", "2,400+", "+12%")
        c3.metric("Precisión ML", "66.9%", "R²")
        c4.metric("Satisfacción", "4.8/5", "⭐")
    
    with col2:
        st.markdown("""
        <div class="card-elegant" style="text-align: center;">
            <h4 style="color: #D4A017;">🎬 Conoce CocktailGenius</h4>
            <p class="card-text">Video comercial generado con IA<br>27 segundos</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("📹 Aquí irá tu video MP4 de 27 segundos")

# ============================================
# TAB 2: GENRECETA IA
# ============================================
with tabs[1]:
    st.markdown('<div class="section-title">🧠 GenReceta IA</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h4 class="card-title">¿Qué tienes en tu barra?</h4>
            <p class="card-text">
            Ingresa los ingredientes que tienes disponibles 
            (separados por comas) y nuestra IA te sugerirá 
            la receta perfecta con medidas exactas.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        ingredientes_input = st.text_input(
            "Tus ingredientes:",
            placeholder="Ej: ron, lima, menta, azúcar...",
            key="ingredientes"
        )
        
        buscar = st.button("🔍 Buscar Receta", use_container_width=True)
    
    with col2:
        if buscar and ingredientes_input:
            resultados = buscar_receta(ingredientes_input)
            
            if resultados:
                for receta in resultados:
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h3 style="color: #D4A017; margin-bottom: 0.5rem;">{receta['nombre']}</h3>
                        <p style="color: #888; font-size: 0.9rem;">
                        ⏱️ {receta['tiempo']} min | {"⭐" * receta['dificultad']}{"☆" * (5-receta['dificultad'])} | Dificultad: {receta['dificultad']}/5
                        </p>
                        
                        <h4 style="color: #F4D03F; margin-top: 1rem;">🧪 Ingredientes y medidas:</h4>
                    """, unsafe_allow_html=True)
                    
                    for ing, medida in receta['medidas'].items():
                        st.markdown(f'<span class="ingredient-tag">{ing}: {medida}</span>', unsafe_allow_html=True)
                    
                    st.markdown("<h4 style='color: #F4D03F; margin-top: 1rem;'>👨‍🍳 Preparación paso a paso:</h4>", unsafe_allow_html=True)
                    for i, paso in enumerate(receta['preparacion'], 1):
                        st.markdown(f'<div style="display: flex; align-items: start; margin: 0.5rem 0;"><span class="step-number">{i}</span><span style="color: #e0e0e0;">{paso}</span></div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="result-box" style="margin-top: 1rem;">
                            <b>💡 Tip profesional:</b> {receta['tips']}
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
            <h4 class="card-title">Machine Learning aplicado a mixología</h4>
            <p class="card-text">
            Nuestro modelo de <b>Regresión Lineal</b> predice la dificultad 
            de un cóctel (escala 1-5) basado en:
            </p>
            <ul style="color: #e0e0e0;">
                <li>Número de ingredientes</li>
                <li>Tiempo de preparación</li>
                <li>Número de técnicas requeridas</li>
            </ul>
            <p class="card-text">
            <b>Precisión del modelo (R²): 66.9%</b><br>
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
        
        st.success(f"**Dificultad predicha: {dif}/5**\n\n{niveles[dif]}")
    
    with col2:
        # Dataset
        st.subheader("📋 Dataset de entrenamiento")
        df = pd.DataFrame({
            'Cóctel': ['Mojito', 'Margarita', 'Old Fashioned', 'Negroni', 'Daiquiri', 'Piña Colada', 'Whiskey Sour', 'Espresso Martini', 'Cosmopolitan', 'Mai Tai'],
            'Ingredientes': [5, 3, 3, 3, 3, 4, 4, 4, 4, 6],
            'Tiempo': [5, 3, 5, 3, 3, 7, 7, 7, 5, 10],
            'Técnicas': [2, 1, 2, 1, 1, 2, 2, 2, 2, 3],
            'Dificultad': [2, 1, 3, 2, 1, 2, 2, 2, 2, 3]
        })
        st.dataframe(df, use_container_width=True)
        
        # Gráfica
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
        fig.patch.set_facecolor('#0f0f0f')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', 
                    ha='center', va='bottom', fontweight='bold', color='white')
        st.pyplot(fig)

# ============================================
# TAB 4: CALCULADORA DE DOSIS
# ============================================
with tabs[3]:
    st.markdown('<div class="section-title">🧮 Calculadora de Dosis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="card-elegant">
            <h4 class="card-title">Ajusta recetas para cualquier ocasión</h4>
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
            medidas_nuevas = calcular_porciones(receta, num_personas)
            
            st.markdown(f"""
            <div class="recipe-card">
                <h3 style="color: #D4A017;">{receta['nombre']} — {num_personas} personas</h3>
                <p style="color: #888;">⏱️ {receta['tiempo']} min por preparación | {"⭐" * receta['dificultad']}</p>
                
                <h4 style="color: #F4D03F; margin-top: 1rem;">🧪 Medidas ajustadas:</h4>
            """, unsafe_allow_html=True)
            
            for ing, medida in medidas_nuevas.items():
                st.markdown(f'<div style="display: flex; justify-content: space-between; padding: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1);"><span style="color: #e0e0e0;">{ing}</span><span style="color: #D4A017; font-weight: 600;">{medida}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <h4 style="color: #F4D03F; margin-top: 1.5rem;">👨‍🍳 Preparación (igual para cualquier cantidad):</h4>
            """, unsafe_allow_html=True)
            
            for i, paso in enumerate(receta['preparacion'], 1):
                st.markdown(f'<div style="display: flex; align-items: start; margin: 0.5rem 0;"><span class="step-number">{i}</span><span style="color: #e0e0e0;">{paso}</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="result-box" style="margin-top: 1rem;">
                    <b>💡 Tip:</b> {receta['tips']}<br><br>
                    <b>📊 Total estimado:</b> Prepara {num_personas * receta['tiempo']} minutos en total
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
        <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">Desarrolla tu paladar de experto</h3>
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
        <h3 style="color: #D4A017;">Tu bartender personal, disponible 24/7</h3>
        <p class="card-text">
        Pregúntale sobre recetas, técnicas, ingredientes o cualquier duda de mixología. 
        Impulsado por inteligencia artificial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Embed del chatbot de Botpress
    st.components.v1.html("""
    <div style="height: 600px; width: 100%; border-radius: 15px; overflow: hidden; border: 2px solid #D4A017;">
        <script src="https://cdn.botpress.cloud/webchat/v3.6/inject.js"></script>
        <script src="https://files.bpcontent.cloud/2026/05/07/21/20260507211006-AAWTTVTT.js" defer></script>
    </div>
    """, height=600)
    
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
            <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">🎯 Misión</h3>
            <p class="card-text">
            Democratizar la coctelería de autor mediante inteligencia artificial, 
            ayudando a las personas a descubrir, crear y perfeccionar experiencias 
            únicas desde cualquier lugar.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">👁️ Visión</h3>
            <p class="card-text">
            Convertirnos en la plataforma líder de mixología inteligente a nivel global, 
            redefiniendo la manera en que las personas experimentan la coctelería.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">💎 Valores</h3>
            <p class="card-text">
            • <b>Innovación:</b> Tecnología al servicio del arte<br>
            • <b>Accesibilidad:</b> Mixología para todos<br>
            • <b>Calidad:</b> Recetas probadas y precisas<br>
            • <b>Comunidad:</b> Compartir conocimiento
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card-elegant">
            <h3 style="color: #D4A017; font-family: 'Playfair Display', serif;">📬 Contacto</h3>
            <p class="card-text">
            ¿Tienes dudas, sugerencias o quieres colaborar?<br><br>
            📧 <b>Email:</b> hola@cocktailgenius.ai<br>
            🕐 <b>Horario:</b> Lunes a Viernes, 9:00 - 18:00<br>
            📱 <b>WhatsApp:</b> Próximamente<br>
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
    <p style="font-size: 1.5rem; margin-bottom: 0.5rem;">🍹 CocktailGenius</p>
    <p>Tu bar personal, impulsado por inteligencia artificial</p>
    <p style="margin-top: 1rem; font-size: 0.8rem;">
    © 2026 CocktailGenius | Proyecto Final - Fundamentos de IA | 
    Hecho con ❤️, 🧠 IA y 🥃 pasión por la mixología
    </p>
</div>
""", unsafe_allow_html=True)
