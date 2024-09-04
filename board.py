import utime
from machine import ADC, UART, Pin, Timer

# 1. System Initialization
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
uart.init(115200, bits=8, parity=None, stop=1)

speed_sensor = Pin(21, Pin.IN, Pin.PULL_DOWN)
h_bridge_left = Pin(28, Pin.OUT)
h_bridge_right = Pin(22, Pin.OUT)
adc = ADC(Pin(26))

last_timestamp = 0

# 2. Speed Sensor Handling
def speed_sensor_callback(pin):
    global last_timestamp
    current_time = utime.ticks_ms()
    if utime.ticks_diff(current_time, last_timestamp) > 10:  # Debounce
        last_timestamp = current_time
        uart.write(f"S:{current_time}\r\n")

speed_sensor.irq(trigger=Pin.IRQ_RISING, handler=speed_sensor_callback)

# 3. Variable Resistor Readings
def read_resistors(timer):
    value = adc.read_u16()
    uart.write(f"V:{value}\r\n")

resistor_timer = Timer()
resistor_timer.init(period=100, mode=Timer.PERIODIC, callback=read_resistors)

# 4. Serial Communication Protocol
def parse_command(command):
    debug_print(f"Received command: {command}")
    if command == b'l':
        move_left()
    elif command == b'r':
        move_right()
    elif command == b's':
        stop_motor()

# 5. Motor Control
motor_timer = Timer()

def move_left(pulse_sec=1.0):
    h_bridge_left.value(1)
    h_bridge_right.value(0)
    motor_timer.deinit()  # Reset the timer
    motor_timer.init(period=int(pulse_sec * 1000), mode=Timer.ONE_SHOT, callback=lambda t: stop_motor())

def move_right(pulse_sec=1.0):
    h_bridge_left.value(0)
    h_bridge_right.value(1)
    motor_timer.deinit()  # Reset the timer
    motor_timer.init(period=int(pulse_sec * 1000), mode=Timer.ONE_SHOT, callback=lambda t: stop_motor())

def stop_motor():
    h_bridge_left.value(0)
    h_bridge_right.value(0)

# 6. Main Loop with UART Polling
def main():
    while True:
        if uart.any():
            command = uart.read(1)  # Read a single ASCII character
            parse_command(command)

# 7. Error Handling and Robustness
def safe_adc_read(adc):
    try:
        return adc.read_u16()
    except Exception as e:
        print(f"ADC read error: {e}")
        return 0

DEBUG = True

def debug_print(message):
    if DEBUG:
        print(message)

debug_print("Made with Love.")
main()