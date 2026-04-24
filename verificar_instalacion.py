"""
Script para verificar que todas las dependencias están instaladas correctamente
"""
import sys
import io

# Configurar salida para Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 50)
print("VERIFICANDO INSTALACION")
print("=" * 50)
print()

# Verificar versión de Python
print(f"[OK] Python {sys.version}")
print()

# Lista de módulos requeridos
modulos_requeridos = [
    ('streamlit', 'Streamlit'),
    ('pandas', 'Pandas'),
    ('openpyxl', 'OpenPyXL'),
    ('plotly', 'Plotly'),
    ('numpy', 'NumPy')
]

errores = []
exitosos = []

print("Verificando modulos requeridos:")
print("-" * 50)

for modulo, nombre in modulos_requeridos:
    try:
        mod = __import__(modulo)
        version = getattr(mod, '__version__', 'version desconocida')
        print(f"[OK] {nombre:15} - version {version}")
        exitosos.append(nombre)
    except ImportError as e:
        print(f"[ERROR] {nombre:15} - NO INSTALADO")
        errores.append(nombre)

print()
print("=" * 50)
print("RESULTADO")
print("=" * 50)

if errores:
    print(f"[ERROR] Faltan {len(errores)} modulo(s):")
    for modulo in errores:
        print(f"  - {modulo}")
    print()
    print("Para instalar los modulos faltantes, ejecute:")
    print("  pip install -r requirements.txt")
    sys.exit(1)
else:
    print(f"[OK] Todos los modulos instalados correctamente ({len(exitosos)}/{len(modulos_requeridos)})")
    print()
    print("La aplicacion esta lista para usar!")
    print()
    print("Para iniciar la aplicacion:")
    print("  1. Ejecute: streamlit run app.py")
    print("  2. O haga doble clic en: ejecutar.bat")
    sys.exit(0)

