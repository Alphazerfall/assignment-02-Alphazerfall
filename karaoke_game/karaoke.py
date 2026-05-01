import pyglet
from audio import AudioInput

audio = AudioInput()
window = pyglet.window.Window(400, 200, caption="Karaoke")

label = pyglet.text.Label("-- Hz", font_size=48, x=200, y=100, anchor_x="center", anchor_y="center")

@window.event
def on_draw():
    window.clear()
    label.draw()

def update(dt):
    pitch = audio.get_pitch()
    label.text = f"{pitch:.0f} Hz"

pyglet.clock.schedule_interval(update, 1/30)

with audio:
    pyglet.app.run()
