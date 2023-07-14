import os

import pyautogui
import json

from towerInfo import towerData
from menuNavInfo import menuNavData



def nameConversion(hotkey):
    if hotkey == 'q':
        return 'dart'
    elif hotkey == 'w':
        return 'boomerang'
    elif hotkey == 'e':
        return 'bomb_shooter'
    elif hotkey == 'r':
        return 'tack_shooter'
    elif hotkey == 't':
        return 'ice'
    elif hotkey == 'y':
        return 'glue_gunner'
    elif hotkey == 'z':
        return 'sniper'
    elif hotkey == 'x':
        return 'sub'
    elif hotkey == 'c':
        return 'buccaneer'
    elif hotkey == 'v':
        return 'plane'
    elif hotkey == 'b':
        return 'heli_pilot'
    elif hotkey == 'n':
        return 'mortar'
    elif hotkey == 'm':
        return 'dartling'
    elif hotkey == 'a':
        return 'wizard'
    elif hotkey == 's':
        return 'super_monkey'
    elif hotkey == 'd':
        return 'ninja'
    elif hotkey == 'f':
        return 'alchemist'
    elif hotkey == 'g':
        return 'druid'
    elif hotkey == 'h':
        return 'farm'
    elif hotkey == 'j':
        return 'spike'
    elif hotkey == 'k':
        return 'village'
    elif hotkey == 'l':
        return 'engineer'
    elif hotkey == 'i':
        return 'beast_handler'
    else:
        return 'error'


def gen(towerData, menuNavData, fileName):
    width, height = pyautogui.size()
    x_fact = width/1920
    y_fact = height/1080
    towerx_fact = x_fact
    towery_fact = y_fact

    check = abs(y_fact/x_fact)
    if check > 1.3 or check < 0.74:
        towerx_fact = x_fact*1.1578125
        towery_fact = y_fact/1.10925925925

    data = {"towers": {},
            "menuNav": {}}
    counter = {}

    for tower in towerData:
        exists = data["towers"].get(nameConversion(tower.hotkey)+"_pos")
        if(exists is None):
            data["towers"][nameConversion(tower.hotkey)+"_pos"] = {"hotkey": tower.hotkey, "x": (towerx_fact * tower.x),
                                                                   "y": (towery_fact * tower.y), "top": tower.top,
                                                                   "middle": tower.middle, "bottom": tower.bottom}
        else:
            inCounter = counter.get(tower)
            if(inCounter is None):
                counter[tower] = 2
            else:
                counter[tower] += 1
            data["towers"][nameConversion(tower.hotkey)+"_"+str(counter[tower])+"_pos"] = {"hotkey": tower.hotkey, "x": (towerx_fact * tower.x),
                                                                                           "y": (towery_fact * tower.y), "top": tower.top,
                                                                                           "middle": tower.middle, "bottom": tower.bottom}

    data["menuNav"] = {"mapDifficulty": menuNavData.mapDifficulty,
                       "map": menuNavData.map,
                       "difficulty": menuNavData.difficulty,
                       "mode": menuNavData.mode}

    with open('Tower Positions/' + fileName +'.json', 'w') as f:
        json.dump(data, f)
