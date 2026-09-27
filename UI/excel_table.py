from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QFrame,
    QPushButton
)

from PySide6.QtCore import Qt, Signal


class ExcelTableWidget(QWidget):

    selection_changed = Signal()

    def __init__(self, reader=None, parent=None):

        super().__init__(parent)

        self.reader = reader
        self.current_sheet = ""
        self.current_header_row = None
        self.company_column = None

        self.build_ui()

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        title = QLabel(
            "2. Préparer les données"
        )

        title.setObjectName("sectionTitle")

        subtitle = QLabel(
            "Choisissez la feuille, la ligne d’en-tête "
            "et la colonne contenant les entreprises."
        )

        subtitle.setObjectName("sectionSubtitle")

        root.addWidget(title)
        root.addWidget(subtitle)

        # -----------------------------------------------------
        # CONFIGURATION
        # -----------------------------------------------------

        config_card = QFrame()
        config_card.setObjectName("configCard")

        config_layout = QVBoxLayout(config_card)

        config_layout.setContentsMargins(
            20, 20, 20, 20
        )

        config_layout.setSpacing(15)

        # Feuille

        sheet_label = QLabel("Feuille Excel")
        sheet_label.setObjectName("fieldLabel")

        self.sheet_combo = QComboBox()

        self.sheet_combo.currentIndexChanged.connect(
            self.on_sheet_changed
        )

        config_layout.addWidget(sheet_label)
        config_layout.addWidget(self.sheet_combo)

        # Header

        header_label = QLabel(
            "Ligne contenant les en-têtes"
        )

        header_label.setObjectName("fieldLabel")

        self.header_combo = QComboBox()

        self.header_combo.currentIndexChanged.connect(
            self.on_header_changed
        )

        config_layout.addWidget(header_label)
        config_layout.addWidget(self.header_combo)

        # Entreprise

        company_label = QLabel(
            "Colonne des entreprises"
        )

        company_label.setObjectName("fieldLabel")

        self.company_combo = QComboBox()

        self.company_combo.currentIndexChanged.connect(
            self.on_company_column_changed
        )

        config_layout.addWidget(company_label)
        config_layout.addWidget(self.company_combo)

        root.addWidget(config_card)

        # -----------------------------------------------------
        # ENTREPRISES
        # -----------------------------------------------------

        selection_card = QFrame()
        selection_card.setObjectName("selectionCard")

        selection_layout = QVBoxLayout(
            selection_card
        )

        selection_layout.setContentsMargins(
            20, 20, 20, 20
        )

        selection_layout.setSpacing(12)

        selection_header = QHBoxLayout()

        company_title = QLabel(
            "Entreprises"
        )

        company_title.setObjectName(
            "cardTitle"
        )

        self.selection_count = QLabel(
            "0 sélectionnée"
        )

        self.selection_count.setObjectName(
            "counterBadge"
        )

        selection_header.addWidget(
            company_title
        )

        selection_header.addStretch()

        selection_header.addWidget(
            self.selection_count
        )

        selection_layout.addLayout(
            selection_header
        )

        self.company_list = QListWidget()

        self.company_list.setSelectionMode(
            QAbstractItemView.NoSelection
        )

        self.company_list.itemChanged.connect(
            self.on_company_selection_changed
        )

        selection_layout.addWidget(
            self.company_list
        )

        actions = QHBoxLayout()

        select_all = QPushButton(
            "Tout sélectionner"
        )

        clear_all = QPushButton(
            "Tout désélectionner"
        )

        select_all.setObjectName(
            "secondaryButton"
        )

        clear_all.setObjectName(
            "secondaryButton"
        )

        select_all.clicked.connect(
            lambda: self.set_all_companies(True)
        )

        clear_all.clicked.connect(
            lambda: self.set_all_companies(False)
        )

        actions.addWidget(select_all)
        actions.addWidget(clear_all)
        actions.addStretch()

        selection_layout.addLayout(actions)

        root.addWidget(selection_card)

        # -----------------------------------------------------
        # PREVIEW
        # -----------------------------------------------------

        preview_title = QLabel(
            "Aperçu des données"
        )

        preview_title.setObjectName(
            "cardTitle"
        )

        root.addWidget(preview_title)

        self.table = QTableWidget()

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        root.addWidget(self.table)

    # =========================================================
    # READER
    # =========================================================

    def set_reader(self, reader):

        self.reader = reader

        self.sheet_combo.blockSignals(True)

        self.sheet_combo.clear()

        self.sheet_combo.addItems(
            reader.get_sheet_names()
        )

        self.sheet_combo.blockSignals(False)

        if self.sheet_combo.count():
            self.on_sheet_changed(0)

    # =========================================================
    # SHEET
    # =========================================================

    def on_sheet_changed(self, index):

        if not self.reader or index < 0:
            return

        self.current_sheet = (
            self.sheet_combo.currentText()
        )

        self.header_combo.blockSignals(True)
        self.header_combo.clear()

        candidates = (
            self.reader.get_header_candidates(
                self.current_sheet
            )
        )

        for row_number, values in candidates:

            preview = " | ".join(
                str(value)
                for value in values[:8]
                if value is not None
            )

            if not preview:
                preview = "Ligne vide"

            self.header_combo.addItem(
                f"Ligne {row_number} — {preview}",
                row_number
            )

        self.header_combo.blockSignals(False)

        if self.header_combo.count():

            self.header_combo.setCurrentIndex(0)

            self.on_header_changed(0)

    # =========================================================
    # HEADER
    # =========================================================

    def on_header_changed(self, index):

        if not self.reader or index < 0:
            return

        row_number = self.header_combo.itemData(index)

        if row_number is None:
            return

        self.current_header_row = int(row_number)

        headers = self.reader.get_headers(
            self.current_sheet,
            self.current_header_row
        )

        self.company_combo.blockSignals(True)
        self.company_combo.clear()

        for column_index, header in enumerate(
            headers,
            start=1
        ):

            self.company_combo.addItem(
                f"{header} · Colonne {column_index}",
                column_index
            )

        self.company_combo.blockSignals(False)

        # Proposition automatique uniquement :
        # l'utilisateur garde la possibilité de changer.

        preferred_index = 0

        for index, header in enumerate(headers):

            normalized = header.lower()

            if (
                "raison sociale" in normalized
                or "entreprise" in normalized
                or "société" in normalized
                or "societe" in normalized
                or "company" in normalized
            ):
                preferred_index = index
                break

        self.company_combo.setCurrentIndex(
            preferred_index
        )

        self.on_company_column_changed(
            preferred_index
        )

        self.refresh_preview()

    # =========================================================
    # COMPANY COLUMN
    # =========================================================

    def on_company_column_changed(self, index):

        if not self.reader or index < 0:
            return

        self.company_column = (
            self.company_combo.itemData(index)
        )

        if self.company_column is None:
            return

        self.load_companies()

    # =========================================================
    # COMPANIES
    # =========================================================

    def load_companies(self):

        self.company_list.blockSignals(True)
        self.company_list.clear()

        companies = (
            self.reader.get_unique_company_names(
                self.current_sheet,
                self.current_header_row,
                self.company_column
            )
        )

        for company in companies:

            item = QListWidgetItem(company)

            item.setFlags(
                item.flags()
                | Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.Unchecked
            )

            self.company_list.addItem(item)

        self.company_list.blockSignals(False)

        self.update_counter()
        self.selection_changed.emit()

    # =========================================================
    # SELECT ALL
    # =========================================================

    def set_all_companies(self, checked):

        state = (
            Qt.Checked
            if checked
            else Qt.Unchecked
        )

        self.company_list.blockSignals(True)

        for index in range(
            self.company_list.count()
        ):

            self.company_list.item(index).setCheckState(
                state
            )

        self.company_list.blockSignals(False)

        self.update_counter()
        self.selection_changed.emit()

    # =========================================================
    # SELECTION
    # =========================================================

    def on_company_selection_changed(self, item):

        self.update_counter()
        self.selection_changed.emit()

    def get_selected_companies(self):

        companies = []

        for index in range(
            self.company_list.count()
        ):

            item = self.company_list.item(index)

            if item.checkState() == Qt.Checked:
                companies.append(item.text())

        return companies

    def update_counter(self):

        count = len(
            self.get_selected_companies()
        )

        if count <= 1:
            text = f"{count} sélectionnée"
        else:
            text = f"{count} sélectionnées"

        self.selection_count.setText(text)

    # =========================================================
    # PREVIEW
    # =========================================================

    def refresh_preview(self):

        if not self.reader:
            return

        preview = self.reader.get_preview(
            self.current_sheet,
            self.current_header_row,
            max_rows=12
        )

        headers = preview.headers
        rows = preview.rows

        self.table.clear()

        self.table.setColumnCount(
            len(headers)
        )

        self.table.setHorizontalHeaderLabels(
            headers
        )

        self.table.setRowCount(
            len(rows)
        )

        for row_index, row in enumerate(rows):

            for column_index in range(
                len(headers)
            ):

                value = ""

                if column_index < len(row):
                    raw = row[column_index]

                    if raw is not None:
                        value = str(raw)

                self.table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(value)
                )

        self.table.resizeColumnsToContents()

    # =========================================================
    # RESET
    # =========================================================

    def clear(self):

        self.sheet_combo.clear()
        self.header_combo.clear()
        self.company_combo.clear()
        self.company_list.clear()
        self.table.clear()

        self.selection_count.setText(
            "0 sélectionnée"
        )

    # =========================================================
    # READY
    # =========================================================

    def is_ready(self):

        return bool(
            self.reader
            and self.current_sheet
            and self.current_header_row
            and self.company_column
            and self.get_selected_companies()
        )