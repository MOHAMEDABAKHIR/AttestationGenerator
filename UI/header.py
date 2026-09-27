import os

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


def create_header():

    container = QWidget()

    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(18)

    # ---------------------------------------------------------
    # LOGO
    # ---------------------------------------------------------

    base_path = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    logo_path = os.path.join(
        base_path,
        "assets",
        "image.png"
    )

    logo = QLabel()

    pixmap = QPixmap(logo_path)

    if not pixmap.isNull():

        pixmap = pixmap.scaled(
            72,
            72,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        logo.setPixmap(pixmap)

    logo.setFixedSize(76, 76)

    # ---------------------------------------------------------
    # TITRE
    # ---------------------------------------------------------

    text_container = QVBoxLayout()
    text_container.setSpacing(3)

    title = QLabel(
        "Génération des attestations"
    )

    title.setObjectName("appTitle")

    subtitle = QLabel(
        "Importez vos données Excel et préparez "
        "vos attestations en quelques étapes."
    )

    subtitle.setObjectName("appSubtitle")

    text_container.addWidget(title)
    text_container.addWidget(subtitle)

    layout.addWidget(logo)
    layout.addLayout(text_container)
    layout.addStretch()

    return container