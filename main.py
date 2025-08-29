import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, timedelta
from event_manager import EventManager
from notification_service import NotificationService
from add_event_dialog import AddEventDialog

class SmartOfficePlannerApp:
    """Glavni prozor aplikacije za Pametni Kancelarijski Planer."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pametni Kancelarijski Planer")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Inicijalizuje menadžere
        self.event_manager = EventManager()
        self.notification_service = NotificationService(self.event_manager)
        
        # Počinje praćenje obaveštenja
        self.notification_service.start_monitoring()
        
        # Kreira korisničku interfejs
        self.create_widgets()
        self.refresh_event_list()
        
        # Počinje automatsko osvežavanje
        self.start_auto_refresh()
        
        # Rukuje zatvaranjem prozora
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Kreira glavne elemente aplikacije."""
        # Glavni kontejner
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfiguracija težina mreže
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Naslov
        title_label = ttk.Label(main_frame, text="Pametni Kancelarijski Planer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Levi panel - Kontrole
        control_frame = ttk.LabelFrame(main_frame, text="Kontrole", padding="10")
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Dugme za dodavanje događaja
        ttk.Button(control_frame, text="Dodaj novi događaj", 
                  command=self.add_event, width=20).grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Dugme za izmenu događaja
        ttk.Button(control_frame, text="Izmeni izabrani", 
                  command=self.edit_event, width=20).grid(row=1, column=0, pady=(0, 10), sticky=tk.W)
        
        # Dugme za brisanje događaja
        ttk.Button(control_frame, text="Obriši izabrani", 
                  command=self.delete_event, width=20).grid(row=2, column=0, pady=(0, 10), sticky=tk.W)
        
        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Dugme za osvežavanje
        ttk.Button(control_frame, text="Osveži događaje", 
                  command=self.refresh_event_list, width=20).grid(row=4, column=0, pady=(0, 10), sticky=tk.W)
        
        # Dugme za test obaveštenja
        ttk.Button(control_frame, text="Test obaveštenja", 
                  command=self.test_notification, width=20).grid(row=5, column=0, pady=(0, 10), sticky=tk.W)
        
        # Separator
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=6, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # Opcije filtera
        ttk.Label(control_frame, text="Prikaži događaje:").grid(row=7, column=0, sticky=tk.W, pady=(0, 5))
        
        self.filter_var = tk.StringVar(value="all")
        filter_frame = ttk.Frame(control_frame)
        filter_frame.grid(row=8, column=0, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(filter_frame, text="Sve", variable=self.filter_var, 
                       value="all", command=self.refresh_event_list).pack(anchor=tk.W)
        ttk.Radiobutton(filter_frame, text="Danas", variable=self.filter_var, 
                       value="today", command=self.refresh_event_list).pack(anchor=tk.W)
        ttk.Radiobutton(filter_frame, text="Ova nedelja", variable=self.filter_var, 
                       value="week", command=self.refresh_event_list).pack(anchor=tk.W)
        ttk.Radiobutton(filter_frame, text="Predstojeći", variable=self.filter_var, 
                       value="upcoming", command=self.refresh_event_list).pack(anchor=tk.W)
        
        # Status
        self.status_var = tk.StringVar(value="Spreman")
        status_label = ttk.Label(control_frame, textvariable=self.status_var, 
                                font=("Arial", 9))
        status_label.grid(row=9, column=0, sticky=tk.W, pady=(20, 0))
        
        # Desni panel - Lista događaja
        list_frame = ttk.LabelFrame(main_frame, text="Događaji", padding="10")
        list_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview za događaje
        columns = ("Naslov", "Datum i vreme", "Vreme do", "Status")
        self.event_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=20)
        
        # Konfiguracija zaglavlja kolona i širina
        self.event_tree.heading("Naslov", text="Naslov događaja")
        self.event_tree.heading("Datum i vreme", text="Datum i vreme")
        self.event_tree.heading("Vreme do", text="Vreme do")
        self.event_tree.heading("Status", text="Status")
        
        self.event_tree.column("Naslov", width=250, minwidth=200)
        self.event_tree.column("Datum i vreme", width=150, minwidth=120)
        self.event_tree.column("Vreme do", width=120, minwidth=100)
        self.event_tree.column("Status", width=100, minwidth=80)
        
        # Klizači
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.event_tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.event_tree.xview)
        
        self.event_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Postavlja treeview i klizače
        self.event_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Vezuje dupli klik za izmenu
        self.event_tree.bind("<Double-1>", lambda e: self.edit_event())
        
        # Okvir za detalje događaja
        details_frame = ttk.LabelFrame(main_frame, text="Detalji događaja", padding="10")
        details_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        details_frame.columnconfigure(0, weight=1)
        
        self.details_text = tk.Text(details_frame, height=6, wrap=tk.WORD, state=tk.DISABLED)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        self.details_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Vezuje promenu izbora
        self.event_tree.bind("<<TreeviewSelect>>", self.on_event_select)
    
    def add_event(self):
        """Otvara dijalog za dodavanje novog događaja."""
        dialog = AddEventDialog(self.root)
        event = dialog.show()
        
        if event:
            self.event_manager.add_event(event)
            self.refresh_event_list()
            self.status_var.set(f"Dodat događaj: {event.title}")
    
    def edit_event(self):
        """Menja izabrani događaj."""
        selection = self.event_tree.selection()
        if not selection:
            messagebox.showwarning("Nema izbora", "Molimo izaberite događaj za izmenu.")
            return
        
        # Dobija indeks događaja
        item = selection[0]
        event_index = self.event_tree.index(item)
        events = self.get_filtered_events()
        
        if event_index < len(events):
            event = events[event_index]
            dialog = AddEventDialog(self.root, event)
            updated_event = dialog.show()
            
            if updated_event:
                # Pronalazi događaj u potpunoj listi i ažurira ga
                for i, e in enumerate(self.event_manager.events):
                    if e is event:
                        self.event_manager.events[i] = updated_event
                        self.event_manager.save_events()
                        break
                
                self.refresh_event_list()
                self.status_var.set(f"Ažuriran događaj: {updated_event.title}")
    
    def delete_event(self):
        """Briše izabrani događaj."""
        selection = self.event_tree.selection()
        if not selection:
            messagebox.showwarning("Nema izbora", "Molimo izaberite događaj za brisanje.")
            return
        
        # Dobija događaj
        item = selection[0]
        event_index = self.event_tree.index(item)
        events = self.get_filtered_events()
        
        if event_index < len(events):
            event = events[event_index]
            
            result = messagebox.askyesno("Potvrdi brisanje", 
                                       f"Da li ste sigurni da želite da obrišete događaj '{event.title}'?")
            if result:
                # Pronalazi i uklanja događaj iz potpune liste
                for i, e in enumerate(self.event_manager.events):
                    if e is event:
                        self.event_manager.remove_event(i)
                        break
                
                self.refresh_event_list()
                self.status_var.set(f"Obrisan događaj: {event.title}")
    
    def get_filtered_events(self):
        """Dobija događaje na osnovu trenutnog filtera."""
        filter_value = self.filter_var.get()
        
        if filter_value == "all":
            return self.event_manager.get_events()
        elif filter_value == "today":
            today = datetime.now().date()
            return [e for e in self.event_manager.get_events() 
                   if e.date_time.date() == today]
        elif filter_value == "week":
            return self.event_manager.get_upcoming_events(7)
        elif filter_value == "upcoming":
            return [e for e in self.event_manager.get_events() 
                   if e.date_time >= datetime.now()]
        
        return self.event_manager.get_events()
    
    def refresh_event_list(self):
        """Osvežava prikaz liste događaja."""
        # Briše postojeće stavke
        for item in self.event_tree.get_children():
            self.event_tree.delete(item)
        
        # Dobija filtrirane događaje
        events = self.get_filtered_events()
        
        # Dodaje događaje u stablo
        for event in events:
            # Određuje status
            if event.is_overdue():
                status = "⚠️ Prošao je rok"
                tags = ("overdue",)
            elif event.notified:
                status = "🔔 Obavešten"
                tags = ("notified",)
            elif event.is_notification_due():
                status = "📢 Sada je vreme"
                tags = ("due",)
            else:
                status = "📅 Zakazan"
                tags = ("scheduled",)
            
            self.event_tree.insert("", "end", values=(
                event.title,
                event.date_time.strftime("%d.%m.%Y %H:%M"),
                event.time_until_event(),
                status
            ), tags=tags)
        
        # Konfiguracija tagova za boje
        self.event_tree.tag_configure("overdue", background="#ffebee", foreground="#c62828")
        self.event_tree.tag_configure("due", background="#fff3e0", foreground="#ef6c00")
        self.event_tree.tag_configure("notified", background="#e8f5e8", foreground="#2e7d32")
        self.event_tree.tag_configure("scheduled", background="white", foreground="black")
        
        # Ažurira status
        count = len(events)
        filter_text_map = {
            "all": "Sve",
            "today": "Danas", 
            "week": "Ova nedelja",
            "upcoming": "Predstojeći"
        }
        filter_text = filter_text_map.get(self.filter_var.get(), "Sve")
        self.status_var.set(f"Prikazano {count} događaja ({filter_text})")
    
    def on_event_select(self, event):
        """Rukuje izborom događaja u stablu."""
        selection = self.event_tree.selection()
        if not selection:
            self.update_details("")
            return
        
        # Dobija izabrani događaj
        item = selection[0]
        event_index = self.event_tree.index(item)
        events = self.get_filtered_events()
        
        if event_index < len(events):
            selected_event = events[event_index]
            # Srpski dani u nedelji
            days_sr = ["ponedeljak", "utorak", "sreda", "četvrtak", "petak", "subota", "nedelja"]
            day_name = days_sr[selected_event.date_time.weekday()]
            
            # Srpski meseci
            months_sr = ["januar", "februar", "mart", "april", "maj", "jun",
                        "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]
            month_name = months_sr[selected_event.date_time.month - 1]
            
            details = f"Naslov: {selected_event.title}\n\n"
            details += f"Datum i vreme: {day_name}, {selected_event.date_time.day}. {month_name} {selected_event.date_time.year} u {selected_event.date_time.strftime('%H:%M')}\n\n"
            details += f"Vreme do događaja: {selected_event.time_until_event()}\n\n"
            details += f"Obaveštenje: {selected_event.notification_minutes} minuta pre\n\n"
            details += f"Opis:\n{selected_event.description}"
            
            self.update_details(details)
    
    def update_details(self, text):
        """Ažurira oblast sa detaljima teksta."""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", text)
        self.details_text.config(state=tk.DISABLED)
    
    def test_notification(self):
        """Šalje test obaveštenje."""
        try:
            self.notification_service.send_test_notification()
            self.status_var.set("Test obaveštenje poslano!")
        except Exception as e:
            messagebox.showerror("Greška obaveštenja", 
                               f"Neuspešno slanje test obaveštenja:\n{str(e)}")
    
    def start_auto_refresh(self):
        """Počinje automatsko osvežavanje liste događaja."""
        def auto_refresh():
            while True:
                time.sleep(30)  # Osvežava svakih 30 sekundi
                try:
                    self.root.after(0, self.refresh_event_list)
                except:
                    break
        
        refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
        refresh_thread.start()
    
    def on_closing(self):
        """Rukuje zatvaranjem aplikacije."""
        self.notification_service.stop_monitoring()
        self.root.destroy()
    
    def run(self):
        """Pokреće aplikaciju."""
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartOfficePlannerApp()
    app.run()
