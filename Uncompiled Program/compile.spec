block_cipher = None


a = Analysis(['BloonsFarmUI.py'],
             pathex=['C:\\Users\\pdf52\\PycharmProjects\\pythonProject'], # just the directory not the file
             binaries=[],
             datas=[],
             hiddenimports=['keyboard', 'pyautogui', 'pyqt5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('LuckiestGuy-Regular.ttf','C:\\Users\\pdf52\\PycharmProjects\\pythonProject\\LuckiestGuy-Regular.ttf', "DATA"),('Null.ico', 'C:\\Users\\pdf52\\PycharmProjects\\pythonProject\\Null.ico', "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
         cipher=block_cipher)

exe = EXE(pyz,
      a.scripts,
      a.binaries,
      a.zipfiles,
      a.datas,
      name='BloonsFarmUI',
      debug=False,
      strip=False,
      upx=True,
      console=False # set True if command prompt window needed
)