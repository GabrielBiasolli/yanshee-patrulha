# yanshee-patrulha

Patrulha autônoma para o robô humanoide **UBTECH Yanshee** (Raspberry Pi 3B, Python 3.5).

1. **Gravação (teach-in):** o usuário guia o robô com um controle USB 8-bit (frente, esquerda, direita). Cada passo é executado e gravado. START encerra.
2. **Patrulha:** o robô percorre o trajeto em ida e volta. No fim, gira 180° e faz o caminho inverso, com esquerda e direita trocadas.
3. **Detecção:** a cada passo, o robô para e escuta um sensor de som e um PIR. O que os sensores captam enquanto ele anda é descartado, para que o barulho dos servos não dispare alarme.
4. **Reação:** ao detectar som alto ou movimento, pisca o LED vermelho, dança a música da Shakira, volta ao `reset` e encerra.

## Hardware

| Sensor | GPIO (BCM) | Pino físico |
|---|---|---|
| Som KY-037/KY-038 (DO) | 17 | 11 |
| PIR HC-SR501 (OUT) | 27 | 13 |

> O GPIO aceita no máximo **3.3 V**. Alimente o KY-037 em 3.3 V; em 5 V a saída DO pode queimar o pino.

## Estrutura

| Arquivo | Responsabilidade |
|---|---|
| `config.py` | Todas as constantes configuráveis |
| `robo.py` | YanAPI: movimentos, LED, lista de danças |
| `sensores.py` | RPi.GPIO: som e PIR |
| `controle.py` | evdev: controle USB 8-bit |
| `teclado.py` | Substituto do controle para testes |
| `patrulha.py` | As fases: gravar, patrulhar, reagir |
| `main.py` | Ponto de entrada |

## Como rodar

```bash
sudo python3 main.py
```

Rode de dentro da pasta do projeto. Dependências no robô: `YanAPI` (já vem no Yanshee), `RPi.GPIO` e `evdev`.

### Testar sem o controle

Em `config.py`, mude `MODO_ENTRADA`:

- `"teclado"`: grave o trajeto digitando `w` (frente), `a` (esquerda), `d` (direita) e `p` (START) no terminal.
- `"fixo"`: pula a gravação e patrulha direto o `TRAJETO_FIXO`.

Nesses dois modos o `evdev` não é necessário.

## Calibração

- `REPEAT_GIRO_180`: ajuste no chão até o giro dar ~180°.
- `DEVICE_PATH`, `BOTAO_START` e eixos do direcional: confirme com `sudo evtest`.
- `NOME_DANCA_SHAKIRA`: confirme o nome exato com
  `python3 -c "import YanAPI; YanAPI.yan_api_init('127.0.0.1'); print(YanAPI.get_motion_list_value())"`.
  Se o nome não existir, o programa procura na lista algo com "waka" ou "shakira".
