from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
import asyncio
from bleak import BleakScanner
from app.models import get_db, add_db

from app import app


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

@app.route('/add', methods=['POST'])
def submit():
    name = request.form['name']
    address = request.form['address']

    # Basic validation
    if not name or not address:
        flash('All fields are required!')
        return redirect(url_for('index'))

    # Debugging: Print form data
    print(f"Received Name: {name}, Address: {address}")

    # Insert into the database
    add_db(name, address)

    flash('Form submitted successfully!')
    return redirect(url_for('index'))

@app.route('/data')
def data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, address FROM user')
    users = cursor.fetchall()

    return render_template('base.html', users=users)


