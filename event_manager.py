import json
import os
from datetime import datetime, timedelta
from typing import List, Dict

class Event:
    # Predefinisani tagovi
    AVAILABLE_TAGS = [
        "posao",        # work
        "sastanak",     # meeting
        "obrazovanje",  # education
        "zdravlje",     # health
        "sport",        # sports
        "lično",        # personal
        "društveno",    # social
        "kupovina",     # shopping
        "zabava",       # entertainment
        "porodica",     # family
        "putovanje",    # travel
        "projekat",     # project
        "rok",          # deadline
        "drugo"         # other
    ]
    
    def __init__(self, title: str, description: str, date_time: datetime, 
                 notification_minutes: int = 15, tags: List[str] = None):
        self.title = title
        self.description = description
        self.date_time = date_time
        self.notification_minutes = notification_minutes
        self.notified = False
        self.tags = tags if tags else []
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'description': self.description,
            'date_time': self.date_time.isoformat(),
            'notification_minutes': self.notification_minutes,
            'notified': self.notified,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Event':
        event = cls(
            title=data['title'],
            description=data['description'],
            date_time=datetime.fromisoformat(data['date_time']),
            notification_minutes=data['notification_minutes'],
            tags=data.get('tags', [])
        )
        event.notified = data.get('notified', False)
        return event
    
    def is_notification_due(self) -> bool:
        if self.notified:
            return False
        notification_time = self.date_time - timedelta(minutes=self.notification_minutes)
        return datetime.now() >= notification_time
    
    def is_overdue(self) -> bool:
        return datetime.now() > self.date_time
    
    def time_until_event(self) -> str:
        now = datetime.now()
        if now > self.date_time:
            return "Prošao je rok"
        
        diff = self.date_time - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days} dana, {hours} sati"
        elif hours > 0:
            return f"{hours} sati, {minutes} minuta"
        else:
            return f"{minutes} minuta"

class EventManager:
    
    def __init__(self, data_file: str = "dogadjaji.json"):
        self.data_file = data_file
        self.events: List[Event] = []
        self.load_events()
    
    def add_event(self, event: Event) -> None:
        self.events.append(event)
        self.save_events()
    
    def remove_event(self, index: int) -> bool:
        if 0 <= index < len(self.events):
            del self.events[index]
            self.save_events()
            return True
        return False
    
    def get_events(self, sort_by_date: bool = True) -> List[Event]:
        if sort_by_date:
            return sorted(self.events, key=lambda x: x.date_time)
        return self.events.copy()
    
    def get_upcoming_events(self, days: int = 7) -> List[Event]:
        now = datetime.now()
        end_date = now + timedelta(days=days)
        
        upcoming = []
        for event in self.events:
            if now <= event.date_time <= end_date:
                upcoming.append(event)
        
        return sorted(upcoming, key=lambda x: x.date_time)
    
    def get_events_needing_notification(self) -> List[Event]:
        return [event for event in self.events if event.is_notification_due()]
    
    def mark_event_notified(self, event: Event) -> None:
        event.notified = True
        self.save_events()
    
    def save_events(self) -> None:
        try:
            data = [event.to_dict() for event in self.events]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Greška pri čuvanju događaja: {e}")
    
    def load_events(self) -> None:
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.events = [Event.from_dict(item) for item in data]
        except Exception as e:
            print(f"Greška pri učitavanju događaja: {e}")
            self.events = []
