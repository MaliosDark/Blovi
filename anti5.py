import socket
import tkinter as tk
from tkinter import ttk
import threading
import port_control
import info_net  # Importa el módulo info_net para usar la función get_port_info
from tkinter import Text
import tkinter as tk

# Define una función para agregar texto coloreado
def insert_colored_text(text_widget, text, color):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text, color)
    text_widget.see(tk.END)
    text_widget.config(state=tk.DISABLED)

class PortScannerApp:
    # ... (otro código)
    
    def show_port_info_action(self):
        port_ranges = self.port_entry.get().split(',')
        is_infected = False
        for port_range in port_ranges:
            port_range = port_range.strip()
            if '-' in port_range:
                start_port, end_port = map(int, port_range.split('-'))
                for port in range(start_port, end_port + 1):
                    is_infected = info_net.is_port_infected(port)
                    description = f"Puerto {port} - {'Infectado' if is_infected else 'No Infectado'}\n"
                    color = "red" if is_infected else "green"
                    insert_colored_text(self.result_text, description, color)
            else:
                port = int(port_range)
                is_infected = info_net.is_port_infected(port)
                description = f"Puerto {port} - {'Infectado' if is_infected else 'No Infectado'}\n"
                color = "red" if is_infected else "green"
                insert_colored_text(self.result_text, description, color)

