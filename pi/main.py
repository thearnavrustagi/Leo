import serial
import curses
from time import sleep

from errors import QuitError
from constants import P_FREE, P_OCC, MAP_SIZE, L2R
from mapping import Mapping

class Controller(object):
  def __init__(
          self,
          map_specification:str="map_spec.txt"):
    super().__init__()
    self.arduino = serial.Serial('/dev/ttyUSB0', 9600) 
    self.screen = curses.initscr()

    self.mapping = Mapping(MAP_SIZE, L2R, 1)

    curses.noecho()
    curses.cbreak()
    self.screen.keypad(True)

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
      print("sending F")
      self.arduino.write(b'F') 
    elif char == curses.KEY_DOWN:
      print("sending B")
      self.arduino.write(b'B')
    elif char == curses.KEY_LEFT:
      print("sending L")
      self.arduino.write(b'L')
    elif char == curses.KEY_RIGHT:
      print("sending R")
      self.arduino.write(b'R')
    elif char == ord(' '):
      print("sending S")
      self.arduino.write(b'S')
    elif char == ord('m') or char == ord("M"):
      print("sending M")
      self.arduino.write(b'M')
      resp = str(self.recv()).split(":")
      self.arduino.write(b'S')
      print(f"recv : {int(resp[1])}")
      i = int(resp[1])
      self.create_map(i)
    else:
      self.arduino.write(bytes(char))
  
  def create_map(self, grids):
      probabilities = [P_FREE]*grids + [P_OCC]
      print(probabilities)
      #probabilities = (probabilities)

      print(f"probabilities : {probabilities}")


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
    curses.nocbreak()
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
  try:
    cont.event_loop()
  finally:
    cont.close()
