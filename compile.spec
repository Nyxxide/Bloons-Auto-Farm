import sys

a = Analysis(['src/BloonsFarmUI.py'],
             hiddenimports=['keyboard', 'pyautogui', 'pyqt5', 'pynput', 'cv2', 'pyscreeze'],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          # Static link the Visual C++ Redistributable DLLs if on Windows
          a.binaries + [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
                        ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
          if sys.platform == 'win32' else a.binaries,
          a.zipfiles,
          a.datas + [('Resources/UI/LuckiestGuy-Regular.ttf','src/Resources/UI/LuckiestGuy-Regular.ttf', "DATA"),('Resources/UI/btdfarmicon.ico', 'src/Resources/UI/btdfarmicon.ico', "DATA"),
                     ('Resources/MenuNav/homemenu.png', 'src/Resources/MenuNav/homemenu.png', "DATA"), ('Resources/MenuNav/ingame.png', 'src/Resources/MenuNav/ingame.png', "DATA"),
                     ('Resources/MenuNav/tooltipcheck.png', 'src/Resources/MenuNav/tooltipcheck.png', "DATA"),('Resources/MenuNav/endgame.png', 'src/Resources/MenuNav/endgame.png', "DATA"),
                     ('Resources/MenuNav/existinggame.png', 'src/Resources/MenuNav/existinggame.png', "DATA"), ('Resources/MenuNav/backhome.png', 'src/Resources/MenuNav/backhome.png', "DATA"),
                     ('Resources/MenuNav/collectionevent.png', 'src/Resources/MenuNav/collectionevent.png', "DATA"), ('Resources/MenuNav/endcollection.png', 'src/Resources/MenuNav/endcollection.png', "DATA"),
                     ('Resources/MenuNav/endgame2.png', 'src/Resources/MenuNav/endgame2.png', "DATA"), ('Resources/MenuNav/existingok.png', 'src/Resources/MenuNav/existingok.png', "DATA"),
                     ('Resources/MenuNav/instamonkey.png', 'src/Resources/MenuNav/instamonkey.png', "DATA"), ('Resources/Maps/infernal.png', 'src/Resources/Maps/infernal.png', "DATA"),
                     ('Resources/MapDifficulty/expert.png', 'src/Resources/MapDifficulty/expert.png', "DATA"), ('Resources/Difficulty/easy.png', 'src/Resources/Difficulty/easy.png', "DATA"),
                     ('Resources/Mode/deflation.png', 'src/Resources/Mode/deflation.png', "DATA"), ('Resources/MenuNav/levelup.png', 'src/Resources/MenuNav/levelup.png', "DATA")],
          name=os.path.join('dist', 'BloonsFarmUI' + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='src/Resources/UI/btdfarmicon.ico')

# Build a .app if on OS X
if sys.platform == 'darwin':
   app = BUNDLE(exe,
                name='BloonsFarmUI.app',
                icon='src/Resources/UI/btdfarmicon.ico')
