# app.py
from flask import Flask, render_template, Response
# Uncomment below if using CORS:
# from flask_cors import CORS
from flask_socketio import SocketIO
import cv2
from dnt import detect_and_overlay

# Initialize Flask with explicit template folder
app = Flask(__name__, template_folder='templates')
# CORS(app)  # Uncomment if CORS is needed
socketio = SocketIO(app, cors_allowed_origins="*")  # allow CORS for all origins

# Open video capture
cap = cv2.VideoCapture(0)

@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

# Generator for video frames and emit finger count
def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame, count = detect_and_overlay(frame)
        socketio.emit('gesture_update', count)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index2.html')
@app.route('/order/bunbo')
def order_bun_bo():
    return render_template('order_bunbo.html')
@app.route('/order/buncha')
def order_bun_cha():
    return render_template('order_buncha.html')
@app.route('/order/comtam')
def order_comtam():
    return render_template('order_comtam.html')
@app.route('/order/phobo')
def order_phobo():
    return render_template('order_phobo.html')
@app.route('/order/bundau')
def order_bundau():
    return render_template('order_bundau.html')
@app.route('/order/burger')
def order_burger():
    return render_template('order_burger.html')
@app.route('/order/garan')
def order_garan():
    return render_template('order_garan.html')
@app.route('/order/suonnuong')
def order_suonnuong():
    return render_template('order_suonnuong.html')
@app.route('/order/canhkimchi')
def order_canhkimchi():
    return render_template('order_canhkimchi.html')
@app.route('/order/hutieu')
def order_hutieu():
    return render_template('order_hutieu.html')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)  # bind all interfaces
