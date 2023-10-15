import psutil

def get_port_info(port):
    try:
        connections = psutil.net_connections(kind='inet')
        for conn in connections:
            if conn.laddr.port == port:
                status = 'Listening' if conn.status == psutil.CONN_LISTEN else 'Connected'
                pid = conn.pid
                process = psutil.Process(pid)
                cpu_percent = process.cpu_percent(interval=0.1)
                memory_info = process.memory_info()
                return f'Puerto {port} - {status}\n' \
                       f'PID: {pid}\n' \
                       f'CPU Usage: {cpu_percent:.2f}%\n' \
                       f'Memory Usage: {memory_info.rss / (1024 * 1024):.2f} MB'
        return f'Port {port} - Closed'
    except Exception as e:
        return f'Error fetching information for port {port}: {str(e)}'

def is_port_infected(port):
    # Lógica para determinar si el puerto está infectado o no
    return True  # Reemplaza esto con tu lógica real
