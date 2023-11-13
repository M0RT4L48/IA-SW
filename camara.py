import cv2
import mediapipe as mp
import pyautogui
import math

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
current_x, current_y = 0, 0
is_clicking = False

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
            index_x, index_y, thumb_x, thumb_y = None, None, None, None

            for id, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Dedo índice
                    cv2.circle(frame, (x, y), 10, (0, 255, 255))
                    index_x, index_y = screen_width * x / frame_width, screen_height * y / frame_height

                if id == 4:  # Dedo pulgar
                    cv2.circle(frame, (x, y), 10, (0, 255, 255))
                    thumb_x, thumb_y = screen_width * x / frame_width, screen_height * y / frame_height

            if all((index_x, index_y, thumb_x, thumb_y)):
                distance = math.sqrt((index_x - thumb_x) ** 2 + (index_y - thumb_y) ** 2)
                click_threshold = 30  # Ajusta el valor según sea necesario

                if distance < click_threshold:
                    if not is_clicking:
                        pyautogui.mouseDown()
                        is_clicking = True
                else:
                    if is_clicking:
                        pyautogui.mouseUp()
                        is_clicking = False
                    pyautogui.moveTo(thumb_x, thumb_y)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Presionar 'Esc' para salir del bucle
        break

cap.release()
cv2.destroyAllWindows()

