#!/usr/bin/env python3
"""
Test skripta za dvostruki klik funkcionalnost
"""

import tkinter as tk
from main import SmartOfficePlannerApp
from event_manager import Event
from datetime import datetime, timedelta

def test_double_click():
    """Testira dvostruki klik funkcionalnost"""
    
    print("🧪 Testiranje dvostruki klik funkcionalnosti...")
    
    # Kreira aplikaciju
    app = SmartOfficePlannerApp()
    
    # Dodaje test događaje
    test_events = [
        Event('Sastanak tima', 'Dnevni standup', datetime.now() + timedelta(hours=1), 15),
        Event('Prezentacija', 'Prezentacija projekta', datetime.now() + timedelta(days=1), 30),
        Event('Pauza za kafu', 'Kratka pauza', datetime.now() + timedelta(minutes=30), 10)
    ]
    
    for event in test_events:
        app.event_manager.add_event(event)
    
    app.refresh_event_list()
    
    print(f"✅ Dodano {len(test_events)} test događaja")
    print(f"📊 Ukupno događaja u manageru: {len(app.event_manager.events)}")
    
    # Simulira selekciju prvog događaja
    items = app.event_tree.get_children()
    if items:
        # Postavlja selekciju
        app.event_tree.selection_set(items[0])
        app.event_tree.focus(items[0])
        
        print("🎯 Simuliranje dvostrukog klika...")
        
        try:
            # Poziva edit_event direktno
            app.edit_event()
            print("✅ edit_event metoda pozvan uspešno!")
            print("✅ Dijalog za izmenu treba da se otvori sa popunjenim poljima")
            
        except Exception as e:
            print(f"❌ Greška pri pozivu edit_event: {e}")
            return False
    else:
        print("❌ Nema događaja za testiranje")
        return False
    
    # Čeka malo pa zatvara aplikaciju
    app.root.after(3000, app.root.destroy)  # Zatvori nakon 3 sekunde
    
    print("🚀 Pokretanje GUI za vizuelno testiranje...")
    print("   Pokušaj dvostruki klik na neki događaj u listi!")
    
    try:
        app.run()
        print("✅ Test završen uspešno!")
        return True
    except Exception as e:
        print(f"❌ Greška u aplikaciji: {e}")
        return False

if __name__ == "__main__":
    success = test_double_click()
    if success:
        print("\n🎉 Svi testovi su prošli!")
    else:
        print("\n💥 Neki testovi nisu prošli!")
