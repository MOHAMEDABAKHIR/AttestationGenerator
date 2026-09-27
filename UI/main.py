import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from .header import create_header
from .workscpace import create_workspace
from .footer import create_footer


APP_STYLE = """

/* =========================================================
   GLOBAL
   ========================================================= */

QWidget {
    font-family: "Segoe UI", "Inter", Arial, sans-serif;
    color: #17202A;
    font-size: 13px;
}

QMainWindow,
QWidget#mainWindow {
    background-color: #F5F7FA;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}


/* =========================================================
   HEADER
   ========================================================= */

QLabel#appTitle {
    font-size: 28px;
    font-weight: 700;
    color: #17202A;
}

QLabel#appSubtitle {
    font-size: 13px;
    color: #6B7280;
}


/* =========================================================
   SECTION
   ========================================================= */

QLabel#sectionTitle {
    font-size: 20px;
    font-weight: 700;
    color: #17202A;
    margin-top: 8px;
}

QLabel#sectionSubtitle {
    color: #6B7280;
    font-size: 13px;
}


/* =========================================================
   CARDS
   ========================================================= */

QFrame#importCard,
QFrame#configCard,
QFrame#selectionCard,
QFrame#actionCard {

    background-color: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 16px;
}

QLabel#cardTitle {
    font-size: 15px;
    font-weight: 700;
    color: #17202A;
}

QLabel#cardDescription {
    color: #6B7280;
    font-size: 12px;
}


/* =========================================================
   IMPORT
   ========================================================= */

QLabel#importIcon {
    font-size: 32px;
}

QFrame#fileArea {

    background-color: #F8FAFC;

    border: 1px dashed #CBD5E1;

    border-radius: 12px;
}

QLabel#fileName {

    font-size: 14px;

    font-weight: 600;

    color: #17202A;
}

QLabel#fileStatus {

    color: #64748B;

    font-size: 12px;
}

QLabel#successStatus {

    color: #16803C;

    font-weight: 600;
}


/* =========================================================
   FORM
   ========================================================= */

QLabel#fieldLabel {

    font-weight: 600;

    color: #374151;

    font-size: 12px;

    margin-bottom: 3px;
}

QComboBox {

    min-height: 42px;

    padding-left: 12px;
    padding-right: 12px;

    background-color: #FFFFFF;

    border: 1px solid #D1D5DB;

    border-radius: 9px;

    color: #111827;
}

QComboBox:hover {

    border-color: #94A3B8;
}

QComboBox:focus {

    border: 2px solid #2E7D32;
}

QComboBox QAbstractItemView {

    background-color: #FFFFFF;

    border: 1px solid #D1D5DB;

    selection-background-color: #E8F5E9;

    selection-color: #166534;
}


/* =========================================================
   BUTTONS
   ========================================================= */

QPushButton {

    border: none;

    border-radius: 9px;

    padding: 10px 16px;

    font-weight: 600;
}

QPushButton#primaryButton {

    background-color: #1B5E20;

    color: white;

    min-height: 42px;
}

QPushButton#primaryButton:hover {

    background-color: #2E7D32;
}

QPushButton#primaryButton:pressed {

    background-color: #145A18;
}

QPushButton#secondaryButton {

    background-color: #F1F5F9;

    color: #334155;

    border: 1px solid #E2E8F0;
}

QPushButton#secondaryButton:hover {

    background-color: #E2E8F0;
}

QPushButton#generateButton {

    background-color: #1B5E20;

    color: #FFFFFF;

    font-size: 14px;

    padding: 12px 22px;
}

QPushButton#generateButton:hover {

    background-color: #2E7D32;
}

QPushButton#generateButton:pressed {

    background-color: #145A18;
}

QPushButton#generateButton:disabled {

    background-color: #CBD5E1;

    color: #64748B;
}


/* =========================================================
   COMPANY LIST
   ========================================================= */

QListWidget {

    background-color: #F8FAFC;

    border: 1px solid #E2E8F0;

    border-radius: 10px;

    padding: 6px;

    min-height: 130px;
}

QListWidget::item {

    padding: 9px;

    border-radius: 7px;

    color: #334155;
}

QListWidget::item:hover {

    background-color: #F1F5F9;
}

QListWidget::item:selected {

    background-color: #E8F5E9;

    color: #166534;
}


/* =========================================================
   BADGE
   ========================================================= */

QLabel#counterBadge {

    background-color: #E8F5E9;

    color: #166534;

    border-radius: 12px;

    padding: 5px 10px;

    font-size: 11px;

    font-weight: 700;
}


/* =========================================================
   TABLE
   ========================================================= */

QTableWidget {

    background-color: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 12px;

    gridline-color: #EDF2F7;

    alternate-background-color: #F8FAFC;

    selection-background-color: #E8F5E9;

    selection-color: #166534;
}

QTableWidget::item {

    padding: 7px;
}

QHeaderView::section {

    background-color: #F1F5F9;

    color: #334155;

    padding: 10px;

    border: none;

    border-bottom: 1px solid #E2E8F0;

    font-weight: 700;

    font-size: 12px;
}


/* =========================================================
   FOOTER
   ========================================================= */

QLabel#footerText {

    color: #94A3B8;

    font-size: 11px;
}

QLabel#footerVersion {

    color: #94A3B8;

    font-size: 11px;
}
/* =========================================================
   DIALOGS
   ========================================================= */

QLabel#dialogTitle {

    font-size: 24px;

    font-weight: 700;

    color: #17202A;
}

QLabel#dialogDescription {

    color: #64748B;

    font-size: 13px;
}


/* =========================================================
   GENDER CARD
   ========================================================= */

QFrame#genderCard {

    background-color: #F8FAFC;

    border: 1px solid #E2E8F0;

    border-radius: 12px;
}

QLabel#genderCompany {

    font-size: 14px;

    font-weight: 700;

    color: #17202A;
}

QLabel#genderCeo {

    font-size: 12px;

    color: #64748B;
}

QRadioButton#genderRadio {

    spacing: 7px;

    color: #334155;

    font-weight: 600;
}

QRadioButton#genderRadio::indicator {

    width: 17px;

    height: 17px;
}

QRadioButton#genderRadio::indicator:checked {

    background-color: #1B5E20;

    border: 4px solid #FFFFFF;

    border-radius: 10px;
}


/* =========================================================
   PREVIEW
   ========================================================= */

QFrame#previewCard {

    background-color: #FFFFFF;

    border: 1px solid #E2E8F0;

    border-radius: 12px;
}

QLabel#previewCompany {

    font-size: 16px;

    font-weight: 700;

    color: #1B5E20;

    padding-bottom: 4px;
}

QLabel#previewLabel {

    color: #64748B;

    font-size: 11px;

    font-weight: 600;
}

QLabel#previewValue {

    color: #17202A;

    font-size: 13px;

    font-weight: 600;
}
"""


