import pyautogui
import json

def main():
    width, height = pyautogui.size()
    x_fact = width/1920
    y_fact = height/1080
    towerx_fact = x_fact
    towery_fact = y_fact

    check = abs(y_fact/x_fact)
    if check > 1.3 or check < 0.74:
        towerx_fact = x_fact*1.1578125
        towery_fact = y_fact/1.10925925925

    pos = {

        "snipx": (towerx_fact * 1608),
        "snipy": (towery_fact * 501),
        "alchx": (towerx_fact * 1551),
        "alchy": (towery_fact * 544),
        "vilx": (towerx_fact * 1581),
        "vily": (towery_fact * 622),

        "nintopx": (towerx_fact * 824),
        "nintopy": (towery_fact * 366),
        "alchtopx": (towerx_fact * 831),
        "alchtopy": (towery_fact * 307),
        "alchbottomx": (towerx_fact * 834),
        "alchbottomy": (towery_fact * 764),
        "ninbottomx": (towerx_fact * 835),
        "ninbottomy": (towery_fact * 696)
    }

    with open('towerpos.json', 'w') as f:
        json.dump(pos, f)

if __name__ == '__main__':
    main()


