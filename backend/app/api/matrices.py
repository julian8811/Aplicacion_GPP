from fastapi import APIRouter

router = APIRouter(prefix="/matrices", tags=["matrices"])

# Matrix structure from original app.py
MATRIZ_PA = {
    "PLANEACIÓN": {
        "Análisis del contexto": [
            {"id": "PA_PLANEACIÓN_Análisis del contexto_0", "pregunta": "¿La empresa realiza un análisis externo como base para su planeación estratégica?", "contexto": "Evaluación de factores fuera de la empresa (mercado, competencia, economía, leyes) que pueden afectar el negocio."},
            {"id": "PA_PLANEACIÓN_Análisis del contexto_1", "pregunta": "¿La empresa realiza un análisis interno como base para su planeación estratégica?", "contexto": "Revisión de las capacidades propias (recursos humanos, financieros, tecnológicos) para identificar fortalezas y debilidades."},
            {"id": "PA_PLANEACIÓN_Análisis del contexto_2", "pregunta": "Aplicación de herramientas de análisis como la matriz DOFA, PESTEL, Las 5 Fuerzas de Porter, Benchmarking, entre otras", "contexto": "Uso de métodos formales para estructurar la información obtenida en los análisis internos y externos."}
        ],
        "Existencia de un plan estratégico": [
            {"id": "PA_PLANEACIÓN_Existencia de un plan estratégico_0", "pregunta": "En qué medida considera que la misión de la empresa está claramente definida y comunicada a todos los miembros de la organización", "contexto": "Claridad sobre la razón de ser de la empresa y si todos los empleados la conocen."},
            {"id": "PA_PLANEACIÓN_Existencia de un plan estratégico_1", "pregunta": "En qué medida considera que la visión de la empresa está claramente definida y comunicada a todos los miembros de la organización", "contexto": "Claridad sobre dónde quiere llegar la empresa en el futuro y si esta meta es compartida."},
            {"id": "PA_PLANEACIÓN_Existencia de un plan estratégico_2", "pregunta": "En qué medida considera que el establecimiento tiene definidos y comunicados sus objetivos estratégicos", "contexto": "Metas específicas y medibles que la organización se ha propuesto alcanzar."},
            {"id": "PA_PLANEACIÓN_Existencia de un plan estratégico_3", "pregunta": "Documento que evidencie el plan estratégico a largo o mediano plazo", "contexto": "Existencia física o digital de un plan que guíe las acciones de la empresa."}
        ],
        "Estructura organizativa": [
            {"id": "PA_PLANEACIÓN_Estructura organizativa_0", "pregunta": "¿El establecimiento cuenta con un organigrama claramente definido?", "contexto": "Representación gráfica de la estructura jerárquica y las relaciones entre departamentos."}
        ],
        "Departamentalización": [
            {"id": "PA_PLANEACIÓN_Departamentalización_0", "pregunta": "¿Se tienen claramente identificados los procesos de la organización?", "contexto": "División de las actividades en procesos lógicos (compras, ventas, producción, etc.) para una mejor gestión."}
        ],
        "Procesos documentados": [
            {"id": "PA_PLANEACIÓN_Procesos documentados_0", "pregunta": "¿Existen perfiles de cargo definidos para cada función?", "contexto": "Descripción clara de las responsabilidades, requisitos y habilidades necesarias para cada puesto de trabajo."},
            {"id": "PA_PLANEACIÓN_Procesos documentados_1", "pregunta": "¿El establecimiento tiene debidamente documentado cada proceso (mapas de proceso, flujogramas, procedimientos, normas, etc)?", "contexto": "Guías escritas que explican paso a paso cómo se deben realizar las tareas para asegurar la consistencia."},
            {"id": "PA_PLANEACIÓN_Procesos documentados_2", "pregunta": "¿El establecimiento tiene caracterizado los procesos?", "contexto": "Definición de entradas, salidas, responsables, recursos y controles de cada proceso específico."}
        ],
        "Ciclo PHVA": [
            {"id": "PA_PLANEACIÓN_Ciclo PHVA_0", "pregunta": "¿Tiene implementado el ciclo PHVA (Planear, Hacer, Verificar, Actuar) en el establecimiento?", "contexto": "Método de mejora continua que asegura que los procesos se planifican, se ejecutan, se miden y se corrigen."}
        ]
    },
    "ORGANIZACIÓN": {
        "Existencia de una estructura organizativa": [
            {"id": "PA_ORGANIZACIÓN_Existencia de una estructura organizativa_0", "pregunta": "¿La empresa cuenta con un organigrama actualizado?", "contexto": "Verificar que el organigrama refleje la estructura actual de la empresa y esté disponible para todos los empleados.", "aspecto": "ORGANIZACIÓN", "peso": 1},
            {"id": "PA_ORGANIZACIÓN_Existencia de una estructura organizativa_1", "pregunta": "¿Se publican y comunican las funciones y responsabilidades de cada puesto?", "contexto": "Asegurar que cada empleado conoce sus responsabilidades y a quién reporta dentro de la organización.", "aspecto": "ORGANIZACIÓN", "peso": 1},
            {"id": "PA_ORGANIZACIÓN_Existencia de una estructura organizativa_2", "pregunta": "¿Se realizan descripciones de puestos documentadas?", "contexto": "Contar con documentos formalizados que describan las funciones, requisitos y competencias de cada cargo.", "aspecto": "ORGANIZACIÓN", "peso": 1}
        ],
        "Departamentalización": [
            {"id": "PA_ORGANIZACIÓN_Departamentalización_0", "pregunta": "¿La empresa tiene claramente identificados los procesos por departamento?", "contexto": "Verificar que existen descripciones de procesos por área funcional (compras, ventas, producción, etc.).", "aspecto": "ORGANIZACIÓN", "peso": 1}
        ],
        "Procesos documentados": [
            {"id": "PA_ORGANIZACIÓN_Procesos documentados_0", "pregunta": "¿Existen perfiles de cargo definidos para cada función?", "contexto": "Descripción clara de las responsabilidades, requisitos y habilidades necesarias para cada puesto de trabajo.", "aspecto": "ORGANIZACIÓN", "peso": 1}
        ]
    },
    "DIRECCIÓN": {
        "Liderazgo organizacional": [
            {"id": "PA_DIRECCIÓN_Liderazgo organizacional_0", "pregunta": "¿La alta dirección demuestra compromiso con la calidad?", "contexto": "Verificar que la dirección establece políticas de calidad y participa activamente en su implementación.", "aspecto": "DIRECCIÓN", "peso": 1},
            {"id": "PA_DIRECCIÓN_Liderazgo organizacional_1", "pregunta": "¿Se establecen políticas y objetivos de calidad claros?", "contexto": "Asegurar que existen políticas documentadas y objetivos medibles en materia de calidad.", "aspecto": "DIRECCIÓN", "peso": 1},
            {"id": "PA_DIRECCIÓN_Liderazgo organizacional_2", "pregunta": "¿Se revisa periódicamente el desempeño de la calidad?", "contexto": "Verificar que la dirección realiza reuniones periódicas para evaluar indicadores de calidad.", "aspecto": "DIRECCIÓN", "peso": 1}
        ],
        "Canales de comunicación efectivos": [
            {"id": "PA_DIRECCIÓN_Canales de comunicación efectivos_0", "pregunta": "¿La empresa cuenta con canales de comunicación interna efectivos?", "contexto": "Verificar que existen mecanismos para comunicar decisiones y novedades a todo el personal.", "aspecto": "DIRECCIÓN", "peso": 1}
        ],
        "Cultura organizacional": [
            {"id": "PA_DIRECCIÓN_Cultura organizacional_0", "pregunta": "¿Se promueve una cultura de mejora continua en la organización?", "contexto": "Verificar que existen programas de reconocimiento y motivación del personal.", "aspecto": "DIRECCIÓN", "peso": 1}
        ]
    },
    "CONTROL": {
        "Sistemas de control": [
            {"id": "PA_CONTROL_Sistemas de control_0", "pregunta": "¿Se realizan auditorías internas de calidad?", "contexto": "Verificar que existen programas de auditorías internas para evaluar el cumplimiento de procesos.", "aspecto": "CONTROL", "peso": 1},
            {"id": "PA_CONTROL_Sistemas de control_1", "pregunta": "¿Se registran y analizan los productos no conformes?", "contexto": "Asegurar que existe un procedimiento para identificar, registrar y corregir productos fuera de especificación.", "aspecto": "CONTROL", "peso": 1},
            {"id": "PA_CONTROL_Sistemas de control_2", "pregunta": "¿Se implementan acciones correctivas y preventivas?", "contexto": "Verificar que se documentan las acciones tomadas para eliminar las causas de no conformidades.", "aspecto": "CONTROL", "peso": 1}
        ],
        "Auditorías internas": [
            {"id": "PA_CONTROL_Auditorías internas_0", "pregunta": "¿Se realizan auditorías internas de calidad?", "contexto": "Verificar que existe un programa formal de auditorías internas documentadas.", "aspecto": "CONTROL", "peso": 1}
        ],
        "Acciones correctivas y preventivas": [
            {"id": "PA_CONTROL_Acciones correctivas y preventivas_0", "pregunta": "¿Se implementan acciones correctivas y preventivas?", "contexto": "Verificar que existe un procedimiento documentado para gestionar no conformidades.", "aspecto": "CONTROL", "peso": 1}
        ]
    }
}

