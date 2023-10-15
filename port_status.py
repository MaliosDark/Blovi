import subprocess

def get_active_ports():
    try:
        # Utiliza el comando netstat para obtener la lista de puertos activos
        result = subprocess.check_output(["netstat", "-an"], universal_newlines=True)
        return result
    except Exception as e:
        return f"No se pudo obtener la lista de puertos activos. Error: {str(e)}"
