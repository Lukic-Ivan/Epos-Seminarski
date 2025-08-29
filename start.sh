#!/bin/bash

# Skripta za pokretanje Pametnog Kancelarijskog Planera
# Ova skripta postavlja virtuelno okruženje i pokreće aplikaciju

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🏢 Pametni Kancelarijski Planer"
echo "================================"

# Proverava da li virtuelno okruženje postoji
if [ ! -d "venv" ]; then
    echo "Kreiranje virtuelnog okruženja..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Neuspešno kreiranje virtuelnog okruženja. Molimo proverite da je python3-venv instaliran."
        echo "Pokrenite: sudo apt install python3-venv"
        exit 1
    fi
fi

# Aktivira virtuelno okruženje
echo "Aktiviranje virtuelnog okruženja..."
source venv/bin/activate

# Instalira zavisnosti ako je potrebno
echo "Provera zavisnosti..."
pip install -r requirements.txt > /dev/null 2>&1

# Proverava da li je tkinter dostupan (treba da bude instaliran na nivou sistema)
python -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ tkinter nije dostupan. Molimo instalirajte ga:"
    echo "   sudo apt install python3-tk"
    exit 1
fi

# Testira sistem obaveštenja
echo "Testiranje sistema obaveštenja..."
python -c "
try:
    from plyer import notification
    notification.notify(
        title='Pametni Kancelarijski Planer',
        message='Pokretanje... Sistem obaveštenja radi!',
        timeout=3
    )
    print('✅ Sistem obaveštenja radi')
except Exception as e:
    print(f'⚠️  Sistem obaveštenja možda neće raditi ispravno: {e}')
"

echo "🚀 Pokretanje Pametnog Kancelarijskog Planera..."
echo "   Možete zatvoriti ovaj terminal nakon što se aplikacija pokrene."
echo ""

# Pokreće aplikaciju
python main.py

echo "👋 Hvala vam što koristite Pametni Kancelarijski Planer!"
