"""“一箭又一箭”基础版。

运行方式：python3 arrow_game.py
只使用 Python 自带的 tkinter，因此不需要额外安装第三方库。
"""

from dataclasses import dataclass
import tkinter as tk


# 方向对应的行、列变化。row 向下增加，col 向右增加。
DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

DIRECTION_TEXT = {"up": "↑", "down": "↓", "left": "←", "right": "→"}
DIRECTION_COLOR = {
    "up": "#2a9d8f",
    "down": "#457b9d",
    "left": "#f4a261",
    "right": "#9b5de5",
}


@dataclass(frozen=True)
class Arrow:
    """棋盘上一支箭头的位置和方向。"""

    row: int
    col: int
    direction: str


# 每关都经过手工试玩。前面的箭头有时会被后面的箭头挡住，
# 因此需要观察并按合适的顺序点击。
LEVELS = [
    [
        Arrow(2, 0, "right"),
        Arrow(2, 2, "up"),
        Arrow(0, 3, "up"),
        Arrow(4, 1, "down"),
        Arrow(1, 4, "right"),
    ],
    [
        Arrow(1, 0, "right"),
        Arrow(1, 2, "right"),
        Arrow(1, 4, "up"),
        Arrow(3, 4, "left"),
        Arrow(3, 2, "down"),
        Arrow(4, 0, "left"),
    ],
    [
        Arrow(0, 1, "down"),
        Arrow(2, 1, "right"),
        Arrow(2, 3, "up"),
        Arrow(4, 3, "left"),
        Arrow(4, 0, "up"),
        Arrow(1, 4, "down"),
        Arrow(3, 4, "left"),
    ],
]


