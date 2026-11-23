#!/bin/sh
# Instala as dependencias do controle USB no Yanshee. Rodar uma vez:
#   ./instalar.sh
# YanAPI e RPi.GPIO ja vem instalados no robo. Sem o evdev, o programa
# ainda roda: ele usa o modo web (celular) no lugar do controle.

echo "[*] Instalando evdev e evtest..."
if ! sudo apt-get install -y python3-evdev evtest; then
    echo "[!] apt falhou; tentando pelo pip"
    sudo pip3 install evdev
fi

echo "[*] Conferindo..."
python3 -c "import evdev; print('[+] evdev OK')" || echo "[-] evdev NAO instalado"
python3 -c "import YanAPI; print('[+] YanAPI OK')" || echo "[-] YanAPI NAO encontrado"
python3 -c "import RPi.GPIO; print('[+] RPi.GPIO OK')" || echo "[-] RPi.GPIO NAO encontrado"
