import math
import random
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pywt


# ----------------------------------------------------------------------------------------------------------------------
# Создание синусоиды
# ----------------------------------------------------------------------------------------------------------------------
def createSinSignal(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(256 * period):
        point = Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180)
        signal.append(point)
        timer.append(tim * i)
    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание синусоиды с искажением
# ----------------------------------------------------------------------------------------------------------------------
def createSinNoiseSignal(Am, phs, freq, period, AmNois, phsNois, freqNois):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(256 * period):
        point = (Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180)) + (
                AmNois * math.sin(2 * math.pi * freqNois * (tim * i) + phsNois * math.pi / 180))
        signal.append(point)
        timer.append(tim * i)
    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание синусоиды с изменяющейся частотой
# ----------------------------------------------------------------------------------------------------------------------
def createSinChang(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(256 * period):
        if i <= 64 * period:
            point = Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180)
            signal.append(point)
            timer.append(tim * i)
        elif 65 * period < i <= 128 * period:
            point = Am * math.sin(2 * math.pi * 10 * freq * (tim * i) + phs * math.pi / 180)
            signal.append(point)
            timer.append(tim * i)
        elif 129 * period < i <= 192 * period:
            point = Am * math.sin(2 * math.pi * 20 * freq * (tim * i) + phs * math.pi / 180)
            signal.append(point)
            timer.append(tim * i)
        else:
            point = Am * math.sin(2 * math.pi * 30 * freq * (tim * i) + phs * math.pi / 180)
            signal.append(point)
            timer.append(tim * i)

    return signal, timer


# ----------------------------------------------------------------------------------------------------------------------
# Создание синусоиды со случайным искажением
# ----------------------------------------------------------------------------------------------------------------------
def createSinNoiseRandom(Am, phs, freq, period):
    signal = []
    timer = []
    tim = 1 / (256 * freq)
    for i in range(256 * period):
        point = (Am * math.sin(2 * math.pi * freq * (tim * i) + phs * math.pi / 180)) + Am * 0.1 * random.randint(0, 10)
        signal.append(point)
        timer.append(tim * i)
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


# ----------------------------------------------------------------------------------------------------------------------
# Метод по расчету коэффициентов Аппроксимирующих и Детализирующих
# ----------------------------------------------------------------------------------------------------------------------
def createCoefAD(signal):
    mass_A = []  # Аппроксимирующие
    mass_D = []  # Детализирующие

    new_len = len(signal)

    for i in range(0, new_len - 1, 2):
        mass_A.append((signal[i] + signal[i + 1]) / 2)
        mass_D.append((signal[i] - signal[i + 1]) / 2)

    return mass_A, mass_D


# ----------------------------------------------------------------------------------------------------------------------
# Метод по расчету всех уровней Вейвлет преобразований
# ----------------------------------------------------------------------------------------------------------------------
def calculateCoefAD(signal):
    mass_A_List = []
    mass_D_List = []

    len_mass = len(signal)

    while len_mass > 1:
        mass_A, mass_D = createCoefAD(signal)
        mass_A_List.append(mass_A)
        mass_D_List.append(mass_D)

        signal = mass_A

        len_mass = len(signal)

    return mass_A_List, mass_D_List


# ----------------------------------------------------------------------------------------------------------------------
# Вывод уровней
# ----------------------------------------------------------------------------------------------------------------------
def printCoefAD(mass_A, mass_D):
    for i in range(len(mass_A)):
        print(f"Уровень {i + 1}")
        print(f"Коэффициенты A: {mass_A[i]}")
        print(f"Коэффициенты D: {mass_D[i]} \n")


# ----------------------------------------------------------------------------------------------------------------------
# Метод по восстановлению предыдущего уровня Вейвлет преобразования
# ----------------------------------------------------------------------------------------------------------------------
def recoveryCoefAD(mass_a, mass_d):
    old_mass_A = []

    for i in range(len(mass_a)):
        old_mass_A.append(mass_a[i] + mass_d[i])
        old_mass_A.append(mass_a[i] - mass_d[i])

    return old_mass_A


# ----------------------------------------------------------------------------------------------------------------------
# Метод по восстановлению исходного сигнала
# ----------------------------------------------------------------------------------------------------------------------
def recoveryCalculateCoefAD(mass_a_list, mass_d_list):
    signal = mass_a_list[-1]

    for i in range(len(mass_a_list)):
        signal = recoveryCoefAD(signal, mass_d_list[- 1 - i])

    return signal


# ----------------------------------------------------------------------------------------------------------------------
# Метод по устранению помех в исходном сигнале
# ----------------------------------------------------------------------------------------------------------------------
def eliminateInterference(mass_a, mass_d, mass_d_base):
    new_A_coef = [mass_a[-1]]

    for i in range((len(mass_a) - 1), -1, -1):
        D_coef_dif = adjustmentDCoef(mass_d[i], mass_d_base[i])
        A_coef_recover = []
        for j in range(len(mass_a[i])):
            A_coef_recover.append(new_A_coef[-1][j] + D_coef_dif[j])
            A_coef_recover.append(new_A_coef[-1][j] - D_coef_dif[j])
        new_A_coef.append(A_coef_recover)

    return new_A_coef[-1]


