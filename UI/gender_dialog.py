from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QFrame,
    QMessageBox,
    QScrollArea,
    QWidget
)

from PySide6.QtCore import Qt


class GenderDialog(QDialog):

    def __init__(
        self,
        companies_data,
        parent=None
    ):
        super().__init__(parent)

        self.companies_data = companies_data
        self.gender_groups = {}

        self.setWindowTitle(
            "Informations du dirigeant"
        )

        self.setMinimumSize(
            650,
            500
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

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        hello = QLabel(
            "Bonjour 👋"
        )

        hello.setObjectName(
            "dialogTitle"
        )

        description = QLabel(
            "Avant de continuer, veuillez préciser "
            "le sexe du PDG pour chaque entreprise sélectionnée."
        )

        description.setObjectName(
            "dialogDescription"
        )

        description.setWordWrap(True)

        root.addWidget(hello)
        root.addWidget(description)

        # -----------------------------------------------------
        # SCROLL AREA
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

        content_layout.setSpacing(12)

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

        cancel_button = QPushButton(
            "Annuler"
        )

        cancel_button.setObjectName(
            "secondaryButton"
        )

        cancel_button.clicked.connect(
            self.reject
        )

        next_button = QPushButton(
            "Suivant  →"
        )

        next_button.setObjectName(
            "primaryButton"
        )

        next_button.setMinimumWidth(
            150
        )

        next_button.clicked.connect(
            self.validate_and_continue
        )

        actions.addWidget(
            cancel_button
        )

        actions.addStretch()

        actions.addWidget(
            next_button
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
            "genderCard"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            18,
            16,
            18,
            16
        )

        layout.setSpacing(10)

        company_name = company.get(
            "company",
            "Entreprise"
        )

        ceo_name = company.get(
            "ceo",
            ""
        )

        company_label = QLabel(
            company_name
        )

        company_label.setObjectName(
            "genderCompany"
        )

        ceo_label = QLabel(
            f"PDG : {ceo_name}"
        )

        ceo_label.setObjectName(
            "genderCeo"
        )

        layout.addWidget(
            company_label
        )

        layout.addWidget(
            ceo_label
        )

        gender_layout = QHBoxLayout()

        monsieur = QRadioButton(
            "Monsieur"
        )

        madame = QRadioButton(
            "Madame"
        )

        monsieur.setObjectName(
            "genderRadio"
        )

        madame.setObjectName(
            "genderRadio"
        )

        group = QButtonGroup(
            self
        )

        group.addButton(
            monsieur
        )

        group.addButton(
            madame
        )

        gender_layout.addWidget(
            monsieur
        )

        gender_layout.addWidget(
            madame
        )

        gender_layout.addStretch()

        layout.addLayout(
            gender_layout
        )

        self.gender_groups[
            company_name
        ] = {
            "group": group,
            "monsieur": monsieur,
            "madame": madame,
        }

        return card

    # =========================================================
    # VALIDATION
    # =========================================================

    def validate_and_continue(self):

        missing = []

        for company_name, controls in self.gender_groups.items():

            if not (
                controls["monsieur"].isChecked()
                or controls["madame"].isChecked()
            ):

                missing.append(
                    company_name
                )

        if missing:

            QMessageBox.warning(
                self,
                "Information manquante",
                (
                    "Veuillez choisir le sexe du PDG "
                    "pour chaque entreprise avant de continuer."
                )
            )

            return

        self.accept()

    # =========================================================
    # RESULT
    # =========================================================

    def get_gender_data(self):

        result = {}

        for company_name, controls in self.gender_groups.items():

            if controls["monsieur"].isChecked():
                result[company_name] = "Monsieur"

            elif controls["madame"].isChecked():
                result[company_name] = "Madame"

        return result