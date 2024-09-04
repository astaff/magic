import asyncio
from typing import AsyncGenerator

import serial
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

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
                await speed_queue.put(response)
            elif response.startswith("V:"):
                await position_queue.put(response)
        await asyncio.sleep(0.001)

async def stream_data(queue: asyncio.Queue) -> AsyncGenerator[str, None]:
    while True:
        data = await queue.get()
        yield f"{data[2:]}\n\n"

@app.on_event("startup")
async def startup_event():
    await connect_to_device()

@app.get("/speed")
async def get_speed():
    return StreamingResponse(stream_data(speed_queue), media_type="text/event-stream")

@app.get("/position")
async def get_position():
    return StreamingResponse(stream_data(position_queue), media_type="text/event-stream")

@app.get("/left")
async def move_left():
    await send_command('l')
    return {"message": "Moving left"}

@app.get("/right")
async def move_right():
    await send_command('r')
    return {"message": "Moving right"}

@app.get("/stop")
async def stop():
    await send_command('s')
    return {"message": "Stopping"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)