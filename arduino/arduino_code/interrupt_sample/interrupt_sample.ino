/*
  This example shows the use of external interrupts.

  The circuit:
  - Arduino Nano 33 BLE and BLE Sense
  - connect BUTTON_PIN and PULSE_PIN using a wire or low value resistor

  This example code is in the public domain.
*/

#define BUTTON_PIN              2
#define PULSE_PIN               10
#define LED_PIN                 LED_BUILTIN

volatile uint32_t counter = 0;

void setup()
{
  Serial.begin( 9600 );
  while ( !Serial );

  pinMode( BUTTON_PIN, INPUT );
  pinMode( PULSE_PIN, OUTPUT );

  attachInterrupt( digitalPinToInterrupt( BUTTON_PIN ), buttonHandler, CHANGE );
}


void loop()
{
  printCounterTask();
  pulseTask();
}


void buttonHandler( void )
{
  counter++;
}


void printCounterTask()
{
  #define PRINT_COUNTER_INTERVAL  1000

  static uint32_t previousMillis = 0;

  uint32_t currentMillis = millis();
  if ( currentMillis - previousMillis < PRINT_COUNTER_INTERVAL )
  {
    return;
  }
  previousMillis = currentMillis;
  Serial.print( "Counter: " );
  Serial.println( counter );
  counter = 0;
}


void pulseTask()
{
  #define PULSE_INTERVAL          80
  static bool state = LOW;

  static uint32_t previousMillis = 0;

  uint32_t currentMillis = micros();
  if ( currentMillis - previousMillis < PULSE_INTERVAL )
  {
    return;
  }
  previousMillis = currentMillis;
  digitalWrite( PULSE_PIN, state );
  state = !state;
}