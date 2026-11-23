# -*- coding: utf-8 -*-
"""Estado atual da missao, exibido na pagina do celular (modo web)."""

ESTADO = {"fase": "Iniciando", "mensagem": "", "trajeto": []}


def atualizar(**campos):
    ESTADO.update(campos)


def copia():
    dados = dict(ESTADO)
    dados["trajeto"] = list(dados["trajeto"])
    return dados
