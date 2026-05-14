import requests
from flask import Flask, redirect, Response

app = Flask(__name__)

# CONFIGURACIÓN DE TU CUENTA DE JOY
# (Como es para tu negocio, estos datos quedan fijos acá)
USUARIO = "ojmario00912@gmail.com"
CLAVE = "M10118310M"

# IDs de los canales (estos no suelen cambiar)
CHANNELS = {
    "tnt": "hg35c-k15n6-nn351-lje0m_720p",
    "espn": "56cl9-6dffj-hb9op-hik52_1080p"
}

def obtener_token_real(id_canal):
    """Esta función entra a Joy y genera el link con el token actual"""
    cabeceras = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://joy.media.edge-apps.net/',
        'Origin': 'https://joy.media.edge-apps.net'
    }
    
    try:
        session = requests.Session()
        # 1. Login
        login_url = "https://joy.media.edge-apps.net/api/v1/auth/login"
        payload = {"email": USUARIO, "password": CLAVE}
        r_login = session.post(login_url, json=payload, headers=cabeceras, timeout=10)
        
        if r_login.status_code == 200:
            # 2. Obtener el link de video
            stream_url = f"https://joy.media.edge-apps.net/api/v1/streams/{id_canal}/index.m3u8"
            # allow_redirects=False para atrapar el link que tiene el token
            r_stream = session.get(stream_url, headers=cabeceras, allow_redirects=False, timeout=10)
            
            link_final = r_stream.headers.get('Location')
            return link_final
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/playlist.m3u8')
def playlist():
    """Este es el archivo que tus clientes cargan en su app de IPTV"""
    # Obtenemos el nombre del servidor que nos da Render automáticamente
    host = requests.utils.urlparse(requests.request.url_root).netloc
    
    m3u = "#EXTM3U\n"
    m3u += "#EXTINF:-1 tvg-name=\"TNT Sports Premium\" tvg-logo=\"https://i.imgur.com/your-logo.png\" group-title=\"DEPORTES\", TNT Sports Premium\n"
    m3u += f"http://{host}/vivo/tnt\n"
    m3u += "#EXTINF:-1 tvg-name=\"ESPN Premium\" tvg-logo=\"https://i.imgur.com/your-logo2.png\" group-title=\"DEPORTES\", ESPN Premium\n"
    m3u += f"http://{host}/vivo/espn\n"
    return Response(m3u, mimetype='application/vnd.apple.mpegurl')

@app.route('/vivo/<canal>')
def vivo(canal):
    """Cuando el cliente hace clic, esta ruta busca el token y lo conecta"""
    id_real = CHANNELS.get(canal.lower())
    if id_real:
        link = obtener_token_real(id_real)
        if link:
            return redirect(link)
    return "Error: No se pudo conectar con el servidor de origen", 403

if __name__ == '__main__':
    # Render usa el puerto 10000 por defecto
    app.run(host='0.0.0.0', port=10000)
  
