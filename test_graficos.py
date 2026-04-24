"""
Script de prueba para verificar los gráficos
"""
import plotly.graph_objects as go

# Probar gráfico de barras
try:
    fig = go.Figure(data=[
        go.Bar(
            x=[75, 60, 80],
            y=['Test 1', 'Test 2', 'Test 3'],
            orientation='h',
            marker=dict(
                color=['#10B981', '#F59E0B', '#10B981'],
                line=dict(color='rgba(255, 255, 255, 0.8)', width=2),
            ),
            text=[f"<b>{p:.1f}%</b>" for p in [75, 60, 80]],
            textposition='outside',
            textfont=dict(size=14, family='Montserrat, sans-serif'),
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="<b>Test de Gráfico de Barras</b>",
            font=dict(size=24, family='Montserrat, sans-serif', color='#0A1929'),
        ),
        height=400,
    )
    
    print("✅ Gráfico de barras: OK")
except Exception as e:
    print(f"❌ Error en gráfico de barras: {e}")

# Probar gráfico gauge
try:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=75,
        title={'text': "<b>Test Gauge</b>"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667EEA"},
            'steps': [
                {'range': [0, 60], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [60, 75], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
        }
    ))
    print("✅ Gráfico gauge: OK")
except Exception as e:
    print(f"❌ Error en gráfico gauge: {e}")

# Probar gráfico radar
try:
    areas = ['Test 1', 'Test 2', 'Test 3']
    valores = [75, 60, 80]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=areas,
        fill='toself',
        name='Test',
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
    )
    print("✅ Gráfico radar: OK")
except Exception as e:
    print(f"❌ Error en gráfico radar: {e}")

# Probar gráfico de dona
try:
    fig = go.Figure(data=[go.Pie(
        labels=['Alta', 'Media', 'Baja'],
        values=[5, 3, 2],
        marker=dict(
            colors=['#EF4444', '#F59E0B', '#10B981'],
        ),
        hole=0.45,
    )])
    print("✅ Gráfico de dona: OK")
except Exception as e:
    print(f"❌ Error en gráfico de dona: {e}")

print("\n✅ Todas las pruebas de gráficos completadas")

