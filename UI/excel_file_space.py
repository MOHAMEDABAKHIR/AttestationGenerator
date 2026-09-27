import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QFrame
)

from PySide6.QtCore import (
    Qt,
    Signal,
    QSettings
)

from PySide6.QtGui import QPixmap


class ExcelImportWidget(QFrame):

    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_file = ""

        self.setObjectName("importCard")

        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            28,
            24,
            28,
            24
        )

        root.setSpacing(16)

        # -----------------------------------------------------
        # TOP
        # -----------------------------------------------------

        top = QHBoxLayout()

        icon = QLabel("📊")
        icon.setObjectName("importIcon")

        title_container = QVBoxLayout()
        title_container.setSpacing(2)

        title = QLabel(
            "Importer un fichier Excel"
        )

        title.setObjectName("cardTitle")

        description = QLabel(
            "Formats acceptés : .xlsx, .xlsm, .xls"
        )

        description.setObjectName("cardDescription")

        title_container.addWidget(title)
        title_container.addWidget(description)

        top.addWidget(icon)
        top.addLayout(title_container)
        top.addStretch()

        root.addLayout(top)

        # -----------------------------------------------------
        # FILE AREA
        # -----------------------------------------------------

        file_area = QFrame()
        file_area.setObjectName("fileArea")

        file_layout = QVBoxLayout(file_area)

        file_layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        file_layout.setSpacing(10)

        self.file_label = QLabel(
            "Aucun fichier sélectionné"
        )

        self.file_label.setObjectName(
            "fileName"
        )

        self.file_label.setWordWrap(True)

        self.status_label = QLabel(
            "Commencez par sélectionner votre fichier."
        )

        self.status_label.setObjectName(
            "fileStatus"
        )

        file_layout.addWidget(
            self.file_label
        )

        file_layout.addWidget(
            self.status_label
        )

        root.addWidget(file_area)

        # -----------------------------------------------------
        # BUTTON
        # -----------------------------------------------------

        buttons = QHBoxLayout()

        self.import_button = QPushButton(
            "📂  Choisir un fichier Excel"
        )

        self.import_button.setObjectName(
            "primaryButton"
        )

        self.import_button.setCursor(
            Qt.PointingHandCursor
        )

        self.import_button.clicked.connect(
            self.select_file
        )

        buttons.addWidget(
            self.import_button
        )

        buttons.addStretch()

        root.addLayout(buttons)

        self.restore_last_file()

    # ---------------------------------------------------------
    # ACTION
    # ---------------------------------------------------------

    def select_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier Excel",
            "",
            "Fichiers Excel (*.xlsx *.xlsm *.xls);;"
            "Tous les fichiers (*)"
        )

        if not file_path:
            return

        self.set_file(file_path)

    def set_file(self, file_path: str):

        self.selected_file = file_path

        settings = QSettings(
            "MLFileExcel",
            "MlCertificateGenerator"
        )

        settings.setValue(
            "excel/last_file",
            file_path
        )

        self.file_label.setText(
            os.path.basename(file_path)
        )

        self.status_label.setText(
            "✓ Fichier chargé avec succès"
        )

        self.status_label.setObjectName(
            "successStatus"
        )

        self.status_label.style().unpolish(
            self.status_label
        )

        self.status_label.style().polish(
            self.status_label
        )

        self.file_selected.emit(
            file_path
        )

    def restore_last_file(self):

        settings = QSettings(
            "MLFileExcel",
            "MlCertificateGenerator"
        )

        last_file = settings.value(
            "excel/last_file",
            ""
        )

        if (
            last_file
            and os.path.exists(last_file)
        ):
            self.set_file(last_file)


def excel_file_drop_space(parent=None):

    return ExcelImportWidget(parent)


def import_file(parent=None):

    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Sélectionner un fichier Excel",
        "",
        "Fichiers Excel (*.xlsx *.xlsm *.xls);;"
        "Tous les fichiers (*)"
    )

    return file_path or None


def export_file_path():

    settings = QSettings(
        "MLFileExcel",
        "MlCertificateGenerator"
    )

    return settings.value(
        "excel/last_file",
        ""
    )