import serial
import curses
from time import sleep

from errors import QuitError
from constants import P_FREE, P_OCC, MAP_SIZE, L2R
from constants import FWD, RGT, BWD, LFT, STATES, INITIAL_POSN
from mapping import Mapping

class Controller(object):
  def __init__(
          self,
          initial_position=INITIAL_POSN,
          initial_state=INITIAL_STATE,
          map_args=(MAP_SIZE,L2R,1)):
    super().__init__()
    self.arduino = serial.Serial('/dev/ttyUSB0', 9600) 
    self.screen = curses.initscr()
    self.inital_position = initial_position
    self.initial_state = initial_state

    self.position = initial_position
    self.state = initial_state

    self.mapping = Mapping(*map_args)

    curses.noecho()
    curses.cbreak()
    self.screen.keypad(True)

  def getch(self) -> str:
    return self.screen.getch()

  def recv(self) -> str:
    line = self.arduino.readline().decode('utf-8').strip()
    return line

  def send(self,char:str) -> None:
    if char == ord('q'):
      raise QuitError("bye bye")
    elif char == curses.KEY_UP:
      self.forward()
    elif char == curses.KEY_DOWN:
      self.backward()
    elif char == curses.KEY_LEFT:
      self.left()
    elif char == curses.KEY_RIGHT:
      self.right()
    elif char == ord(' '):
      self.write('S')
    elif char == ord('m') or char == ord("M"):
      self.write('M')
      resp = str(self.recv()).split(":")
      self.write(b'S')
      print(f"recv : {int(resp[1])}")
      i = int(resp[1])
      self.update_map(i)
    else:
      self.write(bytes(char.upper()))
  
  def write(self,c):
      print("sending",c)
      self.arduino.write(bytes(c))

  def forward(self) -> None:
      self.position = tuple(map(lambda a,b: a+b, self.position,self.state))
      self.write('F')

  def backward(self) -> None:
      self.position = tuple(map(lambda a,b: a-b, self.position,self.state))
      self.write('B')

  def right(self) -> None:
      self.state = STATES[(self.position.index(self.state)+1)%len(self.position)]
      self.write('R')

  def left(self) -> None:
      rpos = self.position
      self.state = STATES[(rpos.index(self.state)-1)%len(rpos)]
      self.write('L')

  def create_map(self, grids):
      probabilities = [P_FREE]*grids + [P_OCC]
      def fnc (g,a,b): 
        return (a[0]+g*b[0],a[1]+g*b[1])

      positions = tuple(map(fnc, range(1,grids+2), self.position,self.state))

      print(f"probabilities : {probabilities}, {positions}")
      self.mapping.update_log_odds(positions, probabilities)

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
