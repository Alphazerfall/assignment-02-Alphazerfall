import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from audio import AudioInput

audio = AudioInput()

app = pg.mkQApp()
win = pg.GraphicsLayoutWidget(title="Audio Visualizer")

plot = win.addPlot()
plot.setYRange(-1, 1)
curve = plot.plot(pen='w')

win.nextRow()
pitch_label = pg.LabelItem("-- Hz", size="40pt", color="w")
win.addItem(pitch_label)
win.show()

def update():
    curve.setData(audio.buffer)
    pitch = audio.get_pitch()
    pitch_label.setText(f"{pitch:.0f} Hz")

timer = QTimer()
timer.timeout.connect(update)
timer.start(30)

with audio:
    pg.exec()