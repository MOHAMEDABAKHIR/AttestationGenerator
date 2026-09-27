from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QDialog,
    QInputDialog
)

from PySide6.QtCore import Qt
import os
import re
import sys
from excel.read_file_excel import ExcelReader

from utils.period import calculate_period

from .excel_file_space import ExcelImportWidget
from .excel_table import ExcelTableWidget
from .gender_dialog import GenderDialog
from .attestation_preview import AttestationPreviewDialog

from datetime import datetime

from generation.template_generator import (
    TemplateGenerator
)

from .generation_options_dialog import (
    GenerationOptionsDialog
)



class Workspace(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.reader = None

        self.build_ui()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root.setSpacing(22)

        # -----------------------------------------------------
        # STEP 1
        # -----------------------------------------------------

        step1 = QLabel(
            "1. Importer votre fichier"
        )

        step1.setObjectName(
            "sectionTitle"
        )

        root.addWidget(step1)

        self.import_widget = ExcelImportWidget()

        self.import_widget.file_selected.connect(
            self.on_file_selected
        )

        root.addWidget(
            self.import_widget
        )

        # -----------------------------------------------------
        # STEP 2
        # -----------------------------------------------------

        self.table_widget = ExcelTableWidget()

        self.table_widget.setVisible(
            False
        )

        self.table_widget.selection_changed.connect(
            self.update_generate_state
        )

        root.addWidget(
            self.table_widget
        )

        # -----------------------------------------------------
        # GENERATION AREA
        # -----------------------------------------------------

        self.action_card = QFrame()

        self.action_card.setObjectName(
            "actionCard"
        )

        action_layout = QHBoxLayout(
            self.action_card
        )

        action_layout.setContentsMargins(
            24,
            20,
            24,
            20
        )

        info = QVBoxLayout()

        self.ready_title = QLabel(
            "Prêt à générer"
        )

        self.ready_title.setObjectName(
            "cardTitle"
        )

        self.ready_description = QLabel(
            "Sélectionnez au moins une entreprise "
            "pour continuer."
        )

        self.ready_description.setObjectName(
            "cardDescription"
        )

        info.addWidget(
            self.ready_title
        )

        info.addWidget(
            self.ready_description
        )

        action_layout.addLayout(
            info
        )

        action_layout.addStretch()

        self.generate_button = QPushButton(
            "✨  Générer l'attestation"
        )

        self.generate_button.setObjectName(
            "generateButton"
        )

        self.generate_button.setMinimumHeight(
            48
        )

        self.generate_button.setMinimumWidth(
            240
        )

        self.generate_button.setCursor(
            Qt.PointingHandCursor
        )

        self.generate_button.setEnabled(
            False
        )

        self.generate_button.clicked.connect(
            self.start_generation
        )

        action_layout.addWidget(
            self.generate_button
        )

        self.action_card.setVisible(
            False
        )

        root.addWidget(
            self.action_card
        )

        root.addStretch()

    # =========================================================
    # FILE
    # =========================================================

    def on_file_selected(
        self,
        file_path
    ):

        try:

            self.reader = ExcelReader(
                file_path
            )

            self.table_widget.set_reader(
                self.reader
            )

            self.table_widget.setVisible(
                True
            )

            self.action_card.setVisible(
                True
            )

            self.update_generate_state()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Erreur lors de l'import",
                (
                    "Impossible de lire le fichier Excel.\n\n"
                    f"{error}"
                )
            )

    # =========================================================
    # GENERATION STATE
    # =========================================================

    def update_generate_state(self):

        ready = (
            self.table_widget.is_ready()
        )

        self.generate_button.setEnabled(
            ready
        )

        if ready:

            selected = (
                self.table_widget
                .get_selected_companies()
            )

            self.ready_title.setText(
                "✓ Données prêtes"
            )

            self.ready_description.setText(
                f"{len(selected)} entreprise(s) "
                "sélectionnée(s)."
            )

        else:

            self.ready_title.setText(
                "Prêt à générer"
            )

            self.ready_description.setText(
                "Sélectionnez au moins une entreprise "
                "pour continuer."
            )

    # =========================================================
    # START GENERATION
    # =========================================================

    def start_generation(self):
        """
        Lance le processus complet de génération des attestations.

        Workflow :
        1. Récupérer les entreprises sélectionnées
        2. Demander le sexe du PDG pour chaque entreprise
        3. Choisir la qualité du signataire
        4. Demander le montant uniquement pour les attestations avec retard
        5. Calculer la période
        6. Afficher l'aperçu
        7. Choisir le dossier de sortie
        8. Générer chaque document avec son propre type d'attestation
        """

        # ============================================================
        # 1. RÉCUPÉRER LES ENTREPRISES SÉLECTIONNÉES
        # ============================================================

        selected_companies = self.table_widget.get_selected_companies()

        if not selected_companies:
            QMessageBox.warning(
                self,
                "Aucune entreprise",
                "Veuillez sélectionner au moins une entreprise."
            )
            return

        # ============================================================
        # 2. CONSTRUIRE LES DONNÉES DES ENTREPRISES
        # ============================================================

        companies_data = self.build_selected_companies_data(
            selected_companies
        )

        if not companies_data:
            QMessageBox.warning(
                self,
                "Erreur",
                "Impossible de récupérer les données des entreprises."
            )
            return

        # ============================================================
        # 3. SEXE DU PDG
        # ============================================================

        gender_dialog = GenderDialog(
            companies_data,
            self
        )

        if gender_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        gender_data = gender_dialog.get_gender_data()

        # Exemple :
        #
        # {
        #     "Entreprise A": "Monsieur",
        #     "Entreprise B": "Madame"
        # }

        # ============================================================
        # 4. CHOIX DE LA QUALITÉ DU SIGNATAIRE
        # ============================================================

        # Le signataire est commun à toute la génération.
        #
        # Exemple :
        # - Commissaire aux comptes
        # OU
        # - Expert-comptable

        options_dialog = GenerationOptionsDialog(
            self
        )

        if options_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        signer_quality = options_dialog.get_quality()

        # ============================================================
        # 5. PRÉPARER LES DONNÉES FINALES
        # ============================================================

        final_companies_data = []

        for company_data in companies_data:

            company_name = company_data.get(
                "company",
                ""
            )

            certificate_type = company_data.get(
                "certificate_type",
                ""
            )

            # --------------------------------------------------------
            # Vérification du type d'attestation
            # --------------------------------------------------------

            certificate_type_normalized = (
                str(certificate_type)
                .strip()
                .lower()
            )

            if not certificate_type_normalized:
                QMessageBox.warning(
                    self,
                    "Type d'attestation manquant",
                    (
                        f"Le type d'attestation est manquant "
                        f"pour l'entreprise :\n\n"
                        f"{company_name}"
                    )
                )
                return

            # --------------------------------------------------------
            # Vérifier que le type est bien reconnu
            # --------------------------------------------------------

            if (
                "avec retard" not in certificate_type_normalized
                and
                "sans retard" not in certificate_type_normalized
            ):
                QMessageBox.warning(
                    self,
                    "Type d'attestation invalide",
                    (
                        f"Le type d'attestation de :\n\n"
                        f"{company_name}\n\n"
                        f"n'est pas reconnu.\n\n"
                        f"Valeur trouvée : "
                        f"{certificate_type}"
                    )
                )
                return

            # --------------------------------------------------------
            # Calcul de la période
            # --------------------------------------------------------

            exercice = company_data.get(
                "exercice"
            )

            trimestre = company_data.get(
                "trimestre"
            )

            period = calculate_period(
                exercice,
                trimestre
            )

            if not period:
                QMessageBox.warning(
                    self,
                    "Période invalide",
                    (
                        f"Impossible de calculer la période "
                        f"pour :\n\n"
                        f"{company_name}\n\n"
                        f"Exercice : {exercice}\n"
                        f"Trimestre : {trimestre}"
                    )
                )
                return

            # --------------------------------------------------------
            # Sexe du PDG
            # --------------------------------------------------------

            gender = gender_data.get(
                company_name
            )

            if not gender:
                QMessageBox.warning(
                    self,
                    "Sexe du PDG manquant",
                    (
                        f"Le sexe du PDG n'a pas été défini "
                        f"pour :\n\n"
                        f"{company_name}"
                    )
                )
                return

            # --------------------------------------------------------
            # Montant
            # --------------------------------------------------------

            amount = ""

            # IMPORTANT :
            # "Sans retard" ne doit PAS déclencher la demande
            # de montant.
            #
            # On vérifie donc explicitement "Avec retard".

            is_with_delay = (
                "avec retard" in certificate_type_normalized
                and
                "sans retard" not in certificate_type_normalized
            )

            if is_with_delay:

                while True:

                    amount, ok = QInputDialog.getText(
                        self,
                        "Montant des factures en retard",
                        (
                            f"Entreprise : {company_name}\n\n"
                            f"Cette attestation est de type "
                            f"« Avec retard ».\n\n"
                            f"Veuillez saisir le montant "
                            f"des factures en retard :"
                        )
                    )

                    if not ok:
                        return

                    amount = amount.strip()

                    if amount:
                        break

                    QMessageBox.warning(
                        self,
                        "Montant obligatoire",
                        (
                            "Veuillez saisir un montant "
                            "pour une attestation avec retard."
                        )
                    )

            # --------------------------------------------------------
            # Date de signature
            # --------------------------------------------------------

            signature_date = datetime.now().strftime(
                "%d/%m/%Y"
            )

            # --------------------------------------------------------
            # Ajouter toutes les informations
            # --------------------------------------------------------

            company_data["gender"] = gender

            company_data["period"] = period

            company_data["signer_quality"] = signer_quality

            company_data["certificate_type"] = certificate_type

            company_data["amount"] = amount

            company_data["signature_date"] = signature_date

            final_companies_data.append(
                company_data
            )

        # ============================================================
        # 6. APERÇU
        # ============================================================

        preview_dialog = AttestationPreviewDialog(
            final_companies_data,
            self
        )

        if preview_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        # ============================================================
        # 7. CHOISIR LE DOSSIER DE SORTIE
        # ============================================================

        output_directory = QFileDialog.getExistingDirectory(
            self,
            "Choisir le dossier où enregistrer les attestations"
        )

        if not output_directory:
            return

        # ============================================================
        # 8. GÉNÉRATION DES DOCUMENTS
        # ============================================================

        try:

            # Le dossier templates doit être situé à la racine
            # du projet :
            #
            # templates/
            #     CAC_avec_retard.docx
            #     CAC_sans_retard.docx
            #     EC_avec_retard.docx
            #     EC_sans_retard.docx

            templates_dir = self.get_templates_directory()

            generator = TemplateGenerator(
                templates_dir
            )

            generated_files = []

            for company_data in final_companies_data:

                output_path = generator.generate(
                    company_data,
                    output_directory
                )

                generated_files.append(
                    output_path
                )

            # ========================================================
            # 9. MESSAGE DE SUCCÈS
            # ========================================================

            files_text = "\n".join(
                f"• {os.path.basename(path)}"
                for path in generated_files
            )

            QMessageBox.information(
                self,
                "Génération terminée",
                (
                    f"{len(generated_files)} "
                    f"attestation(s) générée(s) avec succès.\n\n"
                    f"{files_text}"
                )
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur de génération",
                (
                    "Une erreur est survenue pendant "
                    "la génération des attestations.\n\n"
                    f"Détail :\n{str(e)}"
                )
            )
    # =========================================================
    # BUILD DATA
    # =========================================================

    def build_selected_companies_data(
        self,
        selected_companies
    ):

        sheet = self.reader.get_sheet(
            self.table_widget.current_sheet
        )

        header_row = self.table_widget.current_header_row

        headers = self.reader.get_headers(
            self.table_widget.current_sheet,
            header_row
        )

        company_column = self.table_widget.company_column

        results = []

        # =====================================================
        # COLONNES À EXCLURE
        # =====================================================

        excluded_headers = {
            "colonne 6",
            "type d'attestation"
        }

        # =====================================================
        # PARCOURIR LES LIGNES EXCEL
        # =====================================================

        for row_number in range(
            header_row + 1,
            sheet.max_row + 1
        ):

            row_values = []

            for column_number in range(
                1,
                sheet.max_column + 1
            ):
                row_values.append(
                    sheet.cell(
                        row=row_number,
                        column=column_number
                    ).value
                )

            # =================================================
            # ENTREPRISE
            # =================================================

            company_index = company_column - 1

            if company_index >= len(row_values):
                continue

            company_value = row_values[company_index]

            if company_value is None:
                continue

            company_name = str(
                company_value
            ).strip()

            if company_name not in selected_companies:
                continue

            # =================================================
            # DONNÉES AFFICHÉES
            # =================================================

            display_data = {}

            for index, header in enumerate(headers):

                if index >= len(row_values):
                    continue

                if header is None:
                    continue

                normalized_header = str(
                    header
                ).strip().lower()

                if normalized_header in excluded_headers:
                    continue

                value = row_values[index]

                if value is None:
                    value = ""

                display_data[
                    str(header).strip()
                ] = value

            # =================================================
            # EXERCICE / TRIMESTRE
            # =================================================

            exercice = ""
            trimestre = ""

            for index, header in enumerate(headers):

                if index >= len(row_values):
                    continue

                normalized_header = str(
                    header
                ).strip().lower()

                value = row_values[index]

                if normalized_header == "exercice":
                    exercice = value

                elif normalized_header == "trimestre":
                    trimestre = value

            # =================================================
            # PDG
            # =================================================

            ceo = ""

            for index, header in enumerate(headers):

                if index >= len(row_values):
                    continue

                normalized_header = str(
                    header
                ).strip().lower()

                if normalized_header in {
                    "nom du pdg",
                    "pdg",
                    "nom pdg"
                }:

                    value = row_values[index]

                    if value is not None:
                        ceo = str(value).strip()

                    break

            # =================================================
            # ADRESSE
            # =================================================

            address = ""

            for index, header in enumerate(headers):

                if index >= len(row_values):
                    continue

                normalized_header = str(
                    header
                ).strip().lower()

                if (
                    "adresse" in normalized_header
                    or "address" in normalized_header
                ):

                    value = row_values[index]

                    if value is not None:
                        address = str(value).strip()

                    break

            # =================================================
            # TYPE D'ATTESTATION
            # =================================================

            certificate_type = ""

            for index, header in enumerate(headers):

                if index >= len(row_values):
                    continue

                normalized_header = str(
                    header
                ).strip().lower()

                if (
                    "type d'attestation" in normalized_header
                    or "type attestation" in normalized_header
                ):

                    value = row_values[index]

                    if value is not None:
                        certificate_type = str(
                            value
                        ).strip()

                    break

            # =================================================
            # AJOUTER L'ENTREPRISE
            # =================================================

            results.append({

                "company": company_name,

                "ceo": ceo,

                "address": address,

                "exercice": exercice,

                "trimestre": trimestre,

                "certificate_type": certificate_type,

                "display_data": display_data,

                "gender": "",

                "period": "",

                "amount": "",

                "signer_quality": "",

                "signature_date": ""
            })

        # =====================================================
        # RETOURNER LES RÉSULTATS
        # =====================================================

        return results
    def ask_amount(
        self,
        company_name
    ):

        amount, ok = QInputDialog.getText(
            self,
            "Montant des factures en retard",
            (
                f"Entreprise : {company_name}\n\n"
                "Veuillez saisir le montant total "
                "des factures non payées dans les délais :"
            )
        )

        if not ok:
            return None

        amount = amount.strip()

        if not amount:

            QMessageBox.warning(
                self,
                "Montant obligatoire",
                "Le montant est obligatoire pour une attestation avec retard."
            )

            return self.ask_amount(
                company_name
            )

        return amount
    def generate_documents(
        self,
        companies_data,
        output_directory
    ):

        try:

            templates_directory = self.get_templates_directory()

            generator = TemplateGenerator(
                templates_directory
            )

            generated_files = []

            for company in companies_data:

                company_directory = (
                    self.get_company_output_directory(
                        output_directory,
                        company["company"]
                    )
                )

                output_path = generator.generate(
                    company,
                    company_directory
                )

                generated_files.append(
                    output_path
                )

            QMessageBox.information(
                self,
                "Génération terminée",
                (
                    f"{len(generated_files)} attestation(s) "
                    "ont été générées avec succès."
                )
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Erreur de génération",
                (
                    "Une erreur est survenue pendant "
                    "la génération de l'attestation.\n\n"
                    f"{error}"
                )
            )
    def get_templates_directory(self):

        if getattr(sys, "frozen", False):
            # Application construite avec PyInstaller
            base_directory = os.path.dirname(
                sys.executable
            )
        else:
            # Application lancée depuis le projet
            base_directory = os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )

        return os.path.join(
            base_directory,
            "templates"
        )


    def get_company_output_directory(
        self,
        output_directory,
        company_name
    ):

        import os
        import re

        safe_name = re.sub(
    r'[<>:"/\\|?*]',
    "_",
    str(company_name)
)
        safe_name = safe_name.strip()

        company_directory = os.path.join(
            output_directory,
            safe_name
        )

        os.makedirs(
            company_directory,
            exist_ok=True
        )

        return company_directory


def create_workspace():

    return Workspace()