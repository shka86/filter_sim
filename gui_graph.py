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


class Agraph(tk.Frame):
    def __init__(self, master, params):
        super().__init__(master)
        self.master = master
        self.params = params
        frame = tk.Frame(self.master)
        frame.pack()

        fig = Figure()
        self.ax = fig.add_subplot(1, 1, 1)
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        button = tk.Button(self.master, text="Draw Graph", command=self.button_click)
        button.pack()

    def button_click(self):
        x = np.arange(-np.pi, np.pi, 0.001)
        y = np.sin(x * self.params.param1.var.get())
        self.ax.plot(x, y)
        self.fig_canvas.draw()


class ParamSlider():
    """ パラメータを入力するためのスライダおよび入力BOX
        値： self.var
        init(option): 初期値
    """

    def __init__(self, master, label, min_, max_, init=None):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame_box = tk.Frame(self.frame)

        # パラメータ
        self.var = tk.IntVar(value=init)

        # -----------------------------------
        # スライダー
        self.scale = tk.Scale(self.frame, label=label, variable=self.var,
                              from_=min_, to=max_, showvalue=False, tickinterval=(max_ - min_), orient=tk.HORIZONTAL)
        # self.scale.bind(sequence="<Motion>", func=self.when_param_update)
        self.scale.grid(row=0, column=0, padx=3, pady=3)

        # -----------------------------------
        self.frame_box.grid(row=0, column=1)

        # spin box
        self.spinbox = tk.Spinbox(self.frame_box, textvariable=self.var, width=10, from_=min_, to=max_, increment=1)
        self.spinbox.pack()

        # entry(独立に入力可能とするために、Enterを押したときにだけ更新するようにつくる。textvariableを使ってはいけない)
        self.entry = tk.Entry(self.frame_box, width=12)
        self.entry.insert(0, f"{int(self.var.get()):#010x}")
        self.entry.bind(sequence="<Return>", func=self.when_entry_input)
        self.entry.pack()

        # -----------------------------------

        self.var.trace('w', self.when_param_update)  # パラメータのtraceは最後にしないと起動時にエラーメッセージが出る
        self.frame.pack()

    def when_param_update(self, *args):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, f"{int(self.var.get()):#010x}")

    def when_entry_input(self, event):
        self.var.set(int(self.entry.get(), 0))


class Params():
    """ このクラスでは、計算に使用するパラメータを定義します。
        master: パラメータを調整するスライダなどのウィジェットを置く場所を指定します。

        パラメータを一つのインスタンスにまとめることで、あとあとあれこれいろんなことから
        パラメータを引っ張ってきて計算したくなる場合にスムーズに対応できるようにしておく。
    """

    def __init__(self):
        pass

    def def_tab1(self, master):
        self.param1 = ParamSlider(master, "param1", 0, 100, init=5)
        self.param2 = ParamSlider(master, "param2", 50, 100)
        self.param3 = ParamSlider(master, "param3", 50, 100)
        self.param4 = ParamSlider(master, "param4", 50, 100)
        self.param5 = ParamSlider(master, "param5", 80, 200)

    def def_tab2(self, master):
        self.param6 = ParamSlider(master, "param6", 0, 100)
        self.param7 = ParamSlider(master, "param7", 50, 100)
        self.param8 = ParamSlider(master, "param8", 50, 100)
        self.param9 = ParamSlider(master, "param9", 50, 100)
        self.param10 = ParamSlider(master, "param10", 80, 200)


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
        nb_left.grid(row=0, column=0, sticky="news")

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
        nb_right.grid(row=0, column=1)

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
