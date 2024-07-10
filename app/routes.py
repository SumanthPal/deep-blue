from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
import asyncio
from bleak import BleakScanner
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import get_user_by_username
from app.models import get_db, add_db, delete_db, increment_frequency
from app import app
from werkzeug.security import generate_password_hash, check_password_hash

#returns scanned devices in JSON Format
async def scan_ble():
    devices = await BleakScanner.discover()
    return [{"name": device.name, "address": device.address} for device in devices]

#used to calculate how many times a device has connected to the PC
def calculate_frequency():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices = loop.run_until_complete(scan_ble())
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT name FROM user')
    users = cursor.fetchall()
    for device in devices:
        device_name = device.get('name')
        if not device_name:
            continue
        for user in users:
            if device_name == user[0]:
                increment_frequency(user[0])

#main route to index page
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

#calls the scan_ble method to return a list of all the devices
@app.route('/scan')
def scan():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    devices = loop.run_until_complete(scan_ble())
    calculate_frequency()
    return jsonify(devices)

#route used for registering a device to connect with the PC
@app.route('/add', methods=['POST'])
def submit():
    name = request.form['name']
    address = request.form['address']
    if name == "" or address == "":
        flash('Please enter a valid name/address', 'error')
    else:
        flash('Form submitted successfully!', 'success')
        add_db(name, address)
        print(f"Received Name: {name}, Address: {address}")
    return redirect(url_for('index'))

#route used to delete registered devices
@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    print(f"Received Name: {name}")
    delete_db(name)
    return redirect(url_for('index'))


#route to check registered devices
@app.route('/data')
def data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, name, address FROM user')
    users = cursor.fetchall()
    return render_template('base.html', users=users)

#login route

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, 'user'))
        db.commit()
        flash('Registration successful, please login.')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
