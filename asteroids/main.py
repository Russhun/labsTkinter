import random
from tkinter import *
from PIL import ImageTk, Image


class Asteroid:
    def __init__(self, asteroid_id, asteroid_size, spawn_x):
        self.WINDOW_WIDTH = 600
        self.WINDOW_HEIGHT = 500

        self.asteroid_id = asteroid_id
        self.size = asteroid_size
        self.BASE_SPEED_Y = {
            "1": 2,
            "2": 4,
            "3": 4,
            "4": 5,
            "5": 8
        }[str(self.size)]
        self.BASE_SPEED_X = {
            "1": random.randint(1, 2),
            "2": random.randint(2, 4),
            "3": random.randint(3, 5),
            "4": random.randint(5, 6),
            "5": random.randint(5, 10)
        }[str(self.size)]
        self.speed_x = 0
        self.speed_y = self.BASE_SPEED_Y

        if spawn_x < 50:
            self.speed_x = self.BASE_SPEED_X
        elif spawn_x > 450:
            self.speed_x = -self.BASE_SPEED_X
        else:
            self.speed_x *= random.choice([-1, 1])


class AsteroidCanvas(Canvas):
    def __init__(self, parent, *args, **kwargs) -> None:
        Canvas.__init__(self, parent, *args, **kwargs)

        self.WINDOW_WIDTH = 600
        self.WINDOW_HEIGHT = 500

        self.SPACESHIP_WIDTH = 40
        self.SPACESHIP_HEIGHT = 70
        self.SPACESHIP_DEFAULT_SPEED = 5
        self.spaceship_x_speed = 0
        self.spaceship_y_speed = 0
        self.spaceship_health = 50

        self.score = 0

        self.asteroids = []
        self.explosions = []
        self.ASTEROID_SIZE = 192
        self.EXPLOSION_SIZE_WIDTH = 199
        self.EXPLOSION_SIZE_HEIGHT = 170

        self.back_pil_image = Image.open("background.jpg").resize((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.back_image = ImageTk.PhotoImage(self.back_pil_image)
        self.player_pil_image = Image.open("player.png").resize((self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT))
        self.player_image = ImageTk.PhotoImage(self.player_pil_image)

        self.explosion_pil_images = [Image.open("explosion.png").resize((int(self.EXPLOSION_SIZE_WIDTH/i),
                                                                         int(self.EXPLOSION_SIZE_HEIGHT/i))) for i in range(1, 7)]
        self.explosion_images_list = [ImageTk.PhotoImage(i) for i in self.explosion_pil_images]

        self.asteroids_pil_list = [Image.open("asteroid.png").resize((int(self.ASTEROID_SIZE/i),
                                                                  int(self.ASTEROID_SIZE/i))) for i in range(1, 7)]
        self.asteroid_image_list = [ImageTk.PhotoImage(i) for i in self.asteroids_pil_list]

        self.create_image(300, 250, image=self.back_image)
        self.spaceship = self.create_image(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT-self.SPACESHIP_HEIGHT/2,
                                           image=self.player_image)

        self.health_label = self.create_text(50, 50, font=("", 14), text=f"HP: {self.spaceship_health}", fill="white")

        self.enter = self.create_text(300, 300, font=("", 36, "bold"), text=f"PRESS ENTER TO PLAY", fill="green")

    def spawn_asteroid(self, size):
        asteroid_spawn_x = random.randint(-40, self.WINDOW_WIDTH+40)
        asteroid_spawn_y = -100
        self.asteroids.append(Asteroid(self.create_image(asteroid_spawn_x, asteroid_spawn_y, image=self.asteroid_image_list[size]),
                                       size, asteroid_spawn_x))

    def move_asteroids(self) -> None:
        if len(self.asteroids) < 15:
            asteroid_chance = random.randint(0, 100)
            if 40 < asteroid_chance < 50:
                self.spawn_asteroid(1)
            elif 50 < asteroid_chance < 65:
                self.spawn_asteroid(2)
            elif 65 < asteroid_chance < 75:
                self.spawn_asteroid(3)
            elif 75 < asteroid_chance < 85:
                self.spawn_asteroid(4)
            elif 85 < asteroid_chance < 100:
                self.spawn_asteroid(5)
        for i, asteroid in enumerate(self.asteroids):
            asteroid_x, asteroid_y = self.coords(asteroid.asteroid_id)
            if asteroid_y > self.WINDOW_HEIGHT:
                self.asteroids.pop(i)
                self.delete(asteroid.asteroid_id)
                self.score += asteroid.size
            else:
                self.move(asteroid.asteroid_id, asteroid.speed_x, asteroid.speed_y)

    def move_ship(self) -> None:
        self.move(self.spaceship, self.spaceship_x_speed, self.spaceship_y_speed)
        spaceship_x, spaceship_y = self.coords(self.spaceship)
        if spaceship_x > self.WINDOW_WIDTH:
            self.coords(self.spaceship, 0, spaceship_y)
        elif spaceship_x < 0:
            self.coords(self.spaceship, self.WINDOW_WIDTH, spaceship_y)
        if spaceship_y > self.WINDOW_HEIGHT:
            self.coords(self.spaceship, spaceship_x, 0)
        elif spaceship_y < 0:
            self.coords(self.spaceship, spaceship_x, self.WINDOW_HEIGHT)
        for i, asteroid in enumerate(self.asteroids):
            asteroid_x, asteroid_y = self.coords(asteroid.asteroid_id)
            asteroid_size = asteroid.size
            size_m = {
                "1": 50,
                "2": 20,
                "3": 13,
                "4": 11,
                "5": 10
            }[str(asteroid_size)]
            x1 = asteroid_x - (self.ASTEROID_SIZE / asteroid_size) / 2 + size_m
            y1 = asteroid_y - (self.ASTEROID_SIZE / asteroid_size) / 2 + size_m
            x2 = asteroid_x + (self.ASTEROID_SIZE / asteroid_size) / 2 - size_m
            y2 = asteroid_y + (self.ASTEROID_SIZE / asteroid_size) / 2 - size_m
            explosion = False
            if (x2 > spaceship_x+self.SPACESHIP_WIDTH/2 > x1) and (y1 < spaceship_y < y2):
                explosion = True
            elif (x2 > spaceship_x-self.SPACESHIP_WIDTH/2 > x1) and (y1 < spaceship_y < y2):
                explosion = True
            elif (y2 > spaceship_y+self.SPACESHIP_HEIGHT/2 > y1) and (x1 < spaceship_x < x2):
                explosion = True
            elif (y2 > spaceship_y-self.SPACESHIP_HEIGHT/2 > y1) and (x1 < spaceship_x < x2):
                explosion = True

            if explosion:
                self.itemconfig(asteroid.asteroid_id, image=self.explosion_images_list[asteroid_size])
                self.spaceship_health -= 6 - asteroid_size
                self.itemconfig(self.health_label, text=f"HP: {self.spaceship_health}")
                self.asteroids.pop(i)
                self.explosions.append(asteroid.asteroid_id)
                self.after(500, self.delete_explosions)

    def delete_explosions(self):
        for explosion in self.explosions:
            self.delete(explosion)

    def movement_handler(self, event: Event) -> None:
        if event.keysym not in history:
            history.append(event.keysym)
        if "space" in history:
            self.SPACESHIP_DEFAULT_SPEED = 10
        if "w" in history:
            self.spaceship_y_speed = -self.SPACESHIP_DEFAULT_SPEED
        elif "s" in history:
            self.spaceship_y_speed = self.SPACESHIP_DEFAULT_SPEED
        if "a" in history:
            self.spaceship_x_speed = -self.SPACESHIP_DEFAULT_SPEED
        elif "d" in history:
            self.spaceship_x_speed = self.SPACESHIP_DEFAULT_SPEED

    def stop_movement(self, event: Event) -> None:
        if event.keysym in history:
            history.pop(history.index(event.keysym))

        if "w" not in history and "s" not in history:
            self.spaceship_y_speed = 0
        if "a" not in history and "d" not in history:
            self.spaceship_x_speed = 0
        if "space" not in history:
            self.SPACESHIP_DEFAULT_SPEED = 5

    def start(self) -> None:
        if self.spaceship_health > 0:
            self.move_asteroids()
            self.move_ship()
            root.after(30, self.start)
        else:
            self.create_text(300, 300, font=("", 64, "bold"), text=f"GAME OVER\n SCORE:{self.score}", fill="red")


def pre_start(event: Event) -> None:
    game.delete(game.enter)
    game.bind("<KeyPress>", game.movement_handler)
    game.bind("<KeyRelease>", game.stop_movement)
    game.unbind("<Enter>", bind_enter_id)
    game.start()


root = Tk()
root.title("Asteroids")
root.geometry("600x500")
history = []

game = AsteroidCanvas(root, width=600, height=500)
game.pack(expand=True, fill="both")
game.focus_set()


bind_enter_id = game.bind("<Return>", pre_start)

root.mainloop()