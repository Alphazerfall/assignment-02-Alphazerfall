import sys
import pyglet
from pyglet import window
from audio import AudioInput


WINDOW_W, WINDOW_H = 1200, 600


class Game:
    def __init__(self):
        self.audio = AudioInput()
        self.label = pyglet.text.Label("-- Hz", font_size=48, x=WINDOW_W//2, y=WINDOW_H//2, anchor_x="center", anchor_y="center")
    
    def update(self, dt):
        pitch = self.audio.get_pitch()
        self.label.text = f"{pitch:.0f} Hz"
        pass

    def draw(self):
        self.label.draw()


if __name__ == "__main__":
    win = pyglet.window.Window(WINDOW_W, WINDOW_H, caption="Karaoke")
    game = Game()

    @win.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()
            sys.exit(0)
    
    @win.event
    def on_draw():
        win.clear()
        game.draw()

    pyglet.clock.schedule_interval(game.update, 1/60)  # update at 60 FPS
    with game.audio:
        pyglet.app.run()
