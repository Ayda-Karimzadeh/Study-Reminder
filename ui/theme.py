from __future__ import annotations

DARK_STYLESHEET = """
QWidget {
    background-color: #14151A;
    color: #F2F3F7;
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 14px;
}

#mainContainer {
    background-color: #14151A;
}

#headerTitle {
    font-size: 24px;
    font-weight: 700;
    color: #FFFFFF;
}

#headerSubtitle {
    color: #8A8D9A;
    font-size: 13px;
}

QLineEdit#searchInput {
    background-color: #1E2028;
    border: 1px solid #2B2E38;
    border-radius: 10px;
    padding: 10px 14px;
    color: #F2F3F7;
    font-size: 13px;
}

QLineEdit#searchInput:focus {
    border: 1px solid #7C5CFF;
}

QPushButton#primaryButton {
    background-color: #7C5CFF;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton#primaryButton:hover {
    background-color: #8E71FF;
}

QPushButton#primaryButton:pressed {
    background-color: #6A49E8;
}

QPushButton#secondaryButton {
    background-color: transparent;
    color: #B7B9C4;
    border: 1px solid #2B2E38;
    border-radius: 10px;
    padding: 10px 18px;
    font-size: 13px;
}

QPushButton#secondaryButton:hover {
    background-color: #1E2028;
    color: #FFFFFF;
}

QFrame#topicCard {
    background-color: #1B1D24;
    border-radius: 14px;
    border: 1px solid #262932;
}

QFrame#topicCard[status="due"] {
    border: 1px solid #F5B342;
}

QFrame#topicCard[status="overdue"] {
    border: 1px solid #FF5C6C;
}

QFrame#topicCard[status="completed"] {
    border: 1px solid #3AD68C;
}

QLabel#topicName {
    font-size: 16px;
    font-weight: 600;
    color: #FFFFFF;
    background: transparent;
}

QLabel#topicMeta {
    color: #8A8D9A;
    font-size: 12px;
    background: transparent;
}

QLabel#statusBadge {
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    background-color: #262932;
    color: #C7C9D4;
    min-width: 96px;
    qproperty-alignment: AlignCenter;
}

QLabel#statusBadge[status="due"] {
    background-color: rgba(245, 179, 66, 40);
    color: #F5B342;
}

QLabel#statusBadge[status="overdue"] {
    background-color: rgba(255, 92, 108, 40);
    color: #FF5C6C;
}

QLabel#statusBadge[status="completed"] {
    background-color: rgba(58, 214, 140, 40);
    color: #3AD68C;
}

QLabel#dialogTitle {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    background: transparent;
}

QLabel#dialogSubtitle {
    color: #8A8D9A;
    font-size: 12px;
    background: transparent;
}

QLineEdit#topicInput {
    background-color: #1E2028;
    border: 1px solid #2B2E38;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 14px;
}

QLineEdit#topicInput:focus {
    border: 1px solid #7C5CFF;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2B2E38;
    border-radius: 4px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #3A3D4A;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QLabel#emptyStateLabel {
    color: #63666F;
    font-size: 14px;
    background: transparent;
}

QMenu {
    background-color: #1E2028;
    border: 1px solid #2B2E38;
    border-radius: 8px;
    padding: 6px;
}

QMenu::item {
    padding: 8px 16px;
    border-radius: 6px;
}

QMenu::item:selected {
    background-color: #2B2E38;
}
"""
