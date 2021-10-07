from adafruit_circuitplayground import cp
import audiocore
import audioio
import board
import array
import time
import math
import digitalio
from audiocore import RawSample
from audioio import AudioOut


spkrenable = cp._speaker_enable
spkrenable.direction = digitalio.Direction.OUTPUT
spkrenable.value = True
audio = AudioOut(board.SPEAKER)

cp.pixels.brightness = 0.03
grav = 9.8
tone_volume = 0  # Increase this to increase the volume of the tone.
frequency = 300  # Set this to the Hz of the tone you want to generate.
length = 8000 // frequency
sine_wave = array.array("H", [0] * length)

while True:
    x, y, z = cp.acceleration
    r = int(abs(x / grav * 127))
    g = int(abs(y / grav * 127))
    b = int(abs(z / grav * 127))
    cp.pixels.fill([r, g, b])
    theta = ((math.acos((z) / math.sqrt(x**2 + y**2 + z**2))) / math.pi * 180)
    azimuthal = ((math.acos((x) / math.sqrt(x**2 + y**2 + z**2))) / math.pi * 180)
    time.sleep(0.05)
    if int(abs(theta * 100)) in range(8950, 9050, 1):
        if int(abs(azimuthal *100)) in range(1650,1800, 1):
            cp.pixels.fill([127, 127, 127])
            time.sleep(0.25)
        for i in range(length):
            sine_wave[i] = int((1 + math.sin(math.pi * 2 * i / length)) * tone_volume * (2 ** 15 - 1))
            sine_wave_sample = audiocore.RawSample(sine_wave)
            audio.play(sine_wave_sample, loop=True)
            time.sleep(0.1)
            audio.stop()
            break
    if cp.button_a:
        print((theta, azimuthal))
