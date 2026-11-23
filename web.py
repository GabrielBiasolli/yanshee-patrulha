# -*- coding: utf-8 -*-
"""Controle pelo celular: o robo serve uma pagina com botoes na rede Wi-Fi.

Tem as mesmas funcoes do controle.py (abrir, fechar, descartar_pendentes,
esperar_comando), entao a Fase 1 funciona igual. Alem das setas e do START,
a pagina simula os sensores (som / movimento) e tem um botao PARAR que
encerra a patrulha e volta o robo ao reset.

So usa a biblioteca padrao (Python 3.5).
"""

import json
import queue
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import config
import estado
import sensores

COMANDOS_TRAJETO = ("frente", "esquerda", "direita", "start")
COMANDOS_SENSOR = ("som", "movimento", "parada")

_fila = queue.Queue()

PAGINA = """<!doctype html>
<html lang="pt-br"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yanshee</title>
<style>
body{font-family:sans-serif;margin:0;padding:16px;background:#111;color:#eee;text-align:center}
#estado{background:#222;border-radius:8px;padding:12px;margin:0 auto 16px;max-width:360px;line-height:1.5}
.grade{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:360px;margin:0 auto 16px}
button{font-size:20px;padding:22px 0;border:0;border-radius:10px;background:#2d6cdf;color:#fff}
button:active{opacity:.6}
.start{background:#2a9d4b}.sim{background:#555}
.parar{background:#c62828;width:100%;max-width:360px}
h2{font-size:14px;color:#999;margin:18px 0 8px;font-weight:normal}
</style></head><body>
<div id="estado">conectando...</div>
<div class="grade">
<span></span><button onclick="cmd('frente')">&#8593;</button><span></span>
<button onclick="cmd('esquerda')">&#8592;</button>
<button class="start" onclick="cmd('start')">START</button>
<button onclick="cmd('direita')">&#8594;</button>
</div>
<h2>Simular sensores</h2>
<div class="grade" style="grid-template-columns:1fr 1fr">
<button class="sim" onclick="cmd('som')">Som</button>
<button class="sim" onclick="cmd('movimento')">Movimento</button>
</div>
<button class="parar" onclick="cmd('parada')">PARAR PATRULHA</button>
<script>
function cmd(c){fetch('/cmd/'+c,{method:'POST'}).then(atualizar);}
function atualizar(){
  fetch('/estado').then(function(r){return r.json();}).then(function(e){
    document.getElementById('estado').innerHTML='<b>'+e.fase+'</b><br>'+e.mensagem+
      '<br>Trajeto: '+(e.trajeto.join(', ')||'-');
  }).catch(function(){
    document.getElementById('estado').textContent='sem conexao com o robo';
  });
}
setInterval(atualizar,1000);atualizar();
</script></body></html>"""


class _Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self._responder(200, "text/html; charset=utf-8", PAGINA)
        elif self.path == "/estado":
            self._responder(200, "application/json", json.dumps(estado.copia()))
        else:
            self._responder(404, "text/plain", "nao encontrado")

    def do_POST(self):
        nome = self.path[len("/cmd/"):] if self.path.startswith("/cmd/") else ""
        if nome in COMANDOS_TRAJETO:
            _fila.put(nome)
        elif nome in COMANDOS_SENSOR:
            sensores.disparar_manual(nome)
        else:
            self._responder(404, "text/plain", "comando desconhecido")
            return
        print("[web] {}".format(nome))
        self._responder(200, "application/json", '{"ok": true}')

    def _responder(self, codigo, tipo, corpo):
        dados = corpo.encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, formato, *args):
        pass   # a pagina consulta o estado a cada segundo: sem log no terminal


class _Servidor(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def _ip_local():
    """Descobre o IP do robo na rede (nenhum pacote e enviado)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        sock.close()
        return ip
    except OSError:
        return "<IP_DO_ROBO>"


def abrir():
    servidor = _Servidor(("0.0.0.0", config.PORTA_WEB), _Handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    print("[+] Modo web: abra no celular  http://{}:{}".format(
        _ip_local(), config.PORTA_WEB))
    print("    (o celular precisa estar na mesma rede Wi-Fi do robo)")
    return servidor


def fechar(servidor):
    servidor.shutdown()
    servidor.server_close()


def descartar_pendentes(servidor):
    """Joga fora os botoes apertados enquanto o robo se mexia."""
    while True:
        try:
            _fila.get_nowait()
        except queue.Empty:
            return


def esperar_comando(servidor):
    """Bloqueia ate chegar um comando da pagina."""
    while True:
        try:
            return _fila.get(timeout=0.5)   # timeout: Ctrl+C continua funcionando
        except queue.Empty:
            pass
