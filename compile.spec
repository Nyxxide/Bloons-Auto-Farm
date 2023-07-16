import sys

block_cipher=None

a = Analysis(['src/BloonsFarmUI.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['keyboard', 'pyautogui', 'pyqt5', 'pynput', 'cv2', 'pyscreeze'],
             hookspath=None,
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
          a.binaries + [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
                        ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]
          if sys.platform == 'win32' else a.binaries,
          a.datas + [
             
                     ('Resources/UI/LuckiestGuy-Regular.ttf','src/Resources/UI/LuckiestGuy-Regular.ttf', "DATA"),('Resources/UI/btdfarmicon.ico', 'src/Resources/UI/btdfarmicon.ico', "DATA"),
                     ('Resources/UI/btdfarmicon.icns', 'src/Resources/UI/btdfarmicon.icns', "DATA"),

                     ('Resources/MenuNav/homemenu.png', 'src/Resources/MenuNav/homemenu.png', "DATA"), ('Resources/MenuNav/ingame.png', 'src/Resources/MenuNav/ingame.png', "DATA"),
                     ('Resources/MenuNav/tooltipcheck.png', 'src/Resources/MenuNav/tooltipcheck.png', "DATA"),('Resources/MenuNav/endgame.png', 'src/Resources/MenuNav/endgame.png', "DATA"),
                     ('Resources/MenuNav/existinggame.png', 'src/Resources/MenuNav/existinggame.png', "DATA"), ('Resources/MenuNav/backhome.png', 'src/Resources/MenuNav/backhome.png', "DATA"),
                     ('Resources/MenuNav/collectionevent.png', 'src/Resources/MenuNav/collectionevent.png', "DATA"), ('Resources/MenuNav/endcollection.png', 'src/Resources/MenuNav/endcollection.png', "DATA"),
                     ('Resources/MenuNav/endgame2.png', 'src/Resources/MenuNav/endgame2.png', "DATA"), ('Resources/MenuNav/existingok.png', 'src/Resources/MenuNav/existingok.png', "DATA"),
                     ('Resources/MenuNav/instamonkey.png', 'src/Resources/MenuNav/instamonkey.png', "DATA"), ('Resources/MenuNav/levelup.png', 'src/Resources/MenuNav/levelup.png', "DATA"),

                     ('Resources/MapDifficulty/beginner.png', 'src/Resources/MapDifficulty/beginner.png', "DATA"), ('Resources/MapDifficulty/intermediate.png', 'src/Resources/MapDifficulty/intermediate.png', "DATA"),
                     ('Resources/MapDifficulty/advanced.png', 'src/Resources/MapDifficulty/advanced.png', "DATA"), ('Resources/MapDifficulty/expert.png', 'src/Resources/MapDifficulty/expert.png', "DATA"),

                     ('Resources/Maps/alpine_run.png', 'src/Resources/Maps/alpine_run.png', "DATA"), ('Resources/Maps/candy_falls.png', 'src/Resources/Maps/candy_falls.png', "DATA"), 
                     ('Resources/Maps/carved.png', 'src/Resources/Maps/carved.png', "DATA"), ('Resources/Maps/cubism.png', 'src/Resources/Maps/cubism.png', "DATA"), 
                     ('Resources/Maps/end_of_the_road.png', 'src/Resources/Maps/end_of_the_road.png', "DATA"), ('Resources/Maps/four_circles.png', 'src/Resources/Maps/four_circles.png', "DATA"), 
                     ('Resources/Maps/frozen_over.png', 'src/Resources/Maps/frozen_over.png', "DATA"), ('Resources/Maps/hedge.png', 'src/Resources/Maps/hedge.png', "DATA"), 
                     ('Resources/Maps/in_the_loop.png', 'src/Resources/Maps/in_the_loop.png', "DATA"), ('Resources/Maps/logs.png', 'src/Resources/Maps/logs.png', "DATA"), 
                     ('Resources/Maps/lotus_island.png', 'src/Resources/Maps/lotus_island.png', "DATA"), ('Resources/Maps/middle_of_the_road.png', 'src/Resources/Maps/middle_of_the_road.png', "DATA"), 
                     ('Resources/Maps/monkey_meadow.png', 'src/Resources/Maps/monkey_meadow.png', "DATA"), ('Resources/Maps/one_two_tree.png', 'src/Resources/Maps/one_two_tree.png', "DATA"), 
                     ('Resources/Maps/park_path.png', 'src/Resources/Maps/park_path.png', "DATA"), ('Resources/Maps/resort.png', 'src/Resources/Maps/resort.png', "DATA"), 
                     ('Resources/Maps/scrapyard.png', 'src/Resources/Maps/scrapyard.png', "DATA"), ('Resources/Maps/skates.png', 'src/Resources/Maps/skates.png', "DATA"), 
                     ('Resources/Maps/the_cabin.png', 'src/Resources/Maps/the_cabin.png', "DATA"), ('Resources/Maps/town_center.png', 'src/Resources/Maps/town_center.png', "DATA"), 
                     ('Resources/Maps/tree_stump.png', 'src/Resources/Maps/tree_stump.png', "DATA"), ('Resources/Maps/winter_park.png', 'src/Resources/Maps/winter_park.png', "DATA"), 



                     ('Resources/Maps/infernal.png', 'src/Resources/Maps/infernal.png', "DATA"),

                     ('Resources/Difficulty/easy.png', 'src/Resources/Difficulty/easy.png', "DATA"), ('Resources/Difficulty/medium.png', 'src/Resources/Difficulty/medium.png', "DATA"),
                     ('Resources/Difficulty/hard.png', 'src/Resources/Difficulty/hard.png', "DATA"),

                     ('Resources/Mode/deflation.png', 'src/Resources/Mode/deflation.png', "DATA")
                     
                     ],
          [],
          exclude_binaries=True,
          name=os.path.join('dist', 'BloonsUIFarm' + ('.exe' if sys.platform == 'win32' else '')),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          icon='src/Resources/UI/btdfarmicon.ico',
          entitlements_file=None )
if sys.platform == 'darwin':
   coll = COLLECT(exe,
                  a.binaries,
                  a.zipfiles,
                  a.datas,
                  strip=False,
                  upx=True,
                  upx_exclude=[],
                  name='BloonsUIFarm')
   app = BUNDLE(coll,
                name='BloonsFarmUI.app',
                icon='src/Resources/UI/btdfarmicon.ico',
                bundle_identifier=None)
  
