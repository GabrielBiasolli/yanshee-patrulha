# -*- coding: utf-8 -*-
"""As quatro fases da missao: gravar, patrulhar, detectar e reagir."""

import estado
import robo
import sensores


def gravar_trajeto(entrada, dispositivo):
    """Fase 1: teach-in. Cada comando executa o passo e entra no trajeto.

    `entrada` e o modulo de onde vem os comandos (controle ou teclado).
    """
    print("\n=== FASE 1: GRAVACAO DO TRAJETO ===")
    print("Comandos: frente | esquerda | direita")
    print("START encerra a gravacao e inicia a patrulha\n")

    trajeto = []
    estado.atualizar(fase="Gravacao", mensagem="Guie o robo; START encerra",
                     trajeto=[])
    while True:
        entrada.descartar_pendentes(dispositivo)
        comando = entrada.esperar_comando(dispositivo)

        if comando == "start":
            if trajeto:
                break
            print("[!] Grave pelo menos um passo antes de apertar START.")
            estado.atualizar(mensagem="Grave pelo menos um passo antes do START")
            continue

        estado.atualizar(mensagem="Executando: {}".format(comando))
        robo.executar_passo(comando)
        trajeto.append(comando)
        print("[+] Passo {} gravado. Trajeto: {}".format(len(trajeto), trajeto))
        estado.atualizar(mensagem="Passo {} gravado".format(len(trajeto)),
                         trajeto=list(trajeto))

    print("[+] Gravacao encerrada com {} passos.".format(len(trajeto)))
    return trajeto


def inverter_trajeto(trajeto):
    """Caminho de volta: ordem invertida, com esquerda e direita trocadas
    (o robo ja girou 180 graus, entao continua andando de frente)."""
    troca = {"esquerda": "direita", "direita": "esquerda"}
    return [troca.get(acao, acao) for acao in reversed(trajeto)]


def patrulhar(trajeto):
    """Fases 2 e 3: ida e volta, parando para escutar a cada passo,
    ate algum sensor disparar. Retorna "som", "movimento" ou "parada"."""
    print("\n=== FASE 2: PATRULHA ===")
    sensores.limpar_disparo_manual()   # ignora botoes apertados antes da patrulha
    sentido = list(trajeto)
    percurso = 0
    while True:
        percurso += 1
        print("\n[*] Percurso {}: {}".format(percurso, sentido))
        for acao in sentido + ["giro_180"]:
            estado.atualizar(fase="Patrulha", trajeto=list(sentido),
                             mensagem="Percurso {}: {}".format(percurso, acao))
            robo.executar_passo(acao)
            estado.atualizar(mensagem="Percurso {}: escutando".format(percurso))
            sensor = sensores.escutar_anormalidade()
            if sensor:
                return sensor
        sentido = inverter_trajeto(sentido)


def reagir_anormalidade(sensor, danca):
    """Fase 4: alerta, danca e volta ao reset."""
    print("\n=== FASE 4: ANORMALIDADE DETECTADA ({}) ===".format(sensor.upper()))
    estado.atualizar(fase="Alerta", mensagem="Detectado: {}. Dancando.".format(sensor))
    robo.led_alerta()
    print("[*] Dancando '{}'...".format(danca))
    robo.tocar_movimento(danca)
    print("[*] Voltando a posicao padrao.")
    robo.resetar()
    robo.led_normal()
