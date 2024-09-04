import asyncio

import serial
from fasthtml.common import *

app, rt = fast_app()

# Global variables
ser = None
speed_queue = asyncio.Queue()
position_queue = asyncio.Queue()

async def connect_to_device(port='/dev/ttyUSB0', baudrate=115200):
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port}")
        asyncio.create_task(read_serial())
    except serial.SerialException as e:
        print(f"Error connecting to {port}: {e}")

async def send_command(command: str):
    if ser:
        ser.write(command.encode())
        print(f"Sent command: {command}")

async def read_serial():
    while True:
        if ser and ser.in_waiting:
            response = ser.readline().decode().strip()
            if response.startswith("S:"):
                await speed_queue.put(response[2:])
            elif response.startswith("V:"):
                await position_queue.put(response[2:])
        await asyncio.sleep(0.001)

@app.on_event("startup")
async def startup_event():
    await connect_to_device()

@rt("/")
def get():
    return Titled("Device Control",
        Div(
            Button("Left", hx_get="/left", hx_swap="none"),
            Button("Stop", hx_get="/stop", hx_swap="none"),
            Button("Right", hx_get="/right", hx_swap="none"),
        ),
        Div(
            P("Speed: ", Span(id="speed")),
            P("Position: ", Span(id="position")),
        ),
        Script("""
            const speedSource = new EventSource('/speed');
            speedSource.onmessage = function(event) {
                document.getElementById('speed').textContent = event.data;
            };
            const positionSource = new EventSource('/position');
            positionSource.onmessage = function(event) {
                document.getElementById('position').textContent = event.data;
            };
        """)
    )

@rt("/speed")
async def get_speed():
    async def stream():
        while True:
            data = await speed_queue.get()
            yield f"data: {data}\n\n"
    return EventStream(stream())

@rt("/position")
async def get_position():
    async def stream():
        while True:
            data = await position_queue.get()
            yield f"data: {data}\n\n"
    return EventStream(stream())

@rt("/left")
async def move_left():
    await send_command('l')
    return "Moving left"

@rt("/right")
async def move_right():
    await send_command('r')
    return "Moving right"

@rt("/stop")
async def stop():
    await send_command('s')
    return "Stopping"

serve()