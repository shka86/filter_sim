#!/usr/bin/python3
# -*- coding: utf-8 -*-

from mimetypes import init
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import sys
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib as plt
from pathlib import Path as p

import param_widgets as pw

class Agraph(tk.Frame):
    """ このクラスでは、描画されるグラフを定義します。
        master は AppMain の タブ です。
        params は グラフに描画するパラメータを与えるためのタブです。

        描画に関するボタン類、グラフ、計算式 で構成されています。
        グラフのパラメータは クラス: Params で設定する
    """

    def __init__(self, master, params):
        super().__init__(master)
        self.master = master
        self.params = params

        # --- 描画制御用のボタンを配置するフレーム -----------------------------------
        control_frame = tk.Frame(self.master)
        control_frame.pack(fill="both", expand=True)

        # 描画開始、都度描画ボタン
        button = tk.Button(control_frame, text="Draw Graph", command=self.button_click)
        button.pack(side="left")

        # 連続描画enable
        self.graph_enable = pw.ParamCheckBox(control_frame, "graph_enable")
        self.graph_enable.var.trace("w", self.graph_update)

        # --- グラフを配置するフレーム -----------------------------------
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True)

        # --- グラフの中身 -----------------------------------
        x = self.func_x()
        y = self.func_y(x)

        fig = Figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.line, = self.ax.plot(x, y)
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill="both", expand=True)

    def func_x(self):
        return np.arange(-np.pi, np.pi, 0.001)

    def func_y(self, x):
        return np.sin(x * self.params.param1.var.get()) * self.params.param6.var.get()

    def button_click(self):
        self.graph_update()

    def graph_update(self, *args):

        x = self.func_x()
        y = self.func_y(x)
        self.line.set_ydata(y)
        self.fig_canvas.draw()
        if self.graph_enable.var.get():
            self.after(1, self.graph_update)
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

    def def_tab1(self, master):
        self.param1 = pw.ParamSlider(master, "param1", 0, 100, init=5)
        self.param2 = pw.ParamSlider(master, "param2", 50, 100)
        self.param3 = pw.ParamSlider(master, "param3", 50, 100)
        self.param4 = pw.ParamSlider(master, "param4", 50, 100)
        self.param5 = pw.ParamSlider(master, "param5", 80, 200)

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

        # tab1
        self.tab1 = tk.Frame(nb_left)
        nb_left.add(self.tab1, text='tab1')
        self.params.def_tab1(self.tab1)

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
        graph = Agraph(tab_graph1, self.params)


if __name__ == '__main__':

    # main window
    root = tk.Tk()
    app = AppMain(master=root)

    # Start App
    app.mainloop()
