import requests
from flask import Flask, Response, request

app = Flask(__name__)

# CONFIGURACIÓN DE SEGURIDAD (Cambiá esto por lo que vos quieras)
USUARIO_CLIENTE = "maxi"
CLAVE_CLIENTE = "premium2026"

# Tu lista base de GitHub
URL_LISTA_ORIGINAL = "https://raw.githubusercontent.com/shouuker/Shouukertv/refs/heads/Tvshouuker/Tv40.m3u"

@app.route('/playlist.m3u8')
def playlist():
    # Obtenemos el usuario y clave que vienen en el link
    user = request.args.get('user')
    password = request.args.get('pass')

    # Verificamos si los datos son correctos
    if user == USUARIO_CLIENTE and password == CLAVE_CLIENTE:
        try:
            respuesta = requests.get(URL_LISTA_ORIGINAL, timeout=10)
            return Response(respuesta.text, mimetype='application/vnd.apple.mpegurl')
        except:
            return "Error al cargar la fuente", 500
    else:
        # Si los datos están mal o no existen, tiramos error de acceso
        return "Acceso Denegado: Usuario o Clave incorrectos", 401

@app.route('/')
def index():
    return "Servidor de TV Protegido - Maxi TV Digital", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
