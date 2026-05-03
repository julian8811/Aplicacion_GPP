"""
Aplicación de Evaluación de Gestión Por Procesos (GPP)
Convierte la herramienta de Excel en una aplicación web interactiva
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
import os
from datetime import datetime
from pdf_generator import crear_pdf_auditoria
from recomendaciones import obtener_recomendaciones_criticas

# Configuración de la página
st.set_page_config(
    page_title="GPP_CORE | Audit System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS profesionales - Rediseño 'B2B SaaS Premium v2.1' (Linear/Stripe Aesthetic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    :root {
        --primary: #004191;
        --brand-accent: #0058be;
        --bg-workspace: #f7f9fb;
        --surface-white: #ffffff;
        --sidebar-bg: #0f172a;
        --text-display: #0f172a;
        --text-body: #1e293b;
        --text-subtle: #64748b;
        --border-subtle: #e2e8f0;
        --success-premium: #059669;
        --warning-premium: #d97706;
        --error-premium: #be123c;
        --font-main: 'Inter', sans-serif;
        
        /* Linear Shadow Model */
        --shadow-ambient: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        --shadow-lift: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
        --radius-bento: 16px;
        --radius-interactive: 8px;
    }

    /* Global Interface Refinement */
    .stApp {
        background-color: var(--bg-workspace);
        font-family: var(--font-main);
        color: var(--text-body);
    }

    /* Hide Streamlit Native Decorations for App Feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    /* Sidebar - High-End Obsidian Theme */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid #1e293b;
        padding-top: 1rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em;
    }

    /* Typography & Headers */
    h1, h2, h3, h4 {
        font-family: var(--font-main) !important;
        color: var(--text-display) !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }

    .title-modern {
        font-weight: 900;
        font-size: 2.5rem;
        letter-spacing: -0.05em;
        background: linear-gradient(to bottom, #0f172a, #334155);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
    }

    /* Bento Cards - Minimalist & Tactile */
    .bento-card {
        background: var(--surface-white);
        padding: 24px;
        border-radius: var(--radius-bento);
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-ambient);
        margin-bottom: 24px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        overflow: hidden;
    }
    
    .bento-card:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lift);
        border-color: #cbd5e1;
    }

    /* Metric Data (Tabular Lining) */
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--brand-accent);
        line-height: 1;
        letter-spacing: -0.04em;
        font-variant-numeric: tabular-nums; /* Align numbers perfectly */
    }

    .metric-label {
        color: var(--text-subtle);
        font-weight: 600;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
    }

    /* Navigation Header */
    .nav-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        border-bottom: 1px solid var(--border-subtle);
        margin: -1rem -4rem 3rem -4rem;
        background: rgba(255, 255, 255, 0.85);
        position: sticky;
        top: 0;
        z-index: 1000;
        backdrop-filter: blur(12px);
    }

    /* Material Icons Helper */
    .icon {
        font-family: 'Material Symbols Outlined';
        vertical-align: middle;
        font-size: 1.3em;
        margin-right: 6px;
    }

    /* Component Overrides (Buttons & Sliders) */
    .stButton > button {
        border-radius: var(--radius-interactive) !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        transition: all 0.2s !important;
        border: 1px solid var(--border-subtle) !important;
    }

    /* Pilled Status Badges (Stripe Style) */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px; /* Full pill */
        font-size: 0.65rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-primary { background: rgba(0, 88, 190, 0.08); color: #0058be; border: 1px solid rgba(0, 88, 190, 0.1); }
    .badge-success { background: rgba(5, 150, 105, 0.08); color: #059669; border: 1px solid rgba(5, 150, 105, 0.1); }
    .badge-warning { background: rgba(217, 119, 6, 0.08); color: #d97706; border: 1px solid rgba(217, 119, 6, 0.1); }
    .badge-error { background: rgba(190, 18, 60, 0.08); color: #be123c; border: 1px solid rgba(190, 18, 60, 0.1); }

    /* Section & Question Refinement */
    .question-block {
        padding: 1.5rem 0;
        border-bottom: 1px solid #f1f5f9;
    }

    .question-text {
        font-weight: 600;
        font-size: 1.05rem;
        color: var(--text-display);
        margin-bottom: 0.5rem;
    }

    .context-text {
        font-size: 0.85rem;
        color: var(--text-subtle);
        line-height: 1.5;
        padding-left: 1rem;
        border-left: 2px solid #f1f5f9;
    }

    </style>
    """, unsafe_allow_html=True)

