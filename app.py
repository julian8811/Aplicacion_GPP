"""
Aplicación de Evaluación de Gestión Por Procesos (GPP)
Convierte la herramienta de Excel en una aplicación web interactiva
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Evaluación GPP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS profesionales y modernos - Diseño 'Stitch Modern UI Redesign'
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --primary: #0058be;
        --primary-container: #2170e4;
        --secondary: #545f73;
        --tertiary: #b81120;
        --bg-main: #f7f9fb;
        --bg-card: #ffffff;
        --text-base: #191c1e;
        --text-muted: #424754;
        --border-color: #e0e3e5;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ba1a1a;
        --font-main: 'Inter', sans-serif;
        --shadow-sm: 0px 4px 12px rgba(30, 41, 59, 0.05);
        --shadow-md: 0px 10px 25px rgba(30, 41, 59, 0.1);
    }

    /* Global Streamlit Overrides */
    .stApp {
        background-color: var(--bg-main);
        font-family: var(--font-main);
        color: var(--text-base);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

    /* Typography */
    h1, h2, h3, h4 {
        font-family: var(--font-main) !important;
        color: var(--text-base) !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em;
    }

    .title-modern {
        font-family: var(--font-main);
        color: var(--text-base);
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.02em;
    }

    /* Modern Cards (Bento Style) */
    .modern-card {
        background: var(--bg-card);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .modern-card:hover {
        box-shadow: var(--shadow-md);
    }

    .metric-card-modern {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
        text-align: left;
    }

    .metric-value-modern {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-base);
        line-height: 1.2;
    }

    .metric-label-modern {
        color: var(--text-muted);
        font-weight: 500;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 0.75rem !important;
        border: none !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
        box-shadow: 0 4px 6px -1px rgba(0, 88, 190, 0.2);
    }

    .stButton > button:hover {
        background-color: var(--primary-container) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 88, 190, 0.3) !important;
    }

    /* Tabs/Expanders */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        gap: 12px !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px !important;
        border-radius: 0.75rem !important;
        border: 1px solid var(--border-color) !important;
        background-color: white !important;
        color: var(--text-muted) !important;
        padding: 0 1.5rem !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }

    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        border-radius: 0.75rem !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Header Nav Simulation */
    .nav-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem;
    }

    .logo-text {
        font-weight: 900;
        letter-spacing: -0.03em;
        font-size: 1.25rem;
        color: #0f172a;
    }

    /* Banner */
    .banner-modern {
        background: white;
        color: var(--text-base);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }

    /* Footer */
    .footer-modern {
        margin-top: 5rem;
        padding: 3rem 0;
        border-top: 1px solid var(--border-color);
        text-align: center;
        font-size: 0.8rem;
        color: var(--text-muted);
    }

    </style>
    """, unsafe_allow_html=True)

# Definición de las matrices de evaluación
MATRIZ_PA = {
    "PLANEACIÓN": {
        "Análisis del contexto": [
            "¿La empresa realiza un análisis externo como base para su planeación estratégica?",
            "¿La empresa realiza un análisis interno como base para su planeación estratégica?",
            "Aplicación de herramientas de análisis como la matriz DOFA, PESTEL, Las 5 Fuerzas de Porter, Benchmarking, entre otras"
        ],
        "Existencia de un plan estratégico": [
            "En qué medida considera que la misión de la empresa está claramente definida y comunicada a todos los miembros de la organización",
            "En qué medida considera que la visión de la empresa está claramente definida y comunicada a todos los miembros de la organización",
            "En qué medida considera que el establecimiento tiene definidos y comunicados sus objetivos estratégicos",
            "Documento que evidencie el plan estratégico a largo o mediano plazo"
        ]
    },
    "ORGANIZACIÓN": {
        "Existencia de una estructura organizativa": [
            "¿El establecimiento cuenta con un organigrama claramente definido?"
        ],
        "Departamentalización": [
            "¿Se tienen claramente identificados los procesos de la organización?"
        ],
        "Procesos documentados": [
            "¿Existen perfiles de cargo definidos para cada función?",
            "¿El establecimiento tiene debidamente documentado cada proceso (mapas de proceso, flujogramas, procedimientos, normas, etc)?",
            "¿El establecimiento tiene caracterizado los procesos?"
        ],
        "Ciclo PHVA": [
            "¿Tiene implementado el ciclo PHVA (Planear, Hacer, Verificar, Actuar) en el establecimiento?"
        ]
    },
    "DIRECCIÓN": {
        "Liderazgo organizacional": [
            "¿Existen líderes proactivos y motivadores en el establecimiento?"
        ],
        "Canales de comunicación efectivos": [
            "¿Existe un sistema de comunicación formal (vertical y horizontal) que permita el flujo de información en la organización?"
        ],
        "Cultura organizacional": [
            "¿Se fomenta el trabajo en equipo y la participación del personal en la toma de decisiones?",
            "¿Se promueve la innovación y la mejora continua en los procesos?",
            "¿Se reconocen los logros y se incentiva el buen desempeño del personal?",
            "¿Se cuenta con un código de ética o valores organizacionales claramente definidos y comunicados?",
            "¿Existe un sentido de pertenencia del personal hacia la organización?"
        ]
    },
    "CONTROL": {
        "Sistemas de control": [
            "¿Se realiza seguimiento periódico al cumplimiento de los objetivos estratégicos?",
            "¿Se utilizan indicadores de gestión para medir el desempeño de los procesos?"
        ],
        "Auditorías internas": [
            "¿Se realizan auditorías internas de forma periódica para evaluar el cumplimiento de los procesos?"
        ],
        "Acciones correctivas y preventivas": [
            "¿Existe un procedimiento establecido para implementar acciones correctivas cuando se detectan desviaciones?",
            "¿Se implementan acciones preventivas para evitar problemas antes de que ocurran?"
        ]
    }
}

