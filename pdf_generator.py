from fpdf import FPDF

def normalizar_texto(texto):
    """Limpia el texto para compatibilidad con fuentes estándar de PDF (latin-1)"""
    if not texto:
        return ""
    # Mapeo manual de caracteres comunes en español
    replacements = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N', '¿': '', '¡': ''
    }
    for char, replacement in replacements.items():
        texto = texto.replace(char, replacement)
    return texto

class GPP_PDF(FPDF):
    def header(self):
        # Fondo del encabezado
        self.set_fill_color(15, 23, 42) # Azul oscuro profundo (Slate 900)
        self.rect(0, 0, 210, 45, 'F')
        
        self.set_font('helvetica', 'B', 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 25, 'GPP_CORE | AUDIT REPORT', ln=True, align='C')
        
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(148, 163, 184) # Slate 400
        self.cell(0, -5, 'SISTEMA DE EVALUACION DE GESTION POR PROCESOS', ln=True, align='C')
        self.ln(25)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 116, 139) # Slate 500
        self.cell(0, 10, f'Pagina {self.page_no()} | GPP_CORE Engine v2.6.0 | Empresa Segura, Proceso Eficiente', align='C')

def crear_pdf_auditoria(nombre_est, fecha, resultados, evaluaciones_pa, evaluaciones_po, matriz_pa, matriz_po):
    pdf = GPP_PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Resumen Ejecutivo
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, f'Resumen de Auditoria: {normalizar_texto(nombre_est)}', ln=True)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 10, f'Fecha de Evaluacion: {fecha}', ln=True)
    pdf.ln(5)
    
    # Índice de Salud Global
    porcentaje_global = resultados['general'].get('porcentaje', 0)
    promedio_global = resultados['general'].get('promedio', 0)
    
    pdf.set_fill_color(248, 250, 252) # Slate 50
    pdf.rect(10, pdf.get_y(), 190, 35, 'F')
    pdf.set_draw_color(226, 232, 240) # Slate 200
    pdf.rect(10, pdf.get_y(), 190, 35, 'D')
    
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_text_color(71, 85, 105) # Slate 600
    pdf.cell(95, 10, '   INDICE DE SALUD GLOBAL', align='L')
    
    pdf.set_font('helvetica', 'B', 24)
    pdf.set_text_color(0, 88, 190)
    pdf.cell(85, 10, f'{porcentaje_global:.1f}%', align='R', ln=True)
    
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(95, 10, f'   Calificacion Media: {promedio_global:.2f} / 5.0', align='L')
    
    estado = "CRITICO" if porcentaje_global < 60 else "ALERTA" if porcentaje_global < 75 else "OPTIMO"
    color_estado = (185, 28, 28) if estado == "CRITICO" else (180, 83, 9) if estado == "ALERTA" else (4, 120, 87)
    
    pdf.set_text_color(*color_estado)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(85, 10, f'ESTADO: {estado}   ', align='R', ln=True)
    
    pdf.ln(15)
    
    # Desglose por Áreas (Resumen)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, 'Desglose por Areas de Gestion', ln=True)
    pdf.ln(2)
    
    # Tabla de resultados resumida
    pdf.set_fill_color(51, 65, 85) # Slate 700
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(80, 10, ' AREA / ASPECTO', 1, 0, 'L', True)
    pdf.cell(40, 10, 'CUMPLIMIENTO', 1, 0, 'C', True)
    pdf.cell(70, 10, 'PRIORIDAD', 1, 1, 'C', True)
    
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.set_font('helvetica', '', 8)
    
    for tipo, label in [('pa', 'Administrativo'), ('po', 'Operativo')]:
        for aspecto, data in resultados[tipo].items():
            if 'porcentaje_aspecto' in data:
                pdf.cell(80, 8, f' {label}: {normalizar_texto(aspecto)}', 1)
                pdf.cell(40, 8, f"{data['porcentaje_aspecto']:.1f}%", 1, 0, 'C')
                
                prioridad = "BAJA" if data['porcentaje_aspecto'] >= 75 else "MEDIA" if data['porcentaje_aspecto'] >= 60 else "ALTA"
                pdf.cell(70, 8, prioridad, 1, 1, 'C')

    pdf.ln(10)
    
    # Hallazgos Críticos
    pdf.set_font('helvetica', 'B', 13)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(0, 10, 'Hallazgos Criticos (Atencion Prioritaria)', ln=True)
    pdf.ln(2)
    
    criticos = []
    for tipo in ['pa', 'po']:
        for aspecto, elementos_data in resultados[tipo].items():
            for elemento, data in elementos_data.items():
                if elemento not in ['promedio_aspecto', 'porcentaje_aspecto'] and data['prioridad'] == 'ALTA':
                    criticos.append(f"{aspecto}: {elemento} ({data['porcentaje']:.1f}%)")
    
    pdf.set_text_color(15, 23, 42)
    if not criticos:
        pdf.set_font('helvetica', 'I', 9)
        pdf.cell(0, 10, 'No se detectaron hallazgos criticos en esta auditoria.', ln=True)
    else:
        pdf.set_font('helvetica', '', 8)
        for c in criticos:
            pdf.multi_cell(0, 6, f'- {normalizar_texto(c)}', border=0)
            pdf.ln(1)

    # DETALLES COMPLETOS
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 15)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, 'Evidencia Detallada del Analisis', ln=True)
    pdf.ln(5)

    def agregar_detalle_proceso(pdf, matriz, evaluaciones, prefijo, titulo):
        pdf.set_font('helvetica', 'B', 11)
        pdf.set_fill_color(241, 245, 249)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 10, f' {titulo}', 0, 1, 'L', True)
        pdf.ln(3)

        for aspecto, elementos in matriz.items():
            # Título de Aspecto
            pdf.set_font('helvetica', 'B', 9)
            pdf.set_text_color(0, 88, 190)
            pdf.cell(0, 8, f' Aspecto: {normalizar_texto(aspecto)}', ln=True)
            pdf.set_text_color(15, 23, 42)
            
            for elemento, items in elementos.items():
                # Título de Elemento
                pdf.set_font('helvetica', 'B', 8)
                pdf.set_fill_color(248, 250, 252)
                pdf.cell(0, 6, f'   Elemento: {normalizar_texto(elemento)}', ln=True, fill=True)
                
                for i, item in enumerate(items):
                    key = f"{prefijo}_{aspecto}_{elemento}_{i}"
                    calificacion = evaluaciones.get(key, 0)
                    
                    # Dibujar pregunta con control de desbordamiento
                    pdf.set_font('helvetica', '', 8)
                    pdf.set_text_color(71, 85, 105)
                    
                    # Guardar posición actual
                    y_start = pdf.get_y()
                    
                    # Texto normalizado
                    p_txt = normalizar_texto(item['pregunta'])
                    
                    # Multi-cell para la pregunta (ancho 150)
                    pdf.set_x(15)
                    pdf.multi_cell(155, 5, f"- {p_txt}", border=0)
                    y_end = pdf.get_y()
                    
                    # Dibujar calificación al lado (alineado al tope de la pregunta)
                    pdf.set_xy(175, y_start)
                    pdf.set_font('helvetica', 'B', 8)
                    pdf.set_text_color(15, 23, 42)
                    pdf.cell(20, 5, f"Ptos: {calificacion}", align='R', ln=True)
                    
                    # Volver al final del bloque para la siguiente pregunta
                    pdf.set_y(y_end + 1)
                    
                    if pdf.get_y() > 265:
                        pdf.add_page()
                pdf.ln(2)
            pdf.ln(2)

    agregar_detalle_proceso(pdf, matriz_pa, evaluaciones_pa, "PA", "1.0 ANALISIS ADMINISTRATIVO")
    pdf.ln(5)
    agregar_detalle_proceso(pdf, matriz_po, evaluaciones_po, "PO", "2.0 ANALISIS OPERATIVO")

    # Nota final
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 8)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 5, normalizar_texto('Este informe es un diagnostico basado en la evaluacion GPP_CORE. Se recomienda implementar las acciones correctivas sugeridas en el Plan de Accion.'))

    return pdf.output()
