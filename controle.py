# -*- coding: utf-8 -*-
"""Leitura do controle USB 8-bit via evdev."""

from evdev import InputDevice, ecodes

import config


def abrir():
    dispositivo = InputDevice(config.DEVICE_PATH)
    print("[+] Controle: {} ({})".format(dispositivo.name, config.DEVICE_PATH))
    try:
        dispositivo.grab()   # uso exclusivo: os botoes nao vazam para o sistema
    except IOError:
        pass
    return dispositivo


def fechar(dispositivo):
    try:
        dispositivo.ungrab()
    except IOError:
        pass
    dispositivo.close()


def traduzir_evento(evento):
    """Converte um evento do evdev em "frente", "esquerda", "direita",
    "start" ou None. So reage ao apertar (ignora o soltar)."""
    if evento.type == ecodes.EV_KEY:
        if evento.code == config.BOTAO_START and evento.value == 1:
            return "start"
    elif evento.type == ecodes.EV_ABS:
        if evento.code == config.EIXO_VERTICAL and evento.value == config.VALOR_EIXO_MIN:
            return "frente"
        if evento.code == config.EIXO_HORIZONTAL:
            if evento.value == config.VALOR_EIXO_MIN:
                return "esquerda"
            if evento.value == config.VALOR_EIXO_MAX:
                return "direita"
    return None


def descartar_pendentes(dispositivo):
    """Joga fora o que foi apertado enquanto o robo se mexia, para nao
    virar passo fantasma."""
    while dispositivo.read_one() is not None:
        pass


def esperar_comando(dispositivo):
    """Bloqueia ate chegar um comando valido do controle."""
    for evento in dispositivo.read_loop():
        comando = traduzir_evento(evento)
        if comando:
            return comando
