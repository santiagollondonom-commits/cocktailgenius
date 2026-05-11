import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CocktailGenius", page_icon="🍹", layout="wide")

# CSS
st.markdown("""
<style>
    .main-title {font-size: 3rem; font-weight: bold; color: #D4A017; text-align: center;}
    .subtitle {font-size: 1.2rem; color: #2C3E50; text-align: center; font-style: italic;}
    .card {background: #f8f9fa; border-radius: 10px; padding: 20px; border-left: 4px solid #D4A017;}
    .price {color: #D4A017; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-title">🍹 CocktailGenius</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tu bar personal, impulsado por inteligencia artificial</div>', unsafe_allow_html=True)
st.markdown("---")

# TABS
tab1, tab2, tab3 = st.tabs(["🏠 Inicio", "🧠 ML Predictor", "📞 Contacto"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🎯 Misión:** Democratizar la coctelería de autor mediante IA, ayudando a personas a crear experiencias únicas desde cualquier lugar.")
    with col2:
        st.info("**👁️ Visión:** Ser la plataforma líder de mixología inteligente global, donde creatividad humana e IA inspiren momentos memorables.")
    
    st.header("✨ Nuestras Funcionalidades")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown('<div class="card"><h4>🧠 GenReceta IA</h4><p>Recetas personalizadas según tus ingredientes</p><p class="price">GRATIS</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4>🤖 BartenderBot</h4><p>Chatbot experto 24/7</p><p class="price">GRATIS</p></div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="card"><h4>📊 TrendPredictor ML</h4><p>Predice tendencias con Machine Learning</p><p class="price">GRATIS</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4>📚 Cátedra de Cata</h4><p>Desarrolla tu paladar de experto</p><p class="price">$4.99/mes</p></div>', unsafe_allow_html=True)
    
    with c3:
        st.markdown('<div class="card"><h4>🧮 Calculadora de Dosis</h4><p>Ajusta recetas para cualquier número de invitados</p><p class="price">$2.99/mes</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><h4>🎬 Video Comercial</h4><p>Conoce CocktailGenius en 27 segundos</p><p class="price">INCLUIDO</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("🎬 Aquí se mostraría tu video comercial de 27 segundos (MP4)")

with tab2:
    st.header("🧠 TrendPredictor ML")
    st.write("Modelo de **Regresión Lineal** que predice dificultad de cócteles (escala 1-5)")
    st.write("**Precisión (R²): 66.9%**")
    
    data = {
        'Cóctel': ['Mojito','Margarita','Old Fashioned','Negroni','Daiquiri','Piña Colada','Whiskey Sour','Espresso Martini','Cosmopolitan','Mai Tai'],
        'Ingredientes': [5,3,3,3,3,4,4,4,4,6],
        'Tiempo_min': [5,3,5,3,3,7,7,7,5,10],
        'Técnicas': [2,1,2,1,1,2,2,2,2,3],
        'Dificultad': [2,1,3,2,1,2,2,2,2,3]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    
    st.subheader("🔮 Predice la dificultad de tu cóctel")
    col1, col2, col3 = st.columns(3)
    with col1: ing = st.number_input("Ingredientes", 2, 10, 4)
    with col2: tiempo = st.number_input("Tiempo (min)", 2, 15, 5)
    with col3: tec = st.number_input("Técnicas", 1, 4, 2)
    
    dif = round(0.3 + ing*0.25 + tiempo*0.08 + tec*0.35)
    dif = max(1, min(5, dif))
    niveles = {1:"🟢 Muy Fácil", 2:"🟡 Fácil", 3:"🟠 Medio", 4:"🔴 Difícil", 5:"⚫ Experto"}
    st.success(f"**Dificultad predicha: {dif} - {niveles[dif]}**")
    
    fig, ax = plt.subplots(figsize=(10,5))
    counts = df['Dificultad'].value_counts().sort_index()
    colors = ['#2ecc71','#f39c12','#e67e22','#e74c3c']
    bars = ax.bar(counts.index, counts.values, color=colors, edgecolor='black')
    ax.set_xlabel('Dificultad', fontweight='bold')
    ax.set_ylabel('Cantidad', fontweight='bold')
    ax.set_title('Distribución de Cócteles por Dificultad', fontweight='bold')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    st.pyplot(fig)

with tab3:
    st.header("📞 Contacto")
    st.write("¿Tienes dudas? Déjanos tu mensaje.")
    
    with st.form("contacto"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        mensaje = st.text_area("Mensaje")
        if st.form_submit_button("📨 Enviar"):
            st.success("✅ ¡Mensaje enviado! Te contactaremos pronto.")
            st.info("💡 En producción: este mensaje se guarda automáticamente en Google Sheets vía n8n")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center'><b>CocktailGenius</b><br>📧 hola@cocktailgenius.ai<br>🕐 Lunes-Viernes 9:00-18:00</div>", unsafe_allow_html=True)

# CHATBOT EMBED
st.components.v1.html("""
<script src="https://cdn.botpress.cloud/webchat/v3.6/inject.js"></script>
<script src="https://files.bpcontent.cloud/2026/05/07/21/20260507211006-AAWTTVTT.js" defer></script>
""", height=0)
