import serial
import curses
from time import sleep

from errors import QuitError
from constants import P_FREE, P_OCC, MAP_SIZE, L2R, T2B
from constants import FWD, RGT, BWD, LFT, STATES, INITIAL_POSN, INITIAL_STATE
from mapping import Mapping

class Controller(object):
  def __init__(
          self,
          initial_position=INITIAL_POSN,
          initial_state=INITIAL_STATE,
          map_args=(MAP_SIZE,T2B,1)):
    super().__init__()
    self.arduino = serial.Serial('/dev/ttyUSB0', 9600) 
    self.screen = curses.initscr()
    self.inital_position = initial_position
    self.initial_state = initial_state

    self.position = initial_position
    self.state = initial_state

    self.mapping = Mapping(*map_args)
    self.controls = [
            (ord("w"),b"W"),
            (ord("a"),b"A"),
            (ord("d"),b"D"),
            ]

    curses.noecho()
    curses.cbreak()
    self.screen.keypad(True)

  def getch(self) -> str:
    return self.screen.getch()

  def recv(self) -> str:
    line = self.arduino.readline().decode('utf-8').strip()
    open("out.txt","a").write(line)
    return line

  def send(self,char) -> None:
    print("initial state :", self.state, "initial posn :", self.position)
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
      self.write(b'S')
    elif char == ord('m') or char == ord("M"):
      self.write(b'M')
      resp = str(self.recv()).split(":")
      self.write(b'S')
      print(f"recv : {resp}")
      i = int(resp[1])
      self.update_map(i)
    elif char == ord('e') or char == ord('E'):
        self.export_map()
    elif char in (ord('p'), ord('P')):
        self.path_plan()
    else:
        for i,x in self.controls:
            if i == char:
                self.write(x)
    print("final state :", self.state, "final posn :", self.position)
  
  def write(self,c):
      print("sending",c)
      self.arduino.write((c))

  def forward(self) -> None:
      self.position = tuple(map(lambda a,b: a+b, self.position,self.state))
      self.write(b'F')

  def backward(self) -> None:
      self.position = tuple(map(lambda a,b: a-b, self.position,self.state))
      self.state = STATES[(STATES.index(self.state)+2)%len(STATES)]
      self.write(b'B')

  def right(self) -> None:
      self.state = STATES[(STATES.index(self.state)+1)%len(STATES)]
      self.write(b'R')

  def left(self) -> None:
      rpos = STATES[::-1]
      self.state = rpos[(rpos.index(self.state)+1)%len(rpos)]
      self.write(b'L')

  def update_map(self, grids):
      probabilities = [P_FREE]*grids + [P_OCC]
      def fnc (g,a,b): 
        return (a[0]+g*b[0],a[1]+g*b[1])

      g,a,b = range(1,grids+2), self.position,self.state
      positions = list(map(fnc, g,[a]*(grids+2),[b]*(grids+2)))

      self.mapping.update_log_odds(positions, probabilities)

  def export_map(self):
      self.mapping.export(self.position, self.state)

  def path_plan(self):
      start = self.get_int("give start point")
      start_pose = self.get_int("give start pose")
      end = self.get_int("give end point")
      end_pose = self.get_int("give end pose")

      self.goto(start, start_pose)
      sleep(10)
      self.goto(end, end_pose)

  def goto(self, end, end_pose):
      end = self.mapping.idx_to_posn(end, self.mapping.grid_size)
      print("end", end)
      print(f" end : {end}")
      for instruction in self.get_path(end):
          print(instruction)
          match instruction:
              case 'F':
                  self.forward()
              case 'R':
                  self.right()
              case 'L':
                  self.left()
              case 'B':
                  self.backward()
          sleep(5)
      print("I AM AT SOME POSE WHICH IS COOL")
      while self.state != STATES[end_pose]:
          self.right()

      
  def get_path(self, end_posn):
      y_dist = end_posn[1] - self.position[1]
      x_dist = end_posn[0] - self.position[0]
      while self.position != end_posn:
          if self.position[1] != end_posn[1]:
              if self.state == STATES[FWD]:
                  yield 'F' if y_dist > 0 else 'B'
              if self.state == STATES[BWD]:
                  yield 'F' if y_dist < 0 else 'B'
              if self.state == STATES[LFT]:
                  yield 'R'
              if self.state == STATES[RGT]:
                  yield 'L'
          else:
              if self.state ==  STATES[FWD]:
                  yield 'R'
              if self.state == STATES[BWD]:
                  yield 'L'
              if self.state == STATES[LFT]:
                  yield 'F' if x_dist < 0 else 'B'
              if self.state ==  STATES[RGT]:
                  yield 'F' if x_dist > 0 else 'B'

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

  def get_int(self,prompt):
    print(prompt)
    ch, out = '', ''
    while ch != '\n':
        ch = chr(self.screen.getch())
        out += ch
    return int(out)

if __name__ == "__main__":
  cont = Controller()
  try:
    cont.event_loop()
  finally:
    cont.close()
