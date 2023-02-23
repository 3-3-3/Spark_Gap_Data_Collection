import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.integrate import quadrature

def gaussian(t, mean, std):
    return 1 / (std * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((t-mean) / std) ** 2)


def gaussian_from(dt):
    mean = dt.mean()
    std = dt.std()

    t = np.linspace(mean - 4 * std, mean + 4 * std, 10000)
    return (mean, std, t, gaussian(t, mean, std))

def gaussian_expected_values(mean, std, edges):
    expected_values = []

    for i in range(len(edges) - 1):
        expected_values.append(quadrature(gaussian, edges[i], edges[i + 1], args=(mean, std))[0])

    return np.array(expected_values)

def rc_basic(t,xi,tau,t0=0):
    '''
    t: times
    xi: applied voltage
    tau: rc
    '''
    return xi * (1 - np.exp(-(t-t0) / tau))

def dt(t, V, threshold=-0.4):
    '''
    Return dt between discharges
    given a voltage array and a time array
    V: voltage array
    t: time array
    '''
    dV = np.diff(V)
    t = t[1:len(t)]

    dt = []
    t_last = 0

    points = 0
    delta_V = 0

    for i in range(len(dV)):
        if np.sign(dV[i]) == -1:
            delta_V += dV[i]
            points += 1

        else:
            if delta_V < threshold:
                #Do not use first measurement
                if t_last != 0:
                    dt.append(t[i-points] - t_last)
                t_last = t[i-points]

            delta_V = 0
            points = 0

    return np.array(dt)

def dt_from_measurement_dir(dir,threshold=-300):
    d = np.array([])
    for file in os.listdir(dir):
        data = np.load(os.path.join(dir, file), allow_pickle=True)
        d = np.append(d,dt(data[0],data[1],threshold=threshold))

    return d

def dt_hist(dt, title='????', color='green', bins=70):
    plt.style.use('ggplot')
    plt.title(title)
    plt.xlabel(r'dt ($\mu $s)')
    plt.ylabel('Count')
    plt.hist(dt * 1e6,bins=bins,color=color,edgecolor='black')

    save_string = title.replace(' ', '')
    plt.savefig(f'{save_string}.png')
    plt.show()

def frames(V, threshold = -0.4):
    frames = []
    dV = np.diff(V)
    i_1 = 0
    i_2 = 0
    points = 0
    delta_V = 0

    for i in range(len(dV)):
        if np.sign(dV[i]) == -1:
            points += 1
            delta_V += dV[i]


        else:
            if delta_V < threshold:
                #Detect discharge
                frames.append(V[i_1:i_2-points])
                i_1 = i_2
            delta_V = 0; points = 0

        i_2 += 1

    return frames

def av_frames(V, threshold=9,points=100):
    frames = []
    dV = np.diff(V)

    index = 0
    DV = 0
    i = 0

    while i < len(dV):
        if np.sign(dV[i]) == 1:
            DV += dV[i]

        else:
            if np.abs(DV) > threshold:
                frames.append(V[index : index+points])
                i += (points - 1)


            DV = 0
            index = i

        i += 1
    return frames

def av_dt(t,V,threshold=9):
    dV = np.diff(V)
    dt = []
    t_last = 0

    DV = 0
    i = 0

    for i in range(len(dV)):
        if np.sign(dV[i]) == 1:
            DV += dV[i]

        else:
            if np.abs(DV) > threshold:
                if t_last != 0:
                    dt.append(t[i] - t_last)
                t_last = t[i]


            DV = 0

    return np.array(dt)

def av_dt_from_measurement_dir(dir,threshold=9):
    d = np.array([])

    for file in os.listdir(dir):
        data = np.load(os.path.join(dir, file), allow_pickle=True)
        d = np.append(d,av_dt(data[0],data[1],threshold=threshold))

    return d

def t_V_from_measurement_dir(dir):
    V_out = np.array([]); V_in = np.array([]); t = np.array([])

    for file in os.listdir(dir):
        data = np.load(os.path.join(dir, file), allow_pickle=True)
        if t.size > 0:
            t = np.append(t,data[0] + t[-1])
        else:
            t = data[0]

        V_out = np.append(V_out,data[1])
        V_in = np.append(V_in,data[2])

    return (t, V_out, V_in)
