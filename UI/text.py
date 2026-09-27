import sys
import os
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QPushButton, QVBoxLayout,QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from excel.read_file_excel import findTableHeader

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logoML_path = os.path.join(base_path, "assets", "image.png")

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Génération des attestations")
window.resize(800, 600)

# --- Layout racine ---
root = QVBoxLayout(window)
# root.setContentsMargins(20, 20, 20, 20)
root.setSpacing(20)

# --- Header ---
header = QHBoxLayout() 
header.setAlignment(Qt.AlignTop)

logoMlLabel=QLabel()
pixmap = QPixmap(logoML_path)
if pixmap.isNull():
    print("Erreur : L'image n'a pas été trouvée au chemin :", logoML_path)
else:
    print("Image chargée avec succès !")
    pixmap = pixmap.scaled(170, 170, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    logoMlLabel.setPixmap(pixmap)
    logoMlLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    header.addWidget(logoMlLabel)
    

title = QLabel("Logiciel de génération des Attestations")
title.setStyleSheet("font-size: 30px;")
title.setAlignment(Qt.AlignCenter)
title.setContentsMargins(0, 20, 0, 0)
header.addWidget(title)
root.addLayout(header)         

# --- Workspace ---
workspace = QVBoxLayout()
workspace.setAlignment(Qt.AlignCenter)

button = QPushButton("Cliquer")
button.clicked.connect(findTableHeader)
workspace.addWidget(button)
root.addLayout(workspace)


root.addStretch()   

# --- Footer ---
footer=QVBoxLayout()
footer.setAlignment(Qt.AlignBottom) 
footer_text=QLabel("Tous les droits sont reservés")
footer.addWidget(footer_text)
root.addLayout(footer)

            

window.show()
sys.exit(app.exec())