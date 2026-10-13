#!/usr/bin/env python3
"""
Test de conexión del bot C2
Verifica que el bot puede conectarse y enviar mensajes al canal
"""

import os
import sys
import discord
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(os.path.join(os.path.dirname(__file__), 'attacker', '.env'))

BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', '')
COMMAND_CHANNEL_ID = int(os.getenv('COMMAND_CHANNEL_ID', '0'))

print("=" * 50)
print("TEST DE CONEXIÓN - BOT C2 DISCORD")
print("=" * 50)
print(f"\n[1] Token cargado: {BOT_TOKEN[:25]}...")
print(f"[2] Channel ID: {COMMAND_CHANNEL_ID}")

# Verificar intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"\n[3] ✅ Bot conectado como: {client.user}")
    print(f"[4] ✅ ID del bot: {client.user.id}")
    print(f"[5] ✅ Servidores conectados: {len(client.guilds)}")
    
    for guild in client.guilds:
        print(f"    - {guild.name} (ID: {guild.id})")
    
    # Verificar canal
    channel = client.get_channel(COMMAND_CHANNEL_ID)
    if channel:
        print(f"\n[6] ✅ Canal encontrado: #{channel.name}")
        print(f"[7] ✅ Tipo de canal: {channel.type}")
        
        # Enviar mensaje de prueba
        try:
            embed = discord.Embed(
                title="🟢 TEST EXITOSO",
                description="El bot C2 está funcionando correctamente.",
                color=0x00ff00
            )
            embed.add_field(name="Estado", value="Conectado y operativo", inline=False)
            embed.add_field(name="Canal", value=f"#{channel.name}", inline=False)
            
            await channel.send(embed=embed)
            print(f"[8] ✅ Mensaje enviado al canal #{channel.name}")
            print("\n" + "=" * 50)
            print("✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
            print("=" * 50)
            print("\nEl bot está listo para recibir comandos.")
            print("Ve a Discord y verifica el mensaje en el canal.\n")
            
        except discord.Forbidden:
            print(f"\n[8] ❌ ERROR: Sin permisos para enviar mensajes en #{channel.name}")
            print("    Solución: Re-invita el bot con permisos 'Send Messages'")
        except Exception as e:
            print(f"\n[8] ❌ ERROR al enviar mensaje: {e}")
    else:
        print(f"\n[6] ❌ ERROR: Canal {COMMAND_CHANNEL_ID} no encontrado")
        print("    Posibles causas:")
        print("    - El bot no está en el servidor")
        print("    - El Channel ID es incorrecto")
        print("    - El bot no tiene acceso al canal")
    
    await client.close()

# Ejecutar test
print("\n[0] Conectando a Discord...\n")
try:
    client.run(BOT_TOKEN)
except discord.LoginFailure:
    print("❌ ERROR: Token inválido")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR de conexión: {e}")
    sys.exit(1)
