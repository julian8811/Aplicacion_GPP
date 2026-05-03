# Diccionario maestro de recomendaciones estratégicas
MATRIZ_RECOMENDACIONES = {
    "PLANEACIÓN": {
        "Análisis del contexto": "Implementar un análisis PESTEL y DOFA formal cada 6 meses involucrando a los líderes de área.",
        "Existencia de un plan estratégico": "Definir objetivos SMART y socializar la visión empresarial mediante talleres de alineación cultural."
    },
    "ORGANIZACIÓN": {
        "Existencia de una estructura organizativa": "Actualizar el organigrama y definir claramente las líneas de reporte para evitar duplicidad de mando.",
        "Departamentalización": "Agrupar actividades por procesos lógicos y asignar dueños de proceso con autoridad de decisión.",
        "Procesos documentados": "Iniciar la estandarización de procesos críticos (compras, producción) mediante flujogramas y perfiles de cargo.",
        "Ciclo PHVA": "Establecer reuniones de mejora continua para analizar desviaciones y ajustar planes operativos."
    },
    "DIRECCIÓN": {
        "Liderazgo organizacional": "Desarrollar un programa de capacitación en liderazgo situacional para supervisores y jefes de cocina.",
        "Canales de comunicación efectivos": "Implementar un tablero de gestión visual (Obeya) y herramientas digitales de comunicación interna.",
        "Cultura organizacional": "Crear un programa de incentivos no monetarios y reforzar el sentido de pertenencia con actividades de Team Building."
    },
    "CONTROL": {
        "Sistemas de control": "Implementar un Cuadro de Mando Integral (Balanced Scorecard) con indicadores financieros y operativos.",
        "Auditorías internas": "Programar auditorías cruzadas entre departamentos para asegurar la objetividad en las revisiones.",
        "Acciones correctivas y preventivas": "Documentar cada falla mediante el método de los 5 Porqués para eliminar la causa raíz."
    },
    "LOGÍSTICA DE COMPRAS": {
        "Logística de entrada": "Homologar proveedores y establecer acuerdos de nivel de servicio (SLA) para insumos críticos.",
        "Gestión de inventarios": "Implementar un software de gestión de inventarios con alertas de stock mínimo y control PEPS riguroso."
    },
    "GESTIÓN DE PRODUCCIÓN": {
        "Equipos": "Establecer un plan de mantenimiento preventivo anual y renovar equipos con baja eficiencia energética.",
        "Infraestructura": "Rediseñar el flujo de la cocina bajo el principio de 'Marcha Adelante' para evitar contaminaciones cruzadas.",
        "Distribución de los procesos (flujo)": "Señalizar áreas de trabajo y optimizar el layout para reducir tiempos de desplazamiento del personal.",
        "Planeación de la producción": "Implementar fichas técnicas estandarizadas con costeo real para cada plato del menú.",
        "Materia prima": "Fortalecer la inspección de recibo de mercancía con termómetros y listas de chequeo de calidad.",
        "Control de la producción": "Digitalizar el registro de tiempos y temperaturas durante el servicio para asegurar inocuidad."
    },
    "LOGÍSTICA EXTERNA": {
        "Distribución": "Implementar encuestas de satisfacción digitales (NPS) y protocolos de recuperación de servicios fallidos."
    }
}

def obtener_recomendaciones_criticas(resultados):
    """Filtra las recomendaciones para elementos con prioridad ALTA o MEDIA"""
    recomendaciones = []
    
    for tipo in ['pa', 'po']:
        for aspecto, elementos_data in resultados[tipo].items():
            for elemento, data in elementos_data.items():
                if elemento in MATRIZ_RECOMENDACIONES.get(aspecto, {}):
                    if data['prioridad'] in ['ALTA', 'MEDIA']:
                        recomendaciones.append({
                            'Aspecto': aspecto,
                            'Elemento': elemento,
                            'Cumplimiento': f"{data['porcentaje']:.1f}%",
                            'Recomendación': MATRIZ_RECOMENDACIONES[aspecto][elemento],
                            'Prioridad': data['prioridad']
                        })
                elif elemento not in ['promedio_aspecto', 'porcentaje_aspecto']:
                    # Aspecto sin recomendaciones definidas - logging silencioso para debug
                    pass
    
    return recomendaciones
