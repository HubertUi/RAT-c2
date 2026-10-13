#!/usr/bin/env python3
"""
Configuración para el bot C2 del atacante
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DiscordConfig:
    """Configuración de Discord"""
    bot_token: str
    command_channel_id: int
    
    @classmethod
    def from_env(cls) -> 'DiscordConfig':
        """Crea configuración desde variables de entorno"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        channel_id_str = os.getenv('COMMAND_CHANNEL_ID')
        
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN no está definida en variables de entorno")
        
        if not channel_id_str:
            raise ValueError("COMMAND_CHANNEL_ID no está definida en variables de entorno")
        
        try:
            channel_id = int(channel_id_str)
        except ValueError:
            raise ValueError("COMMAND_CHANNEL_ID debe ser un número entero")
        
        return cls(
            bot_token=token,
            command_channel_id=channel_id
        )


@dataclass
class ServerConfig:
    """Configuración del servidor"""
    host: str = "localhost"
    port: int = 8080
    debug: bool = False


@dataclass
class LoggingConfig:
    """Configuración de logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None


class AppConfig:
    """Configuración principal de la aplicación"""
    
    def __init__(self):
        self.discord = DiscordConfig.from_env()
        self.server = ServerConfig()
        self.logging = LoggingConfig()
    
    def validate(self):
        """Valida la configuración"""
        # Validar Discord config
        if not self.discord.bot_token or len(self.discord.bot_token) < 10:
            raise ValueError("Token de Discord inválido")
        
        if self.discord.command_channel_id <= 0:
            raise ValueError("ID de canal de Discord inválido")
        
        return True
    
    def __str__(self) -> str:
        """Representación string de la configuración"""
        return f"""
Configuración C2:
- Canal de comandos Discord: {self.discord.command_channel_id}
- Servidor: {self.server.host}:{self.server.port}
- Debug: {self.server.debug}
- Nivel de logging: {self.logging.level}
"""