import asyncio

from bleak import BleakClient, BleakScanner

HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

async def main():
    print("Scanning for Polar H7 device...")
    devices = await BleakScanner.discover()
    polar_device = next((d for d in devices if "Polar H7" in d.name), None)

    if not polar_device:
        print("Polar H7 device not found. Make sure it's turned on and nearby.")
        return

    print(f"Found Polar H7 device: {polar_device.name}")

    async with BleakClient(polar_device.address) as client:
        print("Connected. Streaming heart rate data...")

        def callback(sender, data):
            heart_rate = data[1]
            print(f"Heart Rate: {heart_rate} bpm")

        await client.start_notify(HEART_RATE_UUID, callback)

        while True:
            await asyncio.sleep(1)

asyncio.run(main())