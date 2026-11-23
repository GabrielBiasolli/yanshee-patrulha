# -*- coding: utf-8 -*-
"""Todas as constantes configuraveis do projeto. Ajuste aqui, nao no codigo."""

ROBO_IP = "127.0.0.1"

# --- Modo de entrada da Fase 1 (gravacao do trajeto) --------------------------
#  "controle" -> controle USB 8-bit via evdev (modo final)
#  "web"      -> pagina no celular com setas, START, simulacao dos sensores
#                e botao PARAR (melhor modo para testar andando junto)
#  "teclado"  -> digita os comandos no terminal/SSH (teste sem controle)
#                w = frente | a = esquerda | d = direita | p = START
#  "fixo"     -> pula a gravacao e patrulha direto o TRAJETO_FIXO
# Se o controle (ou o evdev) nao for encontrado, o programa cai sozinho no
# modo "web" em vez de travar.
MODO_ENTRADA = "controle"
TRAJETO_FIXO = ["frente", "frente", "esquerda", "frente"]
PORTA_WEB = 8000   # modo web: http://<IP_DO_ROBO>:8000 no celular

# --- Sensores (numeracao BCM) -----------------------------------------------
# ATENCAO: o GPIO do Raspberry Pi aceita no maximo 3.3 V.
#  - KY-037/KY-038: alimente em 3.3 V (pino fisico 1). Em 5 V a saida DO sai
#    em 5 V e pode queimar o pino. Calibre o limiar no trimpot azul.
#  - HC-SR501: pode ser alimentado em 5 V; a saida OUT ja e 3.3 V.
#    Use o jumper em "L" (disparo unico) e o trimpot de tempo no minimo.
#    Ele precisa de ~1 min apos ligar para estabilizar: a fase de
#    teach-in costuma cobrir esse tempo.
PINO_SOM = 17   # pino fisico 11
PINO_PIR = 27   # pino fisico 13
SOM_ATIVO_EM_ALTO = True   # alguns clones do KY-037 sao ativos em LOW: use False
PIR_ATIVO_EM_ALTO = True

# --- Controle USB 8-bit (evdev) ---------------------------------------------
# None = procura sozinho o primeiro joystick/gamepad conectado.
# Se tiver mais de um, fixe o caminho, ex.: "/dev/input/event2"
# (descubra com "sudo evtest"; veja o fim do main.py).
DEVICE_PATH = None

# A maioria dos controles 8-bit genericos ("USB Gamepad", DragonRise) manda o
# direcional como EIXO (EV_ABS) com valores 0 / 127 / 255.
# Se o seu mandar como HAT, use eixos 16/17 (ABS_HAT0X/ABS_HAT0Y) e
# valores -1 / 1.
EIXO_HORIZONTAL = 0     # ABS_X   (esquerda / direita)
EIXO_VERTICAL = 1       # ABS_Y   (cima / baixo)
VALOR_EIXO_MIN = 0      # cima ou esquerda
VALOR_EIXO_MAX = 255    # baixo ou direita
BOTAO_START = 297       # BTN_BASE4 na maioria dos genericos; confirme no evtest

# --- Tempos ------------------------------------------------------------------
TEMPO_ESCUTA = 1.5          # s parado ouvindo os sensores a cada passo
TEMPO_ESTABILIZACAO = 0.3   # s de espera apos o passo para os servos assentarem
INTERVALO_LEITURA = 0.02    # s entre leituras dos sensores durante a escuta

# --- Movimentos ----------------------------------------------------------------
VELOCIDADE = "normal"       # "slow" | "normal" | "fast"
REPEAT_PASSO = 1            # repeticoes do movimento a cada comando do controle
REPEAT_GIRO_180 = 6         # repeticoes de "turn around" para ~180 graus.
                            # CALIBRE no chao onde o robo vai andar.

# Acao gravada -> (nome do movimento, direcao) para o YanAPI.sync_play_motion.
# Para passo lateral em vez de giro, use ("walk", "left") / ("walk", "right").
MOVIMENTOS = {
    "frente":   ("walk", "forward"),
    "esquerda": ("turn around", "left"),
    "direita":  ("turn around", "right"),
    "giro_180": ("turn around", "left"),
}

# Nome exato da danca da Shakira na lista de movimentos do robo.
# Confirme com YanAPI.get_motion_list_value() (comando no fim do main.py).
# Se o nome exato nao existir, o programa procura na lista um movimento que
# contenha alguma das PALAVRAS_DANCA e avisa qual escolheu.
NOME_DANCA_SHAKIRA = "WakaWaka"
PALAVRAS_DANCA = ("waka", "shakira")

# LED do botao do peito: (cor, modo)
LED_ALERTA = ("red", "blink")
LED_NORMAL = ("green", "on")
