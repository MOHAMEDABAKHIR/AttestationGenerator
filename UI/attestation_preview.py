from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QWidget,
    QGridLayout
)

from PySide6.QtCore import Qt


class AttestationPreviewDialog(QDialog):

    def __init__(
        self,
        companies_data,
        parent=None
    ):
        super().__init__(parent)

        self.companies_data = companies_data

        self.setWindowTitle(
            "Préparation de l'attestation"
        )

        self.setMinimumSize(
            850,
            650
        )

        self.build_ui()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            30,
            28,
            30,
            25
        )

        root.setSpacing(18)

        title = QLabel(
            "Informations de l'attestation"
        )

        title.setObjectName(
            "dialogTitle"
        )

        subtitle = QLabel(
            "Vérifiez les informations avant de lancer "
            "la génération de l'attestation."
        )

        subtitle.setObjectName(
            "dialogDescription"
        )

        root.addWidget(title)
        root.addWidget(subtitle)

        # -----------------------------------------------------
        # SCROLL
        # -----------------------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            5,
            10,
            5
        )

        content_layout.setSpacing(18)

        for company in self.companies_data:

            card = self.create_company_card(
                company
            )

            content_layout.addWidget(
                card
            )

        content_layout.addStretch()

        scroll.setWidget(
            content
        )

        root.addWidget(
            scroll,
            1
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = QHBoxLayout()

        back_button = QPushButton(
            "← Retour"
        )

        back_button.setObjectName(
            "secondaryButton"
        )

        back_button.clicked.connect(
            self.reject
        )

        generate_button = QPushButton(
            "✨  Générer l'attestation"
        )

        generate_button.setObjectName(
            "generateButton"
        )

        generate_button.setMinimumWidth(
            230
        )

        generate_button.clicked.connect(
            self.generate
        )

        actions.addWidget(
            back_button
        )

        actions.addStretch()

        actions.addWidget(
            generate_button
        )

        root.addLayout(
            actions
        )

    # =========================================================
    # COMPANY CARD
    # =========================================================

    def create_company_card(
        self,
        company
    ):

        card = QFrame()

        card.setObjectName(
            "previewCard"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        layout.setSpacing(15)

        company_name = company.get(
            "company",
            ""
        )

        title = QLabel(
            company_name
        )

        title.setObjectName(
            "previewCompany"
        )

        layout.addWidget(title)

        # -----------------------------------------------------
        # INFORMATIONS
        # -----------------------------------------------------

        grid = QGridLayout()

        grid.setHorizontalSpacing(35)
        grid.setVerticalSpacing(14)

        row = 0

        # Toutes les informations Excel
        # sauf Colonne 6 et Type d'attestation.

        display_data = company.get(
            "display_data",
            {}
        )

        for label, value in display_data.items():

            self.add_field(
                grid,
                row,
                label,
                value
            )

            row += 1

        # -----------------------------------------------------
        # SEXE
        # -----------------------------------------------------

        self.add_field(
            grid,
            row,
            "Sexe du PDG",
            company.get(
                "gender",
                ""
            )
        )

        row += 1

        # -----------------------------------------------------
        # PERIODE
        # -----------------------------------------------------

        self.add_field(
            grid,
            row,
            "Période",
            company.get(
                "period",
                ""
            )
        )

        layout.addLayout(
            grid
        )

        return card

    # =========================================================
    # FIELD
    # =========================================================

    def add_field(
        self,
        grid,
        row,
        label,
        value
    ):

        label_widget = QLabel(
            label
        )

        label_widget.setObjectName(
            "previewLabel"
        )

        value_widget = QLabel(
            str(value)
            if value is not None
            else ""
        )

        value_widget.setObjectName(
            "previewValue"
        )

        value_widget.setWordWrap(
            True
        )

        grid.addWidget(
            label_widget,
            row,
            0
        )

        grid.addWidget(
            value_widget,
            row,
            1
        )

    # =========================================================
    # GENERATE
    # =========================================================

    def generate(self):

        # Pour le moment la génération réelle
        # n'est pas encore implémentée.

        self.accept()

    # =========================================================
    # DATA
    # =========================================================

    def get_data(self):

        return self.companies_data