# ----------------------------------------------------------------------------------------------------------------------
# Метод по корректировке детализирующих коэффициентов
# ----------------------------------------------------------------------------------------------------------------------
def adjustmentDCoef(mass_d, mass_d_base):
    mass_d_help = mass_d
    for k in range(len(mass_d_help)):
        if mass_d_help[k] != mass_d_base[k]:
            dif = mass_d_help[k] - mass_d_base[k]
            mass_d_help[k] = mass_d_help[k] - dif

    return mass_d_help


# ----------------------------------------------------------------------------------------------------------------------
# Метод построения скейлограммы по вейвлету "Мексиканская шляпа"
# ----------------------------------------------------------------------------------------------------------------------
def waveletMexH(signal):
    scales = np.arange(1, 100)
    coef, freqs = pywt.cwt(signal, scales, 'mexh')
    plt.imshow(np.abs(coef), extent=[0, len(signal), freqs[-1], freqs[0]], cmap='jet', aspect='auto')
    plt.colorbar()
    plt.title('Скейлограмма вейвлета Мексиканская шляпа')
    plt.xlabel('t')
    plt.ylabel('Scale')
    plt.show()


# ----------------------------------------------------------------------------------------------------------------------
# Метод построения скейлограммы по вейвлету "Морлета"
# ----------------------------------------------------------------------------------------------------------------------
def waveletMorlet(signal):
    scales = np.arange(1, 100)
    coef, freqs = pywt.cwt(signal, scales, 'morl')
    plt.imshow(np.abs(coef), extent=[0, len(signal), freqs[-1], freqs[0]], cmap='jet', aspect='auto')
    plt.colorbar()
    plt.title('Скейлограмма вейвлета Морлета')
    plt.xlabel('t')
    plt.ylabel('Scale')
    plt.show()


signal_list_1, timer_list_1 = createSinSignal(5, 0, 50, 4)  # Исходный сигнал
signal_list_2, timer_list = createSinNoiseSignal(5, 0, 50, 4, 1, 40, 500)  # Исходный сигнал с помехами
signal_list_3, timer_list_3 = createSinChang(5, 0, 50, 4)  # Сигнал с изменяющейся частотой
signal_list_4, timer_list_4 = createSinNoiseRandom(5, 0, 50, 4)  # Исходный сигнал со случайным искажением
signal_list_5, timer_list_5 = createMeandr(5, 0, 50, 4)

A_list_1, D_list_1 = calculateCoefAD(signal_list_1)  # Коэффициенты сигнала без помех
A_list_2, D_list_2 = calculateCoefAD(signal_list_2)  # Коэффициенты сигнала с помехами
A_list_2_1, D_list_2_1 = calculateCoefAD(signal_list_2)  # Коэффициенты сигнала с помехами
A_list_3, D_list_3 = calculateCoefAD(signal_list_3)
A_list_4, D_list_4 = calculateCoefAD(signal_list_4)
A_list_5, D_list_5 = calculateCoefAD(signal_list_5)

printCoefAD(A_list_2, D_list_2)

signal_without = eliminateInterference(A_list_2, D_list_2, D_list_1)  # Сигнал с устраненными помехами

signal_rev = recoveryCalculateCoefAD(A_list_2_1, D_list_2_1)  # Восстановленный сигнал
signal_rev_3 = recoveryCalculateCoefAD(A_list_3, D_list_3)
signal_rev_4 = recoveryCalculateCoefAD(A_list_4, D_list_4)
signal_rev_5 = recoveryCalculateCoefAD(A_list_5, D_list_5)

fig, ax = plt.subplots(nrows=6, ncols=1)
ax[0].plot(timer_list_1, signal_list_1, c='red')
ax[1].plot(timer_list_1, signal_list_2, c='blue')
ax[2].plot(timer_list_1, signal_rev, c='green')
ax[3].plot(timer_list_1, signal_without, c='black')
ax[4].plot(timer_list_3, signal_list_3, c='orange')
ax[5].plot(timer_list_5, signal_list_5, c='pink')
# ax[6].plot(timer_list_5, signal_list_5, c='red')
# ax[7].plot(timer_list_5, signal_rev_5, c='blue')

ax[0].set_title('Исходный сигнал')
ax[1].set_title('Исходный сигнал с помехами')
ax[2].set_title('Восстановленный сигнал')
ax[3].set_title('Сигнал с устраненными помехами')
ax[4].set_title('Сигнал с изменяющейся частотой')
ax[5].set_title('Сигнал со случайными искажениямиф')
# ax[6].set_title('Сигнал меандра')
# ax[7].set_title('Сигнал меандра восстановленный')
fig.suptitle('Графики сигналов')
plt.show()

waveletMexH(signal_list_1)
waveletMexH(signal_list_2)
waveletMexH(signal_list_3)
waveletMexH(signal_list_4)
waveletMexH(signal_list_5)

waveletMorlet(signal_list_1)
waveletMorlet(signal_list_2)
waveletMorlet(signal_list_3)
waveletMorlet(signal_list_4)
waveletMorlet(signal_list_5)
