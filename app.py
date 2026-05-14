import requests
from flask import Flask, Response, request

app = Flask(__name__)

# --- LISTA DE CLIENTES ACTIVOS ---
# Para agregar más, poné una coma y el nombre abajo entre comillas.
CLIENTES_PERMITIDOS = [
    "maxi",
]
# ---------------------------------

PASS_UNICA = "vip2026"
URL_LISTA_ORIGINAL = "https://raw.githubusercontent.com/shouuker/Shouukertv/refs/heads/Tvshouuker/Tv40.m3u"

@app.route('/playlist.m3u8')
def playlist():
    user = request.args.get('user')
    password = request.args.get('pass')

    if user in CLIENTES_PERMITIDOS and password == PASS_UNICA:
        try:
            respuesta = requests.get(URL_LISTA_ORIGINAL, timeout=10)
            return Response(respuesta.text, mimetype='application/vnd.apple.mpegurl')
        except:
            return "Error al conectar con la fuente", 500
    else:
        return "Acceso Denegado: Usuario no autorizado o cuenta vencida", 401

@app.route('/')
def index():
    return "Servidor Maxi TV Digital - Activo y Protegido", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
