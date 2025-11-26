import threading
import time
from plyer import notification
from typing import List
from event_manager import Event, EventManager

class NotificationService:
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager
        self.running = False
        self.check_thread = None
    
    def send_notification(self, event: Event) -> None:
        try:
            time_until = event.time_until_event()
            
            # Format tags for notification
            tags_str = f" [{', '.join(event.tags)}]" if event.tags else ""
            
            if event.is_overdue():
                title = f"⚠️ Prošao je rok: {event.title}{tags_str}"
                message = f"Događaj je bio zakazan za {event.date_time.strftime('%d.%m.%Y %H:%M')}\n\n{event.description}"
            else:
                title = f"🔔 Predstojeći događaj: {event.title}{tags_str}"
                message = f"Zakazano za: {event.date_time.strftime('%d.%m.%Y %H:%M')}\nVreme do događaja: {time_until}\n\n{event.description}"
            
            notification.notify(
                title=title,
                message=message,
                app_name="Pametne Kancelarije",
                timeout=10
            )
            self.event_manager.mark_event_notified(event)
            
        except Exception as e:
            print(f"Greška pri slanju obaveštenja: {e}")
    
    def check_for_notifications(self) -> None:
        events_to_notify = self.event_manager.get_events_needing_notification()
        for event in events_to_notify:
            self.send_notification(event)
    
    def start_monitoring(self) -> None:
        if self.running:
            return
        self.running = True
        self.check_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.check_thread.start()
    
    def stop_monitoring(self) -> None:
        self.running = False
        if self.check_thread and self.check_thread.is_alive():
            self.check_thread.join(timeout=1)
    
    def _monitor_loop(self) -> None:
        while self.running:
            try:
                self.check_for_notifications()
                time.sleep(60)  # Proverava svakog minuta
            except Exception as e:
                print(f"Greška u praćenju obaveštenja: {e}")
                time.sleep(60)
    
    def send_test_notification(self) -> None:
        try:
            notification.notify(
                title="🧪 Test aplikacije Pametne Kancelarije",
                message="Sistem obaveštenja radi ispravno!",
                app_name="Pametne Kancelarije",
                timeout=5
            )
        except Exception as e:
            print(f"Greška pri slanju test obaveštenja: {e}")
            raise