def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "Certificate Generator"
    )

    app.setOrganizationName(
        "ML"
    )

    app.setStyleSheet(
        APP_STYLE
    )

    window = QWidget()

    window.setObjectName(
        "mainWindow"
    )

    window.setWindowTitle(
        "Génération des attestations"
    )

    window.resize(
        1280,
        850
    )

    window.setMinimumSize(
        1050,
        700
    )

    # =========================================================
    # SCROLL
    # =========================================================

    scroll = QScrollArea()

    scroll.setWidgetResizable(
        True
    )

    content = QWidget()

    content_layout = QVBoxLayout(
        content
    )

    content_layout.setContentsMargins(
        42,
        32,
        42,
        25
    )

    content_layout.setSpacing(
        24
    )

    # =========================================================
    # HEADER
    # =========================================================

    header = create_header()

    content_layout.addWidget(
        header
    )

    # =========================================================
    # WORKSPACE
    # =========================================================

    workspace = create_workspace()

    content_layout.addWidget(
        workspace
    )

    # =========================================================
    # FOOTER
    # =========================================================

    footer = create_footer()

    content_layout.addWidget(
        footer
    )

    scroll.setWidget(
        content
    )

    root = QVBoxLayout(
        window
    )

    root.setContentsMargins(
        0,
        0,
        0,
        0
    )

    root.addWidget(
        scroll
    )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()