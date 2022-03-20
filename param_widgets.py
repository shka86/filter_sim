#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk

""" パラメータ調整用の定型ウィジェットを分離して、
    アプリケーション側のコードは固有の機能的なコードのみにして可読性を高める
"""


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

class ParamRadio():
    """ パラメータを入力するためのラジオボタン
        値： self.var
        choices: 下記形式の、選択肢と値のリスト
        [
            [param1 name, value],
            [param2 name, value],
            ...,
        ] 
        init(option): 初期値
    """

    def __init__(self, master, label, choices, init=None):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame_box = tk.Frame(self.frame)

        # パラメータ
        self.var = tk.DoubleVar(value=init)

        # -----------------------------------
        # ラベルフレーム
        self.lframe = tk.LabelFrame(self.master, text=label, labelanchor="nw")
        self.lframe.pack(fill="x", padx=3, pady=0)

        # -----------------------------------
        # ラジオボタン
        self.radios = []
        for choice in choices:
            self.radios.append(
                tk.Radiobutton(self.lframe, text=choice[0], value=choice[1], variable=self.var)
            )
        for radio in self.radios:
            radio.pack(anchor="nw")
