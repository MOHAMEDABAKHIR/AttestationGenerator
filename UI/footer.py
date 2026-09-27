from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

from PySide6.QtCore import Qt


def create_footer():

    container = QWidget()

    layout = QHBoxLayout(container)

    layout.setContentsMargins(
        0,
        10,
        0,
        0
    )

    copyright_label = QLabel(
        "Génération des attestations"
    )

    copyright_label.setObjectName(
        "footerText"
    )

    version_label = QLabel(
        "v2.0"
    )

    version_label.setObjectName(
        "footerVersion"
    )

    layout.addWidget(
        copyright_label
    )

    layout.addStretch()

    layout.addWidget(
        version_label
    )

    return container