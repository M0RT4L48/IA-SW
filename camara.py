import cv2
import mediapipe as mp
import pyautogui
import time

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

ADJUSTMENT_DISTANCE = 30
ADJUSTMENT_SPEED = 5
CLICK_DELAY = 3  # Tiempo de espera antes de hacer clic izquierdo

last_click_time = time.time()

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    print('Outside:', abs(index_y - thumb_y))

                    if abs(index_y - thumb_y) < ADJUSTMENT_DISTANCE:
                        adjustment_factor = ADJUSTMENT_SPEED * (ADJUSTMENT_DISTANCE - abs(index_y - thumb_y))
                        if thumb_y < index_y:
                            index_y -= adjustment_factor
                        else:
                            index_y += adjustment_factor

                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

                        # Hacer clic izquierdo después de 3 segundos
                        current_time = time.time()
                        if current_time - last_click_time > CLICK_DELAY:
                            pyautogui.click()
                            last_click_time = current_time

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
