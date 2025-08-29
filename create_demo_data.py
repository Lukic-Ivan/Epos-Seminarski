import json
from datetime import datetime, timedelta
from event_manager import Event, EventManager

def create_demo_events():
    """Kreira demo događaje za testiranje."""
    
    # Inicijalizuje menadžer događaja
    event_manager = EventManager()
    
    # Briše postojeće događaje za demo
    event_manager.events = []
    
    # Kreira demo događaje
    now = datetime.now()
    
    # Sastanak za 30 minuta
    meeting = Event(
        title="Jutarnji standup tim",
        description="Dnevni standup sastanak sa razvojnim timom. Diskusija o napretku, preprekama i planu za dan.",
        date_time=now + timedelta(minutes=30),
        notification_minutes=15
    )
    
    # Prezentacija sutra
    presentation = Event(
        title="Prezentacija projekta",
        description="Prezentacija Pametnog Kancelarijskog Planera zainteresovanim stranama. Priprema slajdova i demo.",
        date_time=now + timedelta(days=1, hours=2),
        notification_minutes=60
    )
    
    # Poziv klijenta sledeće nedelje
    client_call = Event(
        title="Pregled zahteva klijenta",
        description="Pregled zahteva klijenta za nove funkcionalnosti. Priprema pitanja i dokumentacije.",
        date_time=now + timedelta(days=7, hours=-2),
        notification_minutes=30
    )
    
    # Rok za 3 dana
    deadline = Event(
        title="Predaja seminarskog rada",
        description="Predaja seminarskog rada o Pametnim kancelarijama. Potreban je finalni pregled i formatiranje.",
        date_time=now + timedelta(days=3, hours=8),
        notification_minutes=120
    )
    
    # Pauza za kafu danas
    coffee_break = Event(
        title="Pauza za kafu sa kolegama",
        description="Neformalna pauza za kafu za diskusiju novih ideja i timsko okupljanje.",
        date_time=now + timedelta(hours=2),
        notification_minutes=10
    )
    
    # Dodaje sve događaje
    events = [meeting, presentation, client_call, deadline, coffee_break]
    for event in events:
        event_manager.add_event(event)
    
    print(f"Kreiran {len(events)} demo događaja:")
    for event in events:
        print(f"- {event.title} ({event.date_time.strftime('%d.%m.%Y %H:%M')})")

if __name__ == "__main__":
    create_demo_events()
