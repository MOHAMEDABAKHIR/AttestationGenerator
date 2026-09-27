from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
    QMessageBox
)


class GenerationOptionsDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle(
            "Paramètres de génération"
        )

        self.setMinimumWidth(
            520
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
            28
        )

        root.setSpacing(18)

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = QLabel(
            "Paramètres de génération"
        )

        title.setObjectName(
            "dialogTitle"
        )

        subtitle = QLabel(
            "Sélectionnez la qualité du signataire "
            "avant de continuer."
        )

        subtitle.setObjectName(
            "dialogDescription"
        )

        root.addWidget(
            title
        )

        root.addWidget(
            subtitle
        )

        # -----------------------------------------------------
        # CARD
        # -----------------------------------------------------

        card = QFrame()

        card.setObjectName(
            "genderCard"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(10)

        # -----------------------------------------------------
        # QUALITY
        # -----------------------------------------------------

        quality_label = QLabel(
            "Qualité du signataire"
        )

        quality_label.setObjectName(
            "fieldLabel"
        )

        self.quality_combo = QComboBox()

        self.quality_combo.addItem(
            "Commissaire aux comptes",
            "commissaire_aux_comptes"
        )

        self.quality_combo.addItem(
            "Expert-comptable",
            "expert_comptable"
        )

        layout.addWidget(
            quality_label
        )

        layout.addWidget(
            self.quality_combo
        )

        root.addWidget(
            card
        )

        # -----------------------------------------------------
        # ACTIONS
        # -----------------------------------------------------

        actions = QHBoxLayout()

        cancel = QPushButton(
            "Annuler"
        )

        cancel.setObjectName(
            "secondaryButton"
        )

        cancel.clicked.connect(
            self.reject
        )

        next_button = QPushButton(
            "Suivant  →"
        )

        next_button.setObjectName(
            "primaryButton"
        )

        next_button.clicked.connect(
            self.validate
        )

        actions.addWidget(
            cancel
        )

        actions.addStretch()

        actions.addWidget(
            next_button
        )

        root.addLayout(
            actions
        )

    # =========================================================
    # VALIDATE
    # =========================================================

    def validate(self):

        if self.quality_combo.currentIndex() < 0:

            QMessageBox.warning(
                self,
                "Qualité manquante",
                "Veuillez sélectionner la qualité du signataire."
            )

            return

        self.accept()

    # =========================================================
    # DATA
    # =========================================================

    def get_quality(self):

        return self.quality_combo.currentData()