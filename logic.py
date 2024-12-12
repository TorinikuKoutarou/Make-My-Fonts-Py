import sys
import tkinter
import numpy as np


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



# def draw_view_canvas(_ctx, _x_y, _canvas):






root = tkinter.Tk()
root.title(u"Make-My-Font-py")
root.geometry("1000x800")

root.configure(bg='#a7c1d6') #背景色
#canvas = tkinter.Canvas(root,)

root.mainloop()