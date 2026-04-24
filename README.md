# 📊 Aplicación de Evaluación de Gestión Por Procesos (GPP)

¡Bienvenido! Esta es una herramienta interactiva diseñada para la evaluación y visualización de la **Gestión Por Procesos (GPP)** en el entorno de **Gastrocolma**. La aplicación transforma herramientas tradicionales en una experiencia web moderna, facilitando la toma de decisiones basada en datos.

## 🚀 Características Principales

- **Dashboard Interactivo:** Visualización en tiempo real de los resultados de gestión.
- **Evaluación Detallada:** Módulos específicos para procesos **Administrativos** y **Operativos**.
- **Gráficos Modernos:** Implementación de gráficos dinámicos (Plotly) para análisis de prioridades, escalas de calificación y flujos de trabajo.
- **Diseño "Bento Grid":** Interfaz de usuario limpia, moderna y profesional utilizando fuentes de alta legibilidad (Inter).
- **Persistencia de Datos:** Capacidad para guardar y cargar evaluaciones en formato JSON.
- **Exportación:** Generación de reportes listos para el análisis gerencial.

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.x
- **Framework Web:** [Streamlit](https://streamlit.io/)
- **Visualización:** Plotly Express & Graph Objects
- **Procesamiento de Datos:** Pandas & NumPy
- **Estilos:** CSS3 personalizado con variables para temas modernos.

## 💻 Instalación Local

Si querés correr la aplicación en tu máquina, seguí estos pasos:

1. **Cloná el repositorio:**
   ```bash
   git clone https://github.com/julian8811/Aplicacion_GPP.git
   cd Aplicacion_GPP
   ```

2. **Creá un entorno virtual (opcional pero recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalá las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutá la aplicación:**
   ```bash
   streamlit run app.py
   ```

## ☁️ Despliegue

La aplicación está lista para ser desplegada en plataformas como **Vercel** o **Streamlit Community Cloud**. 

- El archivo `vercel.json` ya está configurado para el despliegue en Vercel.
- Asegurate de que el archivo `runtime.txt` especifique la versión de Python deseada.

---
Desarrollado con ❤️ para mejorar la eficiencia operativa.
