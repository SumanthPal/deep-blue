from flask import Flask, render_template, jsonify
import asyncio
from bleak import BleakScanner

app = Flask(__name__)


async def scan_ble():
    devices = await BleakScanner.discover()
    return [{"name": device.name, "address": device.address} for device in devices]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan')
def scan():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices = loop.run_until_complete(scan_ble())
    return jsonify(devices)


if __name__ == '__main__':
    app.run(debug=True)
