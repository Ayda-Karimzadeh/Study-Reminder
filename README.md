# Study Reminder

A focused desktop application that helps you remember what you've learned using
spaced repetition. Nothing else.

## What it does

1. You click **Add Topic** and type a topic name (e.g. `Binary Search`).
2. The learning date is set automatically to today.
3. A review schedule is generated automatically for **Day 1, 3, 7, 21, 30, 60,
   120, 240, 365** — fast repetition early to consolidate the memory, then
   progressively wider spacing for long-term retention. Only the first
   review is counted from the learning date; every review after that is
   counted from the date the *previous* review was actually confirmed, so
   reviewing late never compresses the following reviews into an instant
   backlog.
4. The app checks every minute for topics due today. When one is due, it sends
   a native desktop notification.
5. **The review only counts once you tick "Mark as reviewed" on that topic's
   card.** Nothing advances automatically — if you don't tick it, the topic
   keeps showing up as due and you'll get reminded again the next day, so a
   review can never be silently skipped.
6. Closing the window does not quit the app — it keeps running from the
   system tray, still checking dates and sending notifications.
7. The app can start automatically when you turn on your computer (see
   below).

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
  or completed (all 9 stages finished).
- **"Mark as reviewed" checkbox** — appears only on cards that are due or
  overdue. Ticking it is the only thing that advances a topic to its next
  stage. Until you tick it, the topic stays due and keeps notifying you.
- **Right-click a card** — lets you delete a topic you added by mistake.
- **Closing the window** — hides it to the system tray; the app keeps running.
- **Tray icon** — right-click for **Open** (show the window again),
  **Start with Windows** (toggle auto-launch at login — only shown/functional
  in the packaged `.exe`, not when running from source), or **Exit** (fully
  quit the app). Double-clicking the tray icon also opens the window.

## Architecture

Clean, modular, and UI-independent scheduling logic:

```
study_reminder/
├── main.py                      # Composition root: wires everything together
├── core/
│   ├── scheduler.py              # ReviewScheduler — runs every minute, has no UI dependency
│   ├── notification_service.py   # Wraps native tray notifications
│   └── startup_manager.py        # Windows "start at login" via the Run registry key
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
  9-stage schedule can't drift between features. Every review after the
  first is scheduled from the date it was actually confirmed, not from a
  fixed origin date, so a late review never creates a compounding backlog.
- **Reviews are never auto-completed** — `ReviewScheduler` only reads
  (`get_topics_pending_notification`) and marks topics as notified; only
  `TopicRepository.advance_review_stage`, triggered by the "Mark as
  reviewed" checkbox, moves a topic to its next stage. This guarantees a
  review is only counted when it actually happens.
- **No manual date entry anywhere** — the user only ever types a topic name.

## Packaging as a standalone .exe (optional)

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --icon="assets/icons/app_icon.ico" --name "StudyReminder" main.py
```

The generated executable will be in `dist/StudyReminder.exe`.

> **Start with Windows** only works for this packaged `.exe` — the app
> detects whether it's running as a frozen executable and silently skips
> registering itself for auto-start when run as a plain Python script.
> On first launch of the `.exe`, it registers itself to start at login
> automatically; you can turn this off any time from the tray icon menu.

## Version history

- **v2.0.1** — Fixed: reviewing a topic late no longer pushes every
  following review into an immediate backlog. Each review after the first
  is now scheduled from the date it was actually confirmed, not from the
  original learning date.
- **v2.0.0** — Reviews now require manual confirmation via a "Mark as
  reviewed" checkbox instead of advancing automatically. Updated schedule
  to Day 1, 3, 7, 21, 30, 60, 120, 240, 365. Added "Start with Windows"
  support.
- **v1.0.0** — Initial release.
