import math
from decimal import Decimal


def forward_kinematics(serv1, serv2, serv3, bone1, bone2, bone3, start_position = (0,0)):
    """принимает градусы поворота сервопривода и длину кости.
    использует 3 вертикальных сервопривода
    рассчитывает координату кончика
    serv2  - 45-135
    serv3  - 30-150"""

    serv2 = 180 - serv2
    serv3 = 180 - serv3

    C2C4 = find_C2_C4(bone2, bone3, serv3)
    print("C2C4 =", C2C4)


    C3C2C4 = find_C3C2C4(C2C4, bone2, bone3)
    print("C3C2C4 =", C3C2C4)


    OC2C4 = serv2 - C3C2C4
    print("OC2C4 =", OC2C4)


    x = find_absolute_long(C2C4, OC2C4) + bone1
    y = find_absolute_height(C2C4, OC2C4)

    return round(x, 12), round(y, 12)

def find_C2_C4(bone2, bone3, serv3):
    C2C4_squ = bone2 ** 2 + bone3 ** 2 - 2 * round(math.cos(math.radians(serv3)),12) * bone2 * bone3
    return math.sqrt(C2C4_squ)

def find_C3C2C4(C2C4, bone2,bone3 ):
    up = C2C4 ** 2 + bone2 ** 2 - bone3 ** 2
    down = 2 * C2C4 * bone2
    if down == 0:
        return 0
    cosC3C2C4 = up / down
    rad_C3C2C4 = math.acos(cosC3C2C4)
    angleC3C2C4 = math.degrees(rad_C3C2C4)
    return angleC3C2C4

def find_absolute_long(C2C4, OC2C4):
    return round(math.sin(math.radians(OC2C4)), 12) * C2C4

def find_absolute_height(C1C4, OC2C4):
    return round(math.cos(math.radians(OC2C4)),12) * C1C4
# ------------------------------------------
# print(forward_kinematics(180,90,90,1.0,1.0,1.0))



def serv_coordinates(serv, bone, start_position = (0,0), old_angle = 0):
    serv = serv-90+old_angle
    x = round(math.cos(math.radians(serv)),12) * bone
    y=round(math.sin(math.radians(serv)),12) * bone
    return start_position[0] + x, start_position[1] + y, serv

def find_all_servs_coordinates(servs ,start= (0,0)):
    """стартовая позиция должна взаранее сдвигаться на длину первой кости из за особенности сгибания"""
    print(start)
    group1 = servs[0]
    serv1, bone1 = group1
    start = (bone1+start[0], start[1])
    angle = 0
    print(start)
    for group in servs[1:]:
        serv, bone = group
        x,y,angle = serv_coordinates(serv1, bone, start, angle)
        start = x,y
        print(start)

data = [
    (180,1),
    (0,1),
    (0,1),

]
НУ УЧИТЫВАЕТСЯ ТО ЧТО УШЕЛ В НИЗ ВЕРОЯТНО НАСТРОИТЬ ANGLE
print(find_all_servs_coordinates(data))