#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import math
import copy


class Lpf_fir1():

    def __init__(self):
        self.z1 = 0
        self.z2 = 0
        self.z3 = 0

        self.k0 = -0.1
        self.k1 = 0.3
        self.k2 = 0.8
        self.k3 = 0.2

    def do(self, x):
        self.z3 = self.z2
        self.z2 = self.z1
        self.z1 = x

        self.y = (self.k0 * x
                  + self.k1 * self.z1
                  + self.k2 * self.z2
                  + self.k3 * self.z3
                  )
        return self.y


def main():
    # データのパラメータ
    N = 40000             # サンプル数
    dt = 1 * 1e-5           # サンプリング間隔

    # 軸の計算
    list_t = np.arange(0, N * dt, dt)  # 時間軸
    list_x = 1 * (list_t > 10000 * dt)
    list_y = []

    print(list_t)
    print(list_x)

    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1)
    line1, = ax.plot(list_t, list_x)
    ax.set_xlabel('time[s]')
    # ax.set_ylabel('')
    ax.set_xlim([0, N * dt])
    line1.set_data(list_t, list_x)

    lpf = Lpf_fir1()

    for i, t in enumerate(list_t):

        y = lpf.do(list_x[i])
        list_y.append(y)
        
    line2, = ax.plot(list_t, list_y)
    line2.set_data(list_t, list_y)
    plt.pause(0.01)
    plt.show()



if __name__ == "__main__":
    main()
