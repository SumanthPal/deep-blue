from flask import Flask, render_template, jsonify, g
import asyncio
import sqlite3
from bleak import BleakScanner
from app import app, models

DATABASE = 'database.db'

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

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()
