import urllib.request
import sys

print("-" * 60)
print("🔍 RECONOCIMIENTO WEB: EXTRACCIÓN DE CABECERAS HTTP")
print("-" * 60)

url = input("Introduce la web a analizar (ej: http://example.com): ")

# Asegurar que la URL empiece con http
if not url.startswith("http"):
    url = "http://" + url

try:
    # Simular un navegador real para que el servidor no nos bloquee
    peticion = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    # Conectarse a la web
    with urllib.request.urlopen(peticion, timeout=5) as respuesta:
        print("\n[+] Conexión exitosa. Analizando metadatos del servidor...\n")
        cabeceras = respuesta.info()
        
        # Mostrar las cabeceras clave para el auditor de seguridad
        for clave, valor in cabeceras.items():
            # Resaltar datos críticos como el software del servidor
            if clave.lower() in ["server", "x-powered-by", "set-cookie"]:
                print(f"⚠️  {clave}: {valor}")
            else:
                print(f"   {clave}: {valor}")

except Exception as e:
    print(f"\n❌ Error al conectar: {e}")
    sys.exit()
