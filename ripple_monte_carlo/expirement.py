import numpy as np
from numpy.random import normal
from scipy.integrate import quadrature
import matplotlib.pyplot as plt

def expirement(V_app, R, C, ripple=0.01):
    dt = (R * C) / 1000
    t = np.linspace(0, dt * 2000, 2000)
    sigma = ripple * V_app

    xi = normal(V_app, sigma, len(t-1))
    Q = [0]

    for i in range(1,len(t)):
        dQ = (C * xi[i] - Q[-1]) / (R * C) * dt
        Q.append(Q[-1] + dQ)

    return (t, np.array(Q))

if __name__ == '__main__':
    R = 100
    C = 1e-9
    V_app = 1000
    t = []
    target = 8e-7

    for i in range(500):
        e = expirement(V_app,R,C)
        #plt.plot(*e)
        #plt.plot(e[0],target * np.ones(len(e[0])))
        #plt.show()
        idx = (np.abs(e[1] - target)).argmin()
        t.append(e[0][idx])

    t = np.array(t)
    t.sort()
    print(t)
    plt.hist(t,bins=15,edgecolor='black')
    plt.show()
