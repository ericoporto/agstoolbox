# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [
         ('src/agstoolbox/data/*.png', 'data'),
         ]

a = Analysis(['agstoolbox'],
             pathex=['src'],
             binaries=[],
             datas=added_files,
             hiddenimports=['agstoolbox'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='agstoolbox',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, 
		  icon='at_icon_pi.ico' )
