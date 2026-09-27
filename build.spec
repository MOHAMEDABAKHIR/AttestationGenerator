from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules("docxtpl")

a = Analysis(
    ["UI/main.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("templates", "templates"),
    ],
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