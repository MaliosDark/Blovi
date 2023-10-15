import subprocess

def block_port(port_to_block):
    try:
        # Ejecutar el comando netsh para bloquear el puerto
        command = f"netsh advfirewall firewall add rule name=\"Block Port {port_to_block}\" dir=in action=block protocol=TCP localport={port_to_block}"
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()

        if process.returncode == 0:
            return f"Puerto {port_to_block} bloqueado con éxito."
        else:
            return f"No se pudo bloquear el puerto {port_to_block}. Error: {err.decode('utf-8')}"
    except Exception as e:
        return f"Error al bloquear el puerto {port_to_block}. Detalles: {str(e)}"

    

def unblock_port(port_number):
    try:
        # Utiliza el comando netsh para desbloquear el puerto en Windows
        command = f"netsh advfirewall firewall delete rule name='Block Port {port_number}'"
        subprocess.run(command, shell=True, check=True)
        return f"Puerto {port_number} desbloqueado con éxito."
    except Exception as e:
        return f"No se pudo desbloquear el puerto {port_number}. Error: {str(e)}"

def get_active_ports():
    try:
        # Utiliza el comando netstat para obtener la lista de puertos activos
        result = subprocess.check_output(["netstat", "-an"], universal_newlines=True)
        return result
    except Exception as e:
        return f"No se pudo obtener la lista de puertos activos. Error: {str(e)}"

