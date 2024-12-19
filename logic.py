import sys
import os
import tkinter as tk
import numpy as np
import json

import save_data
import plot


# 初期化
drawing = False
x_list = []
y_list = []
pre_x = -1
pre_y = -1

# 同じ文字について複数のa_bを保存しておくための配列
all_x_y_a_b = [[], []]

# 一文字のa_bを保存しておくための配列
x_a_b = [[], []]
y_a_b = [[], []]

# 平均文字のa_bを保存しておくための配列
ave_x_a_b = None
ave_y_a_b = None

# 追加した文字のプレビューを行うためのx_y座標の配列
view_x_y = []
ave_x_y = []

kakusuu = 0
point_nums = []

# 一文字について書いた個数
draw_num = 0

# 同期処理のために使用
counter = 0

# 登録した字数
saved_char_num = 0

# 全ての文字の総画数
total_stroke_num = 0

# ターゲットの文字の画数
target_stroke_num = 0

# ターゲットの文字
target_char_str = ''

def init():
    # 初期化処理
    global pre_x, pre_y, kakusuu, counter, x_a_b, y_a_b, view_x_y, point_nums

    x_a_b = [[], []]
    y_a_b = [[], []]
    view_x_y = []
    kakusuu = 0
    pre_x = -1
    pre_y = -1

    point_nums = [0] * 30

    counter = 0

def averaging_all_x_y_a_b():
    global ave_x_a_b, ave_y_a_b

    tmp_x = np.zeros(50)
    tmp_y = np.zeros(50)

    _ave_x_a_b = [[], []]
    _ave_y_a_b = [[], []]

    for a_b in range(2):
        for j in range(kakusuu):
            tmp_x.fill(0)
            tmp_y.fill(0)
            
            for k in range(51):
                for i in range(draw_num):
                    tmp_x[k] += all_x_y_a_b[0][i][a_b][j][k] / draw_num
                    tmp_y[k] += all_x_y_a_b[1][i][a_b][j][k] / draw_num
                    # all_x_y_a_b[x_or_y][書いた文字のNo][a_or_b][画数][フーリエ級数の係数]
            
            _ave_x_a_b[a_b].append(tmp_x.copy())
            _ave_y_a_b[a_b].append(tmp_y.copy())

    ave_x_a_b = _ave_x_a_b
    ave_y_a_b = _ave_y_a_b

def draw_view_canvas(ctx,x_y,canvas):
    ctx.set_fill_style("#000000")
    pen_size = 0.8
    if canvas.width >= 300:
        pen_size = 3

    for i in range(len(x_y[0])):
        for j in range(len(x_y[0][i])):
            ctx.fill_rect(((canvas.width)* x_y[0][i][j])/400,
                          canvas.width * (400 - x_y[1][i][j])/400,
                            pen_size,
                            pen_size)

# 点を減らし、線でつなぐ方法 
"""     for i in range(len(x_y[0])):
        for j in range(len(x_y[0][i]) - 1):
            ctx.begin_path() ctx.move_to((canvas.width * x_y[0][i][j])/400,
                                           canvas.width * (400 - x_y[1][i][j])/400)
            ctx.line_to((canvas.width * x_y[0][i][j + 1])/400,
                          canvas.width * (400 - x_y[1][i][j + 1])/400) 
            ctx.close_path() 
            ctx.stroke()
""" 
def init_canvas(cv, cx):
    cx.set_fill_style('#f0f5f9')
    cx.fill_rect(0, 0, cv.width, cv.height)
    grid_num = 20 * 2 
    margin = cv.height/(grid_num - 2) / 2 
    cx.set_stroke_style("#a7c1d6") 

    for i in range(0, grid_num, 2): 
        cx.begin_path() 
        cx.move_to(cv.width/2, cv.height/grid_num * i + margin) 
        cx.line_to(cv.width/2, cv.height/grid_num * (i + 1) + margin) 
        cx.close_path() 
        cx.stroke() 
    for i in range(0, grid_num, 2):
        cx.begin_path()
        cx.move_to(cv.width/grid_num * i + margin, cv.height/2)
        cx.line_to(cv.width/grid_num * (i + 1) + margin, cv.height/2)
        cx.close_path()
        cx.stroke()

def plot(x_a_b, y_a_b, ctx, canvas):
    ave_x_y = [] 
    x_y_a_b = { "x": x_a_b, "y": y_a_b, "point_nums": point_nums }
    x_y_a_b_json_str = json.dumps(x_y_a_b)
    data = send_to_python_script('plot.py', x_y_a_b_json_str)
    ave_x_y.append(data['x'])
    ave_x_y.append(data['y'])
    draw_view_canvas(ctx, ave_x_y, canvas)

def view_plot(x_a_b, y_a_b, ctx, canvas):
    view_x_y = [] 
    x_y_a_b = { "x": x_a_b, "y": y_a_b, "point_nums": point_nums }
    x_y_a_b_json_str = json.dumps(x_y_a_b) 
    data = send_to_python_script('plot.py', x_y_a_b_json_str)
    view_x_y.append(data['x']) 
    view_x_y.append(data['y']) 
    draw_view_canvas(ctx, view_x_y, canvas) 

def save_data():
    send_json = {target_char_str: ave_x_y}
    send_to_python_script('save_data.py', json.dumps(send_json))

def check(file_path): 
    return os.path.exists(file_path) 

def read_json(file_path): 
    if check(file_path): 
        with open(file_path, 'r', encoding='utf8') as f:
            return f.read()
    return ""

def send_to_python_script(script,data):
    if script == "save_data.py":
        return save_data.main(data)
    elif script == "plot.py":
        return plot(data)









root = tkinter.Tk()
root.title(u"Make-My-Font-py")
root.geometry("1000x800")

root.configure(bg='#a7c1d6') #背景色
#canvas = tkinter.Canvas(root,)

root.mainloop()