# Definición de las matrices de evaluación con contexto
MATRIZ_PA = {
    "PLANEACIÓN": {
        "Análisis del contexto": [
            {
                "pregunta": "¿La empresa realiza un análisis externo como base para su planeación estratégica?",
                "contexto": "Evaluación de factores fuera de la empresa (mercado, competencia, economía, leyes) que pueden afectar el negocio."
            },
            {
                "pregunta": "¿La empresa realiza un análisis interno como base para su planeación estratégica?",
                "contexto": "Revisión de las capacidades propias (recursos humanos, financieros, tecnológicos) para identificar fortalezas y debilidades."
            },
            {
                "pregunta": "Aplicación de herramientas de análisis como la matriz DOFA, PESTEL, Las 5 Fuerzas de Porter, Benchmarking, entre otras",
                "contexto": "Uso de métodos formales para estructurar la información obtenida en los análisis internos y externos."
            }
        ],
        "Existencia de un plan estratégico": [
            {
                "pregunta": "En qué medida considera que la misión de la empresa está claramente definida y comunicada a todos los miembros de la organización",
                "contexto": "Claridad sobre la razón de ser de la empresa y si todos los empleados la conocen."
            },
            {
                "pregunta": "En qué medida considera que la visión de la empresa está claramente definida y comunicada a todos los miembros de la organización",
                "contexto": "Claridad sobre dónde quiere llegar la empresa en el futuro y si esta meta es compartida."
            },
            {
                "pregunta": "En qué medida considera que el establecimiento tiene definidos y comunicados sus objetivos estratégicos",
                "contexto": "Metas específicas y medibles que la organización se ha propuesto alcanzar."
            },
            {
                "pregunta": "Documento que evidencie el plan estratégico a largo o mediano plazo",
                "contexto": "Existencia física o digital de un plan que guíe las acciones de la empresa."
            }
        ]
    },
    "ORGANIZACIÓN": {
        "Existencia de una estructura organizativa": [
            {
                "pregunta": "¿El establecimiento cuenta con un organigrama claramente definido?",
                "contexto": "Representación gráfica de la estructura jerárquica y las relaciones entre departamentos."
            }
        ],
        "Departamentalización": [
            {
                "pregunta": "¿Se tienen claramente identificados los procesos de la organización?",
                "contexto": "División de las actividades en procesos lógicos (compras, ventas, producción, etc.) para una mejor gestión."
            }
        ],
        "Procesos documentados": [
            {
                "pregunta": "¿Existen perfiles de cargo definidos para cada función?",
                "contexto": "Descripción clara de las responsabilidades, requisitos y habilidades necesarias para cada puesto de trabajo."
            },
            {
                "pregunta": "¿El establecimiento tiene debidamente documentado cada proceso (mapas de proceso, flujogramas, procedimientos, normas, etc)?",
                "contexto": "Guías escritas que explican paso a paso cómo se deben realizar las tareas para asegurar la consistencia."
            },
            {
                "pregunta": "¿El establecimiento tiene caracterizado los procesos?",
                "contexto": "Definición de entradas, salidas, responsables, recursos y controles de cada proceso específico."
            }
        ],
        "Ciclo PHVA": [
            {
                "pregunta": "¿Tiene implementado el ciclo PHVA (Planear, Hacer, Verificar, Actuar) en el establecimiento?",
                "contexto": "Método de mejora continua que asegura que los procesos se planifican, se ejecutan, se miden y se corrigen."
            }
        ]
    },
    "DIRECCIÓN": {
        "Liderazgo organizacional": [
            {
                "pregunta": "¿Existen líderes proactivos y motivadores en el establecimiento?",
                "contexto": "Presencia de personas que guían al equipo, fomentan la iniciativa y mantienen la moral alta."
            }
        ],
        "Canales de comunicación efectivos": [
            {
                "pregunta": "¿Existe un sistema de comunicación formal (vertical y horizontal) que permita el flujo de información en la organización?",
                "contexto": "Medios oficiales (reuniones, correos) para que la información fluya entre niveles jerárquicos y compañeros."
            }
        ],
        "Cultura organizacional": [
            {
                "pregunta": "¿Se fomenta el trabajo en equipo y la participación del personal en la toma de decisiones?",
                "contexto": "Grado en que se escuchan las opiniones de los empleados y se trabaja colaborativamente."
            },
            {
                "pregunta": "¿Se promueve la innovación y la mejora continua en los procesos?",
                "contexto": "Apertura a nuevas ideas y búsqueda constante de formas más eficientes de trabajar."
            },
            {
                "pregunta": "¿Se reconocen los logros y se incentiva el buen desempeño del personal?",
                "contexto": "Existencia de programas o gestos que premien el esfuerzo y los resultados positivos."
            },
            {
                "pregunta": "¿Se cuenta con un código de ética o valores organizacionales claramente definidos y comunicados?",
                "contexto": "Principios morales y de comportamiento que rigen la conducta de todos en la empresa."
            },
            {
                "pregunta": "¿Existe un sentido de pertenencia del personal hacia la organización?",
                "contexto": "Nivel de compromiso y orgullo de los empleados por formar parte de la empresa."
            }
        ]
    },
    "CONTROL": {
        "Sistemas de control": [
            {
                "pregunta": "¿Se realiza seguimiento periódico al cumplimiento de los objetivos estratégicos?",
                "contexto": "Revisión constante para ver si se están alcanzando las metas propuestas en el plan."
            },
            {
                "pregunta": "¿Se utilizan indicadores de gestión para medir el desempeño de los procesos?",
                "contexto": "Uso de números o métricas (KPIs) para evaluar si un proceso está funcionando bien."
            }
        ],
        "Auditorías internas": [
            {
                "pregunta": "¿Se realizan auditorías internas de forma periódica para evaluar el cumplimiento de los procesos?",
                "contexto": "Evaluaciones hechas por la misma empresa para verificar que se sigan las reglas y procedimientos."
            }
        ],
        "Acciones correctivas y preventivas": [
            {
                "pregunta": "¿Existe un procedimiento establecido para implementar acciones correctivas cuando se detectan desviaciones?",
                "contexto": "Plan de acción para arreglar un problema cuando algo no sale como se esperaba."
            },
            {
                "pregunta": "¿Se implementan acciones preventivas para evitar problemas antes de que ocurran?",
                "contexto": "Medidas tomadas para anticiparse a posibles fallas y evitar que sucedan."
            }
        ]
    }
}

