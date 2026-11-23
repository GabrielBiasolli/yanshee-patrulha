#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patrulha Yanshee - ponto de entrada.

  config.py    constantes configuraveis (pinos, controle, tempos, danca)
  robo.py      YanAPI: movimentos, LED, lista de dancas
  sensores.py  RPi.GPIO: som e PIR com anti-falso positivo
  controle.py  evdev: leitura do controle USB 8-bit
  web.py       controle pelo celular (pagina com botoes) para testes
  teclado.py   substituto do controle para testes (comandos no terminal)
  estado.py    estado atual da missao, exibido na pagina do celular
  patrulha.py  as fases: gravar, patrulhar, reagir

Para testar sem o controle, mude MODO_ENTRADA no config.py para "web",
"teclado" ou "fixo".

Compativel com Python 3.5 (Raspberry Pi 3B do Yanshee).
Rodar de dentro desta pasta:  sudo python3 main.py

Os textos impressos nao tem acento de proposito: no Python 3.5 com locale "C"
um print() com acento derruba o programa com UnicodeEncodeError.
"""

import config
import patrulha
import robo
import sensores


def _usar_web_no_lugar(motivo):
    print("[!] {}".format(motivo))
    print("[!] Usando o modo web (celular) no lugar do controle.")
    import web
    return web


def escolher_entrada():
    """Devolve o modulo de entrada da Fase 1, ou None no modo "fixo".
    O import e feito aqui para os modos de teste nao exigirem o evdev."""
    if config.MODO_ENTRADA == "controle":
        try:
            import controle
        except ImportError:
            return _usar_web_no_lugar(
                "evdev nao instalado (rode ./instalar.sh).")
        return controle
    if config.MODO_ENTRADA == "web":
        import web
        return web
    if config.MODO_ENTRADA == "teclado":
        import teclado
        return teclado
    if config.MODO_ENTRADA == "fixo":
        return None
    raise ValueError("MODO_ENTRADA invalido: {}".format(config.MODO_ENTRADA))


def abrir_entrada(entrada):
    """Abre a entrada; se o controle nao estiver conectado, cai no modo web.
    Devolve (modulo, dispositivo)."""
    erro_controle = getattr(entrada, "ControleNaoEncontrado", None)
    if erro_controle is None:
        return entrada, entrada.abrir()
    try:
        return entrada, entrada.abrir()
    except erro_controle as erro:
        web = _usar_web_no_lugar(str(erro))
        return web, web.abrir()


def main():
    entrada = None
    dispositivo = None
    try:
        entrada = escolher_entrada()
        robo.iniciar()
        sensores.configurar()
        danca = robo.resolver_nome_danca()
        print("[+] Danca de alerta: '{}'".format(danca))

        robo.resetar()
        robo.led_normal()

        if entrada is None:
            trajeto = list(config.TRAJETO_FIXO)
            print("[+] Modo fixo: pulando a gravacao. Trajeto: {}".format(trajeto))
        else:
            entrada, dispositivo = abrir_entrada(entrada)
            trajeto = patrulha.gravar_trajeto(entrada, dispositivo)

        sensor = patrulha.patrulhar(trajeto)
        if sensor == "parada":
            print("\n[!] Patrulha parada pela pagina. Voltando ao reset.")
            robo.resetar()
            robo.led_normal()
        else:
            patrulha.reagir_anormalidade(sensor, danca)
        print("\n[+] Missao concluida. Encerrando.")

    except KeyboardInterrupt:
        print("\n[!] Interrompido pelo usuario. Voltando ao reset.")
        try:
            robo.resetar()
            robo.led_normal()
        except Exception as erro:
            print("[!] Falha ao resetar o robo: {}".format(erro))

    finally:
        if dispositivo is not None:
            entrada.fechar(dispositivo)
        sensores.liberar()
        print("[+] GPIO liberado.")


if __name__ == "__main__":
    main()


# ============================================================================
# COMANDOS UTEIS (rodar no terminal do Yanshee, via SSH)
# ============================================================================
# 0) Instalar as dependencias do controle (uma vez):
#      ./instalar.sh
#
# 1) Descobrir o eventX do controle e os codigos dos botoes:
#      sudo evtest             # escolha o numero do "USB Gamepad" na lista,
#                               # aperte direcional/START e anote type/code/value
#      ls -l /dev/input/by-id/  # mostra qual eventX e o joystick
#
# 2) Listar os nomes exatos dos movimentos/dancas salvos no robo:
#      python3 -c "import YanAPI; YanAPI.yan_api_init('127.0.0.1'); print(YanAPI.get_motion_list_value())"
#
# 3) Rodar (de dentro da pasta do projeto):
#      sudo python3 main.py
