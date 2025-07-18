# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.scrolledtext', 'os', 'requests', 'encryptor', 'gui_warning', 'keygen', 'target_finder', 'utils', 'decryptor', 'decrypt_runner', 'sys', 'json', 'uuid', 'hashlib', 'cryptography', 'cryptography.hazmat', 'cryptography.hazmat.primitives', 'cryptography.hazmat.primitives.ciphers', 'cryptography.hazmat.primitives.ciphers.modes', 'cryptography.hazmat.primitives.ciphers.algorithms', 'cryptography.hazmat.primitives.padding'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
