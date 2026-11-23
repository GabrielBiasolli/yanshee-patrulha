# -*- coding: utf-8 -*-
"""Sensor de som (KY-037/KY-038) e de presenca (PIR HC-SR501) via RPi.GPIO."""

import time

import RPi.GPIO as GPIO

import config

# Disparo vindo da pagina do celular (modo web): "som", "movimento" ou "parada".
_disparo_manual = None


def disparar_manual(tipo):
    global _disparo_manual
    _disparo_manual = tipo


def limpar_disparo_manual():
    global _disparo_manual
    _disparo_manual = None


def configurar():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pino, ativo_alto in ((config.PINO_SOM, config.SOM_ATIVO_EM_ALTO),
                             (config.PINO_PIR, config.PIR_ATIVO_EM_ALTO)):
        GPIO.setup(pino, GPIO.IN,
                   pull_up_down=GPIO.PUD_DOWN if ativo_alto else GPIO.PUD_UP)
        # A deteccao de borda roda em segundo plano e "guarda" o evento,
        # entao pega ate os pulsos de poucos ms do sensor de som.
        GPIO.add_event_detect(pino, GPIO.RISING if ativo_alto else GPIO.FALLING)


def escutar_anormalidade(duracao=None):
    """Fica parado `duracao` segundos vigiando os sensores.

    Retorna "som", "movimento", "parada" (botao PARAR da pagina) ou None.
    Anti-falso positivo: os eventos que aconteceram enquanto o robo andava
    (barulho dos servos, o PIR "vendo" a cena mudar) sao descartados, e so
    conta o que comecar durante a pausa. Disparos manuais da pagina nao sao
    descartados: foram intencionais.
    """
    global _disparo_manual
    if duracao is None:
        duracao = config.TEMPO_ESCUTA

    time.sleep(config.TEMPO_ESTABILIZACAO)
    GPIO.event_detected(config.PINO_SOM)   # ler a flag tambem a zera
    GPIO.event_detected(config.PINO_PIR)

    fim = time.time() + duracao
    while time.time() < fim:
        if _disparo_manual is not None:
            tipo, _disparo_manual = _disparo_manual, None
            return tipo
        if GPIO.event_detected(config.PINO_SOM):
            return "som"
        if GPIO.event_detected(config.PINO_PIR):
            return "movimento"
        time.sleep(config.INTERVALO_LEITURA)
    return None


def liberar():
    GPIO.cleanup()
