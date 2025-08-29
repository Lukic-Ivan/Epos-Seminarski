#!/usr/bin/env python3
"""
Pametni Kancelarijski Planer - Interfejs komandne linije
Jednostavna CLI verzija za okruženja bez GUI podrške.
"""

import os
import sys
from datetime import datetime, timedelta
from event_manager import EventManager, Event
from notification_service import NotificationService

class PlannerCLI:
    """Interfejs komandne linije za Pametni Kancelarijski Planer."""
    
    def __init__(self):
        self.event_manager = EventManager()
        self.notification_service = NotificationService(self.event_manager)
    
    def show_menu(self):
        """Prikazuje glavni meni."""
        print("\n" + "="*50)
        print("🏢 PAMETNI KANCELARIJSKI PLANER - CLI")
        print("="*50)
        print("1. Prikaži sve događaje")
        print("2. Prikaži predstojeće događaje (narednih 7 dana)")
        print("3. Dodaj novi događaj")
        print("4. Obriši događaj")
        print("5. Proveri obaveštenja")
        print("6. Pošalji test obaveštenje")
        print("7. Izvezi događaje")
        print("0. Izlaz")
        print("-" * 50)
    
    def view_events(self, upcoming_only=False):
        """Prikazuje događaje."""
        if upcoming_only:
            events = self.event_manager.get_upcoming_events(7)
            title = "PREDSTOJEĆI DOGAĐAJI (Narednih 7 Dana)"
        else:
            events = self.event_manager.get_events()
            title = "SVI DOGAĐAJI"
        
        print(f"\n📅 {title}")
        print("-" * 60)
        
        if not events:
            print("Nema pronađenih događaja.")
            return
        
        for i, event in enumerate(events, 1):
            status = "⚠️ PROŠAO JE ROK" if event.is_overdue() else "📅 ZAKAZAN"
            if event.notified:
                status = "🔔 OBAVEŠTEN"
            elif event.is_notification_due():
                status = "📢 SADA JE VREME"
            
            print(f"\n{i}. {event.title}")
            print(f"   📍 Datum: {event.date_time.strftime('%d.%m.%Y %H:%M (%A)')}")
            print(f"   ⏰ Vreme do: {event.time_until_event()}")
            print(f"   🔔 Obavesti: {event.notification_minutes} min pre")
            print(f"   📊 Status: {status}")
            if event.description.strip():
                print(f"   📝 Opis: {event.description[:100]}{'...' if len(event.description) > 100 else ''}")
    
    def add_event(self):
        """Dodaje novi događaj interaktivno."""
        print("\n➕ DODAJ NOVI DOGAĐAJ")
        print("-" * 30)
        
        try:
            title = input("Naslov događaja: ").strip()
            if not title:
                print("❌ Naslov ne može biti prazan.")
                return
            
            description = input("Opis (opciono): ").strip()
            
            # Unos datuma
            print("\n📅 Datum i vreme:")
            print("Primeri: '2025-08-28', 'danas', 'sutra', '+3' (3 dana od danas)")
            date_input = input("Datum (GGGG-MM-DD ili skraćeno): ").strip().lower()
            
            # Parsiranje datuma
            if date_input == "danas":
                target_date = datetime.now().date()
            elif date_input == "sutra":
                target_date = (datetime.now() + timedelta(days=1)).date()
            elif date_input.startswith("+"):
                try:
                    days = int(date_input[1:])
                    target_date = (datetime.now() + timedelta(days=days)).date()
                except ValueError:
                    print("❌ Nevaljan format datuma.")
                    return
            else:
                try:
                    target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                except ValueError:
                    print("❌ Nevaljan format datuma. Koristite GGGG-MM-DD.")
                    return
            
            # Unos vremena
            time_input = input("Vreme (HH:MM) [podrazumevano: trenutno vreme]: ").strip()
            if not time_input:
                current_time = datetime.now().time()
                target_time = current_time.replace(second=0, microsecond=0)
            else:
                try:
                    target_time = datetime.strptime(time_input, "%H:%M").time()
                except ValueError:
                    print("❌ Nevaljan format vremena. Koristite HH:MM.")
                    return
            
            # Kombinuje datum i vreme
            event_datetime = datetime.combine(target_date, target_time)
            
            # Vreme obaveštenja
            print("\nOpcije obaveštenja: 5, 10, 15, 30, 60, 120 minuta")
            notification_input = input("Obavesti me (minuta pre) [podrazumevano: 15]: ").strip()
            try:
                notification_minutes = int(notification_input) if notification_input else 15
                if notification_minutes not in [5, 10, 15, 30, 60, 120]:
                    print("⚠️  Koristi se prilagođeno vreme obaveštenja:", notification_minutes, "minuta")
            except ValueError:
                notification_minutes = 15
            
            # Kreira i čuva događaj
            event = Event(title, description, event_datetime, notification_minutes)
            self.event_manager.add_event(event)
            
            print(f"\n✅ Događaj '{title}' uspešno dodat!")
            print(f"   📅 Zakazan za: {event_datetime.strftime('%d.%m.%Y %H:%M (%A)')}")
            print(f"   🔔 Obaveštenje: {notification_minutes} minuta pre")
            
        except KeyboardInterrupt:
            print("\n❌ Kreiranje događaja otkazano.")
        except Exception as e:
            print(f"❌ Greška pri kreiranju događaja: {e}")
    
    def delete_event(self):
        """Briše događaj."""
        events = self.event_manager.get_events()
        if not events:
            print("\n❌ Nema događaja za brisanje.")
            return
        
        print("\n🗑️  OBRIŠI DOGAĐAJ")
        print("-" * 20)
        
        # Prikazuje događaje sa brojevima
        for i, event in enumerate(events, 1):
            print(f"{i}. {event.title} - {event.date_time.strftime('%d.%m.%Y %H:%M')}")
        
        try:
            choice = input(f"\nUnesite broj događaja za brisanje (1-{len(events)}) [0 za otkazivanje]: ").strip()
            if choice == "0":
                print("❌ Brisanje otkazano.")
                return
            
            index = int(choice) - 1
            if 0 <= index < len(events):
                event = events[index]
                confirm = input(f"Da li ste sigurni da želite da obrišete '{event.title}'? (d/N): ").strip().lower()
                if confirm in ['d', 'da']:
                    # Pronalazi događaj u originalnoj listi i uklanja ga
                    for i, e in enumerate(self.event_manager.events):
                        if e is event:
                            self.event_manager.remove_event(i)
                            break
                    print(f"✅ Događaj '{event.title}' uspešno obrisan!")
                else:
                    print("❌ Brisanje otkazano.")
            else:
                print("❌ Nevaljan broj događaja.")
        except (ValueError, KeyboardInterrupt):
            print("❌ Nevaljan unos ili operacija otkazana.")
    
    def check_notifications(self):
        """Proverava i šalje čekajuća obaveštenja."""
        print("\n🔔 PROVERA OBAVEŠTENJA")
        print("-" * 30)
        
        events_to_notify = self.event_manager.get_events_needing_notification()
        
        if not events_to_notify:
            print("✅ Nema čekajućih obaveštenja.")
            return
        
        print(f"📢 Pronađeno {len(events_to_notify)} događaj(a) koji zahteva obaveštenje:")
        
        for event in events_to_notify:
            print(f"\n📅 {event.title}")
            print(f"   ⏰ Zakazano: {event.date_time.strftime('%d.%m.%Y %H:%M')}")
            print(f"   📍 Status: {event.time_until_event()}")
            
            try:
                self.notification_service.send_notification(event)
                print("   ✅ Desktop obaveštenje poslano!")
            except Exception as e:
                print(f"   ❌ Neuspešno slanje obaveštenja: {e}")
    
    def test_notification(self):
        """Šalje test obaveštenje."""
        print("\n🧪 SLANJE TEST OBAVEŠTENJA")
        print("-" * 35)
        
        try:
            self.notification_service.send_test_notification()
            print("✅ Test obaveštenje poslano! Proverite svoj desktop.")
        except Exception as e:
            print(f"❌ Neuspešno slanje test obaveštenja: {e}")
            print("💡 Proverite da vaš sistem podržava desktop obaveštenja.")
    
    def export_events(self):
        """Izvozi događaje u čitljiv format."""
        events = self.event_manager.get_events()
        if not events:
            print("\n❌ Nema događaja za izvoz.")
            return
        
        filename = f"izvoz_dogadjaja_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PAMETNI KANCELARIJSKI PLANER - IZVOZ DOGAĐAJA\n")
                f.write("=" * 50 + "\n")
                f.write(f"Izvozno na: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
                f.write(f"Ukupno događaja: {len(events)}\n\n")
                
                for i, event in enumerate(events, 1):
                    f.write(f"{i}. {event.title}\n")
                    f.write(f"   Datum: {event.date_time.strftime('%d.%m.%Y %H:%M (%A)')}\n")
                    f.write(f"   Status: {event.time_until_event()}\n")
                    f.write(f"   Obaveštenje: {event.notification_minutes} minuta pre\n")
                    if event.description.strip():
                        f.write(f"   Opis: {event.description}\n")
                    f.write("\n" + "-" * 40 + "\n\n")
            
            print(f"\n✅ Događaji izvozeni u: {filename}")
            
        except Exception as e:
            print(f"❌ Neuspešan izvoz događaja: {e}")
    
    def run(self):
        """Glavna petlja aplikacije."""
        print("🏢 Dobrodošli u Pametni Kancelarijski Planer CLI!")
        print("💡 Ova aplikacija vam pomaže da upravljate važnim kancelarijskim događajima.")
        
        # Početna provera obaveštenja
        self.notification_service.check_for_notifications()
        
        while True:
            try:
                self.show_menu()
                choice = input("Izaberite opciju: ").strip()
                
                if choice == "1":
                    self.view_events()
                elif choice == "2":
                    self.view_events(upcoming_only=True)
                elif choice == "3":
                    self.add_event()
                elif choice == "4":
                    self.delete_event()
                elif choice == "5":
                    self.check_notifications()
                elif choice == "6":
                    self.test_notification()
                elif choice == "7":
                    self.export_events()
                elif choice == "0":
                    print("\n👋 Hvala vam što koristite Pametni Kancelarijski Planer!")
                    print("💼 Ostanite organizovani i produktivni!")
                    break
                else:
                    print("❌ Nevalidna opcija. Molimo pokušajte ponovo.")
                
                input("\nPritisnite Enter za nastavak...")
                
            except KeyboardInterrupt:
                print("\n\n👋 Doviđenja!")
                break
            except Exception as e:
                print(f"\n❌ Došlo je do greške: {e}")
                input("Pritisnite Enter za nastavak...")

if __name__ == "__main__":
    app = PlannerCLI()
    app.run()
