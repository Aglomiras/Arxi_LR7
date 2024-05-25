import math

from matplotlib import pyplot as plt


# ----------------------------------------------------------------------------------------------------------------------
# Создание синусоиды
# ----------------------------------------------------------------------------------------------------------------------
def createSinSignal(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(-127 * period, 128 * period):
        point = Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180)
        signal.append(point)
        timer.append(tim * i)
    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание Вейвлета "Мексиканская шляпа"
# ----------------------------------------------------------------------------------------------------------------------
def createMexican(period):
    signal = []
    timer = []
    tim = 1 / (32 * period)
    for i in range(-127 * period, 128 * period):
        point = (5 - math.pow(i * tim, 2)) * math.exp((- math.pow(i * tim, 2)) / 2)
        signal.append(point)
        timer.append(i * tim)
    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание Вейвлета "Морлета"
# ----------------------------------------------------------------------------------------------------------------------
def createMorlet(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(-127 * period, 128 * period):
        k = math.pow(i / 256, 2) / (-2)
        point = Am * math.exp(k) * math.cos(5 * math.pi * freq * (tim * i))
        signal.append(point)
        timer.append(i * tim)
    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание меандра
# ----------------------------------------------------------------------------------------------------------------------
def createMeandr(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(-127 * period, 128 * period):
        point = Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180) + Am / 3 * math.sin(
            2 * math.pi * 3 * freq * (tim * i) + phs * math.pi / 180) + Am / 5 * math.sin(
            2 * math.pi * 5 * freq * (tim * i) + phs * math.pi / 180) + Am / 7 * math.sin(
            2 * math.pi * 7 * freq * (tim * i) + phs * math.pi / 180) + Am / 9 * math.sin(
            2 * math.pi * 9 * freq * (tim * i) + phs * math.pi / 180) + Am / 11 * math.sin(
            2 * math.pi * 11 * freq * (tim * i) + phs * math.pi / 180) + Am / 13 * math.sin(
            2 * math.pi * 13 * freq * (tim * i) + phs * math.pi / 180) + Am / 15 * math.sin(
            2 * math.pi * 15 * freq * (tim * i) + phs * math.pi / 180) + Am / 17 * math.sin(
            2 * math.pi * 17 * freq * (tim * i) + phs * math.pi / 180) + Am / 19 * math.sin(
            2 * math.pi * 19 * freq * (tim * i) + phs * math.pi / 180) + Am / 21 * math.sin(
            2 * math.pi * 21 * freq * (tim * i) + phs * math.pi / 180) + Am / 23 * math.sin(
            2 * math.pi * 23 * freq * (tim * i) + phs * math.pi / 180) + Am / 25 * math.sin(
            2 * math.pi * 25 * freq * (tim * i) + phs * math.pi / 180) + Am / 27 * math.sin(
            2 * math.pi * 27 * freq * (tim * i) + phs * math.pi / 180) + Am / 29 * math.sin(
            2 * math.pi * 29 * freq * (tim * i) + phs * math.pi / 180)
        signal.append(point)
        timer.append(tim * i)
    return signal, timer


signal_list_1, timer_list_1 = createSinSignal(5, 0, 50, 1)  # Исходный сигнал
signal_list_2, timer_list_2 = createMexican(1)  # Исходный сигнал с помехами
signal_list_3, timer_list_3 = createMorlet(1, 0, 50, 8)  # Исходный сигнал
signal_list_4, timer_list_4 = createMeandr(5, 0, 50, 4)  # Исходный сигнал

fig, ax = plt.subplots(nrows=4, ncols=1)
ax[0].plot(timer_list_1, signal_list_1, c='red')
ax[1].plot(timer_list_2, signal_list_2, c='blue')
ax[2].plot(timer_list_3, signal_list_3, c='green')
ax[3].plot(timer_list_4, signal_list_4, c='red')

ax[0].set_title('Исходный сигнал')
ax[1].set_title('Мексиканская шляпа')
ax[2].set_title('Вейвлет Морлета')
ax[3].set_title('Меандр')

fig.suptitle('Графики сигналов')
plt.show()
