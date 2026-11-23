# -*- coding: utf-8 -*-
"""Substituto do controle para testes: comandos digitados no terminal.

Tem as mesmas funcoes do controle.py (abrir, fechar, descartar_pendentes,
esperar_comando), entao a Fase 1 funciona igual com qualquer um dos dois.
"""

import sys

TECLAS = {
    "w": "frente", "frente": "frente",
    "a": "esquerda", "esquerda": "esquerda",
    "d": "direita", "direita": "direita",
    "p": "start", "start": "start",
}


def abrir():
    print("[+] Modo teclado: w = frente | a = esquerda | d = direita | p = START")
    return None


def fechar(dispositivo):
    pass


def descartar_pendentes(dispositivo):
    """Joga fora o que foi digitado enquanto o robo se mexia."""
    try:
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass   # stdin nao e um terminal (ex.: redirecionado): nada a limpar


def esperar_comando(dispositivo):
    """Bloqueia ate o usuario digitar um comando valido + ENTER."""
    while True:
        texto = input("comando> ").strip().lower()
        if texto in TECLAS:
            return TECLAS[texto]
        print("[!] Comando invalido. Use w, a, d ou p.")
