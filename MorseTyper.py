import time
import threading
import sys
from pynput import keyboard
import pystray
from PIL import Image, ImageDraw
import winsound

# Morse code dictionary
MORSE_CODE = {
    'a': ".-", 'b': "-...", 'c': "-.-.", 'd': "-..",
    'e': ".", 'f': "..-.", 'g': "--.", 'h': "....",
    'i': "..", 'j': ".---", 'k': "-.-", 'l': ".-..",
    'm': "--", 'n': "-.", 'o': "---", 'p': ".--.",
    'q': "--.-", 'r': ".-.", 's': "...", 't': "-",
    'u': "..-", 'v': "...-", 'w': ".--", 'x': "-..-",
    'y': "-.--", 'z': "--.."
}

DOT = 100   # milliseconds
DASH = DOT * 3
GAP = DOT / 2
LETTER_GAP = DOT * 3

muted = False

def play_morse(char):
    global muted
    if muted:
        return
    code = MORSE_CODE.get(char.lower())
    if not code:
        return
    for symbol in code:
        if symbol == ".":
            winsound.Beep(800, DOT)
        elif symbol == "-":
            winsound.Beep(800, DASH)
        time.sleep(GAP / 1000)
    time.sleep(LETTER_GAP / 1000)

def on_press(key):
    try:
        if key.char.isalpha():
            play_morse(key.char)
    except AttributeError:
        pass

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def create_image(color="green"):
    img = Image.new("RGB", (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([16, 28, 48, 36], fill=color)
    return img

def toggle_mute(icon, item):
    global muted
    muted = not muted
    icon.icon = create_image("red" if muted else "green")
    icon.update_menu()

def on_exit(icon, item):
    icon.stop()
    sys.exit(0)

def main():
    t = threading.Thread(target=start_listener, daemon=True)
    t.start()

    icon = pystray.Icon("MorseKeyboard")
    icon.icon = create_image("green")
    icon.title = "Morse Code Keyboard"
    icon.menu = pystray.Menu(
        pystray.MenuItem("Mute/Unmute", toggle_mute, default=True),
        pystray.MenuItem("Exit", on_exit)
    )
    icon.run()

if __name__ == "__main__":
    main()