class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoreo de Puertos")
        self.root.geometry("800x600")
        self.root.style = ttk.Style()
        self.root.style.theme_use("vista")  # Cambia "clam" al tema que prefieras

        self.port_signatures = self.get_ports_from_file()

        ttk.Label(root, text="Dirección IP a Escanear:").pack()
        self.ip_entry = ttk.Entry(root)
        self.ip_entry.pack()

        ttk.Label(root, text="Puertos Personalizados (separados por coma):").pack()
        self.port_entry = ttk.Entry(root)
        self.port_entry.insert(0, "135, 137, 139, 445, 593, 1024-1030, 1080, 1214, 1363, 1364, 1368, 1373, 1377, 2745, 2283, 2535, 2745, 3127-3128, 3410, 4444, 5554, 8866, 9898, 10000, 10080, 12345, 1433, 17300, 27374, 666, 6660-6669, 6666-6669, 7000, 12667, 27665, 31335, 27444, 34555, 35555, 80, 8080, 69")
        self.port_entry.pack()

        ttk.Button(root, text="Detectar IP", command=self.detect_ip).pack()
        self.scan_button = ttk.Button(root, text="Iniciar Monitoreo en Tiempo Real", command=self.start_monitoring_thread)
        self.scan_button.pack()
        self.stop_button = ttk.Button(root, text="Detener Escaneo", command=self.stop_monitoring_thread)
        self.stop_button.config(state="disabled")
        self.stop_button.pack()
        self.show_info_button = ttk.Button(root, text="Mostrar Información del Puerto", command=self.show_port_info_action)
        self.show_info_button.pack()
        self.block_port_button = ttk.Button(root, text="Bloquear Puerto", command=self.block_port_action)
        self.block_port_button.pack()
        self.unblock_port_button = ttk.Button(root, text="Desbloquear Puerto", command=self.unblock_port_action)
        self.unblock_port_button.pack()
        self.show_active_ports_button = ttk.Button(root, text="Mostrar Puertos Activos", command=self.show_active_ports_action)
        self.show_active_ports_button.pack()

        self.result_text = tk.Text(root, height=15, width=60)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.monitoring = False

    def show_port_info_action(self):
        ports = self.port_entry.get().split(',')
        self.result_text.delete(1.0, tk.END)  # Limpia el resultado anterior
        for port_str in ports:
            try:
                port = int(port_str.strip())
                port_info = info_net.get_port_info(port)
                is_infected = info_net.is_port_infected(port)
                if is_infected:
                    info_color = "red"  # Color para puertos infectados
                    info_text = "Infectado"
                else:
                    info_color = "green"  # Color para puertos no infectados
                    info_text = "No infectado"
                
                self.result_text.insert(tk.END, f"Info para el puerto {port}:\n", info_color)
                self.result_text.insert(tk.END, f"Estado: {info_text}\n", info_color)
                self.result_text.insert(tk.END, f"Descripción: {port_info}\n\n")
            except ValueError:
                self.result_text.insert(tk.END, f"El puerto {port_str.strip()} no es un número válido.\n")

    def detect_ip(self):
        detected_ip = socket.gethostbyname(socket.gethostname())
        self.ip_entry.delete(0, tk.END)
        self.ip_entry.insert(0, detected_ip)

    def get_ports_from_file(self):
        port_signatures = {}
        try:
            with open('ports.txt', 'r') as file:
                lines = file.readlines()

            for line in lines:
                if not line.startswith('#') and ':' in line:
                    parts = line.strip().split(':')
                    if len(parts) == 2:
                        port_range = parts[0].strip()
                        signature = parts[1].strip()

                        if '-' in port_range:
                            start_port, end_port = map(int, port_range.split('-'))
                            for port in range(start_port, end_port + 1):
                                port_signatures[port] = signature
                        else:
                            port = int(port_range)
                            port_signatures[port] = signature

            return port_signatures
        except FileNotFoundError:
            self.result_text.insert(tk.END, "El archivo 'ports.txt' no se encontró.\n")
            return {}

    def scan_ports(self):
        target_ip = self.ip_entry.get()
        custom_ports = [port.strip() for port in self.port_entry.get().split(',')]

        self.result_text.delete(1.0, tk.END)
        try:
            new_ports = self.get_ports_from_file()
            self.port_signatures.update(new_ports)
            for port in new_ports:
                if port not in self.port_signatures:
                    self.port_signatures[port] = new_ports[port]
            self.result_text.insert(tk.END, "Lista de puertos actualizada con éxito.\n")
        except Exception as e:
            self.result_text.insert(tk.END, "No se pudo cargar o extender la lista de puertos.\n")

        open_ports = []
        threats = []

        for port in custom_ports:
            try:
                port = int(port)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    try:
                        s.connect((target_ip, port))
                        open_ports.append(port)
                        if port in self.port_signatures:
                            threats.append(self.port_signatures[port])
                        self.result_text.insert(tk.END, f"Puerto {port} - Abierto")
                        if port in self.port_signatures:
                            self.result_text.insert(tk.END, f" (¡Amenaza detectada! - {self.port_signatures[port]})")
                        self.result_text.insert(tk.END, "\n")
                    except PermissionError:
                        self.result_text.insert(tk.END, f"No se pudo acceder al puerto {port}\n")
                    except (socket.timeout, ConnectionRefusedError):
                        pass
            except ValueError:
                self.result_text.insert(tk.END, f"El puerto {port} no es válido\n")

        if self.monitoring:
            self.root.after(30000, self.scan_ports)

    def start_monitoring_thread(self):
        self.monitoring = True
        self.scan_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.block_port_button.config(state="normal")
        self.unblock_port_button.config(state="normal")
        self.show_active_ports_button.config(state="normal")
        self.scan_ports()

    def stop_monitoring_thread(self):
        self.monitoring = False
        self.scan_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.block_port_button.config(state="disabled")
        self.unblock_port_button.config(state="disabled")
        self.show_active_ports_button.config(state="disabled")

    def block_port_action(self):
        port_to_block = self.port_entry.get()
        result = port_control.block_port(port_to_block)
        self.result_text.insert(tk.END, result + "\n")


    def unblock_port_action(self):
        port_to_unblock = self.port_entry.get()
        result = port_control.unblock_port(port_to_unblock)
        self.result_text.insert(tk.END, result + "\n")

    def show_active_ports_action(self):
        active_ports = port_control.get_active_ports()
        self.result_text.insert(tk.END, "Lista de puertos activos:\n")
        self.result_text.insert(tk.END, active_ports)

    

if __name__ == '__main__':
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()