MATRIZ_PO = {
    "LOGÍSTICA DE COMPRAS": {
        "Logística de entrada": [
            "¿La planeación de compras en el establecimiento se realiza de manera organizada, considerando la periodicidad, la gestión de proveedores, las cantidades requeridas y el estado de los inventarios?",
            "¿Se utilizan herramientas de control como formatos, bases de datos o software para la gestión?",
            "¿El establecimiento dispone de condiciones adecuadas de almacenamiento (frío o caliente) según el tipo de producto?"
        ],
        "Gestión de inventarios": [
            "¿Se encuentra implementado un sistema de inventario (PEPS, ABC u otro)?",
            "¿El inventario está automatizado en un software de gestión?"
        ]
    },
    "GESTIÓN DE PRODUCCIÓN": {
        "Equipos": [
            "¿Los equipos e instalaciones son adecuados para el volumen de producción requerido?",
            "¿Se realizan actividades de mantenimiento correctivo, preventivo y de mejora en los equipos e instalaciones?"
        ],
        "Infraestructura": [
            "¿El establecimiento cuenta con un sistema de ventilación y control de humos eficiente?",
            "¿El diseño y distribución de la cocina favorecen un trabajo ordenado y funcional?",
            "¿La iluminación y ventilación de las áreas de trabajo son adecuadas?"
        ],
        "Distribución de los procesos (flujo)": [
            "¿Cada área de trabajo (emplatado, preparación, cocción, limpieza, ubicación de utensilios, etc.) está claramente identificada?",
            "¿El flujo de trabajo en la cocina es lógico y eficiente?"
        ],
        "Planeación de la producción": [
            "¿Se planea adecuadamente los niveles de producción para atender la demanda?",
            "¿Se cuenta con recetas estandarizadas que garanticen la calidad y consistencia de los productos?",
            "¿Se realiza un control de tiempos de preparación y cocción?",
            "¿Se optimiza el uso de los recursos disponibles (tiempo, personal, equipos)?",
            "¿Se tienen definidos procedimientos para el manejo de desperdicios y mermas?"
        ],
        "Materia prima": [
            "¿Las materias primas utilizadas cumplen con estándares de calidad?",
            "¿Se verifica la calidad de las materias primas al momento de recibirlas?"
        ],
        "Control de la producción": [
            "¿Se realiza control de calidad durante el proceso de producción?",
            "¿Se registran y analizan los datos de producción (cantidades, tiempos, costos)?",
            "¿Se implementan acciones de mejora basadas en los datos de producción?"
        ]
    },
    "LOGÍSTICA EXTERNA": {
        "Distribución": [
            "¿El servicio al cliente es ágil y eficiente?",
            "¿Se cuenta con personal capacitado para atender al cliente?",
            "¿Se realiza seguimiento a la satisfacción del cliente?",
            "¿Se gestionan adecuadamente las quejas y reclamos?",
            "¿Se implementan mejoras basadas en la retroalimentación de los clientes?"
        ]
    }
}

# Pesos relativos por elemento (%)
PESOS_PA = {
    "PLANEACIÓN": {
        "Análisis del contexto": 53.75,
        "Existencia de un plan estratégico": 46.25
    },
    "ORGANIZACIÓN": {
        "Existencia de una estructura organizativa": 11.25,
        "Departamentalización": 35.0,
        "Procesos documentados": 33.75,
        "Ciclo PHVA": 20.0
    },
    "DIRECCIÓN": {
        "Liderazgo organizacional": 35.0,
        "Canales de comunicación efectivos": 30.0,
        "Cultura organizacional": 35.0
    },
    "CONTROL": {
        "Sistemas de control": 45.0,
        "Auditorías internas": 25.0,
        "Acciones correctivas y preventivas": 30.0
    }
}

PESOS_PO = {
    "LOGÍSTICA DE COMPRAS": {
        "Logística de entrada": 60.0,
        "Gestión de inventarios": 40.0
    },
    "GESTIÓN DE PRODUCCIÓN": {
        "Equipos": 15.0,
        "Infraestructura": 15.0,
        "Distribución de los procesos (flujo)": 10.0,
        "Planeación de la producción": 25.0,
        "Materia prima": 15.0,
        "Control de la producción": 20.0
    },
    "LOGÍSTICA EXTERNA": {
        "Distribución": 100.0
    }
}

# Funciones auxiliares
def calcular_prioridad(porcentaje):
    """Determina la prioridad según el porcentaje de cumplimiento"""
    if porcentaje >= 75:
        return "BAJA", "success"
    elif porcentaje >= 60:
        return "MEDIA", "warning"
    else:
        return "ALTA", "error"

