import serial
import curses

from errors import QuitError

class Controller(object):
  def __init__(self):
    super().__init__()
    self.arduino = serial.Serial('/dev/ttyUSB0', 9600) 
    self.screen = curses.initscr()

    self.__mapping = False

    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

  def start_mapping(self):
    self.__mapping = True

  def stop_mapping(self):
    self.__mapping = False
  
  def getch(self) -> str:
    return self.screen.getch()

  def recv(self) -> str:
    line = self.arduino.readline().decode('utf-8').strip()
    return line

  def send(self,char:str) -> None:
    if char == ord('q'):
      raise QuitError("bye bye")
    elif char == curses.KEY_UP:
      self.arduino.write(b'F') 
    elif char == curses.KEY_DOWN:
      self.arduino.write(b'B')
    elif char == curses.KEY_LEFT:
      self.arduino.write(b'L')
    elif char == curses.KEY_RIGHT:
      self.arduino.write(b'R')
    elif char == ord(' '):
      self.arduino.write(b'S')
    elif char == ord('m'):
      self.arduino.write(b'm')
      resp = self.recv()
      self.map(int(resp))
    else:
      self.arduino.write(byte(char))

  def display_options(self):
    print(f"""{'='*40} CONTROLS {'='*40}
KEY_UP   : to move forward
KEY_DOWN : to move down
KEY_RIGHT: to move right
KEY_LEFT : to move left

U        : to read data

{'='*40}  INPUTS  {'='*40}
F : forward
B : back
L : left
R : right
S : stop
U : read
          """)

  def close(self):
    curses.nobreak()
    self.screen.keypad(False)
    curses.echo()
    curses.endwin()
    self.arduino.close()


  def event_loop(self):
    self.display_options()
    while True:
      char = self.getch()
      self.send(char)

if __name__ == "__main__":
  cont = Controller()
  cont.event_loop()

  try:
    cont.event_loop()
  finally:
    cont.close()
