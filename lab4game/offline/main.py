from tkinter import *
import random


class PingPongCanvas(Canvas):
    """
    Класс игры
    """
    def __init__(self, parent, *args, **kwargs) -> None:
        Canvas.__init__(self, parent, *args, **kwargs)
        self.WINDOW_WIDTH = 900
        self.WINDOW_HEIGHT = 450

        self.PAD_WIDTH = 10
        self.PAD_HEIGHT = 100
        self.PAD_SPEED = 20
        self.pad1_speed = 0
        self.pad2_speed = 0

        self.BALL_RADIUS = 30

        self.BALL_SPEED_UP = 1.05
        self.BALL_MAX_SPEED = 40
        self.INITIAL_SPEED = 12
        self.ball_x_speed = self.INITIAL_SPEED
        self.ball_y_speed = self.INITIAL_SPEED

        self.player1_score = 0
        self.player2_score = 0

        self.right_line = self.WINDOW_WIDTH - self.PAD_WIDTH

        self.ball: int | None = None
        self.pad2: int | None = None
        self.pad1: int | None = None
        self.score1_text: int | None = None
        self.score2_text: int | None = None

        self._init_field()

    def _init_field(self) -> None:
        """
        Начальная отрисовка элементов на поле
        :return:
        """
        self.create_line(self.WINDOW_WIDTH / 2, 0, self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT, fill="white")
        self.ball = self.create_oval(self.WINDOW_WIDTH / 2 - self.BALL_RADIUS / 2,
                                     self.WINDOW_HEIGHT / 2 - self.BALL_RADIUS / 2,
                                     self.WINDOW_WIDTH / 2 + self.BALL_RADIUS / 2,
                                     self.WINDOW_HEIGHT / 2 + self.BALL_RADIUS / 2, fill="white")

        self.pad2 = self.create_line(self.PAD_WIDTH / 2,
                                     self.WINDOW_HEIGHT / 2 - self.PAD_HEIGHT / 2,
                                     self.PAD_WIDTH / 2,
                                     self.WINDOW_HEIGHT / 2 + self.PAD_HEIGHT / 2,
                                     width=self.PAD_WIDTH, fill="white")

        self.pad1 = self.create_line(self.WINDOW_WIDTH - self.PAD_WIDTH / 2,
                                     self.WINDOW_HEIGHT / 2 - self.PAD_HEIGHT / 2,
                                     self.WINDOW_WIDTH - self.PAD_WIDTH / 2,
                                     self.WINDOW_HEIGHT / 2 + self.PAD_HEIGHT / 2,
                                     width=self.PAD_WIDTH, fill="white")

        self.score1_text = self.create_text(self.WINDOW_WIDTH / 3, self.WINDOW_HEIGHT / 4,
                                            text=0,
                                            font=("", 16),
                                            fill="white")

        self.score2_text = self.create_text(self.WINDOW_WIDTH - self.WINDOW_WIDTH / 3, self.WINDOW_HEIGHT / 4,
                                            text=0,
                                            font=("", 16),
                                            fill="white")

    def update_score(self, player: str) -> None:
        """
        Изменяет счёт игроков
        :param player: Определяет какой игрок получает балл
        :return:
        """
        if player == "player1":
            self.player1_score += 1
            self.itemconfig(self.score1_text, text=self.player1_score)
        elif player == "player2":
            self.player2_score += 1
            self.itemconfig(self.score2_text, text=self.player2_score)

    def spawn_ball(self) -> None:
        """
        Перемещает мяч в центр поля и задаёт случайное направление по X
        :return:
        """
        self.coords(self.ball, self.WINDOW_WIDTH / 2 - self.BALL_RADIUS / 2,
                    self.WINDOW_HEIGHT / 2 - self.BALL_RADIUS / 2,
                    self.WINDOW_WIDTH / 2 + self.BALL_RADIUS / 2,
                    self.WINDOW_HEIGHT / 2 + self.BALL_RADIUS / 2)
        self.ball_x_speed = random.choice([1, -1])*self.INITIAL_SPEED

    def bounce(self, action) -> None:
        """
        Отскок мяча
        :param action: Определяет ось отскока
        :return:
        """
        if action == "bounceX":
            self.ball_y_speed = random.randrange(-10, 10)
            if abs(self.ball_x_speed) < self.BALL_MAX_SPEED:
                self.ball_x_speed *= -self.BALL_SPEED_UP
            else:
                self.ball_x_speed *= -1
        elif action == "bounceY":
            self.ball_y_speed = -self.ball_y_speed

    def move_ball(self) -> None:
        """
        Функция, задающая движение мяча
        :return:
        """
        # noinspection PyTupleAssignmentBalance
        ball_x1, ball_y1, ball_x2, ball_y2 = self.coords([self.ball])
        ball_center = (ball_y1 + ball_y2) / 2

        # Находится ли мяч в рамках игровой зоны
        if ball_x2 + self.ball_x_speed <= self.right_line and \
                ball_x1 + self.ball_x_speed >= self.PAD_WIDTH:
            self.move(self.ball, self.ball_x_speed, self.ball_y_speed)

        elif ball_x2 >= self.right_line or ball_x1 <= self.PAD_WIDTH:
            if ball_x2 > self.WINDOW_WIDTH / 2:
                # noinspection PyUnresolvedReferences
                if self.coords([self.pad1])[1] < ball_center < self.coords([self.pad1])[3]:
                    self.bounce("bounceX")
                else:
                    self.update_score("player1")
                    self.spawn_ball()
            else:
                # noinspection PyUnresolvedReferences
                if self.coords([self.pad2])[1] < ball_center < self.coords([self.pad2])[3]:
                    self.bounce("bounceX")
                else:
                    self.update_score("player2")
                    self.spawn_ball()
        else:
            self.move(self.ball, self.ball_x_speed, self.ball_y_speed)

        if ball_y1 + self.ball_y_speed < 0 or ball_y2 + self.ball_y_speed > self.WINDOW_HEIGHT:
            self.bounce("bounceY")

    def move_pads(self) -> None:
        """
        Движение ракеток
        :return:
        """
        pads = {self.pad2: self.pad1_speed,
                self.pad1: self.pad2_speed}
        for pad in pads:
            self.move(pad, 0, pads[pad])
            # noinspection PyUnresolvedReferences
            if self.coords([pad])[1] < 0:
                # noinspection PyUnresolvedReferences
                self.move([pad], 0, -self.coords([pad])[1])
            elif self.coords([pad])[3] > self.WINDOW_HEIGHT:
                # noinspection PyUnresolvedReferences
                self.move([pad], 0, self.WINDOW_HEIGHT - self.coords([pad])[3])

    def start(self) -> None:
        """
        Основной цикл игры
        :return:
        """
        self.move_ball()
        self.move_pads()
        root.after(30, self.start)

    def movement_handler(self, event: Event) -> None:
        """
        Кнопки для перемещения ракеток
        :param event:
        :return:
        """
        if event.keysym == "w":
            self.pad1_speed = -self.PAD_SPEED
        elif event.keysym == "s":
            self.pad1_speed = self.PAD_SPEED
        elif event.keysym == "Up":
            self.pad2_speed = -self.PAD_SPEED
        elif event.keysym == "Down":
            self.pad2_speed = self.PAD_SPEED

    def stop_pad(self, event: Event) -> None:
        if event.keysym in ("w", "s"):
            self.pad1_speed = 0
        elif event.keysym in ("Up", "Down"):
            self.pad2_speed = 0


root = Tk()
root.title("Ping-Pong")

game = PingPongCanvas(root, width=900, height=450, background="#424242")
game.pack()
game.focus_set()

game.bind("<KeyPress>", game.movement_handler)
game.bind("<KeyRelease>", game.stop_pad)

game.start()

root.mainloop()
