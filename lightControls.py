import asyncio
import logging
from govee_btled_H613B import GoveeInstance
from bleak import BleakScanner

# Constants
MAC_ADDRESS = 'D4:AD:FC:A3:70:54'

# Setup logging
logging.basicConfig()
logging.getLogger('govee_btled_H613B').setLevel(logging.DEBUG)

# Function for the customizable strobe effect
async def customizable_strobe(led, brightness, frequency, colors):
    try:
        while True:  # Infinite loop for the strobe effect
            for color in colors:
                await led.set_color(color)
                await asyncio.sleep(frequency / 2)  # Wait after setting color
                await led.set_brightness(brightness)
                await asyncio.sleep(frequency / 2)  # Wait after setting brightness
    except asyncio.CancelledError:
        pass  # Allow the async task to be cancelled

# Function to start the strobe effect
async def start_strobe(brightness, frequency, colors):
    scanner = BleakScanner()
    device = await scanner.find_device_by_address(MAC_ADDRESS)
    led = GoveeInstance(device)

    await led.turn_on()
    strobe_task = asyncio.create_task(customizable_strobe(led, brightness, frequency, colors))
    return strobe_task, led

# Function to stop the strobe effect
async def stop_strobe(strobe_task, led):
    strobe_task.cancel()
    await led.turn_off()
    await led.disconnect()

# Main function for testing (if run as a standalone script)
async def main():
    brightness = 200  # Example brightness
    frequency = 0.5   # Example frequency in seconds
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Example colors

    strobe_task, led = await start_strobe(brightness, frequency, colors)
    await asyncio.sleep(10)  # Run for 10 seconds
    await stop_strobe(strobe_task, led)

if __name__ == '__main__':
    asyncio.run(main())
