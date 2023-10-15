Blovi ( Bloqueador de Virus )

```markdown
# Aplicación de Monitoreo y Bloqueo de Puertos

Esta aplicación permite monitorear y bloquear puertos en una dirección IP específica. Puede ser útil para administradores de sistemas que desean mantener un registro de los puertos abiertos y bloquear los puertos no deseados en una máquina.

## Características

- Escaneo de puertos personalizados.
- Actualización de la lista de puertos desde un archivo externo.
- Monitoreo en tiempo real de los puertos.
- Bloqueo de puertos no deseados.
- Verificación de si un puerto está infectado o no (requiere módulo externo).
- Temas visuales personalizables.
- Uso de estilos Bootstrap para una interfaz más atractiva.

## Instrucciones de Uso

### Instalación de Dependencias

1. Asegúrate de tener Python 3.x instalado en tu sistema.

2. Abre una terminal o línea de comandos.

3. Navega al directorio donde se encuentra la aplicación.

4. Ejecuta el siguiente comando para instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

### Ejecución de la Aplicación

1. En la misma terminal o línea de comandos, asegúrate de estar en el directorio de la aplicación.

2. Ejecuta el siguiente comando para iniciar la aplicación:

   ```bash
   python anti5.py
   ```

3. La aplicación se ejecutará, y se mostrará una interfaz gráfica para usar todas las funciones.

4. Asegúrate de ejecutar la aplicación con privilegios de administrador para bloquear puertos.

### Uso de la Aplicación

- Introduce la dirección IP que deseas escanear.
- Ingresa los puertos personalizados separados por comas o rangos.
- Puedes presionar "Detectar IP" para obtener automáticamente tu dirección IP local.
- Presiona "Iniciar Monitoreo en Tiempo Real" para comenzar el escaneo de puertos.
- "Detener Escaneo" detiene el monitoreo.
- Utiliza "Bloquear Puerto" y "Desbloquear Puerto" para bloquear o desbloquear puertos (requiere privilegios de administrador).
- "Mostrar Puertos Activos" lista los puertos abiertos en la consola.

## Últimos Defectos y Soluciones Posibles

1. **Bloqueo de Puertos no Funciona**:
   - Algunos sistemas pueden requerir el uso del módulo `subprocess` para bloquear puertos con `netsh`. La aplicación podría no bloquear puertos correctamente utilizando `os.system`. La solución es reemplazar la función `block_port` en `port_control.py` con el siguiente código que utiliza `subprocess`:

   ```python
   import subprocess

   def block_port(port_to_block):
       try:
           command = f"netsh advfirewall firewall add rule name=\"Block Port {port_to_block}\" dir=in action=block protocol=TCP localport={port_to_block}"
           process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
           out, err = process.communicate()

           if process.returncode == 0:
               return f"Puerto {port_to_block} bloqueado con éxito."
           else:
               return f"No se pudo bloquear el puerto {port_to_block}. Error: {err.decode('utf-8')}"
       except Exception as e:
           return f"Error al bloquear el puerto {port_to_block}. Detalles: {str(e)}"
   ```

2. **Verificación de Puertos Infectados no Muestra Colores**:
   - La aplicación debería mostrar si un puerto está infectado o no en colores. Para implementar esto, se necesita modificar la función `show_port_info_action` en `anti5.py` para cambiar el color del texto en la consola en función del estado del puerto.

3. **Bloqueo de Puertos no Funciona en Algunos Sistemas**:
   - Asegúrate de ejecutar la aplicación con privilegios de administrador para que tenga los permisos necesarios para bloquear puertos. Puedes ejecutar la aplicación desde la línea de comandos con privilegios de administrador o crear un acceso directo con la opción "Ejecutar como administrador".

4. **Temas Visuales no se Aplican Correctamente**:
   - La aplicación utiliza el módulo `ttkbootstrap` para aplicar estilos Bootstrap a los elementos de la interfaz gráfica. Si los temas visuales no se aplican correctamente, verifica que `ttkbootstrap` esté instalado. Además, asegúrate de que la última versión de `ttkbootstrap` sea compatible con tu sistema.

Esperamos que esta guía sea útil para ejecutar la aplicación de monitoreo y bloqueo de puertos. Si encuentras algún problema adicional o tienes sugerencias de mejora, no dudes en comunicarlo a los desarrolladores.
```