def calcular_cumplimiento_elemento(calificaciones):
    """Calcula el promedio de calificaciones para un elemento"""
    if not calificaciones:
        return 0
    return np.mean(calificaciones)

def calcular_porcentaje_cumplimiento(promedio):
    """Convierte promedio de 1-5 a porcentaje"""
    return (promedio / 5) * 100

def inicializar_session_state():
    """Inicializa las variables de estado de la sesión"""
    if 'evaluaciones_pa' not in st.session_state:
        st.session_state.evaluaciones_pa = {}
    if 'evaluaciones_po' not in st.session_state:
        st.session_state.evaluaciones_po = {}
    if 'resultados_calculados' not in st.session_state:
        st.session_state.resultados_calculados = False

def guardar_evaluacion():
    """Guarda la evaluación actual en un archivo JSON"""
    datos = {
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'evaluaciones_pa': st.session_state.evaluaciones_pa,
        'evaluaciones_po': st.session_state.evaluaciones_po
    }
    
    archivo = os.path.join(os.path.dirname(__file__), f"evaluacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    return archivo

def cargar_evaluacion(archivo):
    """Carga una evaluación desde un archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    st.session_state.evaluaciones_pa = datos.get('evaluaciones_pa', {})
    st.session_state.evaluaciones_po = datos.get('evaluaciones_po', {})
    st.session_state.resultados_calculados = True

# Función principal
def main():
    inicializar_session_state()
    
    # Header elegante estilo SaaS
    st.markdown('''
    <div class="nav-header">
        <div class="logo-text">GPP_CORE <span style="color: var(--text-muted); font-weight: 300;">/ AUDIT_SYSTEM</span></div>
        <div style="font-size: 0.75rem; color: var(--text-muted); font-weight: 600;">v2.5.0_STABLE</div>
    </div>
    <div class="title-modern">Evaluación de Gestión Por Procesos</div>
    ''', unsafe_allow_html=True)
    
    # Sidebar para navegación
    st.sidebar.title("📋 Navegación")
    pagina = st.sidebar.radio(
        "Seleccione una opción:",
        ["🏠 Inicio", "📝 Proceso Administrativo", "⚙️ Proceso Operativo", 
         "📊 Resultados Generales", "🎯 Prioridades", "💾 Guardar/Cargar"]
    )
    
    if pagina == "🏠 Inicio":
        mostrar_inicio()
    elif pagina == "📝 Proceso Administrativo":
        mostrar_evaluacion_pa()
    elif pagina == "⚙️ Proceso Operativo":
        mostrar_evaluacion_po()
    elif pagina == "📊 Resultados Generales":
        mostrar_resultados_generales()
    elif pagina == "🎯 Prioridades":
        mostrar_prioridades()
    elif pagina == "💾 Guardar/Cargar":
        mostrar_guardar_cargar()
    
    # Footer Moderno
    st.markdown("""
    <div class="footer-modern">
        <div style="font-weight: 700; color: #0f172a; margin-bottom: 0.5rem;">SISTEMA GPP • INTEL_CORE_SYSTEM</div>
        <div>Desarrollado para COLMAYOR | CEITTO © 2025</div>
        <div style="margin-top: 1rem; color: var(--primary); font-weight: 600;">ENTERPRISE_GRADE_INTERFACE</div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_inicio():
    """Muestra la página de inicio con instrucciones"""
    st.markdown("""
    <div class="banner-modern">
        <h1 style="color: white; margin-bottom: 0.5rem; border: none;">Bienvenido al Ecosistema GPP</h1>
        <p style="opacity: 0.9; font-size: 1.1rem;">Optimice la eficiencia operativa y administrativa a través de diagnósticos precisos y análisis de datos en tiempo real.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="modern-card">
            <h3 style="margin-top:0; color: var(--primary);">🚀 Guía de Operación</h3>
            <p style="color: var(--text-base);">Siga el flujo de trabajo establecido para garantizar la integridad de los datos:</p>
            <ul style="color: var(--text-base); line-height: 1.6;">
                <li><b>Diagnóstico</b>: Realice las evaluaciones en los módulos de Administración y Operación.</li>
                <li><b>Análisis</b>: Revise los tableros de control con métricas avanzadas.</li>
                <li><b>Estrategia</b>: Identifique prioridades críticas de intervención.</li>
                <li><b>Archivo</b>: Resguarde sus resultados en formatos estructurados.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Calcular progreso para el dashboard de inicio
        total_pa = sum(len(vars) for aspecto in MATRIZ_PA.values() for vars in aspecto.values())
        total_po = sum(len(vars) for aspecto in MATRIZ_PO.values() for vars in aspecto.values())
        total_preguntas = total_pa + total_po
        preguntas_respondidas = len(st.session_state.evaluaciones_pa) + len(st.session_state.evaluaciones_po)
        progreso = (preguntas_respondidas / total_preguntas) * 100 if total_preguntas > 0 else 0

        st.markdown(f"""
        <div class="modern-card">
            <h3 style="margin-top:0; color: var(--primary);">📊 Estado del Sistema</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="metric-card-modern">
                    <div class="metric-label-modern">PROGRESO</div>
                    <div class="metric-value-modern">{progreso:.1f}%</div>
                </div>
                <div class="metric-card-modern">
                    <div class="metric-label-modern">ENGINE</div>
                    <div class="metric-value-modern">v2.5</div>
                </div>
            </div>
            <div style="margin-top: 1.5rem;">
                <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 0.5rem;">Completado: {preguntas_respondidas} de {total_preguntas} variables</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Niveles de Cumplimiento")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="modern-card" style="border-top: 4px solid var(--error);">
            <div style="color: var(--error); font-weight: 700; margin-bottom: 0.5rem; font-size: 0.75rem; letter-spacing: 0.1em;">NIVEL_CRÍTICO</div>
            <h4 style="margin: 0 0 0.5rem 0;">Prioridad Alta</h4>
            <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 0;">Cumplimiento < 60%. Requiere intervención inmediata.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="modern-card" style="border-top: 4px solid var(--warning);">
            <div style="color: var(--warning); font-weight: 700; margin-bottom: 0.5rem; font-size: 0.75rem; letter-spacing: 0.1em;">NIVEL_ALERTA</div>
            <h4 style="margin: 0 0 0.5rem 0;">Prioridad Media</h4>
            <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 0;">Cumplimiento 60-74%. Planificar a corto plazo.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="modern-card" style="border-top: 4px solid var(--success);">
            <div style="color: var(--success); font-weight: 700; margin-bottom: 0.5rem; font-size: 0.75rem; letter-spacing: 0.1em;">NIVEL_ESTABLE</div>
            <h4 style="margin: 0 0 0.5rem 0;">Prioridad Baja</h4>
            <p style="font-size: 0.875rem; color: var(--text-muted); margin-bottom: 0;">Cumplimiento ≥ 75%. Mantener estándares.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(progreso / 100)

def mostrar_evaluacion_pa():
    """Muestra el formulario de evaluación del proceso administrativo"""
    st.markdown("<h3>Evaluación: Proceso Administrativo</h3>", unsafe_allow_html=True)
    
    st.info("Evalúe cada variable en una escala de 1 a 5, donde 1 = No cumple y 5 = Cumple plenamente")
    
    for aspecto, elementos in MATRIZ_PA.items():
        st.markdown(f"<h3 style='color: #172139; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>{aspecto}</h3>", unsafe_allow_html=True)
        
        for elemento, variables in elementos.items():
            with st.expander(f"📌 {elemento}", expanded=True):
                st.markdown(f"<strong style='color: #172139; font-weight: 700;'>{elemento}</strong>", unsafe_allow_html=True)
                
                for i, variable in enumerate(variables):
                    key = f"PA_{aspecto}_{elemento}_{i}"
                    
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"<small style='color: #172139; font-weight: 500;'>{variable}</small>", unsafe_allow_html=True)
                    
                    with col2:
                        valor = st.selectbox(
                            "Calificación",
                            options=[0, 1, 2, 3, 4, 5],
                            index=st.session_state.evaluaciones_pa.get(key, 0),
                            key=f"select_{key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.evaluaciones_pa[key] = valor
    
    if st.button("✅ Guardar Evaluación del Proceso Administrativo"):
        st.success("✓ Evaluación del Proceso Administrativo guardada correctamente")
        st.session_state.resultados_calculados = True

def mostrar_evaluacion_po():
    """Muestra el formulario de evaluación del proceso operativo"""
    st.markdown("<h3>Evaluación: Proceso Operativo</h3>", unsafe_allow_html=True)
    
    st.info("Evalúe cada variable en una escala de 1 a 5, donde 1 = No cumple y 5 = Cumple plenamente")
    
    for aspecto, elementos in MATRIZ_PO.items():
        st.markdown(f"<h3 style='color: #172139; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>{aspecto}</h3>", unsafe_allow_html=True)
        
        for elemento, variables in elementos.items():
            with st.expander(f"📌 {elemento}", expanded=True):
                st.markdown(f"<strong style='color: #172139; font-weight: 700;'>{elemento}</strong>", unsafe_allow_html=True)
                
                for i, variable in enumerate(variables):
                    key = f"PO_{aspecto}_{elemento}_{i}"
                    
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"<small style='color: #172139; font-weight: 500;'>{variable}</small>", unsafe_allow_html=True)
                    
                    with col2:
                        valor = st.selectbox(
                            "Calificación",
                            options=[0, 1, 2, 3, 4, 5],
                            index=st.session_state.evaluaciones_po.get(key, 0),
                            key=f"select_{key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.evaluaciones_po[key] = valor
    
    if st.button("✅ Guardar Evaluación del Proceso Operativo"):
        st.success("✓ Evaluación del Proceso Operativo guardada correctamente")
        st.session_state.resultados_calculados = True

def calcular_resultados():
    """Calcula todos los resultados de la evaluación"""
    resultados = {
        'pa': {},
        'po': {},
        'general': {}
    }
    
    # Calcular resultados del Proceso Administrativo
    for aspecto, elementos in MATRIZ_PA.items():
        resultados['pa'][aspecto] = {}
        calificaciones_aspecto = []
        
        for elemento, variables in elementos.items():
            calificaciones = []
            for i in range(len(variables)):
                key = f"PA_{aspecto}_{elemento}_{i}"
                if key in st.session_state.evaluaciones_pa:
                    cal = st.session_state.evaluaciones_pa[key]
                    if cal > 0:  # Solo considerar si se calificó
                        calificaciones.append(cal)
            
            if calificaciones:
                promedio = calcular_cumplimiento_elemento(calificaciones)
                porcentaje = calcular_porcentaje_cumplimiento(promedio)
                prioridad, tipo = calcular_prioridad(porcentaje)
                peso = PESOS_PA.get(aspecto, {}).get(elemento, 0)
                
                resultados['pa'][aspecto][elemento] = {
                    'promedio': promedio,
                    'porcentaje': porcentaje,
                    'prioridad': prioridad,
                    'tipo_prioridad': tipo,
                    'peso': peso,
                    'calificaciones': calificaciones
                }
                calificaciones_aspecto.append(promedio)
        
        if calificaciones_aspecto:
            resultados['pa'][aspecto]['promedio_aspecto'] = np.mean(calificaciones_aspecto)
            resultados['pa'][aspecto]['porcentaje_aspecto'] = calcular_porcentaje_cumplimiento(np.mean(calificaciones_aspecto))
    
    # Calcular resultados del Proceso Operativo
    for aspecto, elementos in MATRIZ_PO.items():
        resultados['po'][aspecto] = {}
        calificaciones_aspecto = []
        
        for elemento, variables in elementos.items():
            calificaciones = []
            for i in range(len(variables)):
                key = f"PO_{aspecto}_{elemento}_{i}"
                if key in st.session_state.evaluaciones_po:
                    cal = st.session_state.evaluaciones_po[key]
                    if cal > 0:
                        calificaciones.append(cal)
            
            if calificaciones:
                promedio = calcular_cumplimiento_elemento(calificaciones)
                porcentaje = calcular_porcentaje_cumplimiento(promedio)
                prioridad, tipo = calcular_prioridad(porcentaje)
                peso = PESOS_PO.get(aspecto, {}).get(elemento, 0)
                
                resultados['po'][aspecto][elemento] = {
                    'promedio': promedio,
                    'porcentaje': porcentaje,
                    'prioridad': prioridad,
                    'tipo_prioridad': tipo,
                    'peso': peso,
                    'calificaciones': calificaciones
                }
                calificaciones_aspecto.append(promedio)
        
        if calificaciones_aspecto:
            resultados['po'][aspecto]['promedio_aspecto'] = np.mean(calificaciones_aspecto)
            resultados['po'][aspecto]['porcentaje_aspecto'] = calcular_porcentaje_cumplimiento(np.mean(calificaciones_aspecto))
    
    # Calcular resultado general del establecimiento
    todos_promedios = []
    for aspecto_data in resultados['pa'].values():
        if 'promedio_aspecto' in aspecto_data:
            todos_promedios.append(aspecto_data['promedio_aspecto'])
    for aspecto_data in resultados['po'].values():
        if 'promedio_aspecto' in aspecto_data:
            todos_promedios.append(aspecto_data['promedio_aspecto'])
    
    if todos_promedios:
        resultados['general']['promedio'] = np.mean(todos_promedios)
        resultados['general']['porcentaje'] = calcular_porcentaje_cumplimiento(np.mean(todos_promedios))
    
    return resultados

def mostrar_resultados_generales():
    """Muestra los resultados generales con gráficos"""
    st.markdown("<h3>Reporte General de Resultados</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay evaluaciones registradas. Por favor complete al menos una evaluación.")
        return
    
    resultados = calcular_resultados()
    
    # Resultado general del establecimiento
    if 'porcentaje' in resultados['general']:
        st.markdown("<h4 class='subtitle-serif' style='font-size: 1.5rem; margin-top: 2rem;'>CORE_COMPLIANCE</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            porcentaje_general = resultados['general']['porcentaje']
            prioridad, tipo = calcular_prioridad(porcentaje_general)
            st.markdown(f"""
            <div class="metric-card-modern">
                <div class="metric-label-modern">Cumplimiento Global</div>
                <div class="metric-value-modern" style="color: var(--primary);">{porcentaje_general:.1f}%</div>
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; font-weight: 600;">ESTADO: {prioridad}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="modern-card" style="text-align: center; padding: 1.5rem;">
                <div class="metric-label-modern">Calificación Media</div>
                <div class="metric-value-modern" style="color: #1e293b;">{resultados['general']['promedio']:.2f}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; font-weight: 600;">ESCALA DE 1 A 5</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            nivel_color = {"ALTA": "var(--error)", "MEDIA": "var(--warning)", "BAJA": "var(--success)"}
            color = nivel_color.get(prioridad, "var(--text-base)")
            st.markdown(f"""
            <div class="modern-card" style="text-align: center; padding: 1.5rem; border-top: 4px solid {color};">
                <div class="metric-label-modern">Nivel de Prioridad</div>
                <div class="metric-value-modern" style="color: {color};">{prioridad}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; font-weight: 600;">INTERVENCIÓN REQUERIDA</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de progreso general con gauge Audit-style
    st.markdown("<h4 class='subtitle-serif' style='font-size: 1.2rem; margin-top: 3rem;'>GAUGE_ANALYSIS</h4>", unsafe_allow_html=True)
    
    if 'porcentaje' in resultados['general']:
        porcentaje_general = resultados['general']['porcentaje']
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=porcentaje_general,
            title={'text': "CUMPLIMIENTO GLOBAL", 'font': {'size': 18, 'family': 'Inter, sans-serif', 'color': '#1e293b'}},
            number={'suffix': "%", 'font': {'size': 60, 'family': 'Inter, sans-serif', 'color': '#4f46e5'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': "#4f46e5", 'thickness': 0.3},
                'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "#e2e8f0",
                'steps': [
                    {'range': [0, 60], 'color': '#fee2e2'},
                    {'range': [60, 75], 'color': '#fef3c7'},
                    {'range': [75, 100], 'color': '#ecfdf5'}
                ],
            }
        ))
        
        fig_gauge.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'family': 'Inter, sans-serif'},
            margin=dict(l=20, r=20, t=50, b=20)
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico de cumplimiento por área
    st.markdown("<h4 style='color: #172139; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>📈 Cumplimiento por Área</h4>", unsafe_allow_html=True)
    
    areas = []
    porcentajes = []
    colores = []
    
    for aspecto, data in resultados['pa'].items():
        if 'porcentaje_aspecto' in data:
            areas.append(f"PA: {aspecto}")
            porcentajes.append(data['porcentaje_aspecto'])
            _, tipo = calcular_prioridad(data['porcentaje_aspecto'])
            colores.append('#B4C42C' if tipo == 'success' else '#FBBB28' if tipo == 'warning' else '#E9901E')
    
    for aspecto, data in resultados['po'].items():
        if 'porcentaje_aspecto' in data:
            areas.append(f"PO: {aspecto}")
            porcentajes.append(data['porcentaje_aspecto'])
            _, tipo = calcular_prioridad(data['porcentaje_aspecto'])
            colores.append('#B4C42C' if tipo == 'success' else '#FBBB28' if tipo == 'warning' else '#E9901E')
    
    if areas:
        fig = go.Figure(data=[
            go.Bar(
                x=porcentajes,
                y=areas,
                orientation='h',
                marker=dict(
                    color='#4f46e5',
                    line=dict(color='white', width=1),
                ),
                text=[f"{p:.1f}%" for p in porcentajes],
                textposition='auto',
                textfont=dict(size=12, color='white', family='Inter, sans-serif'),
                hovertemplate='<b>%{y}</b><br>Cumplimiento: <b>%{x:.1f}%</b><extra></extra>',
            )
        ])
        
        fig.update_layout(
            title=dict(
                text="Cumplimiento por Área de Gestión",
                font=dict(size=18, family='Inter, sans-serif', color='#1e293b'),
                x=0,
                xanchor='left'
            ),
            xaxis=dict(
                title=dict(text="Porcentaje (%)", font=dict(size=12, family='Inter, sans-serif')),
                range=[0, 105],
                gridcolor='#f1f5f9',
                showgrid=True,
                zeroline=False,
                tickfont=dict(color='#64748b')
            ),
            yaxis=dict(
                gridcolor='#f1f5f9',
                tickfont=dict(color='#1e293b', family='Inter, sans-serif')
            ),
            height=300 + len(areas) * 35,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=80, b=40),
            font=dict(family='Inter, sans-serif', color='#1e293b'),
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Inter, sans-serif",
                font_color="#1e293b",
                bordercolor="#4f46e5"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Gráfico radial comparativo
    st.markdown("<h4 style='color: #172139; font-weight: 700; text-shadow: 0 1px 2px rgba(0,0,0,0.1);'>🎯 Análisis Comparativo Multidimensional</h4>", unsafe_allow_html=True)
    
    if areas:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[100] * len(areas),
            theta=areas,
            fill='toself',
            name='Ideal',
            line=dict(color='#94a3b8', width=1, dash='dot'),
            fillcolor='rgba(148, 163, 184, 0.05)',
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=porcentajes,
            theta=areas,
            fill='toself',
            name='Actual',
            line=dict(color='#4f46e5', width=3),
            fillcolor='rgba(79, 70, 229, 0.15)',
            marker=dict(size=10, color='#4f46e5', line=dict(color='white', width=2)),
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='white',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor='#f1f5f9',
                    tickfont=dict(size=10, color='#64748b'),
                    ticksuffix='%'
                ),
                angularaxis=dict(
                    gridcolor='#f1f5f9',
                    tickfont=dict(size=11, color='#1e293b', family='Inter, sans-serif'),
                )
            ),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                bgcolor='white',
                bordercolor='#e2e8f0',
                font=dict(size=11, color='#1e293b')
            ),
            title=dict(
                text="Análisis Radar Multidimensional",
                font=dict(size=18, family='Inter, sans-serif', color='#1e293b'),
                x=0.5,
                xanchor='center'
            ),
            height=600,
            paper_bgcolor='white',
            font=dict(family='Inter, sans-serif'),
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_color="#1e293b"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Tabla de resultados detallados
    st.markdown("<h4 class='subtitle-serif' style='margin-top: 3rem;'>DETAILED_LOGS</h4>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Proceso Administrativo", "Proceso Operativo"])
    
    with tab1:
        for aspecto, elementos_data in resultados['pa'].items():
            st.markdown(f"#### {aspecto}")
            if 'porcentaje_aspecto' in elementos_data:
                st.info(f"Cumplimiento del aspecto: {elementos_data['porcentaje_aspecto']:.1f}%")
            
            tabla_data = []
            for elemento, data in elementos_data.items():
                if elemento != 'promedio_aspecto' and elemento != 'porcentaje_aspecto':
                    tabla_data.append({
                        'Elemento': elemento,
                        'Promedio': f"{data['promedio']:.2f}",
                        'Cumplimiento (%)': f"{data['porcentaje']:.1f}%",
                        'Prioridad': data['prioridad']
                    })
            
            if tabla_data:
                df = pd.DataFrame(tabla_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        for aspecto, elementos_data in resultados['po'].items():
            st.markdown(f"#### {aspecto}")
            if 'porcentaje_aspecto' in elementos_data:
                st.info(f"Cumplimiento del aspecto: {elementos_data['porcentaje_aspecto']:.1f}%")
            
            tabla_data = []
            for elemento, data in elementos_data.items():
                if elemento != 'promedio_aspecto' and elemento != 'porcentaje_aspecto':
                    tabla_data.append({
                        'Elemento': elemento,
                        'Promedio': f"{data['promedio']:.2f}",
                        'Cumplimiento (%)': f"{data['porcentaje']:.1f}%",
                        'Prioridad': data['prioridad']
                    })
            
            if tabla_data:
                df = pd.DataFrame(tabla_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

def mostrar_prioridades():
    """Muestra las prioridades de intervención"""
    st.markdown("<h3>Análisis de Prioridades de Intervención</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay evaluaciones registradas. Por favor complete al menos una evaluación.")
        return
    
    st.markdown("""
    <div class="modern-card" style="border-left: 6px solid var(--primary);">
        <h4 style="margin-top:0; margin-bottom: 1rem;">Protocolos de Priorización</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem;">
            <div style="padding: 1rem; border: 1px solid var(--error); border-radius: 0.5rem; background: #fff1f2;">
                <strong style="color: var(--error);">CRÍTICO (< 60%)</strong>
                <p style="font-size: 0.8rem; color: #9f1239; margin-top: 0.25rem; margin-bottom: 0;">ACCIÓN INMEDIATA</p>
            </div>
            <div style="padding: 1rem; border: 1px solid var(--warning); border-radius: 0.5rem; background: #fffbeb;">
                <strong style="color: var(--warning);">ALERTA (60-74%)</strong>
                <p style="font-size: 0.8rem; color: #92400e; margin-top: 0.25rem; margin-bottom: 0;">PLANIFICACIÓN</p>
            </div>
            <div style="padding: 1rem; border: 1px solid var(--success); border-radius: 0.5rem; background: #f0fdf4;">
                <strong style="color: var(--success);">ESTABLE (≥ 75%)</strong>
                <p style="font-size: 0.8rem; color: #166534; margin-top: 0.25rem; margin-bottom: 0;">MANTENIMIENTO</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    resultados = calcular_resultados()
    
    # Agrupar por prioridad
    prioridad_alta = []
    prioridad_media = []
    prioridad_baja = []
    
    # Proceso Administrativo
    for aspecto, elementos_data in resultados['pa'].items():
        for elemento, data in elementos_data.items():
            if elemento not in ['promedio_aspecto', 'porcentaje_aspecto']:
                item = {
                    'Área': 'Proceso Administrativo',
                    'Aspecto': aspecto,
                    'Elemento': elemento,
                    'Cumplimiento (%)': f"{data['porcentaje']:.1f}%",
                    'Prioridad': data['prioridad']
                }
                
                if data['prioridad'] == 'ALTA':
                    prioridad_alta.append(item)
                elif data['prioridad'] == 'MEDIA':
                    prioridad_media.append(item)
                else:
                    prioridad_baja.append(item)
    
    # Proceso Operativo
    for aspecto, elementos_data in resultados['po'].items():
        for elemento, data in elementos_data.items():
            if elemento not in ['promedio_aspecto', 'porcentaje_aspecto']:
                item = {
                    'Área': 'Proceso Operativo',
                    'Aspecto': aspecto,
                    'Elemento': elemento,
                    'Cumplimiento (%)': f"{data['porcentaje']:.1f}%",
                    'Prioridad': data['prioridad']
                }
                
                if data['prioridad'] == 'ALTA':
                    prioridad_alta.append(item)
                elif data['prioridad'] == 'MEDIA':
                    prioridad_media.append(item)
                else:
                    prioridad_baja.append(item)
    
    # Mostrar resumen
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card-modern" style="border-bottom: 4px solid var(--error);">
            <div class="metric-label-modern">Críticos (Alta)</div>
            <div class="metric-value-modern" style="color: var(--error);">{len(prioridad_alta)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card-modern" style="border-bottom: 4px solid var(--warning);">
            <div class="metric-label-modern">Alertas (Media)</div>
            <div class="metric-value-modern" style="color: var(--warning);">{len(prioridad_media)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card-modern" style="border-bottom: 4px solid var(--success);">
            <div class="metric-label-modern">Estables (Baja)</div>
            <div class="metric-value-modern" style="color: var(--success);">{len(prioridad_baja)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de distribución de prioridades mejorado
    total_elementos = len(prioridad_alta) + len(prioridad_media) + len(prioridad_baja)
    
    fig = go.Figure(data=[go.Pie(
        labels=['Alta Prioridad', 'Media Prioridad', 'Baja Prioridad'],
        values=[len(prioridad_alta), len(prioridad_media), len(prioridad_baja)],
        marker=dict(
            colors=['#ef4444', '#f59e0b', '#10b981'],
            line=dict(color='white', width=2)
        ),
        hole=0.6,
        textinfo='label+percent',
        textfont=dict(size=12, color='white', family='Inter, sans-serif'),
        pull=[0.05, 0, 0],
    )])
    
    fig.add_annotation(
        text=f'<span style="color:#64748b; font-size:12px">TOTAL</span><br><b style="color:#1e293b; font-size:30px">{total_elementos}</b>',
        x=0.5, y=0.5,
        showarrow=False,
    )
    
    fig.update_layout(
        title=dict(
            text="Distribución de Carga de Trabajo",
            font=dict(size=18, family='Inter, sans-serif', color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        height=450,
        showlegend=False,
        paper_bgcolor='white',
        font=dict(family='Inter, sans-serif', color='#1e293b'),
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Mostrar detalles por prioridad
    tab1, tab2, tab3 = st.tabs(["🟠 Prioridad Alta", "🟡 Prioridad Media", "🟢 Prioridad Baja"])
    
    with tab1:
        if prioridad_alta:
            st.markdown("### Elementos de Prioridad Alta")
            st.markdown("**Estos elementos requieren atención inmediata:**")
            df_alta = pd.DataFrame(prioridad_alta)
            st.dataframe(df_alta, use_container_width=True, hide_index=True)
        else:
            st.success("¡Excelente! No hay elementos con prioridad alta.")
    
    with tab2:
        if prioridad_media:
            st.markdown("### Elementos de Prioridad Media")
            st.markdown("**Estos elementos deben atenderse en el mediano plazo:**")
            df_media = pd.DataFrame(prioridad_media)
            st.dataframe(df_media, use_container_width=True, hide_index=True)
        else:
            st.success("No hay elementos con prioridad media.")
    
    with tab3:
        if prioridad_baja:
            st.markdown("### Elementos de Prioridad Baja")
            st.markdown("**Estos elementos están en buen estado:**")
            df_baja = pd.DataFrame(prioridad_baja)
            st.dataframe(df_baja, use_container_width=True, hide_index=True)
        else:
            st.info("No hay elementos con prioridad baja aún.")

def mostrar_guardar_cargar():
    """Muestra opciones para guardar y cargar evaluaciones"""
    st.markdown("<h3>Gestión de Datos y Almacenamiento</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💾 Guardar Sesión Actual")
        
        if st.session_state.evaluaciones_pa or st.session_state.evaluaciones_po:
            if st.button("Guardar Evaluación"):
                archivo = guardar_evaluacion()
                st.success(f"✓ Evaluación guardada exitosamente en:\n`{archivo}`")
        else:
            st.info("No hay evaluaciones para guardar.")
    
    with col2:
        st.markdown("### 📂 Cargar Evaluación Anterior")
        
        # Buscar archivos JSON en el directorio
        directorio = os.path.dirname(__file__)
        archivos_json = [f for f in os.listdir(directorio) if f.startswith('evaluacion_') and f.endswith('.json')]
        
        if archivos_json:
            archivo_seleccionado = st.selectbox(
                "Seleccione una evaluación:",
                archivos_json,
                format_func=lambda x: x.replace('evaluacion_', '').replace('.json', '').replace('_', ' ')
            )
            
            if st.button("Cargar Evaluación"):
                try:
                    cargar_evaluacion(os.path.join(directorio, archivo_seleccionado))
                    st.success("✓ Evaluación cargada exitosamente")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al cargar la evaluación: {e}")
        else:
            st.info("No hay evaluaciones guardadas.")
    
    # Exportar a Excel
    st.markdown("### 📊 Exportar Resultados a Excel")
    
    if st.session_state.evaluaciones_pa or st.session_state.evaluaciones_po:
        if st.button("Exportar a Excel"):
            try:
                resultados = calcular_resultados()
                
                # Crear un archivo Excel con los resultados
                archivo_excel = os.path.join(directorio, f"resultados_gpp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
                
                with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                    # Hoja de resumen
                    resumen_data = []
                    for aspecto, data in resultados['pa'].items():
                        if 'porcentaje_aspecto' in data:
                            resumen_data.append({
                                'Área': 'Proceso Administrativo',
                                'Aspecto': aspecto,
                                'Cumplimiento (%)': data['porcentaje_aspecto']
                            })
                    
                    for aspecto, data in resultados['po'].items():
                        if 'porcentaje_aspecto' in data:
                            resumen_data.append({
                                'Área': 'Proceso Operativo',
                                'Aspecto': aspecto,
                                'Cumplimiento (%)': data['porcentaje_aspecto']
                            })
                    
                    df_resumen = pd.DataFrame(resumen_data)
                    df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                
                st.success(f"✓ Resultados exportados a:\n`{archivo_excel}`")
            except Exception as e:
                st.error(f"Error al exportar: {e}")

if __name__ == "__main__":
    main()

