import urequests as requests
import os
import machine

class OTAUpdater:
    def __init__(self, repo_url, version_file='version.txt'):
        self.repo_url = repo_url
        self.version_file = version_file

    def check_for_update(self, current_version):
        # Verifica la versión disponible en el servidor
        print("Comprobando actualizaciones...")
        try:
            response = requests.get(f"{self.repo_url}/{self.version_file}")
            if response.status_code == 200:
                new_version = response.text.strip()
                print(f"Versión actual: {current_version}, Versión disponible: {new_version}")
                return new_version != current_version
            else:
                print("Error al obtener la versión.")
                return False
        except Exception as e:
            print(f"Error en la conexión: {e}")
            return False

    def download_update(self, filename='main.py'):
        # Descarga el archivo de actualización
        try:
            print("Descargando actualización...")
            response = requests.get(f"{self.repo_url}/{filename}")
            if response.status_code == 200:
                with open(filename, 'w') as f:
                    f.write(response.text)
                print("Actualización descargada con éxito.")
                return True
            else:
                print("Error al descargar el archivo de actualización.")
                return False
        except Exception as e:
            print(f"Error en la descarga: {e}")
            return False

    def apply_update(self):
        print("Aplicando actualización...")
        machine.reset()  # Reinicia el ESP32 para cargar el nuevo código