MATRIZ_PO = {
    "LOGÍSTICA DE COMPRAS": {
        "Logística de entrada": [
            {
                "pregunta": "¿La planeación de compras en el establecimiento se realiza de manera organizada, considerando la periodicidad, la gestión de proveedores, las cantidades requeridas y el estado de los inventarios?",
                "contexto": "Proceso de decidir qué comprar, a quién, cuánto y cuándo, para no quedarse sin insumos ni tener exceso."
            },
            {
                "pregunta": "¿Se utilizan herramientas de control como formatos, bases de datos o software para la gestión?",
                "contexto": "Uso de registros (digitales o físicos) para llevar el orden de los pedidos y compras."
            },
            {
                "pregunta": "¿El establecimiento dispone de condiciones adecuadas de almacenamiento (frío o caliente) según el tipo de producto?",
                "contexto": "Espacios que cumplen con temperatura e higiene para conservar la materia prima."
            }
        ],
        "Gestión de inventarios": [
            {
                "pregunta": "¿Se encuentra implementado un sistema de inventario (PEPS, ABC u otro)?",
                "contexto": "Métodos para organizar la salida de productos (ej: lo primero que entra es lo primero que sale)."
            },
            {
                "pregunta": "¿El inventario está automatizado en un software de gestión?",
                "contexto": "Control de existencias mediante una computadora o sistema digital en lugar de solo papel."
            }
        ]
    },
    "GESTIÓN DE PRODUCCIÓN": {
        "Equipos": [
            {
                "pregunta": "¿Los equipos e instalaciones son adecuados para el volumen de producción requerido?",
                "contexto": "Capacidad de las máquinas y el espacio para sacar todos los pedidos sin retrasos."
            },
            {
                "pregunta": "¿Se realizan actividades de mantenimiento correctivo, preventivo y de mejora en los equipos e instalaciones?",
                "contexto": "Cuidado regular de las máquinas para que no se dañen y reparación rápida cuando fallan."
            }
        ],
        "Infraestructura": [
            {
                "pregunta": "¿El establecimiento cuenta con un sistema de ventilación y control de humos eficiente?",
                "contexto": "Presencia de campanas, extractores o ventanas que mantengan el aire limpio y fresco."
            },
            {
                "pregunta": "¿El diseño y distribución de la cocina favorecen un trabajo ordenado y funcional?",
                "contexto": "Organización del espacio que permite moverse fácilmente sin chocar ni perder tiempo."
            },
            {
                "pregunta": "¿La iluminación y ventilación de las áreas de trabajo son adecuadas?",
                "contexto": "Luz suficiente para trabajar con seguridad y temperatura cómoda para el personal."
            }
        ],
        "Distribución de los procesos (flujo)": [
            {
                "pregunta": "¿Cada área de trabajo (emplatado, preparación, cocción, limpieza, ubicación de utensilios, etc.) está claramente identificada?",
                "contexto": "Señalización o delimitación de dónde se hace cada tarea específica."
            },
            {
                "pregunta": "¿El flujo de trabajo en la cocina es lógico y eficiente?",
                "contexto": "El recorrido del plato (desde materia prima hasta servido) sigue una línea que evita retrocesos."
            }
        ],
        "Planeación de la producción": [
            {
                "pregunta": "¿Se planea adecuadamente los niveles de producción para atender la demanda?",
                "contexto": "Estimación de cuánta comida preparar según la cantidad esperada de clientes."
            },
            {
                "pregunta": "¿Se cuenta con recetas estandarizadas que garanticen la calidad y consistencia de los productos?",
                "contexto": "Fichas técnicas que aseguran que el plato sepa y se vea igual siempre, sin importar quién lo cocine."
            },
            {
                "pregunta": "¿Se realiza un control de tiempos de preparación y cocción?",
                "contexto": "Medición de cuánto tarda cada plato para asegurar un servicio ágil."
            },
            {
                "pregunta": "¿Se optimiza el uso de los recursos disponibles (tiempo, personal, equipos)?",
                "contexto": "Máximo provecho de lo que se tiene para evitar desperdicios de tiempo o esfuerzo."
            },
            {
                "pregunta": "¿Se tienen definidos procedimientos para el manejo de desperdicios y mermas?",
                "contexto": "Reglas sobre qué hacer con las sobras o partes de alimentos que no se usan."
            }
        ],
        "Materia prima": [
            {
                "pregunta": "¿Las materias primas utilizadas cumplen con estándares de calidad?",
                "contexto": "Uso de ingredientes frescos, seguros y con buen sabor."
            },
            {
                "pregunta": "¿Se verifica la calidad de las materias primas al momento de recibirlas?",
                "contexto": "Revisión de fechas de vencimiento, olor, color y temperatura al llegar el proveedor."
            }
        ],
        "Control de la producción": [
            {
                "pregunta": "¿Se realiza control de calidad durante el proceso de producción?",
                "contexto": "Pruebas o revisiones mientras se cocina para asegurar que todo vaya bien."
            },
            {
                "pregunta": "¿Se registran y analizan los datos de producción (cantidades, tiempos, costos)?",
                "contexto": "Anotar cuánto se produjo y cuánto costó para tomar mejores decisiones."
            },
            {
                "pregunta": "¿Se implementan acciones de mejora basadas en los datos de producción?",
                "contexto": "Cambios en la forma de trabajar cuando los datos muestran que algo puede hacerse mejor."
            }
        ]
    },
    "LOGÍSTICA EXTERNA": {
        "Distribución": [
            {
                "pregunta": "¿El servicio al cliente es ágil y eficiente?",
                "contexto": "Rapidez y amabilidad en la entrega del producto final al cliente."
            },
            {
                "pregunta": "¿Se cuenta con personal capacitado para atender al cliente?",
                "contexto": "Empleados con conocimientos sobre el menú y buen trato al público."
            },
            {
                "pregunta": "¿Se realiza seguimiento a la satisfacción del cliente?",
                "contexto": "Encuestas o preguntas directas para saber si al cliente le gustó la experiencia."
            },
            {
                "pregunta": "¿Se gestionan adecuadamente las quejas y reclamos?",
                "contexto": "Proceso claro para escuchar al cliente cuando algo sale mal y darle una solución."
            },
            {
                "pregunta": "¿Se implementan mejoras basadas en la retroalimentación de los clientes?",
                "contexto": "Cambios en el servicio o producto a partir de lo que los clientes sugieren."
            }
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
    if 'nombre_establecimiento' not in st.session_state:
        st.session_state.nombre_establecimiento = ""
    if 'plan_accion' not in st.session_state:
        st.session_state.plan_accion = []

    # Crear carpeta de datos si no existe
    if not os.path.exists('data'):
        os.makedirs('data')

def guardar_evaluacion(nombre_est):
    """Guarda la evaluación actual en un archivo JSON en la carpeta data/"""
    # Validar nombre antes de procesar
    if not nombre_est or not nombre_est.strip():
        raise ValueError("El nombre del establecimiento no puede estar vacío")
    
    datos = {
        'nombre_establecimiento': nombre_est,
        'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'evaluaciones_pa': st.session_state.evaluaciones_pa,
        'evaluaciones_po': st.session_state.evaluaciones_po,
        'plan_accion': st.session_state.plan_accion
    }
    
    # Limpiar nombre para el archivo
    nombre_limpio = "".join(x for x in nombre_est if x.isalnum() or x in "._- ").strip().replace(" ", "_")
    if not nombre_limpio:
        nombre_limpio = "sin_nombre"
    
    archivo = os.path.join('data', f"eval_{nombre_limpio}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    return archivo

def cargar_evaluacion(archivo):
    """Carga una evaluación desde un archivo JSON"""
    with open(archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    st.session_state.evaluaciones_pa = datos.get('evaluaciones_pa', {})
    st.session_state.evaluaciones_po = datos.get('evaluaciones_po', {})
    st.session_state.nombre_establecimiento = datos.get('nombre_establecimiento', "")
    st.session_state.plan_accion = datos.get('plan_accion', [])
    st.session_state.resultados_calculados = True

# Función principal
def main():
    inicializar_session_state()
    
    # Custom Modern Header
    st.markdown('''
    <div class="nav-header">
        <div class="logo-text">GPP_CORE <span style="color: #64748b; font-weight: 400; font-size: 0.8rem; letter-spacing: 0;">/ AUDIT_SYSTEM</span></div>
        <div style="display: flex; gap: 20px; align-items: center;">
            <div style="font-size: 0.75rem; color: #64748b; font-weight: 600; background: #f1f5f9; padding: 4px 12px; border-radius: 100px;">v2.6.0_STABLE</div>
            <div style="width: 32px; height: 32px; background: #e2e8f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 800;">AD</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar para navegación
    st.sidebar.markdown("<h2 style='color: white; margin-bottom: 2rem;'><span class='material-symbols-outlined' style='vertical-align: bottom; font-size: 1.5rem;'>analytics</span> GPP_CORE</h2>", unsafe_allow_html=True)
    pagina = st.sidebar.radio(
        "SISTEMA DE GESTIÓN",
        ["Inicio", "Proceso Administrativo", "Proceso Operativo", 
         "Resultados Generales", "Prioridades", "Plan de Acción", "Benchmarking", "Historial", "Guardar Auditoría"]
    )
    
    if pagina == "Inicio":
        mostrar_inicio()
    elif pagina == "Proceso Administrativo":
        mostrar_evaluacion_pa()
    elif pagina == "Proceso Operativo":
        mostrar_evaluacion_po()
    elif pagina == "Resultados Generales":
        mostrar_resultados_generales()
    elif pagina == "Prioridades":
        mostrar_prioridades()
    elif pagina == "Plan de Acción":
        mostrar_plan_accion()
    elif pagina == "Benchmarking":
        mostrar_benchmarking()
    elif pagina == "Historial":
        mostrar_historial()
    elif pagina == "Guardar Auditoría":
        mostrar_guardar_cargar()
    
    # Footer Moderno
    st.markdown("""
    <div style="margin-top: 5rem; padding: 3rem 0; border-top: 1px solid var(--border-color); text-align: center; font-size: 0.75rem; color: var(--text-muted);">
        <div style="font-weight: 800; color: #0f172a; margin-bottom: 0.5rem; letter-spacing: 0.05em;">GPP_CORE ENTERPRISE SOLUTIONS</div>
        <div>© 2024-2025 • PROCESSED BY INTEL_CORE_ENGINE</div>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 20px;">
            <span style="font-weight: 600;">PRIVACY POLICY</span>
            <span style="font-weight: 600;">SECURITY AUDIT</span>
            <span style="font-weight: 600;">LICENSE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def mostrar_inicio():
    """Muestra la página de inicio con estética B2B SaaS Premium (Linear/Stripe)"""
    st.markdown("""
    <div class="hero-banner" style="padding: 4rem 3rem; background: radial-gradient(circle at top right, rgba(0, 88, 190, 0.03), transparent); border: none; box-shadow: none; margin-bottom: 0;">
        <div style="position: relative; z-index: 10;">
            <span class="badge badge-primary" style="margin-bottom: 1.5rem; letter-spacing: 0.1em;">SYSTEM_READY // CLOUD_SYNCED</span>
            <h1 class="title-modern" style="margin-bottom: 1rem;">Inteligencia de Auditoría Corporativa</h1>
            <p style="color: var(--text-subtle); font-size: 1.15rem; max-width: 700px; font-weight: 400; line-height: 1.6;">
                Bienvenido al centro de mando GPP_CORE. Gestione el cumplimiento operativo y la eficiencia administrativa a través de diagnósticos de alta precisión basados en estándares internacionales.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        # Calcular progreso
        total_pa = sum(len(items) for aspecto in MATRIZ_PA.values() for items in aspecto.values())
        total_po = sum(len(items) for aspecto in MATRIZ_PO.values() for items in aspecto.values())
        total_preguntas = total_pa + total_po
        preguntas_respondidas = len(st.session_state.evaluaciones_pa) + len(st.session_state.evaluaciones_po)
        progreso = (preguntas_respondidas / total_preguntas) * 100 if total_preguntas > 0 else 0

        st.markdown(f"""
        <div class="bento-card" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-label" style="display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 1rem;">insights</span> HEALTH_INDEX_SCORE
            </div>
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin: 1rem 0;">
                <div class="metric-value">{progreso:.1f}<span style="font-size: 1.2rem; font-weight: 500; opacity: 0.5;">%</span></div>
                <div style="color: var(--success-premium); font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 4px;">
                    <span class="material-symbols-outlined" style="font-size: 1.1rem;">keyboard_double_arrow_up</span> +0.2%
                </div>
            </div>
            <div style="width: 100%; height: 6px; background: #f1f5f9; border-radius: 99px; overflow: hidden; margin-bottom: 0.5rem;">
                <div style="width: {progreso}%; height: 100%; background: var(--brand-accent); border-radius: 99px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="bento-card" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-label">TOTAL_DATA_POINTS</div>
            <div class="metric-value" style="color: var(--text-display);">{len(st.session_state.evaluaciones_pa) + len(st.session_state.evaluaciones_po)}</div>
            <p style="font-size: 0.85rem; color: var(--text-subtle); margin-top: 1rem; font-weight: 500;">Registros procesados</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="bento-card" style="min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-label">GLOBAL_BENCHMARK</div>
            <div class="metric-value" style="color: var(--success-premium);">1.2k</div>
            <p style="font-size: 0.85rem; color: var(--text-subtle); margin-top: 1rem; font-weight: 500;">Validaciones regionales</p>
        </div>
        """, unsafe_allow_html=True)

    # Bloques de Información Refinados
    c_info1, c_info2 = st.columns([1, 1])
    
    with c_info1:
        st.markdown("""
        <div class="bento-card" style="border-top: 4px solid var(--brand-accent);">
            <h3 style="margin-top:0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: var(--brand-accent);">account_tree</span> Protocolo de Auditoría
            </h3>
            <p style="color: var(--text-subtle); font-size: 0.9rem; margin-bottom: 2rem;">Secuencia de ejecución para integridad de datos:</p>
            <div style="display: flex; flex-direction: column; gap: 20px;">
                <div style="display: flex; gap: 16px;">
                    <div style="color: var(--brand-accent); font-weight: 900; font-size: 0.8rem; font-family: monospace;">01</div>
                    <div><b style="font-size: 0.9rem; color: var(--text-display);">DATA_COLLECTION</b><br><span style="font-size: 0.85rem; color: var(--text-subtle);">Ejecute las matrices de revisión estratégica y táctica.</span></div>
                </div>
                <div style="display: flex; gap: 16px;">
                    <div style="color: var(--brand-accent); font-weight: 900; font-size: 0.8rem; font-family: monospace;">02</div>
                    <div><b style="font-size: 0.9rem; color: var(--text-display);">ANALYTICS_VALIDATION</b><br><span style="font-size: 0.85rem; color: var(--text-subtle);">Consolide los hallazgos en los tableros de visualización.</span></div>
                </div>
                <div style="display: flex; gap: 16px;">
                    <div style="color: var(--brand-accent); font-weight: 900; font-size: 0.8rem; font-family: monospace;">03</div>
                    <div><b style="font-size: 0.9rem; color: var(--text-display);">STRATEGIC_PLANNING</b><br><span style="font-size: 0.85rem; color: var(--text-subtle);">Implemente mitigaciones mediante el tracker de compromisos.</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_info2:
        st.markdown("""
        <div class="bento-card">
            <h3 style="margin-top:0; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: var(--brand-accent);">verified_user</span> Niveles de Cumplimiento
            </h3>
            <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 1.5rem;">
                <div style="padding: 16px; border: 1px solid #f1f5f9; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; background: #fafafa;">
                    <div>
                        <span class="badge badge-error" style="margin-bottom: 4px;">CRÍTICO</span>
                        <div style="font-size: 0.85rem; color: var(--text-subtle); font-weight: 500;">Acción táctica inmediata.</div>
                    </div>
                    <div style="font-weight: 800; color: var(--error-premium); font-size: 1.1rem; font-family: monospace;">< 60%</div>
                </div>
                <div style="padding: 16px; border: 1px solid #f1f5f9; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; background: #fafafa;">
                    <div>
                        <span class="badge badge-warning" style="margin-bottom: 4px;">ALERTA</span>
                        <div style="font-size: 0.85rem; color: var(--text-subtle); font-weight: 500;">Plan de mejora a corto plazo.</div>
                    </div>
                    <div style="font-weight: 800; color: var(--warning-premium); font-size: 1.1rem; font-family: monospace;">60-74%</div>
                </div>
                <div style="padding: 16px; border: 1px solid #f1f5f9; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; background: #fafafa;">
                    <div>
                        <span class="badge badge-success" style="margin-bottom: 4px;">ÓPTIMO</span>
                        <div style="font-size: 0.85rem; color: var(--text-subtle); font-weight: 500;">Mantenimiento y excelencia.</div>
                    </div>
                    <div style="font-weight: 800; color: var(--success-premium); font-size: 1.1rem; font-family: monospace;">≥ 75%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h4 style='margin-bottom: 1.5rem; color: var(--text-subtle); font-weight: 700; font-size: 0.8rem; letter-spacing: 0.15em;'>CORE_ACCESS_SHORTCUTS</h4>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("ADMINISTRATIVE_AUDIT", width='stretch'):
            st.info("Navegue al Proceso Administrativo en el menú lateral.")
    with c2:
        if st.button("OPERATIONAL_AUDIT", width='stretch'):
            st.info("Navegue al Proceso Operativo en el menú lateral.")
    with c3:
        if st.button("AUDIT_HISTORY", width='stretch'):
            st.info("Navegue al Historial en el menú lateral.")

def mostrar_evaluacion_pa():
    """Muestra el formulario de evaluación con estilo Audit Interface profesional (Linear)"""
    st.markdown("""
    <div class="bento-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 6px solid var(--brand-accent);">
        <div>
            <h2 style="margin:0; font-size: 1.5rem;">Gestión Administrativa</h2>
            <p style="color: var(--text-subtle); font-size: 0.95rem; margin:0; font-weight: 400;">Módulo 1.0: Strategic & Policy Infrastructure Review</p>
        </div>
        <div style="text-align: right;">
            <div class="metric-label" style="color: var(--brand-accent); margin-bottom: 8px;">COMPLETION_TRACKER</div>
            <div style="width: 200px; height: 6px; background: #f1f5f9; border-radius: 99px; overflow: hidden; border: 1px solid #e2e8f0;">
                <div style="width: 35%; height: 100%; background: var(--brand-accent); border-radius: 99px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for aspecto, elementos in MATRIZ_PA.items():
        with st.expander(f"📁 ASPECTO_REVIEW: {aspecto}", expanded=True):
            for elemento, items in elementos.items():
                st.markdown(f"""
                <div style='padding: 12px 0; margin-top: 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 10px;'>
                    <span class='material-symbols-outlined' style='font-size: 1.1rem; color: var(--brand-accent);'>subdirectory_arrow_right</span>
                    <strong style='color: var(--text-display); font-size: 0.95rem; letter-spacing: -0.01em;'>{elemento.upper()}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                for i, item in enumerate(items):
                    key = f"PA_{aspecto}_{elemento}_{i}"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="question-block">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 32px;">
                                <div style="flex: 1;">
                                    <div class="question-text" style="font-size: 1rem; font-weight: 600;">{item['pregunta']}</div>
                                    <div class="context-text" style="margin-top: 6px;">{item['contexto']}</div>
                                </div>
                                <span class="badge badge-primary" style="opacity: 0.7;">REQUIRED_FIELD</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        valor = st.select_slider(
                            "Calificación",
                            options=[0, 1, 2, 3, 4, 5],
                            value=st.session_state.evaluaciones_pa.get(key, 0),
                            key=f"slider_{key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.evaluaciones_pa[key] = valor
    
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    if st.button("SINCRONIZAR DATOS ADMINISTRATIVOS", type="primary", width='stretch'):
        st.success("✓ Estructura de datos sincronizada con el estado de la sesión.")
        st.session_state.resultados_calculados = True

def mostrar_evaluacion_po():
    """Muestra el formulario de evaluación operativa con estilo Audit Interface profesional (Linear)"""
    st.markdown("""
    <div class="bento-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 6px solid var(--brand-accent);">
        <div>
            <h2 style="margin:0; font-size: 1.5rem;">Gestión Operativa</h2>
            <p style="color: var(--text-subtle); font-size: 0.95rem; margin:0; font-weight: 400;">Módulo 2.0: Operational Efficiency & Value Chain</p>
        </div>
        <div style="text-align: right;">
            <div class="metric-label" style="color: var(--brand-accent); margin-bottom: 8px;">COMPLETION_TRACKER</div>
            <div style="width: 200px; height: 6px; background: #f1f5f9; border-radius: 99px; overflow: hidden; border: 1px solid #e2e8f0;">
                <div style="width: 20%; height: 100%; background: var(--brand-accent); border-radius: 99px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for aspecto, elementos in MATRIZ_PO.items():
        with st.expander(f"⚙️ ASPECTO_REVIEW: {aspecto}", expanded=True):
            for elemento, items in elementos.items():
                st.markdown(f"""
                <div style='padding: 12px 0; margin-top: 1.5rem; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; gap: 10px;'>
                    <span class='material-symbols-outlined' style='font-size: 1.1rem; color: var(--brand-accent);'>subdirectory_arrow_right</span>
                    <strong style='color: var(--text-display); font-size: 0.95rem; letter-spacing: -0.01em;'>{elemento.upper()}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                for i, item in enumerate(items):
                    key = f"PO_{aspecto}_{elemento}_{i}"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="question-block">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 32px;">
                                <div style="flex: 1;">
                                    <div class="question-text" style="font-size: 1rem; font-weight: 600;">{item['pregunta']}</div>
                                    <div class="context-text" style="margin-top: 6px;">{item['contexto']}</div>
                                </div>
                                <span class="badge badge-primary" style="opacity: 0.7;">REQUIRED_FIELD</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        valor = st.select_slider(
                            "Calificación",
                            options=[0, 1, 2, 3, 4, 5],
                            value=st.session_state.evaluaciones_po.get(key, 0),
                            key=f"slider_{key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.evaluaciones_po[key] = valor
    
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    if st.button("SINCRONIZAR DATOS OPERATIVOS", type="primary", width='stretch'):
        st.success("✓ Estructura de datos sincronizada con el estado de la sesión.")
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
        
        for elemento, items in elementos.items():
            calificaciones = []
            for i in range(len(items)):
                key = f"PA_{aspecto}_{elemento}_{i}"
                if key in st.session_state.evaluaciones_pa:
                    cal = st.session_state.evaluaciones_pa[key]
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
        
        for elemento, items in elementos.items():
            calificaciones = []
            for i in range(len(items)):
                key = f"PO_{aspecto}_{elemento}_{i}"
                if key in st.session_state.evaluaciones_po:
                    cal = st.session_state.evaluaciones_po[key]
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
    """Muestra los resultados generales con gráficos y estética corporativa"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>bar_chart</span> Reporte General de Resultados</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay evaluaciones registradas. Por favor complete al menos una evaluación.")
        return
    
    resultados = calcular_resultados()

    # Botón para descargar reporte PDF (Ya estilizado)
    st.markdown("<div style='text-align: right; margin-bottom: 30px;'>", unsafe_allow_html=True)
    nombre_est = st.session_state.get('nombre_establecimiento', 'Sin Nombre')
    fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        pdf_bytes = crear_pdf_auditoria(
            nombre_est, 
            fecha_str, 
            resultados, 
            st.session_state.evaluaciones_pa, 
            st.session_state.evaluaciones_po,
            MATRIZ_PA,
            MATRIZ_PO
        )
        st.download_button(
            label="Descargar Reporte PDF Ejecutivo",
            data=pdf_bytes,
            file_name=f"Reporte_GPP_{nombre_est.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            width='stretch'
        )
    except Exception as e:
        st.error(f"Error al preparar el PDF para '{nombre_est}' (fecha: {fecha_str}): {e}")
    st.markdown("</div>", unsafe_allow_html=True)

    if 'porcentaje' in resultados['general']:
        st.markdown("<h4 style='font-size: 1.1rem; color: var(--text-faded); margin-bottom: 1.5rem;'>CORE_COMPLIANCE_METRICS</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            porcentaje_general = resultados['general']['porcentaje']
            prioridad, tipo = calcular_prioridad(porcentaje_general)
            st.markdown(f"""
            <div class="bento-card" style="text-align: center;">
                <div class="metric-label">Cumplimiento Global</div>
                <div class="metric-value">{porcentaje_general:.1f}%</div>
                <div style="margin-top: 1rem;"><span class="badge badge-primary">ESTADO: {prioridad}</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="bento-card" style="text-align: center;">
                <div class="metric-label">Calificación Media</div>
                <div class="metric-value" style="color: var(--text-base);">{resultados['general']['promedio']:.2f}</div>
                <div style="margin-top: 1rem;"><span class="badge" style="background: #f1f5f9; color: #475569;">ESCALA DE 1 A 5</span></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            nivel_color = {"ALTA": "#e11d48", "MEDIA": "#d97706", "BAJA": "#059669"}
            color = nivel_color.get(prioridad, "var(--text-base)")
            badge_class = "badge-error" if prioridad == "ALTA" else "badge-warning" if prioridad == "MEDIA" else "badge-success"
            st.markdown(f"""
            <div class="bento-card" style="text-align: center; border-top: 4px solid {color};">
                <div class="metric-label">Nivel de Riesgo</div>
                <div class="metric-value" style="color: {color};">{prioridad}</div>
                <div style="margin-top: 1rem;"><span class="badge {badge_class}">INTERVENCIÓN REQUERIDA</span></div>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de progreso general
    st.markdown("<h4 style='font-size: 1.1rem; color: var(--text-faded); margin-top: 3rem; margin-bottom: 1.5rem;'>GAUGE_PERFORMANCE_ANALYSIS</h4>", unsafe_allow_html=True)
    
    if 'porcentaje' in resultados['general']:
        porcentaje_general = resultados['general']['porcentaje']
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=porcentaje_general,
            number={'suffix': "%", 'font': {'size': 60, 'family': 'Inter, sans-serif', 'color': '#0f172a'}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#94a3b8"},
                'bar': {'color': "#0058be", 'thickness': 0.3},
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
            margin=dict(l=30, r=30, t=50, b=20)
        )
        
        st.plotly_chart(fig_gauge, width='stretch', config={'displayModeBar': False})
    
    # Gráfico de cumplimiento por área
    st.markdown("<h3 style='margin-top: 4rem; margin-bottom: 1.5rem;'><span class='material-symbols-outlined icon'>leaderboard</span> Cumplimiento por Área de Gestión</h3>", unsafe_allow_html=True)
    
    areas = []
    porcentajes = []
    
    for aspecto, data in resultados['pa'].items():
        if 'porcentaje_aspecto' in data:
            areas.append(f"PA: {aspecto}")
            porcentajes.append(data['porcentaje_aspecto'])
    
    for aspecto, data in resultados['po'].items():
        if 'porcentaje_aspecto' in data:
            areas.append(f"PO: {aspecto}")
            porcentajes.append(data['porcentaje_aspecto'])
    
    if areas:
        fig = go.Figure(data=[
            go.Bar(
                x=porcentajes,
                y=areas,
                orientation='h',
                marker=dict(color='#0058be', line=dict(color='white', width=1)),
                text=[f"{p:.1f}%" for p in porcentajes],
                textposition='auto',
                textfont=dict(size=12, color='white', family='Inter, sans-serif'),
                hovertemplate='<b>%{y}</b><br>Cumplimiento: <b>%{x:.1f}%</b><extra></extra>',
            )
        ])
        
        fig.update_layout(
            xaxis=dict(range=[0, 105], gridcolor='#f1f5f9', showgrid=True, zeroline=False),
            yaxis=dict(gridcolor='#f1f5f9'),
            height=400 + len(areas) * 20,
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=20, b=20),
            font=dict(family='Inter, sans-serif', color='#0f172a'),
        )
        
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # Tabla de resultados detallados
    st.markdown("<h4 style='font-size: 1.1rem; color: var(--text-faded); margin-top: 4rem; margin-bottom: 1.5rem;'>DETAILED_AUDIT_LOGS</h4>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Proceso Administrativo", "Proceso Operativo"])
    
    with tab1:
        for aspecto, elementos_data in resultados['pa'].items():
            st.markdown(f"<div style='margin-top: 1.5rem; color: var(--primary-accent); font-weight: 800; font-size: 0.9rem;'>{aspecto.upper()}</div>", unsafe_allow_html=True)
            
            tabla_data = []
            for elemento, data in elementos_data.items():
                if elemento != 'promedio_aspecto' and elemento != 'porcentaje_aspecto':
                    tabla_data.append({
                        'Elemento': elemento,
                        'Cumplimiento': f"{data['porcentaje']:.1f}%",
                        'Prioridad': data['prioridad']
                    })
            
            if tabla_data:
                df = pd.DataFrame(tabla_data)
                st.dataframe(df, width='stretch', hide_index=True)
    
    with tab2:
        for aspecto, elementos_data in resultados['po'].items():
            st.markdown(f"<div style='margin-top: 1.5rem; color: var(--primary-accent); font-weight: 800; font-size: 0.9rem;'>{aspecto.upper()}</div>", unsafe_allow_html=True)
            
            tabla_data = []
            for elemento, data in elementos_data.items():
                if elemento != 'promedio_aspecto' and elemento != 'porcentaje_aspecto':
                    tabla_data.append({
                        'Elemento': elemento,
                        'Cumplimiento': f"{data['porcentaje']:.1f}%",
                        'Prioridad': data['prioridad']
                    })
            
            if tabla_data:
                df = pd.DataFrame(tabla_data)
                st.dataframe(df, width='stretch', hide_index=True)

def mostrar_prioridades():
    """Muestra las prioridades de intervención con estética profesional"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>flag</span> Análisis de Prioridades de Intervención</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay evaluaciones registradas. Por favor complete al menos una evaluación.")
        return
    
    st.markdown("""
    <div class="bento-card" style="border-left: 6px solid var(--primary-accent); background: #f8fafc;">
        <h4 style="margin-top:0; margin-bottom: 1rem; color: var(--primary);">Protocolos de Priorización Estándar</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem;">
            <div style="padding: 1rem; border: 1px solid #ffe4e6; border-radius: 8px; background: white;">
                <span class="badge badge-error">CRÍTICO (< 60%)</span>
                <p style="font-size: 0.8rem; color: #9f1239; margin-top: 0.5rem; font-weight: 600;">ACCIÓN INMEDIATA</p>
            </div>
            <div style="padding: 1rem; border: 1px solid #fef3c7; border-radius: 8px; background: white;">
                <span class="badge badge-warning">ALERTA (60-74%)</span>
                <p style="font-size: 0.8rem; color: #92400e; margin-top: 0.5rem; font-weight: 600;">PLANIFICACIÓN</p>
            </div>
            <div style="padding: 1rem; border: 1px solid #d1fae5; border-radius: 8px; background: white;">
                <span class="badge badge-success">ESTABLE (≥ 75%)</span>
                <p style="font-size: 0.8rem; color: #065f46; margin-top: 0.5rem; font-weight: 600;">MANTENIMIENTO</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    resultados = calcular_resultados()
    
    # Agrupar por prioridad
    prioridad_alta = []
    prioridad_media = []
    prioridad_baja = []
    
    for tipo_label, tipo_key in [('Administrativo', 'pa'), ('Operativo', 'po')]:
        for aspecto, elementos_data in resultados[tipo_key].items():
            for elemento, data in elementos_data.items():
                if elemento not in ['promedio_aspecto', 'porcentaje_aspecto']:
                    item = {
                        'Área': tipo_label,
                        'Aspecto': aspecto,
                        'Elemento': elemento,
                        'Cumplimiento': f"{data['porcentaje']:.1f}%",
                        'Prioridad': data['prioridad']
                    }
                    if data['prioridad'] == 'ALTA':
                        prioridad_alta.append(item)
                    elif data['prioridad'] == 'MEDIA':
                        prioridad_media.append(item)
                    else:
                        prioridad_baja.append(item)
    
    # Resumen Numérico
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='bento-card' style='text-align:center; border-bottom: 4px solid #e11d48;'><div class='metric-label'>Críticos</div><div class='metric-value' style='color:#e11d48;'>{len(prioridad_alta)}</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='bento-card' style='text-align:center; border-bottom: 4px solid #d97706;'><div class='metric-label'>Alertas</div><div class='metric-value' style='color:#d97706;'>{len(prioridad_media)}</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='bento-card' style='text-align:center; border-bottom: 4px solid #059669;'><div class='metric-label'>Estables</div><div class='metric-value' style='color:#059669;'>{len(prioridad_baja)}</div></div>", unsafe_allow_html=True)
    
    # Tabs detallados
    tab1, tab2, tab3 = st.tabs(["🔴 Críticos", "🟡 Alertas", "🟢 Estables"])
    
    with tab1:
        if prioridad_alta:
            st.dataframe(pd.DataFrame(prioridad_alta), width='stretch', hide_index=True)
        else:
            st.success("No se detectaron elementos críticos.")
            
    with tab2:
        if prioridad_media:
            st.dataframe(pd.DataFrame(prioridad_media), width='stretch', hide_index=True)
        else:
            st.info("No hay alertas pendientes.")

    with tab3:
        if prioridad_baja:
            st.dataframe(pd.DataFrame(prioridad_baja), width='stretch', hide_index=True)

    # Consultor Virtual GPP
    st.markdown("<h3 style='margin-top: 4rem; margin-bottom: 1.5rem;'><span class='material-symbols-outlined icon'>psychology</span> Consultor Virtual GPP</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #f1f5f9; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
        <p style="margin:0; font-size: 0.95rem; color: var(--text-muted);">Acciones estratégicas generadas a partir de las desviaciones detectadas en la auditoría.</p>
    </div>
    """, unsafe_allow_html=True)
    
    recoms = obtener_recomendaciones_criticas(resultados)
    if recoms:
        for r in recoms:
            color = "#e11d48" if r['Prioridad'] == "ALTA" else "#d97706"
            badge_class = "badge-error" if r['Prioridad'] == "ALTA" else "badge-warning"
            st.markdown(f"""
            <div class="bento-card" style="border-left: 5px solid {color}; padding: 1.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <strong style="color: var(--primary); font-size: 0.95rem;">{r['Aspecto']} > {r['Elemento']}</strong>
                    <span class="badge {badge_class}">{r['Prioridad']} ({r['Cumplimiento']})</span>
                </div>
                <div style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.6; background: #f8fafc; padding: 12px; border-radius: 4px; border: 1px solid #e2e8f0;">
                    {r['Recomendación']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🎉 No se requieren recomendaciones urgentes.")

def mostrar_plan_accion():
    """Muestra la gestión de compromisos y plan de acción profesional"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>task_alt</span> Plan de Acción y Seguimiento</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay evaluaciones activas. Por favor cargue una o realice un diagnóstico.")
        return

    st.markdown("""
    <div class="bento-card" style="border-left: 6px solid var(--success); background: #f0fdf4;">
        <h4 style="margin:0; color: #065f46;">Gestor de Compromisos Operativos</h4>
        <p style="color: #065f46; font-size: 0.9rem; margin-top: 4px;">Defina responsables y fechas límite para mitigar los riesgos detectados.</p>
    </div>
    """, unsafe_allow_html=True)

    # Proponer items desde las recomendaciones
    if not st.session_state.plan_accion:
        resultados = calcular_resultados()
        recoms = obtener_recomendaciones_criticas(resultados)
        for r in recoms:
            st.session_state.plan_accion.append({
                "Elemento": f"{r['Aspecto']} > {r['Elemento']}",
                "Acción Recomendada": r['Recomendación'],
                "Responsable": "",
                "Fecha Límite": datetime.now().strftime("%Y-%m-%d"),
                "Estado": "Pendiente"
            })

    df_plan = pd.DataFrame(st.session_state.plan_accion)
    
    if not df_plan.empty and 'Fecha Límite' in df_plan.columns:
        df_plan['Fecha Límite'] = pd.to_datetime(df_plan['Fecha Límite']).dt.date
    
    edited_df = st.data_editor(
        df_plan,
        column_config={
            "Estado": st.column_config.SelectboxColumn(
                "Estado",
                options=["Pendiente", "En Proceso", "Completado", "Cancelado"],
                required=True,
            ),
            "Fecha Límite": st.column_config.DateColumn(
                "Fecha Límite",
                format="YYYY-MM-DD",
                required=True,
            ),
        },
        width='stretch',
        num_rows="dynamic"
    )

    if st.button("Guardar Cambios en el Plan", type="primary"):
        res_df = edited_df.copy()
        if 'Fecha Límite' in res_df.columns:
            res_df['Fecha Límite'] = res_df['Fecha Límite'].astype(str)
        st.session_state.plan_accion = res_df.to_dict('records')
        st.success("✓ Plan de acción actualizado correctamente.")
        
    st.markdown("---")
    if not edited_df.empty:
        c1, c2, c3 = st.columns(3)
        stats = edited_df['Estado'].value_counts()
        c1.metric("Pendientes", stats.get("Pendiente", 0))
        c2.metric("En Proceso", stats.get("En Proceso", 0))
        c3.metric("Completados", stats.get("Completado", 0))

def calcular_resultados_compactos(pa_data, po_data):
    """Calcula el porcentaje global de cumplimiento a partir de datos crudos"""
    promedios = []
    
    # Procesar PA
    for aspecto, elementos in MATRIZ_PA.items():
        cals_aspecto = []
        for elemento, items in elementos.items():
            cals = []
            for i in range(len(items)):
                key = f"PA_{aspecto}_{elemento}_{i}"
                if key in pa_data and pa_data[key] > 0:
                    cals.append(pa_data[key])
            if cals:
                cals_aspecto.append(np.mean(cals))
        if cals_aspecto:
            promedios.append(np.mean(cals_aspecto))
            
    # Procesar PO
    for aspecto, elementos in MATRIZ_PO.items():
        cals_aspecto = []
        for elemento, items in elementos.items():
            cals = []
            for i in range(len(items)):
                key = f"PO_{aspecto}_{elemento}_{i}"
                if key in po_data and po_data[key] > 0:
                    cals.append(po_data[key])
            if cals:
                cals_aspecto.append(np.mean(cals))
        if cals_aspecto:
            promedios.append(np.mean(cals_aspecto))
            
    if promedios:
        return (np.mean(promedios) / 5) * 100
    return 0

def mostrar_benchmarking():
    """Muestra el tablero comparativo multisitio profesional"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>language</span> Inteligencia Multisitio</h3>", unsafe_allow_html=True)
    
    archivos = [f for f in os.listdir('data') if f.endswith('.json')]
    if not archivos:
        st.info("No hay suficientes auditorías en el historial para realizar un benchmarking.")
        return

    datos_comparativos = []
    for arc in archivos:
        try:
            with open(os.path.join('data', arc), 'r', encoding='utf-8') as f:
                d = json.load(f)
                cumplimiento = calcular_resultados_compactos(
                    d.get('evaluaciones_pa', {}), 
                    d.get('evaluaciones_po', {})
                )
                datos_comparativos.append({
                    'Establecimiento': d.get('nombre_establecimiento', 'Sin Nombre'),
                    'Fecha': d.get('fecha', 'Desconocida'),
                    'Cumplimiento %': cumplimiento,
                    'Estado': "Óptimo" if cumplimiento >= 75 else "Alerta" if cumplimiento >= 60 else "Crítico"
                })
        except Exception as e:
            st.warning(f"⚠️ No se pudo procesar {arc}: {e}")
            continue

    if not datos_comparativos:
        st.warning("No se pudo procesar la información del historial.")
        return

    df_bench = pd.DataFrame(datos_comparativos)
    df_bench = df_bench.sort_values(by='Cumplimiento %', ascending=False)

    st.markdown("""
    <div class="hero-banner" style="padding: 2.5rem; background: #f8fafc;">
        <h4 style="margin:0; color: var(--primary);">Comparativa de Red de Establecimientos</h4>
        <p style="color: var(--text-faded); font-size: 0.9rem; margin-top: 4px;">Visualice el desempeño relativo de todas las sedes auditadas.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            df_bench, 
            x='Cumplimiento %', 
            y='Establecimiento', 
            orientation='h',
            color='Cumplimiento %',
            color_continuous_scale='RdYlGn',
            range_color=[40, 90],
            text_auto='.1f',
        )
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.markdown("<div style='margin-bottom: 1.5rem; font-weight: 800; font-size: 0.8rem; color: var(--text-faded);'>TOP_PERFORMERS</div>", unsafe_allow_html=True)
        for i, row in df_bench.head(3).iterrows():
            st.markdown(f"""
            <div style="padding: 10px; background: white; border: 1px solid #d1fae5; border-radius: 6px; margin-bottom: 8px;">
                <div style="font-size: 0.85rem; font-weight: 700;">{row['Establecimiento']}</div>
                <div style="color: #059669; font-weight: 800;">{row['Cumplimiento %']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 2rem; margin-bottom: 1rem; font-weight: 800; font-size: 0.8rem; color: var(--text-faded);'>REQUEREN_ATENCIÓN</div>", unsafe_allow_html=True)
        for i, row in df_bench.tail(2).iterrows():
            if row['Cumplimiento %'] < 60:
                st.markdown(f"""
                <div style="padding: 10px; background: white; border: 1px solid #ffe4e6; border-radius: 6px; margin-bottom: 8px;">
                    <div style="font-size: 0.85rem; font-weight: 700;">{row['Establecimiento']}</div>
                    <div style="color: #e11d48; font-weight: 800;">{row['Cumplimiento %']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("#### Detalle Transversal de Auditoría")
    st.dataframe(df_bench, width='stretch', hide_index=True)

def mostrar_historial():
    """Muestra el historial de evaluaciones guardadas profesionalmente"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>history</span> Historial de Evaluaciones</h3>", unsafe_allow_html=True)
    
    if not os.path.exists('data'):
        os.makedirs('data')
        
    archivos = [f for f in os.listdir('data') if f.endswith('.json')]
    
    if not archivos:
        st.info("No se encontraron registros de auditoría en el sistema.")
        return

    historial_data = []
    for arc in archivos:
        try:
            with open(os.path.join('data', arc), 'r', encoding='utf-8') as f:
                datos = json.load(f)
                historial_data.append({
                    'Establecimiento': datos.get('nombre_establecimiento', 'Sin nombre'),
                    'Fecha': datos.get('fecha', 'Desconocida'),
                    'Archivo': arc,
                    'fecha_dt': datetime.strptime(datos.get('fecha', '1970-01-01'), "%Y-%m-%d %H:%M:%S") if datos.get('fecha') else datetime.min
                })
        except Exception as e:
            st.warning(f"⚠️ No se pudo cargar {arc}: {e}")
            continue
    
    historial_data.sort(key=lambda x: x['fecha_dt'], reverse=True)

    for item in historial_data:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"<div style='font-weight: 700; color: var(--primary);'>{item['Establecimiento']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<div style='font-size: 0.8rem; color: var(--text-faded); display: flex; align-items: center; gap: 4px;'><span class='material-symbols-outlined' style='font-size: 1rem;'>calendar_today</span> {item['Fecha']}</div>", unsafe_allow_html=True)
            with col3:
                if st.button("Cargar", key=f"btn_load_{item['Archivo']}", width='stretch'):
                    cargar_evaluacion(os.path.join('data', item['Archivo']))
                    st.success("✓ Datos cargados.")
                    st.rerun()
            st.markdown("<div style='height: 1px; background: #e2e8f0; margin: 15px 0;'></div>", unsafe_allow_html=True)

def mostrar_guardar_cargar():
    """Muestra opciones para guardar la evaluación actual con estética profesional"""
    st.markdown("<h3 style='margin-bottom: 2rem;'><span class='material-symbols-outlined icon'>save</span> Gestión de Archivo y Exportación</h3>", unsafe_allow_html=True)
    
    if not st.session_state.evaluaciones_pa and not st.session_state.evaluaciones_po:
        st.warning("⚠️ No hay datos activos para procesar. Realice un diagnóstico primero.")
        return

    st.markdown("""
    <div class="bento-card" style="background: #f8fafc;">
        <h4 style="margin:0; color: var(--primary);">Persistencia de Auditoría</h4>
        <p style="color: var(--text-faded); font-size: 0.9rem; margin-top: 4px;">Asigne un identificador único para almacenar esta sesión en el historial del servidor.</p>
    </div>
    """, unsafe_allow_html=True)

    nombre = st.text_input("Nombre del Establecimiento / Unidad de Negocio", 
                          value=st.session_state.nombre_establecimiento,
                          placeholder="Ej: Sede Principal - Auditoría 2026")
    
    if st.button("💾 Guardar Sesión en Servidor", type="primary", width='stretch'):
        if nombre.strip() == "":
            st.error("Se requiere un nombre de establecimiento válido.")
        else:
            guardar_evaluacion(nombre)
            st.session_state.nombre_establecimiento = nombre
            st.success("✓ Sesión almacenada exitosamente.")
            st.balloons()

    st.markdown("<h4 style='margin-top: 3rem; margin-bottom: 1.5rem;'>Exportación de Datos Legados</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Exportar a Microsoft Excel", width='stretch'):
            try:
                resultados = calcular_resultados()
                archivo_excel = f"resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                    resumen_data = []
                    for tipo_l, tipo_k in [('Administrativo', 'pa'), ('Operativo', 'po')]:
                        for aspecto, data in resultados[tipo_k].items():
                            if 'porcentaje_aspecto' in data:
                                resumen_data.append({
                                    'Área': tipo_l,
                                    'Aspecto': aspecto,
                                    'Cumplimiento (%)': data['porcentaje_aspecto']
                                })
                    pd.DataFrame(resumen_data).to_excel(writer, sheet_name='Resumen', index=False)
                st.success("✓ Archivo Excel generado.")
            except Exception as e:
                st.error(f"Falla en exportación Excel: {e}")
    
    with col2:
        st.info("Para reportes profesionales, utilice el botón 'Descargar Reporte PDF' en la pestaña de Resultados Generales.")

if __name__ == "__main__":
    main()