MATRIZ_PO = {
    "LOGÍSTICA DE COMPRAS": {
        "Logística de entrada": [
            {"id": "PO_LOGÍSTICA DE COMPRAS_Logística de entrada_0", "pregunta": "¿Se cuenta con proveedores homologados para los insumos críticos?", "contexto": "Verificar que existe un proceso formal de evaluación y selección de proveedores.", "aspecto": "LOGÍSTICA DE COMPRAS", "peso": 1},
            {"id": "PO_LOGÍSTICA DE COMPRAS_Logística de entrada_1", "pregunta": "¿Se establecen acuerdos de nivel de servicio (SLA) con proveedores?", "contexto": "Verificar que existen contratos formales con indicadores de desempeño definidos.", "aspecto": "LOGÍSTICA DE COMPRAS", "peso": 1}
        ],
        "Gestión de inventarios": [
            {"id": "PO_LOGÍSTICA DE COMPRAS_Gestión de inventarios_0", "pregunta": "¿Se cuenta con un sistema de control de inventarios?", "contexto": "Verificar que existe un registro actualizado de existencias con método PEPS.", "aspecto": "LOGÍSTICA DE COMPRAS", "peso": 1}
        ]
    },
    "GESTIÓN DE PRODUCCIÓN": {
        "Equipos": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Equipos_0", "pregunta": "¿Se cuenta con un plan de mantenimiento preventivo de equipos?", "contexto": "Verificar que existe un cronograma documentado de mantenimiento de equipos.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ],
        "Infraestructura": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Infraestructura_0", "pregunta": "¿La infraestructura cumple con las normas de inocuidad alimentaria?", "contexto": "Verificar que las instalaciones cumplen con los requisitos legales de higiene y seguridad.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ],
        "Distribución de los procesos (flujo)": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Distribución de los procesos (flujo)_0", "pregunta": "¿Se tiene un layout de producción que evita contaminaciones cruzadas?", "contexto": "Verificar que la distribución de áreas sigue el principio de 'marcha adelante'.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ],
        "Planeación de la producción": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Planeación de la producción_0", "pregunta": "¿Se realizan fichas técnicas para los productos elaborados?", "contexto": "Verificar que existen documentos con recetas, ingredientes y procedimientos estandarizados.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ],
        "Materia prima": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Materia prima_0", "pregunta": "¿Se realiza inspección de calidad en la recepción de materia prima?", "contexto": "Verificar que existen listas de chequeo para la verificación de insumos recibidos.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ],
        "Control de la producción": [
            {"id": "PO_GESTIÓN DE PRODUCCIÓN_Control de la producción_0", "pregunta": "¿Se registran tiempos y temperaturas durante el proceso de producción?", "contexto": "Verificar que existen registros documentados de condiciones críticas de producción.", "aspecto": "GESTIÓN DE PRODUCCIÓN", "peso": 1}
        ]
    },
    "LOGÍSTICA EXTERNA": {
        "Distribución": [
            {"id": "PO_LOGÍSTICA EXTERNA_Distribución_0", "pregunta": "¿Se cuenta con protocolos de distribución que garantizan la calidad del producto?", "contexto": "Verificar que existen procedimientos para el transporte y entrega de productos.", "aspecto": "LOGÍSTICA EXTERNA", "peso": 1},
            {"id": "PO_LOGÍSTICA EXTERNA_Distribución_1", "pregunta": "¿Se implementan encuestas de satisfacción al cliente?", "contexto": "Verificar que existe un sistema para conocer la percepción del cliente sobre el servicio.", "aspecto": "LOGÍSTICA EXTERNA", "peso": 1}
        ]
    }
}


@router.get("")
async def get_matrices():
    """Get PA and PO evaluation matrices (no auth required)"""
    return {
        "PA": MATRIZ_PA,
        "PO": MATRIZ_PO
    }