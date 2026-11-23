# -*- coding: utf-8 -*-
"""Acoes do Yanshee via YanAPI: movimentos, LED e lista de dancas."""

import YanAPI

import config


def iniciar():
    YanAPI.yan_api_init(config.ROBO_IP)


def tocar_movimento(nome, direcao="", repeat=1):
    """Executa um movimento e so retorna quando ele termina."""
    resultado = YanAPI.sync_play_motion(name=nome, direction=direcao,
                                        speed=config.VELOCIDADE, repeat=repeat)
    if isinstance(resultado, dict) and resultado.get("code", 0) != 0:
        print("[!] Movimento '{}' retornou: {}".format(nome, resultado))
    return resultado


def executar_passo(acao):
    """Executa uma acao do trajeto ("frente", "esquerda", "direita", "giro_180")."""
    nome, direcao = config.MOVIMENTOS[acao]
    repeat = config.REPEAT_GIRO_180 if acao == "giro_180" else config.REPEAT_PASSO
    print("[>] {} ({} {} x{})".format(acao, nome, direcao, repeat))
    tocar_movimento(nome, direcao, repeat)


def resetar():
    tocar_movimento("reset")


def definir_led(cor, modo):
    try:
        YanAPI.set_robot_led("button", cor, modo)
    except Exception as erro:
        print("[!] Falha ao ajustar o LED: {}".format(erro))


def led_normal():
    definir_led(*config.LED_NORMAL)


def led_alerta():
    definir_led(*config.LED_ALERTA)


def _extrair_nomes(dado):
    """Achata a resposta de get_motion_list_value() numa lista de nomes,
    seja ela lista, dicionario por categoria ou lista de {"name": ...}."""
    if isinstance(dado, str):
        return [dado]
    if isinstance(dado, dict):
        if "name" in dado:
            return [str(dado["name"])]
        dado = list(dado.values())
    nomes = []
    if isinstance(dado, (list, tuple)):
        for item in dado:
            nomes.extend(_extrair_nomes(item))
    return nomes


def resolver_nome_danca():
    """Confere se a danca existe no robo e devolve o nome a usar."""
    try:
        nomes = _extrair_nomes(YanAPI.get_motion_list_value())
    except Exception as erro:
        print("[!] Nao consegui listar os movimentos: {}".format(erro))
        return config.NOME_DANCA_SHAKIRA

    if config.NOME_DANCA_SHAKIRA in nomes:
        return config.NOME_DANCA_SHAKIRA
    for nome in nomes:
        if any(palavra in nome.lower() for palavra in config.PALAVRAS_DANCA):
            print("[!] '{}' nao existe; usando '{}'.".format(
                config.NOME_DANCA_SHAKIRA, nome))
            return nome
    print("[!] Danca '{}' nao encontrada. Movimentos no robo: {}".format(
        config.NOME_DANCA_SHAKIRA, nomes))
    return config.NOME_DANCA_SHAKIRA
