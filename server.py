import os
import webbrowser
import sys
import ssl
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    from livereload import Server
except ImportError:
    print("[!] Pro automatické obnovování (LiveReload) je potřeba knihovna 'livereload'.")
    print("[*] Nainstalujete ji příkazem: pip install livereload")
    sys.exit(1)

# Konfigurace prostředí
HTTPS_PORT = 8443
HTTP_PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target_url = f"https://localhost:{HTTPS_PORT}{self.path}"
        self.send_response(301)
        self.send_header('Location', target_url)
        self.end_headers()

    def do_POST(self):
        target_url = f"https://localhost:{HTTPS_PORT}{self.path}"
        self.send_response(307)
        self.send_header('Location', target_url)
        self.end_headers()

    def log_message(self, format, *args):
        return # Potlačení logů pro čistší výstup terminálu

def start_redirect_server():
    httpd = HTTPServer(('0.0.0.0', HTTP_PORT), RedirectHandler)
    httpd.serve_forever()

def start_server():
    # Nastavení pracovního adresáře
    os.chdir(DIRECTORY)
    
    # Kontrola existence SSL souborů
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        print("[!] Chybí SSL certifikáty (cert.pem a key.pem).")
        print("[*] Vygenerujte je příkazem: openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes")
        sys.exit(1)

    # Spuštění pomocného HTTP serveru pro přesměrování v samostatném vlákně
    threading.Thread(target=start_redirect_server, daemon=True).start()

    server = Server()

    # Sledování změn: jakmile uložíš HTML nebo změníš obrázek, prohlížeč se sám obnoví
    server.watch("*.html")
    server.watch("images/*")

    print(f"[*] HTTPS Archiv: https://localhost:{HTTPS_PORT}/journal.html")
    print(f"[*] HTTP Redirector aktivní na portu {HTTP_PORT} -> {HTTPS_PORT}")
    print("[*] LiveReload je aktivní. Změny v kódu se projeví okamžitě.")
    
    # Konfigurace SSL pro Tornado (backend livereloadu)
    ssl_options = {
        "certfile": "cert.pem",
        "keyfile": "key.pem",
    }

    webbrowser.open(f"https://localhost:{HTTPS_PORT}/journal.html")
    # Předáme ssl_options do serve metody
    server.serve(root=".", port=HTTPS_PORT, ssl_options=ssl_options)

if __name__ == "__main__":
    start_server()
