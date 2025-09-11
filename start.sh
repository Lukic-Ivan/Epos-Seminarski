#!/bin/bash

# Skripta za pokretanje Pametnog Kancelarijskog Planera
# Ova skripta postavlja virtuelno okruženje i pokreće aplikaciju

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ ! -d "venv" ]; then
    echo "Kreiranje virtuelnog okruženja..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Neuspešno kreiranje virtuelnog okruženja. Molimo proverite da je python3-venv instaliran."
        echo "Pokrenite: sudo apt install python3-venv"
        exit 1
    fi
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter nije dostupan. Molimo instalirajte ga:"
    echo "   sudo apt install python3-tk"
    exit 1
fi

python -c "
try:
    from plyer import notification
    notification.notify(
        title='Pametne Kancelarije',
        message='Pokretanje... Sistem obaveštenja radi!',
        timeout=3
    )
    # print('Sistem obaveštenja radi')
except Exception as e:
    print(f'Sistem obaveštenja neće raditi ispravno: {e}')
"
python main.py
echo "Projektni zadatak za Epos Seminarski"
echo "================================"
