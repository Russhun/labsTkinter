from lab4game.server.models.abstr import AbstractGameField


class QueueRepository:
    def __init__(self):
        self.db = {}

    def get_users_by_lobby_id(self, lobby_id: str):
        pass

    def add_user_id_to_lobby(self, lobby_id: str, user_id: str):
        pass

    def add_lobby_id(self, lobby_id: str, user_id: str):
        pass


class GameRepository:
    def __init__(self):
        self.db = {}

    def add_game_field(self, field_id: str, game_field: AbstractGameField):
        self.db[field_id] = game_field

    def get_game_field(self, field_id: str) -> AbstractGameField | None:
        if field_id in self.db:
            return self.db[field_id]
        return None
