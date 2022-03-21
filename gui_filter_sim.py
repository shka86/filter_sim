#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mimetypes import init
import numpy as np
import scipy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import sys
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib as plt
from pathlib import Path as p
import control.matlab as cm

import param_widgets as pw

class Graph1(tk.Frame):
    def __init__(self, master, params):
        super().__init__(master)
        self.master = master
        self.params = params

        # --- 描画制御用のボタンを配置するフレーム -----------------------------------
        control_frame = tk.Frame(self.master)
        control_frame.pack(fill="both", expand=True)

        # 連続描画enable
        self.graph_enable = pw.ParamCheckBox(control_frame, "graph_enable")
        self.graph_enable.var.trace("w", self.graph_update)

        # --- グラフを配置するフレーム -----------------------------------
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True)

        # --- グラフの中身 -----------------------------------
        fig = Figure()
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill="both", expand=True)

        # グラフ1
        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.set_xlabel("t[us]")
        self.ax.set_ylabel("[mV]")
        self.ax.set_ylim([-5000, 5000])
        self.t = np.arange(0, 1000, 1)

        # 入力波形: input
        self.v_input = self.f_input(self.t)
        self.line_input, = self.ax.plot(self.t, self.v_input)

        # 出力波形: output, ローパスフィルタを挿入した場合
        self.v_output = self.f_output(self.v_input)
        self.line_output, = self.ax.plot(self.t, self.v_output)


    def f_input(self, t):
        vamp = self.params.amplitude.var.get()
        vcom = self.params.vcommon.var.get()
        f = self.params.frequency.var.get()
        input_wave = self.params.input_wave.var.get()
        if input_wave == 0:  # step
            wave = np.where(t < 100, (vcom - vamp / 2), (vcom + vamp / 2))
        if input_wave == 1:  # sin
            wave = np.sin(f * t * 1e-6) * vamp + vcom
        if input_wave == 2:  # squware
            wave = sp.signal.square(f * t * 1e-6) * vamp + vcom
        return wave

    def f_output(self, x):
        lpf_r = self.params.lpf_r.var.get()
        lpf_c = self.params.lpf_c.var.get()
        # filter_t = 1 / (2 * np.pi * lpf_r * lpf_c * 1e-6)
        filter_t = (2 * np.pi * lpf_r * lpf_c * 1e-6)  # 時定数(2pi要るか未確認。検算すればわかるはず)
        num = [1]  # 伝達関数分子
        den = [filter_t, 1]  # 伝達関数分母
        sys = cm.tf(num, den)  # 伝達関数
        y, _, __ = cm.lsim(sys, x, self.t)  # 任意波形に対する応答
        return y

    def graph_update(self, *args):
        self.v_input = self.f_input(self.t)
        self.line_input.set_ydata(self.v_input)

        self.v_output = self.f_output(self.v_input)
        self.line_output.set_ydata(self.v_output)

        self.fig_canvas.draw()
        if self.graph_enable.var.get():
            self.after(100, self.graph_update)
        else:
            pass


class Params():
    """ このクラスでは、計算に使用するパラメータを定義します。
        master: パラメータを調整するスライダなどのウィジェットを置く場所を指定します。

        パラメータを一つのインスタンスにまとめることで、あとあとあれこれいろんなことから
        パラメータを引っ張ってきて計算したくなる場合にスムーズに対応できるようにしておく。
    """

    def __init__(self):
        pass

    def def_input_signal(self, master):
        self.input_wave = pw.ParamRadio(master, "input_wave",
                                        [
                                            ["step", 0],
                                            ["sin", 1],
                                            ["square", 2],
                                        ],
                                        init=0)
        self.frequency = pw.ParamSlider(master, "frequency[Hz]", 1, 1e6, init=10, type_="double")
        self.amplitude = pw.ParamSlider(master, "amplitude[mV]", 0, 3000, init=3000, type_="double")
        self.vcommon = pw.ParamSlider(master, "vcommon[mV]", 0, 3000, init=1500, type_="double")
        self.lpf_r = pw.ParamSlider(master, "lpf_r[ohm]", 1, 10000, init=1000, type_="double")
        self.lpf_c = pw.ParamSlider(master, "lpf_c[uF]", 1, 1000, init=10, type_="double")
        # self.param3 = pw.ParamSlider(master, "param3", 50, 100)
        # self.param4 = pw.ParamSlider(master, "param4", 50, 100)
        # self.param5 = pw.ParamSlider(master, "param5", 80, 200)

    def def_tab2(self, master):
        param6_choices = [
            ["振幅 0.5", 0.5],
            ["振幅 1.0", 1],
            ["振幅 2.0", 2],
            ["振幅 5.0", 5],
            ["振幅 10", 10],
            ["振幅 100", 100],
        ]
        self.param6 = pw.ParamRadio(master, "param6", param6_choices, init=10)
        self.param7 = pw.ParamSlider(master, "param7", 50, 100)
        self.param8 = pw.ParamSlider(master, "param8", 50, 100)
        self.param9 = pw.ParamSlider(master, "param9", 50, 100)
        self.param10 = pw.ParamSlider(master, "param10", 80, 200)


class AppMain(tk.Frame):
    """ このクラスでは、アプリケーションの外形を定義します。
        設定タブの分割やグラフタブなどを定義します。
    """

    def __init__(self, master=None):
        super().__init__(master)
        master.title("gui_graph")
        # master.geometry("500x250")

        # パラメータは全部ここに格納される
        self.params = Params()

        # --- tabs at left -----------------------------------

        nb_left = ttk.Notebook(master)
        nb_left.pack(side="left", fill="y", expand=True)  # できればwidthを固定したいがexpandは縦横両方しかできない？

        # input_signal
        self.input_signal = tk.Frame(nb_left)
        nb_left.add(self.input_signal, text='input_signal')
        self.params.def_input_signal(self.input_signal)

        # tab2
        self.tab2 = tk.Frame(nb_left)
        nb_left.add(self.tab2, text='tab2')
        self.params.def_tab2(self.tab2)

        # --- tabs at right -----------------------------------
        nb_right = ttk.Notebook(master)
        nb_right.pack(side="left", fill="both", expand=True)
        # nb_right.grid(row=0, column=1)

        # graph window
        tab_graph1 = tk.Frame(nb_right)
        nb_right.add(tab_graph1, text='tab_graph1')
        graph = Graph1(tab_graph1, self.params)


if __name__ == '__main__':

    # main window
    root = tk.Tk()
    app = AppMain(master=root)

    # Start App
    app.mainloop()