class Board:
    """保存棋盘状态，负责最重要的路径判断。"""

    def __init__(self, arrows, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.arrows = list(arrows)

    def is_path_clear(self, arrow):
        """检查箭头朝向的同一行或同一列是否还有其他箭头。

        从箭头的下一格开始逐格检查；走出棋盘仍未遇到箭头，就说明
        该箭头可以飞出。这里没有直接只比较一行或一列，是为了让
        上、下、左、右四个方向都使用同一段清晰的逻辑。
        """
        row_step, col_step = DIRECTIONS[arrow.direction]
        row = arrow.row + row_step
        col = arrow.col + col_step

        occupied = {(item.row, item.col) for item in self.arrows if item != arrow}
        while 0 <= row < self.rows and 0 <= col < self.cols:
            if (row, col) in occupied:
                return False
            row += row_step
            col += col_step
        return True

    def remove(self, arrow):
        self.arrows.remove(arrow)


class ArrowGame:
    """Tkinter 图形界面与游戏流程。"""

    BOARD_X = 170
    BOARD_Y = 155
    CELL = 82

    def __init__(self, root):
        self.root = root
        self.root.title("一箭又一箭 - 基础版")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=760, height=650, bg="#f7f8fc", highlightthickness=0)
        self.canvas.pack()
        self.level_index = 0
        self.errors_left = 3
        self.board = None
        self.current_screen = "start"
        self.message = ""
        self.message_color = "#264653"
        self.canvas.bind("<Button-1>", self.on_click)
        self.show_start()

    def clear_screen(self):
        self.canvas.delete("all")

    def button(self, x1, y1, x2, y2, text, tag, color="#355cde"):
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags=(tag, "button"))
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, fill="white",
                                font=("Arial", 15, "bold"), tags=(tag, "button"))

    def show_start(self):
        self.current_screen = "start"
        self.clear_screen()
        self.canvas.create_rectangle(0, 0, 760, 650, fill="#eaf0ff", outline="")
        self.canvas.create_text(380, 165, text="一箭又一箭", fill="#294c9b",
                                font=("Arial", 38, "bold"))
        self.canvas.create_text(380, 220, text="观察方向，找出能飞出棋盘的箭头", fill="#526581",
                                font=("Arial", 16))
        self.canvas.create_text(380, 322, text="游戏规则", fill="#264653", font=("Arial", 18, "bold"))
        rules = "点击前方没有其他箭头的箭头，它会飞出棋盘。\n点击被阻挡的箭头会扣除一次失误机会。\n清空所有箭头即可进入下一关。"
        self.canvas.create_text(380, 390, text=rules, fill="#425466", font=("Arial", 15), justify="center")
        self.button(285, 480, 475, 535, "开始游戏", "start_game")
        self.canvas.create_text(380, 590, text="基础版 · 共 3 关 · Python Tkinter", fill="#75849a", font=("Arial", 12))

    def start_level(self, level_index):
        self.level_index = level_index
        self.errors_left = 3
        self.board = Board(LEVELS[level_index])
        self.current_screen = "game"
        self.message = "请选择一个箭头开始。"
        self.message_color = "#264653"
        self.draw_game()

    def draw_game(self):
        self.clear_screen()
        self.canvas.create_rectangle(0, 0, 760, 105, fill="#294c9b", outline="")
        self.canvas.create_text(65, 36, text="一箭又一箭", fill="white", font=("Arial", 18, "bold"))
        self.canvas.create_text(380, 35, text=f"第 {self.level_index + 1} 关 / {len(LEVELS)}", fill="white",
                                font=("Arial", 19, "bold"))
        self.canvas.create_text(628, 28, text=f"剩余箭头：{len(self.board.arrows)}", fill="#e8f0ff", font=("Arial", 13))
        self.canvas.create_text(628, 55, text=f"失误次数：{self.errors_left}", fill="#ffe5e5", font=("Arial", 13))

        self.canvas.create_text(380, 128, text="点击箭头试试看", fill="#425466", font=("Arial", 14))
        for row in range(5):
            for col in range(5):
                x1 = self.BOARD_X + col * self.CELL
                y1 = self.BOARD_Y + row * self.CELL
                self.canvas.create_rectangle(x1, y1, x1 + self.CELL, y1 + self.CELL,
                                             fill="#ffffff", outline="#cdd8ef", width=2)

        for arrow in self.board.arrows:
            self.draw_arrow(arrow)

        self.canvas.create_text(380, 595, text=self.message, fill=self.message_color, font=("Arial", 14, "bold"))
        self.button(55, 570, 145, 620, "重新开始", "restart", color="#e76f51")
        self.button(615, 570, 705, 620, "返回首页", "home", color="#6c7a89")

    def draw_arrow(self, arrow):
        x = self.BOARD_X + arrow.col * self.CELL + self.CELL / 2
        y = self.BOARD_Y + arrow.row * self.CELL + self.CELL / 2
        color = DIRECTION_COLOR[arrow.direction]
        # 使用字符箭头，四种方向的颜色不同，便于观察和测试。
        self.canvas.create_oval(x - 28, y - 28, x + 28, y + 28, fill="#f3f6ff", outline=color, width=3)
        self.canvas.create_text(x, y - 2, text=DIRECTION_TEXT[arrow.direction], fill=color,
                                font=("Arial", 36, "bold"), tags=("arrow",))

    def arrow_at(self, x, y):
        col = int((x - self.BOARD_X) // self.CELL)
        row = int((y - self.BOARD_Y) // self.CELL)
        for arrow in self.board.arrows:
            if arrow.row == row and arrow.col == col:
                return arrow
        return None

    def on_click(self, event):
        x, y = event.x, event.y
        if self.current_screen == "start":
            if 285 <= x <= 475 and 480 <= y <= 535:
                self.start_level(0)
            return

        if self.current_screen == "result":
            if 225 <= x <= 365 and 450 <= y <= 505:
                self.start_level(self.level_index)
            elif 395 <= x <= 535 and 450 <= y <= 505:
                if self.level_index < len(LEVELS) - 1:
                    self.start_level(self.level_index + 1)
                else:
                    self.show_start()
            elif 305 <= x <= 455 and 525 <= y <= 575:
                self.show_start()
            return

        if self.current_screen != "game":
            return
        if 55 <= x <= 145 and 570 <= y <= 620:
            self.start_level(self.level_index)
            return
        if 615 <= x <= 705 and 570 <= y <= 620:
            self.show_start()
            return

        arrow = self.arrow_at(x, y)
        if arrow is None:
            return
        if self.board.is_path_clear(arrow):
            self.board.remove(arrow)
            self.message = "路径畅通，箭头飞出棋盘！"
            self.message_color = "#218c74"
            self.draw_game()
            if not self.board.arrows:
                self.root.after(450, self.show_pass)
        else:
            self.errors_left -= 1
            self.message = "前方有箭头阻挡，扣除一次失误机会！"
            self.message_color = "#d1495b"
            self.draw_game()
            self.flash_board()
            if self.errors_left == 0:
                self.root.after(500, self.show_fail)

    def flash_board(self):
        """用红色边框提供一次简短、明显的碰撞反馈。"""
        rect = self.canvas.create_rectangle(160, 145, 590, 575, outline="#e63946", width=5, tags="feedback")
        self.root.after(260, lambda: self.canvas.delete(rect))

    def show_pass(self):
        self.show_result(True)

    def show_fail(self):
        self.show_result(False)

    def show_result(self, passed):
        self.current_screen = "result"
        self.clear_screen()
        background = "#e8f8f2" if passed else "#fff0f0"
        main_color = "#218c74" if passed else "#d1495b"
        title = "恭喜通关！" if passed else "本关失败"
        detail = "所有箭头都已飞出棋盘。" if passed else "失误次数已用完，可以重新挑战。"
        self.canvas.create_rectangle(0, 0, 760, 650, fill=background, outline="")
        self.canvas.create_text(380, 210, text="★" if passed else "!", fill=main_color, font=("Arial", 64, "bold"))
        self.canvas.create_text(380, 290, text=title, fill=main_color, font=("Arial", 34, "bold"))
        self.canvas.create_text(380, 338, text=detail, fill="#425466", font=("Arial", 16))
        self.button(225, 450, 365, 505, "重新开始", "restart_result", color="#6c7a89")
        next_text = "下一关" if self.level_index < len(LEVELS) - 1 else "回到首页"
        self.button(395, 450, 535, 505, next_text, "next", color="#355cde")
        self.button(305, 525, 455, 575, "返回首页", "home_result", color="#8d99ae")


if __name__ == "__main__":
    window = tk.Tk()
    ArrowGame(window)
    window.mainloop()
