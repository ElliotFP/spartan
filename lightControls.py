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
        while True:  # Infinite loop
            for color in colors:
                await led.set_color(color)
                await asyncio.sleep(frequency / 2)  # Wait after setting color
                await led.set_brightness(brightness)
                await asyncio.sleep(frequency / 2)  # Wait after setting brightness
    except KeyboardInterrupt:
        pass

# Main function, now accepts parameters for brightness, frequency, and colors
async def main(brightness, frequency, colors):
    # Setup and run the strobe
    scanner = BleakScanner()
    device = await scanner.find_device_by_address(MAC_ADDRESS)
    led = GoveeInstance(device)

    await led.turn_on()
    await customizable_strobe(led, brightness, frequency, colors)
    await led.turn_off()
    await led.disconnect()

if __name__ == '__main__':
    # Example usage with hardcoded values
    brightness = 200  # Example brightness
    frequency = 0.5  # Example frequency in seconds
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # Example colors

    asyncio.run(main(brightness, frequency, colors))