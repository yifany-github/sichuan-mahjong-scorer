# -*- mode: python ; coding: utf-8 -*-
# macOS打包配置文件

block_cipher = None

a = Analysis(
    ['majiang_macos_compatible.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='四川麻将积分系统',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='四川麻将积分系统',
)

app = BUNDLE(
    coll,
    name='四川麻将积分系统.app',
    icon=None,  # 可以添加.icns图标文件路径
    bundle_identifier='com.majiang.scorekeeper',
    info_plist={
        'CFBundleName': '四川麻将积分系统',
        'CFBundleDisplayName': '四川麻将积分系统',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.14.0',
    },
) 