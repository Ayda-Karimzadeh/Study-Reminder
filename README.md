# Study Reminder

A focused desktop application that helps you remember what you've learned using
spaced repetition. Nothing else.

## What it does

1. You click **Add Topic** and type a topic name (e.g. `Binary Search`).
2. The learning date is set automatically to today.
3. A review schedule is generated automatically for **Day 1, 3, 7, 14, 30, 60, 120**.
4. The app checks every minute for topics due today. When one is due, it sends a
   native desktop notification and automatically advances that topic to its
   next review stage.
5. Closing the window does not quit the app — it keeps running from the
   system tray, still checking dates and sending notifications.

There are no notes, flashcards, AI features, accounts, cloud sync, statistics,
or calendars. Just topics and their review schedule.

## Requirements

- Python 3.12+
- Windows (for native toast notifications and system tray integration;
  the app also runs on Linux/macOS with tray support, though notification
  styling will follow the OS's own tray notification system)

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The app stores its SQLite database at `~/.study_reminder/study_reminder.db`
(i.e. `C:\Users\<you>\.study_reminder\study_reminder.db` on Windows).

## Using the app

- **Add Topic** — opens a small dialog asking only for a topic name.
- **Search box** — filters the topic list live as you type.
- **Topic card** — shows the topic name, learning date, and next review date.
  Its border color and badge reflect status: scheduled, due today, overdue,
  or completed (all 7 stages finished).
- **Right-click a card** — lets you delete a topic you added by mistake.
- **Closing the window** — hides it to the system tray; the app keeps running.
- **Tray icon** — right-click for **Open** (show the window again) or
  **Exit** (fully quit the app). Double-clicking the tray icon also opens
  the window.

## Architecture

Clean, modular, and UI-independent scheduling logic:

```
study_reminder/
├── main.py                      # Composition root: wires everything together
├── core/
│   ├── scheduler.py              # ReviewScheduler — runs every minute, has no UI dependency
│   └── notification_service.py   # Wraps native tray notifications
├── database/
│   ├── database.py                # SQLite connection + schema owner
│   ├── repository.py              # Only place that runs SQL (TopicRepository)
│   └── models.py                  # Topic entity + spaced repetition interval logic
├── ui/
│   ├── main_window.py             # The single application window
│   ├── add_topic_dialog.py        # Modal dialog to add a topic name
│   ├── topic_card.py              # Card widget for a single topic
│   ├── tray_icon.py               # System tray icon + Open/Exit menu
│   ├── icon_factory.py            # Generates the app icon in-memory
│   └── theme.py                   # Dark theme stylesheet
└── requirements.txt
```

### Design principles applied

- **Separation of concerns** — `ReviewScheduler` only depends on
  `TopicRepository` and `NotificationService`; it has zero knowledge of any
  widget. The UI subscribes to its `topics_updated` signal to refresh itself.
- **Repository pattern** — `TopicRepository` is the only class that touches
  SQLite. The UI and scheduler never write SQL.
- **Single source of truth for scheduling** — `Topic.compute_next_review_date`
  in `models.py` is the only place review intervals are calculated, so the
  7-stage schedule can't drift between features.
- **No manual date entry anywhere** — the user only ever types a topic name.

## Packaging as a standalone .exe (optional)

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name "StudyReminder" main.py
```

The generated executable will be in `dist/StudyReminder.exe`.
