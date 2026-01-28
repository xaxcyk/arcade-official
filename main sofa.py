import arcade
import time
from game import GameView
from data_manager import DataManager

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Сокровища Чёрного храма"


class MenuView(arcade.View): #главное окно
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.sound_player = None

        self.logo_list = arcade.SpriteList()
        try:
            self.logo_sprite = arcade.Sprite("assets/sprites/nazaglavku.jpg")
            target_height = 360
            self.logo_sprite.scale = target_height / self.logo_sprite.height
            self.logo_sprite.center_x = SCREEN_WIDTH / 2
            self.logo_sprite.center_y = SCREEN_HEIGHT / 2 - 47
            self.logo_list.append(self.logo_sprite)
        except Exception:
            pass

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

        try:
            self.sound = arcade.load_sound("assets/sounds/scary_sound.wav")
            self.sound_player = self.sound.play(volume=0.3, loop=True)
        except Exception:
            pass

    def on_hide_view(self):
        if self.sound_player:
            try:
                self.sound_player.pause()
            except AttributeError:
                pass

    def on_draw(self):
        self.clear()

        arcade.draw_text("Сокровища", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200,
                         (250, 137, 137), font_size=30, anchor_x="center")
        arcade.draw_text("Чёрного храма", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150,
                         arcade.color.DARK_RED, font_size=50, anchor_x="center", bold=True)

        if self.logo_list:
            self.logo_list.draw()

        best_sessions = self.data_manager.get_best_full_sessions(3)

        arcade.draw_text("Нажмите ENTER для старта", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("S - Полная статистика   |   ESC - Выход", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 280,
                         arcade.color.GRAY, font_size=18, anchor_x="center")

    def on_key_press(self, key, modifiers): #нажатия клавиш в главном меню
        if key == arcade.key.ENTER:
            if self.sound_player:
                try:
                    self.sound_player.pause()
                except:
                    pass
            self.data_manager.start_session()
            game_view = GameView(level_num=1, data_manager=self.data_manager)
            self.window.show_view(game_view)
        elif key == arcade.key.S:
            if self.sound_player:
                try:
                    self.sound_player.pause()
                except:
                    pass
            stats_view = StatisticsView(self.data_manager)
            self.window.show_view(stats_view)
        elif key == arcade.key.ESCAPE:
            self.window.close()