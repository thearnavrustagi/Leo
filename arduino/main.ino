const int pinleft1 = 5;
const int pinleft2 = 6;
const int pinright1 = 9;
const int pinright2 = 10;
const int echoPin = 2;
const int trigPin = 3;

char fromPi;

// Function to read the ultrasonic sensor and calculate the number of grids
int read_ultrasonic(float grid_size, int boundary, int no_of_samples) {
  long duration;
  double distance;
  int number_of_grids = 0;

  pinMode(echoPin, INPUT);
  pinMode(trigPin, OUTPUT);

  int grids_arr[no_of_samples];

  for (int i = 0; i < no_of_samples; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);

    digitalWrite(trigPin, LOW);

    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.0344 / 2;
    delay(10);
    number_of_grids = static_cast < int > (round(distance / grid_size));

    if (number_of_grids > boundary) {
      number_of_grids = boundary;
    }

    grids_arr[i] = number_of_grids;
  }

  int maxvalue = 0;
  int maxcount = 0;

  for (int i = 0; i < no_of_samples; ++i) {
    int count = 0;

    for (int j = 0; j < no_of_samples; ++j) {
      if (grids_arr[j] == grids_arr[i])
        count++;
    }

    if (count > maxcount) {
      maxcount = count;
      maxvalue = grids_arr[i];
    }
  }

  return maxvalue;
}

void setup() {
  Serial.begin(9600); // Start serial communication with a baud rate of 9600
  pinMode(pinleft1, OUTPUT);
  pinMode(pinleft2, OUTPUT);
  pinMode(pinright1, OUTPUT);
  pinMode(pinright2, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Example usage
  if (Serial.available() > 0) {
    fromPi = Serial.read();

    if (fromPi == 'F') {
      forward();
    } else if (fromPi == 'B') {
      backward();
    } else if (fromPi == 'R') {
      right();
    } else if (fromPi == 'L') {
      left();
    } else if (fromPi == 'S') {
      stop();
    } else if (fromPi == 'W') {
      manualforward();
    } else if (fromPi == 'A') {
      manualleft();
    } else if (fromPi == 'D') {
      manualright();
    } else if (fromPi == 'p') {
      char instruction;
      do {
        instruction = Serial.read();
        if (instruction == 'F') {
          forward();
        } else if (instruction == 'B') {
          backward();
        } else if (instruction == 'R') {
          right();
        } else if (instruction == 'L') {
          left();
        }
      } while (instruction != 'P');
    } else if (fromPi == 'M') {
      float grid_size = 50; // Example grid size in centimeters
      int boundary = 4;
      int samples = 20;
      int result = read_ultrasonic(grid_size, boundary, samples);

      // Send data to Raspberry Pi or display as needed
      Serial.print("Number of Grids: ");
      Serial.println(result);
      Serial.flush();
    } else {
      stop();
    }
  }
}

void right() { //turnRight
  analogWrite(pinright1, 255);
  analogWrite(pinright2, 0);
  analogWrite(pinleft1, 175);
  analogWrite(pinleft2, 0);
  delay(980);
  stop();
}

void left() { //turnLeft

  analogWrite(pinright1, 0);

  analogWrite(pinright2, 255);

  analogWrite(pinleft1, 0);

  analogWrite(pinleft2, 175);

  delay(1063);

  stop();

}

void stop() { // stop
  analogWrite(pinright1, 0);
  analogWrite(pinright2, 0);
  analogWrite(pinleft1, 0);
  analogWrite(pinleft2, 0);
}

void backward() { // backward
  right();
  delay(100);
  right();
  delay(100);
  forward();
}

void forward() { // forward
  analogWrite(pinright1, 0);
  analogWrite(pinright2, 255);
  analogWrite(pinleft1, 176);
  analogWrite(pinleft2, 0);
  delay(3500);
  stop();
}

void manualright() { //fine tune right
  analogWrite(pinright1, 255);
  analogWrite(pinright2, 0);
  analogWrite(pinleft1, 175);
  analogWrite(pinleft2, 0);
}

void manualleft() { //fine tune left
  analogWrite(pinright1, 0);
  analogWrite(pinright2, 255);
  analogWrite(pinleft1, 0);
  analogWrite(pinleft2, 175);
}

void manualforward() { // manually forward
  analogWrite(pinright1, 0);
  analogWrite(pinright2, 255);
  analogWrite(pinleft1, 176);
  analogWrite(pinleft2, 0);
}
