# --- Imports
# >>> PYGAME
import pygame as pg
import pygame_gui as pg_gui

# >>> SERIAL
import serial.tools.list_ports
import serial


# --- Variables
# <<< WINDOW
windowTitle = "Detector"

width = 500
height = 500

fps = 30

texts = ["Привет x"]
clicks = 0

ports = []

# <<< COLOR
colorBG = (248, 242, 220)
colorText = (43, 83, 32)


# --- Defs
def showText():
    for i in range(len(texts)):
        font = pg.font.SysFont(None, 20)
        showText = font.render(texts[i] + str(clicks), True, colorText)
        screen.blit(showText, (100*i, 100*i))

def getPorts():
    allPorts = list(serial.tools.list_ports.comports())

    for port in allPorts:
        print(f"Порт: {port.device}")
        print(f"Описание: {port.description}")
        print(f"Производитель: {port.manufacturer}\n")

        ports.append(port)

def setConnect():
    print("Connection")

    for port in ports:
        try:
            ser = serial.Serial(port.device, 9600)

            # READ
            data = ser.read(10)
            print(data)

            # WRITE
            ser.write(b'Hello, Arduino!')
            response = ser.readline()
            decoded_response = response.decode('utf-8')

            ser.close()
            print(decoded_response)
        except:
            print(f"Не получилось к {port.device} подключиться :(")


# --- Main
pg.init()
pg.mixer.init()
pg.display.set_caption(windowTitle)
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height))
manager = pg_gui.UIManager((width, height))

click = pg_gui.elements.UIButton(relative_rect=pg.Rect((width*.3, height*.6), (200, 70)),
                                 text="Click-pilick", manager=manager)
connect = pg_gui.elements.UIButton(relative_rect=pg.Rect((width*.3, height*.3), (200, 70)),
                                 text="Connect", manager=manager)

getPorts()

isRunning = True
while isRunning:
    screen.fill(colorBG)

    showText()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:  # Exit the program
               isRunning = False

        if event.type == pg_gui.UI_BUTTON_PRESSED:
            if event.ui_element == click:
                print("Click-pilick!!!")
                clicks += 1

            elif event.ui_element == connect:
                setConnect()

        manager.process_events(event)

    clock.tick(fps)
    time_delta = clock.tick(60) / 1000.0
    manager.update(time_delta)

    manager.draw_ui(screen)
    pg.display.flip()