#define ECHO_PIN = 2;  // attach pin D2 Arduino to pin Echo of HC-SR04
#define TRIG_PIN = 3;  // attach pin D3 Arduino to pin Trig of HC-SR04

int read_ultrasonic(float grid_size, int boundary) {

    long duration;          // Variable to store time taken for the pulse to reach the receiver
    double distance;        // Variable to store distance calculated using a formula
    int number_of_grids = 0; // Number of grids calculated based on distance

    pinMode(TRIG_PIN, OUTPUT); // Sets the TRIG_PIN as an OUTPUT
    pinMode(ECHO_PIN, INPUT);  // Sets the ECHO_PIN as an INPUT

    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);

    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);

    digitalWrite(TRIG_PIN, LOW);

    duration = pulseIn(ECHO_PIN, HIGH);
    distance = duration * 0.0344 / 2;

    // Cast the distance to an integer to get the number of grids
    number_of_grids = static_cast<int>(distance / grid_size);

    // Ensure the number of grids is within the specified boundary
    if (number_of_grids > boundary) {
        number_of_grids = boundary;
    }

    return number_of_grids;
}

void setup() {
    Serial.begin(9600); // Start serial communication with a baud rate of 9600
    delay(500);         // Wait for 500 milliseconds
}

void loop() {
    // Example usage
    float grid_size = 50.0; // Example grid size in centimeters
    int boundary = 10;      // Example boundary for the number of grids

    int result = read_ultrasonic(grid_size, boundary);

    // Send data to Raspberry Pi or display as needed
    Serial.print("Number of Grids: ");
    Serial.println(result);

    delay(1000); // Delay before the next reading
}
