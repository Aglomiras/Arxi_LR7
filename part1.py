import math
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pywt


def create_base_signal(ampl, freq):
    signal = []
    time = []
    t = 0
    dt = (1 / freq) / 256
    for i in range(256):
        point = ampl * math.sin(2 * math.pi * freq * t)
        time.append(t)
        t += dt
        signal.append(point)
    return signal, time


def create_start_coef(signal):
    a_coef = []
    d_coef = []
    points = []
    buf = 0
    for k in range(256 // 2):
        points.append(k)
    for i in range(256):
        point = signal[i]
        if i == 0:
            buf = point
        elif i%2 == 1:
            a_coef.append((buf + point) / 2)
            d_coef.append((buf - point) / 2)
            buf = 0
        else:
            buf = point
    return a_coef, d_coef, points


def create_coef(a_coef):
    a_new = []
    d_new = []
    counter = 0
    size = len(a_coef)
    points = []
    for k in range(len(a_coef) // 2):
        points.append(k)
    while counter <= size - 1:
        a_new.append((a_coef[counter] + a_coef[counter + 1]) / 2)
        d_new.append((a_coef[counter] - a_coef[counter + 1]) / 2)
        counter += 2
    return a_new, d_new, points


def return_coef(signal):
    a_coef_global = []
    d_coef_global = []
    points_global = []
    [a_coef, d_coef, points] = create_start_coef(signal)
    a_coef_global.append(a_coef)
    d_coef_global.append(d_coef)
    points_global.append(points)
    print("Массив коэффициентов A для уровня 1 :")
    print(a_coef_global[0])
    print("Массив коэффициентов D для уровня 1 :")
    print(d_coef_global[0])
    remain = len(signal) // 4
    while remain != 0:
        [a_new, d_new, point] = create_coef(a_coef_global[len(a_coef_global) - 1])
        a_coef_global.append(a_new)
        d_coef_global.append(d_new)
        points_global.append(point)
        index = len(a_coef_global) - 1
        print("\nМассив коэффициентов A для уровня %2d :" % (len(a_coef_global)))
        print(a_coef_global[index])
        print("Массив коэффициентов D для уровня %2d :" % (len(a_coef_global)))
        print(d_coef_global[index])
        remain = remain // 2
    return a_coef_global, d_coef_global, points_global

def random_interf():
    interference = []
    for i in range(256):
        interference.append(randint(0, 10)/10)
    return interference


def meandr_interf():
    interference = []
    counter = 0
    for i in range(256):
        if counter < 5:
            interference.append(1)
            counter += 1
        else:
            interference.append(-1)
            counter += 1
        if counter == 10:
            counter = 0
    return interference


def high_freq_sin_interf(new_ampl, new_freq):
    interference = []
    t = 0
    new_time = []
    dt = ((new_freq/50) / new_freq) / 256
    for i in range(256):
        point = new_ampl * math.sin(2 * math.pi * new_freq * t)
        new_time.append(t)
        t += dt
        interference.append(point)
    return interference


def sum_signals(signal, interference):
    new_signal = []
    for i in range(len(signal)):
        new_signal.append(signal[i] + interference[i])
    return new_signal


def change_coef(d_coef_global, d_coef_base):
    for k in range(len(d_coef_global)):
        if d_coef_global[k] != d_coef_base[k]:
            diff = d_coef_global[k] - d_coef_base[k]
            d_coef_global[k] -= diff
    return d_coef_global


def reverse_conversion(a_coef_global, d_coef_global, d_coef_base):
    k = len(a_coef_global) - 1
    new_d_coef = []
    new_a_coef = []
    new_a_coef.append(a_coef_global[k])
    while k >= 0:
        d_coef = change_coef(d_coef_global[k], d_coef_base[k])
        a_coef = []
        for i in range(len(a_coef_global[k])):
            a_coef.append((new_a_coef[-1])[i] + d_coef[i])
            a_coef.append((new_a_coef[-1])[i] - d_coef[i])
        new_d_coef.append(d_coef)
        new_a_coef.append(a_coef)
        k -= 1
    return new_a_coef, new_d_coef


def grapf(num, title, signal, time):
    if title == "Исходный сигнал" or title == "Востановленный сигнал":
        plt.subplot(2, 1, num)
        plt.ylabel('f(t)', fontsize=9)
        plt.xlabel('t, с', fontsize=9)
        plt.plot(time, signal, 'r')
        plt.grid(True)
        plt.title(title, fontsize=9)
    else:
        plt.subplot(8, 2, num)
        if title == "A8" or title == "D8":
            plt.ylabel(title, fontsize=12)
            plt.plot(time, signal, color='r', marker='.')
            plt.grid(True)
        else:
            plt.ylabel(title, fontsize=12)
            plt.plot(time, signal, 'r')
            plt.grid(True)

def mexican_hat_wavelet(signal):
    scales = np.arange(1, 100)
    coef, freqs = pywt.cwt(signal, scales, 'mexh' )

    plt.imshow(np.abs(coef), extent=[0, len(signal), freqs[-1], freqs[0]], cmap='jet', aspect='auto')
    plt.colorbar()
    plt.title('Скейлограмма вейвлета Мексиканская шляпа')
    plt.xlabel('t')
    plt.ylabel('Scale')
    plt.show()


def morlet_wavelet(signal):
    scales = np.arange(1, 100)
    coef, freqs = pywt.cwt(signal, scales, 'morl')

    plt.imshow(np.abs(coef), extent=[0, len(signal), freqs[-1], freqs[0]], cmap='jet', aspect='auto')
    plt.colorbar()
    plt.title('Скейлограмма вейвлета Морлета')
    plt.xlabel('t')
    plt.ylabel('Scale')
    plt.show()

ampl = 4
freq = 50

[base_signal, time] = create_base_signal(ampl, freq)
[a_coef_base, d_coef_base, points_base] = return_coef(base_signal)
# signal = sum_signals(base_signal, random_interf())
# signal = sum_signals(base_signal, meandr_interf())
signal = sum_signals(base_signal, high_freq_sin_interf(1, 2000))
[a_coef_global, d_coef_global, points_global] = return_coef(signal)

fig, ax = plt.subplots(figsize=(30, 20))
plt.subplots_adjust(wspace=0.24, hspace=0.2, left=0.06, right=0.98, top=0.98, bottom=0.075)
num = 0
for i in range(len(a_coef_global)):
    title_a = f"A{i + 1}"
    grapf(num + 1, title_a, a_coef_global[i], points_global[i])
    title_d = f"D{i + 1}"
    grapf(num + 2, title_d, d_coef_global[i], points_global[i])
    num += 2
# plt.show()

new_a_coef, new_d_coef = reverse_conversion(a_coef_global, d_coef_global, d_coef_base)
new_signal = new_a_coef[-1]
new_a_coef.pop()
new_a_coef.reverse()
new_d_coef.reverse()

fig, ax = plt.subplots(figsize=(30, 20))
plt.subplots_adjust(wspace=0.24, hspace=0.2, left=0.06, right=0.98, top=0.98, bottom=0.075)
num = 0
for i in range(len(new_a_coef)):
    title_a = f"A{i + 1}"
    grapf(num + 1, title_a, new_a_coef[i], points_global[i])
    title_d = f"D{i + 1}"
    grapf(num + 2, title_d, new_d_coef[i], points_global[i])
    num += 2
# plt.show()

fig, ax = plt.subplots(figsize=(30, 10))
grapf(1, "Исходный сигнал", signal, time)
grapf(2, "Востановленный сигнал", new_signal, time)
plt.show()

mexican_hat_wavelet(signal)
morlet_wavelet(signal)