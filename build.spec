import glob
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("docxtpl")

# ==========================================
# Debug + collecte explicite des templates
# (au lieu de compter sur le wildcard implicite
# de PyInstaller, qui échoue silencieusement)
# ==========================================

print("[DEBUG] CWD au moment du build:", __import__("os").getcwd())

template_files = sorted(
    glob.glob("templates/*.docx") + glob.glob("templates/*.doc")
)

print(f"[DEBUG] Fichiers templates trouvés ({len(template_files)}):")
for f in template_files:
    print(f"[DEBUG]   - {f}")

if not template_files:
    raise FileNotFoundError(
        "Aucun fichier .docx/.doc trouvé dans templates/ au moment du build. "
        "Verifie que build.spec est bien lance depuis la racine du repo, "
        "et que les fichiers sont bien presents a cet endroit."
    )

datas = [(f, "templates") for f in template_files]

a = Analysis(
    ["UI/main.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="AttestationGenerator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name="AttestationGenerator",
)
