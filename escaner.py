import socket
import sys

objetivo_input = input("Introduce la IP o dominio a escanear (ej. scanme.nmap.org): ")

try:
    objetivo = socket.gethostbyname(objetivo_input)
except socket.gaierror:
    print("\n❌ Error: No se pudo resolver el nombre.")
    sys.exit()

print("-" * 60)
print(f"Escaneando y capturando banners en: {objetivo}")
print("-" * 60)

# Lista de puertos comunes a revisar
puertos = [21, 22, 80, 110, 143, 443]

for puerto in puertos:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0) 
        
        resultado = s.connect_ex((objetivo, puerto))
        
        if resultado == 0:
            print(f"🟢 Puerto {puerto}: ABIERTO")
            
            try:
                # Si es puerto web, enviamos una petición básica para forzar la respuesta
                if puerto == 80:
                    s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + objetivo_input.encode() + b"\r\n\r\n")
                
                # Intentamos recibir la presentación del servicio
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                
                if banner:
                    print(f"    ↳ 📝 Banner detectado:\n{banner}\n")
                else:
                    print("    ↳ 📝 Conectado, pero el servicio no envió texto automáticamente.\n")
            except:
                print("    ↳ ❌ No se pudo extraer información del servicio.\n")
        
        s.close()

    except KeyboardInterrupt:
        print("\n❌ Escaneo cancelado por el usuario.")
        sys.exit()
    except Exception:
        # Pasa al siguiente puerto si ocurre un error inesperado de red
        pass
