# Smart Office Planner - Project Summary

## Overview
This Smart Office Planner is a Python-based desktop application designed for managing important office events and sending timely notifications. It's built as part of a seminar paper on "Smart Offices" and demonstrates practical implementation of office productivity tools.

## Project Structure
```
/home/ivan/Vault/Programiranje/Epos Seminarski/
├── main.py                 # Main GUI application
├── cli.py                  # Command-line interface version
├── event_manager.py        # Event data management and persistence
├── notification_service.py # Desktop notification handling
├── add_event_dialog.py     # GUI dialog for adding/editing events
├── create_demo_data.py     # Script to create sample events
├── start.sh               # Startup script (recommended way to run)
├── requirements.txt       # Python dependencies
├── README.md             # Detailed documentation
├── PROJECT_SUMMARY.md    # This file
├── venv/                 # Virtual environment (created during setup)
└── events.json          # Data storage (created when events are added)
```

## Features Implemented

### Core Requirements ✅
- **Event Management**: Users can add, edit, and delete important future events
- **Desktop Notifications**: Application sends desktop notifications for approaching events
- **Calendar-like Interface**: Events are displayed chronologically with filtering options
- **No Background Daemon Required**: Application demonstrates notifications when running

### Additional Features
- **Dual Interface**: Both GUI (tkinter) and CLI versions available
- **Persistent Storage**: Events saved in JSON format
- **Smart Filtering**: View all events, today's events, this week, or upcoming only
- **Event Details**: Rich descriptions and customizable notification timing
- **Time Tracking**: Real-time countdown to events
- **Status Indicators**: Visual indicators for overdue, due, notified, and scheduled events
- **Export Functionality**: Export events to text file (CLI version)
- **Auto-refresh**: GUI automatically refreshes event status

## Technical Implementation

### Technologies Used
- **Python 3.12+**: Main programming language
- **tkinter**: GUI framework (system-provided)
- **plyer**: Cross-platform desktop notifications
- **JSON**: Data persistence
- **Threading**: Non-blocking notification monitoring

### Architecture
The application follows a modular design:

1. **Event Model** (`Event` class): Represents individual events with metadata
2. **Data Layer** (`EventManager`): Handles CRUD operations and persistence
3. **Notification Layer** (`NotificationService`): Manages desktop notifications
4. **Presentation Layer**: GUI (`main.py`) and CLI (`cli.py`) interfaces

### Notification Strategy
- **Timing**: Configurable notification timing (5-120 minutes before event)
- **Content**: Rich notifications with event details and time remaining
- **Monitoring**: Background thread checks for due notifications every minute
- **Status Tracking**: Events marked as notified to prevent duplicates

## Smart Office Context

This application addresses several smart office requirements:

### Productivity Enhancement
- Helps employees track important meetings and deadlines
- Reduces missed appointments through proactive notifications
- Provides quick overview of upcoming responsibilities

### Digital Workplace Integration
- Desktop notifications integrate with modern OS notification systems
- Lightweight application suitable for office workstations
- Data portability through JSON export/import

### User Experience
- Simple, intuitive interface suitable for office workers
- Multiple interaction modes (GUI/CLI) for different preferences
- Quick event creation with smart date parsing (CLI version)

## Demonstration Scenarios

### Scenario 1: Meeting Management
1. Employee adds important meeting 2 hours in advance
2. Sets notification for 15 minutes before
3. Application sends desktop notification when due
4. Employee is reminded and can prepare

### Scenario 2: Deadline Tracking
1. Employee enters project deadline with detailed description
2. Sets notification for 2 hours before to allow preparation time
3. Application tracks time remaining and shows countdown
4. Notification provides enough time for final preparations

### Scenario 3: Daily Planning
1. Employee views "Today" filter to see current day's events
2. Gets overview of time until each event
3. Can quickly add new events or modify existing ones
4. Real-time status updates keep information current

## Testing and Quality Assurance

### Tested Scenarios
- ✅ Event creation with various date/time formats
- ✅ Notification delivery on Ubuntu/Linux Mint
- ✅ Data persistence across application restarts
- ✅ Error handling for invalid inputs
- ✅ Multiple events with different notification timings
- ✅ Event filtering and status updates

### Known Limitations
- Desktop notifications depend on system support
- GUI requires X11/Wayland display server
- JSON data storage is not encrypted (suitable for office use)

## Installation and Usage

### Quick Start
```bash
# Clone the project
cd "/path/to/project"

# Run with automatic setup
./start.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
sudo apt install python3-tk  # if needed
pip install -r requirements.txt

# Run GUI version
python main.py

# OR run CLI version
python cli.py
```

## Future Enhancements for Smart Office Integration

### Potential Improvements
1. **Calendar Integration**: Sync with Google Calendar, Outlook
2. **Team Collaboration**: Share events with colleagues
3. **Meeting Room Booking**: Integration with office booking systems
4. **Email Notifications**: Alternative to desktop notifications
5. **Mobile Companion**: Web or mobile app for remote access
6. **Analytics**: Track productivity patterns and meeting frequencies
7. **IoT Integration**: Connect with smart office devices

### Smart Office Features
1. **Presence Detection**: Automatically adjust notifications based on office presence
2. **Resource Management**: Include room and equipment bookings
3. **Integration APIs**: Connect with existing office management systems
4. **Multi-tenant Support**: Support for multiple departments/teams
5. **Reporting**: Generate productivity and meeting reports

## Academic Context

This project demonstrates practical application of software engineering principles in smart office environments:

- **Requirements Analysis**: Translating office productivity needs into software features
- **User Interface Design**: Creating intuitive interfaces for office workers
- **System Integration**: Leveraging OS notification systems
- **Data Management**: Persistent storage of business-critical information
- **Error Handling**: Robust operation in office environments

## Conclusion

The Smart Office Planner successfully implements the core requirements for an office event management system with notifications. It demonstrates how modern software can enhance workplace productivity through intelligent reminders and organized event management. The dual-interface approach (GUI/CLI) ensures compatibility with various office setups and user preferences.

The application serves as a foundation for more advanced smart office systems and showcases the integration of desktop notifications with business applications. Its modular design allows for easy extension and integration with existing office infrastructure.

**Author**: Ivan  
**Course**: Smart Offices Seminar  
**Date**: August 27, 2025  
**Language**: Python 3.12  
**Platform**: Linux (Ubuntu/Mint)
