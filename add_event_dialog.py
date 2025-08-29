import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Optional
from event_manager import Event

class AddEventDialog:
    """Dijalog za dodavanje/izmenu događaja."""
    
    def __init__(self, parent, event: Optional[Event] = None):
        self.parent = parent
        self.event = event
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Dodaj događaj" if event is None else "Izmeni događaj")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrira dijalog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.create_widgets()
        
        if event:
            self.populate_fields()
    
    def create_widgets(self):
        """Kreira elemente dijaloga."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Naslov
        ttk.Label(main_frame, text="Naslov događaja:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Opis
        ttk.Label(main_frame, text="Opis:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.description_text = tk.Text(main_frame, height=6, width=50, wrap=tk.WORD)
        self.description_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Klizač za opis
        desc_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.description_text.yview)
        desc_scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.description_text.config(yscrollcommand=desc_scrollbar.set)
        
        # Datum i vreme
        datetime_frame = ttk.Frame(main_frame)
        datetime_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Datum
        ttk.Label(datetime_frame, text="Datum:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.date_var = tk.StringVar()
        self.date_entry = ttk.Entry(datetime_frame, textvariable=self.date_var, width=12)
        self.date_entry.grid(row=0, column=1, padx=(0, 20))
        ttk.Label(datetime_frame, text="(GGGG-MM-DD)", font=("Arial", 8)).grid(row=0, column=2, sticky=tk.W)
        
        # Vreme
        ttk.Label(datetime_frame, text="Vreme:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(5, 0))
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(datetime_frame, textvariable=self.time_var, width=12)
        self.time_entry.grid(row=1, column=1, padx=(0, 20), pady=(5, 0))
        ttk.Label(datetime_frame, text="(HH:MM)", font=("Arial", 8)).grid(row=1, column=2, sticky=tk.W, pady=(5, 0))
        
        # Brzi datumi
        quick_frame = ttk.Frame(main_frame)
        quick_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(quick_frame, text="Brzi datumi:").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(quick_frame, text="Danas", command=self.set_today, width=8).grid(row=0, column=1, padx=(10, 5))
        ttk.Button(quick_frame, text="Sutra", command=self.set_tomorrow, width=10).grid(row=0, column=2, padx=5)
        ttk.Button(quick_frame, text="Sledeća nedelja", command=self.set_next_week, width=15).grid(row=0, column=3, padx=5)
        
        # Obaveštenje
        notification_frame = ttk.Frame(main_frame)
        notification_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(notification_frame, text="Obavesti me:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.notification_var = tk.StringVar(value="15")
        notification_combo = ttk.Combobox(notification_frame, textvariable=self.notification_var, 
                                        values=["5", "10", "15", "30", "60", "120"], width=10, state="readonly")
        notification_combo.grid(row=0, column=1, padx=(0, 5))
        ttk.Label(notification_frame, text="minuta pre").grid(row=0, column=2, sticky=tk.W)
        
        # Dugmad
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Sačuvaj", command=self.save_event).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Otkaži", command=self.cancel).pack(side=tk.LEFT)
        
        # Postavlja osnovne vrednosti
        now = datetime.now()
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.time_var.set(now.strftime("%H:%M"))
        
        # Fokusira naslov
        self.title_entry.focus()
    
    def populate_fields(self):
        """Popunjava polja kada se menja postojeći događaj."""
        if self.event:
            self.title_var.set(self.event.title)
            self.description_text.insert("1.0", self.event.description)
            self.date_var.set(self.event.date_time.strftime("%Y-%m-%d"))
            self.time_var.set(self.event.date_time.strftime("%H:%M"))
            self.notification_var.set(str(self.event.notification_minutes))
    
    def set_today(self):
        """Postavlja datum na danas."""
        self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def set_tomorrow(self):
        """Postavlja datum na sutra."""
        tomorrow = datetime.now() + timedelta(days=1)
        self.date_var.set(tomorrow.strftime("%Y-%m-%d"))
    
    def set_next_week(self):
        """Postavlja datum na sledeću nedelju."""
        next_week = datetime.now() + timedelta(days=7)
        self.date_var.set(next_week.strftime("%Y-%m-%d"))
    
    def save_event(self):
        """Čuva događaj i zatvara dijalog."""
        # Validira unos
        title = self.title_var.get().strip()
        if not title:
            messagebox.showerror("Greška", "Molimo unesite naslov događaja.")
            return
        
        description = self.description_text.get("1.0", tk.END).strip()
        
        try:
            date_str = self.date_var.get().strip()
            time_str = self.time_var.get().strip()
            datetime_str = f"{date_str} {time_str}"
            event_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # Proverava da li je datum u prošlosti
            if event_datetime < datetime.now():
                result = messagebox.askyesno("Prošli datum", 
                                           "Izabrani datum i vreme su u prošlosti. "
                                           "Da li želite da nastavite?")
                if not result:
                    return
            
        except ValueError:
            messagebox.showerror("Greška", "Molimo unesite važeći datum (GGGG-MM-DD) i vreme (HH:MM).")
            return
        
        try:
            notification_minutes = int(self.notification_var.get())
        except ValueError:
            messagebox.showerror("Greška", "Molimo izaberite važeće vreme obaveštenja.")
            return
        
        # Kreira događaj
        self.result = Event(
            title=title,
            description=description,
            date_time=event_datetime,
            notification_minutes=notification_minutes
        )
        
        self.dialog.destroy()
    
    def cancel(self):
        """Otkazuje i zatvara dijalog."""
        self.dialog.destroy()
    
    def show(self):
        """Prikazuje dijalog i vraća rezultat."""
        self.dialog.wait_window()
        return self.result
