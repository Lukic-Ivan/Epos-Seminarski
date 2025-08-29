# Smart Office Planner

A desktop planner application for smart offices that allows users to manage important events and receive notifications for upcoming activities.

## Features

- **Event Management**: Add, edit, and delete events with detailed information
- **Desktop Notifications**: Automatic notifications for upcoming events
- **Calendar View**: Display events in chronological order with filtering options
- **Smart Filtering**: View events by All, Today, This Week, or Upcoming
- **Event Details**: Rich description support for each event
- **Time Tracking**: Real-time countdown to events
- **Persistent Storage**: Events are saved to local JSON file
- **User-Friendly Interface**: Intuitive GUI built with Tkinter

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- plyer (for desktop notifications)

## Installation

### Prerequisites
- Python 3.7+
- Linux desktop environment with notification support
- tkinter (for GUI version)

### Setup
1. Clone or download this project to your local machine
2. Navigate to the project directory
3. Run the setup script (recommended):

```bash
./start.sh
```

**OR** set up manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install tkinter if not available
sudo apt install python3-tk

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### GUI Version (Recommended)
Run the graphical interface:

```bash
./start.sh
```

Or manually:
```bash
source venv/bin/activate
python main.py
```

### Command Line Version
For headless environments or preference for CLI:

```bash
source venv/bin/activate
python cli.py
```

2. **Adding Events**:
   - Click "Add New Event" button
   - Fill in event title, description, date, and time
   - Set notification timing (5-120 minutes before)
   - Click "Save"

3. **Managing Events**:
   - Select an event from the list to view details
   - Double-click an event or use "Edit Selected" to modify
   - Use "Delete Selected" to remove events

4. **Filtering Events**:
   - Use radio buttons to filter events:
     - **All**: Show all events
     - **Today**: Show today's events only
     - **This Week**: Show events in the next 7 days
     - **Upcoming**: Show all future events

5. **Notifications**:
   - The app automatically monitors for upcoming events
   - Desktop notifications are sent based on your settings
   - Use "Test Notification" to verify notifications work

## File Structure

- `main.py` - Main application window and GUI
- `event_manager.py` - Event data management and persistence
- `notification_service.py` - Desktop notification handling
- `add_event_dialog.py` - Dialog for adding/editing events
- `events.json` - Local storage for events (created automatically)
- `requirements.txt` - Python dependencies

## Event Status Indicators

- 📅 **Scheduled**: Future events not yet due for notification
- 📢 **Due Now**: Events that should trigger notifications
- 🔔 **Notified**: Events for which notifications have been sent
- ⚠️ **Overdue**: Events that have passed their scheduled time

## Notification System

The application uses the `plyer` library to send cross-platform desktop notifications. Notifications include:

- Event title and description
- Scheduled time
- Time remaining until event
- Visual indicators for overdue events

## Smart Office Integration

This planner is designed for smart office environments where:

- Employees need to track meetings, deadlines, and important events
- Desktop notifications help maintain productivity
- Simple interface allows quick event management
- Persistent storage ensures events are not lost between sessions

## Troubleshooting

**Notifications not working?**
- Ensure your system allows desktop notifications
- Try the "Test Notification" button to verify functionality
- Check that `plyer` is properly installed

**Events not saving?**
- Ensure the application has write permissions in its directory
- Check for error messages in the console

**Time zone issues?**
- The application uses local system time
- Ensure your system clock is set correctly

## Future Enhancements

Potential improvements for smart office integration:
- Calendar synchronization (Google Calendar, Outlook)
- Email notifications for important events
- Team event sharing
- Meeting room booking integration
- Smart device integration (IoT notifications)

## License

This project is created for educational purposes as part of a seminar paper on "Smart Offices".
