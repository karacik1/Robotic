import math


def old_forward_kinematics(serv1, serv2, serv3, bone1, bone2, bone3):
    """принимает градусы поворота сервопривода и длину кости.
    использует 3 вертикальных сервопривода"""
    C2C4 = find_C2_C4(bone2, bone3, serv3)

    C3C2C4 = find_C3C2C4(C2C4, bone2, bone3)

    C1C2C4 = serv2 - C3C2C4

    C1C4 = find_C1C4(bone1, C2C4, C1C2C4)

    C2C1C4 = find_C2C1C4(C1C4, bone1, C2C4)



    OC1C4 = serv1 - C2C1C4

    x = find_absolute_long(C1C4, OC1C4)

    y = find_absolute_height(C1C4, OC1C4)

    return x, y


def find_C2_C4(bone2, bone3, serv3):
    C2C4_squ = bone2 ** 2 + bone3 ** 2 - 2 * math.cos(math.radians(serv3)) * bone2 * bone3
    return math.sqrt(C2C4_squ)


def find_C3C2C4(C2C4, bone2, bone3):
    up = C2C4 ** 2 + bone2 ** 2 - bone3 ** 2
    down = 2 * C2C4 * bone2
    cosC3C2C4 = up / down

    rad_C3C2C4 = math.acos(cosC3C2C4)
    angleC3C2C4 = math.degrees(rad_C3C2C4)
    return angleC3C2C4


def find_C1C4(bone1, C2C4, C1C2C4):
    C1C4_squ = bone1 ** 2 + C2C4 ** 2 - 2 * C2C4 * math.cos(math.radians(C1C2C4))
    return math.sqrt(C1C4_squ)


def find_C2C1C4(C1C4, bone1, C2C4):
    up = C1C4 ** 2 + bone1 ** 2 - C2C4 ** 2
    down = 2 * C1C4 * bone1
    cosC1C2C4 = up / down
    rad_C1C2C4 = math.acos(cosC1C2C4)
    angleC1C2C4 = math.degrees(rad_C1C2C4)
    return angleC1C2C4


def find_absolute_long(C1C4, OC1C4):
    return math.cos(math.radians(OC1C4)) * C1C4


def find_absolute_height(C1C4, OC1C4):
    return math.sin(math.radians(OC1C4)) * C1C4


# ------------------------------------------

