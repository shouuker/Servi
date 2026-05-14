import requests
from flask import Flask, Response, request

app = Flask(__name__)

# Esta es la URL de tu lista base en GitHub
URL_LISTA_ORIGINAL = "https://raw.githubusercontent.com/shouuker/Shouukertv/refs/heads/Tvshouuker/Tv40.m3u"

@app.route('/playlist.m3u8')
def playlist():
    """
    Este es el link que le das a tus clientes. 
    Descarga tu lista de GitHub y se la entrega a ellos.
    """
    try:
        # El servidor descarga tu lista actual de GitHub
        respuesta = requests.get(URL_LISTA_ORIGINAL, timeout=10)
        contenido = respuesta.text
        
        # Aquí podrías agregar lógica en el futuro para modificar la lista 
        # (por ejemplo, cambiar logos o nombres de canales)
        
        return Response(contenido, mimetype='application/vnd.apple.mpegurl')
    except Exception as e:
        return f"Error al cargar la lista: {str(e)}", 500

@app.route('/')
def index():
    return "Servidor de TV Activo - Maxi TV Digital", 200

if __name__ == '__main__':
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)
