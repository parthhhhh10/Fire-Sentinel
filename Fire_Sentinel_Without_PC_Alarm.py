import cv2
import serial
import time
import datetime
import pywhatkit
import threading
from ultralytics import YOLO

# ===== CONSTANTS =====
CONFIRMATION_TIME = 3.0  # seconds to confirm fire
COOLDOWN_TIME = 10.0     # seconds after alarm before resetting
WHATSAPP_NUMBER = "+918169155802"  # Replace with your number

# ===== SERIAL SETUP =====
arduino = serial.Serial('COM3', 115200, timeout=0.1)
arduino.flush()

# ===== YOLO MODEL =====
model = YOLO("best.pt").to("cpu")
model.conf = 0.7  # Confidence threshold

# ===== CAMERA =====
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

# ===== STATE =====
fire_detected = False
alarm_triggered = False
whatsapp_sent = False
fire_start = 0

def send_whatsapp_alert():
    """Send alert in background thread"""
    global whatsapp_sent
    try:
        img_path = f"fire_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(img_path, frame)
        
        # Send immediately
        pywhatkit.sendwhats_image(
            receiver=WHATSAPP_NUMBER,
            img_path=img_path,
            caption="🚨 FIRE DETECTED! Immediate action required!",
            tab_close=True,
            close_time=3
        )
        print("WhatsApp alert sent successfully")
    except Exception as e:
        print(f"WhatsApp error: {str(e)}")
    whatsapp_sent = True

def send_command(cmd):
    """Thread-safe serial communication"""
    try:
        arduino.write(f"{cmd}\n".encode())
        time.sleep(0.05)  # Allow Arduino to process
    except:
        print("Serial Error")

def cleanup():
    """Proper shutdown handler"""
    send_command("STOP")
    send_command("RESET")
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print("System shutdown complete")

# Register cleanup
import atexit
atexit.register(cleanup)

# ===== MAIN LOOP =====
try:
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Frame read error")
            continue

        # Clear serial buffer
        while arduino.in_waiting:
            arduino.read()

        # Scan when no fire
        if not fire_detected and not alarm_triggered:
            send_command("ROTATE")

        # YOLO Detection with bounding boxes
        results = model(frame, imgsz=320, verbose=False)
        fire_found = False

        for r in results:
            for box in r.boxes:
                # Draw bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "FIRE", (x1, y1-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                fire_found = True

        # Fire state machine
        if fire_found:
            if not fire_detected:
                fire_detected = True
                fire_start = time.time()
                whatsapp_sent = False
            
            # Show confirmation timer
            if fire_detected and not alarm_triggered:
                timer_remaining = max(0, CONFIRMATION_TIME - (time.time() - fire_start))
                cv2.putText(frame, f"Confirming: {timer_remaining:.1f}s", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
                
            # Trigger alarm after confirmation period
            if time.time() - fire_start > CONFIRMATION_TIME and not alarm_triggered:
                send_command("STOP")
                send_command("FIRE")
                if not whatsapp_sent:
                    threading.Thread(target=send_whatsapp_alert).start()
                alarm_triggered = True
        else:
            # Reset only after cooldown period
            if alarm_triggered and (time.time() - fire_start > COOLDOWN_TIME):
                send_command("RESUME")
                fire_detected = alarm_triggered = whatsapp_sent = False
            elif fire_detected and not alarm_triggered:
                fire_detected = False

        # Display
        cv2.imshow("Fire Detection", frame)
        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    pass
finally:
    cleanup()