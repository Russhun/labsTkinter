from lab4game.server.models.abstr import AbstractGameField


class GameField(AbstractGameField):
    def __init__(self, field_id: str, player1_id: str, player2_id: str):
        self.field_id = field_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.ball_coords = [365, 215, 385, 235]
        self.score = [0, 0]
        self.pad1_coords = [15, 185]
        self.pad2_coords = [725, 185]
        self.pads_speed = 0.02
        self.ball_speed = [0, 0]
