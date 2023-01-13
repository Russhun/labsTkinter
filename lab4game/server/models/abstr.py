
class AbstractGameField:
    field_id: str
    player1_id: str
    player2_id: str
    ball_coords: list[int, int, int, int]
    score: list[int, int]
    pad1_coords: list[int, int]
    pad2_coords: list[int, int]
    pads_speed: float
    ball_speed: list[int, int]
    start: callable
    pad1_movement_is_up: bool | None
