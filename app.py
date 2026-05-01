from flask import Flask, render_template, request
from tutor import responder
from historial import cargar_historial, agregar_interaccion
from datetime import datetime
import sys  # 🆕 Agregado para debug

app = Flask(__name__)

# 🆕 Mostrar información al iniciar
print(f"🐍 Python: {sys.version}")
print("🚀 Servidor Flask iniciando...")

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    pregunta_actual = None
    historial = cargar_historial()
    
    # Agregar timestamps al historial si no existen
    for item in historial:
        if 'timestamp' not in item:
            item['timestamp'] = datetime.now().strftime('%H:%M:%S')
    
    if request.method == 'POST':
        pregunta = request.form['pregunta']
        pregunta_actual = pregunta
        
        if pregunta.lower() != 'salir':
            print(f"📝 Pregunta: {pregunta[:50]}...")  # 🆕 Log en consola
            
            # Obtener respuesta del tutor
            respuesta_texto = responder(pregunta)
            respuesta = respuesta_texto
            
            # Actualizar historial
            historial = cargar_historial()
            if historial:
                historial[-1]['timestamp'] = datetime.now().strftime('%H:%M:%S')
                
            print(f"✅ Respuesta generada ({len(respuesta_texto)} caracteres)")  # 🆕 Log
    
    return render_template('index.html', 
                         respuesta=respuesta, 
                         historial=historial,
                         pregunta_actual=pregunta_actual)

if __name__ == '__main__':
    print("🌐 Abre http://127.0.0.1:5000 en tu navegador")
    app.run(debug=True)
    