import streamlit as st
from PIL import Image
import time
from dotenv import load_dotenv
load_dotenv()

import os
from utils import run_excecuter
from openai import OpenAI

# Crear cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

# Configuración de página
st.set_page_config(
    page_title="AI Sales Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Minimalista y Moderno
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Variables */
    :root {
        --bg-primary: #fafafa;
        --bg-secondary: #ffffff;
        --text-primary: #1a1a1a;
        --text-secondary: #6b7280;
        --accent: #4f46e5;
        --accent-light: #eef2ff;
        --border: #e5e7eb;
        --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Reset base */
    .main {
        background-color: var(--bg-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        padding: 2rem 1rem;
    }
    
    /* Header minimalista */
    .header {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .header h1 {
        font-size: 1.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 0.5rem 0;
    }
    
    .header p {
        color: var(--text-secondary);
        font-size: 1rem;
        margin: 0;
        font-weight: 400;
    }
    
    .header .logo {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar limpio */
    .css-1d391kg {
        background-color: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    .sidebar-section {
        background: var(--bg-secondary);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .sidebar-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .sidebar-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .sidebar-item strong {
        color: var(--text-primary);
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background: #10b981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 0.5rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        margin: 1rem 0 !important;
        box-shadow: var(--shadow) !important;
        padding: 1rem !important;
    }
    
    .stChatMessage[data-testid="chat-message-user"] {
        background: var(--accent-light) !important;
        border-color: var(--accent) !important;
        border-width: 1px !important;
    }
    
    .stChatMessage[data-testid="chat-message-assistant"] {
        background: var(--bg-secondary) !important;
    }
    
    /* Input de chat */
    .stChatInputContainer {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 24px !important;
        box-shadow: var(--shadow) !important;
    }
    
    .stChatInputContainer input {
        background: transparent !important;
        border: none !important;
        color: var(--text-primary) !important;
        font-size: 0.975rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stChatInputContainer input::placeholder {
        color: var(--text-secondary) !important;
    }
    
    /* Botones minimalistas */
    .stButton > button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow) !important;
    }
    
    .stButton > button:hover {
        background: #4338ca !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Spinner limpio */
    .stSpinner > div {
        border-color: var(--accent) !important;
    }
    
    /* Toast notifications */
    .stToast {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Título principal */
    .main-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Responsivo */
    @media (max-width: 768px) {
        .main {
            padding: 1rem 0.5rem;
        }
        .header h1 {
            font-size: 1.5rem;
        }
    }

    /* Ocultar SOLO Print y Record a Screencast del Main Menu */
    ul[role="menu"] > li:nth-child(3),  /* Print */
    ul[role="menu"] > li:nth-child(4)   /* Record a screencast */ {
        display: none !important;
    }

    </style>
""", unsafe_allow_html=True)


# Sidebar minimalista
with st.sidebar:
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-title">⚙️ Configuración</div>
            <div class="sidebar-item">
                <span>Versión</span>
                <strong>v4.0</strong>
            </div>
            <div class="sidebar-item">
                <span>Desarrollador</span>
                <strong>Eduardo Portaro</strong>
            </div>
            <div class="sidebar-item">
                <span>Curso</span>
                <strong>AI Engineer</strong>
            </div>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">📊 Estado</div>
            <div class="sidebar-item">
                <span><span class="status-dot"></span>API</span>
                <strong>Conectada</strong>
            </div>
            <div class="sidebar-item">
                <span><span class="status-dot"></span>Asistente</span>
                <strong>Activo</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Header principal limpio
st.markdown("""
    <div class="header">
        <div class="logo">🤖</div>
        <h1>Asistente de Ventas IA</h1>
        <p>Potenciado por OpenAI • Desarrollado por Eduardo Portaro</p>
    </div>
""", unsafe_allow_html=True)

# Título de la sección de chat
st.markdown('<h2 class="main-title">💬 Chat Inteligente</h2>', unsafe_allow_html=True)

# Inicializar historial de chat
if "thread_id" not in st.session_state:
    st.session_state.thread_id = client.beta.threads.create().id
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Efecto de escritura simple
def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text + " ●")
        time.sleep(1 / speed)
    container.markdown(curr_full_text)

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    # Guardar mensaje usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensaje usuario
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Enviar mensaje a OpenAI
    message_box = client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id, role="user", content=prompt
    )

    # Ejecutar Run
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # Spinner mientras responde
    with st.spinner('Procesando respuesta...'):
        st.toast('Mensaje recibido', icon='✅')

        # Ejecutar asistente
        run_excecuter(run)

        # Obtener última respuesta
        message_assistant = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        ).data[0].content[0].text.value

    # Mostrar respuesta
    with st.chat_message("assistant", avatar="🤖"):
        typewriter(message_assistant, 50)

    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": message_assistant})