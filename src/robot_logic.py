import math

from matplotlib import pyplot as plt


def forward_kinematics(serv1, serv2, serv3, bone1, bone2, bone3, start_position=(0, 0)):
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
    C2C4_squ = bone2 ** 2 + bone3 ** 2 - 2 * round(math.cos(math.radians(serv3)), 12) * bone2 * bone3
    return math.sqrt(C2C4_squ)


def find_C3C2C4(C2C4, bone2, bone3):
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
    return round(math.cos(math.radians(OC2C4)), 12) * C1C4


# ------------------------------------------
# print(forward_kinematics(180,90,90,1.0,1.0,1.0))


def serv_coordinates(serv, bone, current_pos=(0, 0), current_angle=0):
    # приводит положение серв к положению относительно пола
    absolut_angle = serv - 90 + current_angle

    print("угол относительно пола =", absolut_angle)
    x = round(bone * math.cos(math.radians(absolut_angle)), 12)
    y = round(bone * math.sin(math.radians(absolut_angle)), 12)

    return current_pos[0] + x, current_pos[1] + y, absolut_angle


def find_all_servs_coordinates(servs, start=(0, 0)):
    """стартовая позиция должна взаранее сдвигаться на длину первой кости из за особенности сгибания"""
    # координаты первого привода, который прикриплен к корпусу
    coordinates = [start]

    # координаты второго привода
    group2 = servs[0]
    serv2, bone2 = group2
    start = (bone2 + start[0], start[1])
    coordinates.append(start)
    print("serv 2:", start)
    current_angle = 0
    current_pos = start

    # Проходим циклом абсолютно по всем сервоприводам (включая первый!)
    for serv, bone in servs[1:]:
        x, y, current_angle = serv_coordinates(serv, bone, current_pos, current_angle)
        current_pos = (x, y)
        coordinates.append(current_pos)
    return coordinates


class TestServesCoordinates:
    def test_1(self):
        """диаграмма выгляди как закрывающаяся скобочка снизу вверх"""
        data = [
            (180, 1),
            (180, 1),
            (180, 1),
        ]
        coord = find_all_servs_coordinates(data)
        assert coord == [(0, 0), (1, 0), (1, 1), (0, 1)]

    def test_2(self):
        """диаграмма выгляди как закрывающаяся скобочка сверху вниз"""
        data = [
            (0, 1),
            (0, 1),
            (0, 1),
        ]
        coord = find_all_servs_coordinates(data)
        assert coord == [(0, 0), (1, 0), (1, -1), (0, -1)]

    def test_3(self):
        """диаграмма выглядит как прямая вправо"""
        data = [
            (90, 1),
            (90, 1),
            (90, 1),
        ]
        coord = find_all_servs_coordinates(data)
        assert coord == [(0, 0), (1, 0), (2, 0), (3, 0)]


def draw_plot(coor):
    x = []
    y = []
    for coor in coor:
        x.append(coor[0])
        y.append(coor[1])

    # рисуем вертикальную допь ось
    vert = plt.plot([0, 0], [4, -4])
    # горизонатльную
    gor = plt.plot([4, -4], [0, 0], )

    plt.setp(vert, color='y', linewidth=4.0)
    plt.setp(gor, color='y', linewidth=4.0)

    plt.plot(x, y, marker='o', linestyle='-', color='blue', linewidth=4, markersize=8)

    plt.title('Движение по оси OX')
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')

    # Включаем сетку
    plt.axis((-4, 4, -4, 4))

    # Показываем график
    plt.show()


data = [
    (90, 1),
    (180, 1),
    (30, 1),
]
draw_plot(find_all_servs_coordinates(data))
