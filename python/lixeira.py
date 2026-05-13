import RPi.GPIO as GPIO
import time

# --- CONFIGURAÇÕES ---
ID_LIXEIRA = "LIXEIRA_LOCAL" 
ALTURA_MAX_LIXEIRA = 30 
PIN_TRIG, PIN_ECHO = 23, 24
PIN_LED_ABERTO, PIN_BUZZER = 27, 22
PIN_BOTAO, PIN_SERVO = 18, 13
INTERVALO_MEDICAO = 5  

def registrar_evento(evento, nivel=None, distancia=None):
    payload = {
        "id_lixeira": ID_LIXEIRA,
        "evento": evento,
        "nivel": nivel,
        "distancia_cm": distancia,
        "timestamp": time.time(),
    }
    print("[REGISTRO]", payload)

GPIO.setmode(GPIO.BCM)
GPIO.setup([PIN_TRIG, PIN_LED_ABERTO, PIN_BUZZER, PIN_SERVO], GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(PIN_BOTAO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

servo = GPIO.PWM(PIN_SERVO, 50)
servo.start(0)

def medir_nivel_estavel():
    leituras = []
    for _ in range(3):
        GPIO.output(PIN_TRIG, True)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIG, False)
        inicio, fim = time.time(), time.time()
        max_t = time.time()
        while GPIO.input(PIN_ECHO) == 0 and (time.time() - max_t < 0.1): inicio = time.time()
        max_t = time.time()
        while GPIO.input(PIN_ECHO) == 1 and (time.time() - max_t < 0.1): fim = time.time()
        dist = ((fim - inicio) * 34300) / 2
        leituras.append(dist)
        time.sleep(0.05)
    
    dist_media = sum(leituras) / len(leituras)
    if dist_media > 22:
        return "TAMPA_ABERTA", round(dist_media, 1)
    
    ocupacao = (13 - dist_media) / (13 - 2) * 100
    nivel = round(max(0, min(100, ocupacao)), 2)
    return nivel, round(dist_media, 1)

def mover_tampa(abrir):
    ciclo = 7.5 if abrir else 2.5
    servo.ChangeDutyCycle(ciclo)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)

# --- ESTADO INICIAL ---
tampa_aberta = False
tempo_abertura = 0
ultimo_alerta = 0 
ultima_medicao = 0  

print("\n=== SISTEMA INICIADO ===")
mover_tampa(False)

try:
    while True:
        # 1. BOTÃO
        if GPIO.input(PIN_BOTAO) == GPIO.LOW:
            tampa_aberta = not tampa_aberta
            status = "ABERTA" if tampa_aberta else "FECHADA"
            print(f"\n[COMANDO] Tampa {status}")
            GPIO.output(PIN_LED_ABERTO, tampa_aberta)
            mover_tampa(tampa_aberta)
            if not tampa_aberta: GPIO.output(PIN_BUZZER, False)
            
            res, d = medir_nivel_estavel()
            print(f"[INFO] Nível: {res}% ({d}cm)")
            registrar_evento("tampa_alterada", nivel=res, distancia=d)
            tempo_abertura = time.time()
            time.sleep(0.5)

        # 2. ALERTA 10s
        if tampa_aberta and (time.time() - tempo_abertura > 10):
            if time.time() - ultimo_alerta > 2:
                print("[ALERTA] Tampa aberta!")
                GPIO.output(PIN_BUZZER, True)
                time.sleep(0.2)
                GPIO.output(PIN_BUZZER, False)
                ultimo_alerta = time.time()

        # 3. MEDIÇÃO PERIÓDICA
        if time.time() - ultima_medicao > INTERVALO_MEDICAO:
            res, d = medir_nivel_estavel()
            if res == "TAMPA_ABERTA":
                print(f"[AVISO] TAMPA ABERTA ({d}cm)")
            else:
                print(f"[INFO] Nível atual: {res}% ({d}cm)")
            registrar_evento("medicao_periodica", nivel=res, distancia=d)
            ultima_medicao = time.time()

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nEncerrando...")
    servo.stop()
    GPIO.cleanup()