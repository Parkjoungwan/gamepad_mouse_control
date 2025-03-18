import pygame
import ctypes
import threading
import time
import pyautogui
import queue

# 초기화
pygame.init()
pygame.joystick.init()

# 게임패드 연결 확인
if pygame.joystick.get_count() == 0:
    print("❌ 연결된 게임패드가 없습니다. 프로그램을 종료합니다.")
    pygame.quit()
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"🎮 감지된 게임패드: {joystick.get_name()}")

# 설정값
MOUSE_SENSITIVITY = 20        # 좌측 조이스틱 마우스 이동 민감도
SCROLL_SENSITIVITY = 10       # 우측 조이스틱 스크롤 민감도 (증가)
DEADZONE_THRESHOLD = 0.15     # 데드존: 이 값 이하의 입력은 무시
SMOOTHING_FACTOR = 0.2        # 보간 계수 (부드러운 이동)

# 스레드 간 이벤트 전달용 큐 생성
left_queue = queue.Queue()    # 좌측 조이스틱 이벤트 큐 (마우스 이동)
right_queue = queue.Queue()   # 우측 조이스틱 이벤트 큐 (스크롤)
button_queue = queue.Queue()  # 버튼 이벤트 큐

# 좌측 조이스틱 보간용 이전 입력값
prev_x, prev_y = 0, 0
# 우측 조이스틱 스크롤 누적값
scroll_accumulator = 0

# Windows API를 사용한 빠른 마우스 이동 함수
def move_mouse(dx, dy):
    ctypes.windll.user32.mouse_event(0x0001, int(dx), int(dy), 0, 0)

# 좌측 조이스틱 스레드 (마우스 이동)
def left_joystick_thread():
    global prev_x, prev_y
    clock = pygame.time.Clock()
    while True:
        try:
            _ = left_queue.get(timeout=0.01)
        except queue.Empty:
            pass

        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        # 데드존 적용
        if abs(x_axis) < DEADZONE_THRESHOLD:
            x_axis = 0
        if abs(y_axis) < DEADZONE_THRESHOLD:
            y_axis = 0

        # 입력이 0이면 보간값 초기화하여 잔여 움직임 제거
        if x_axis == 0 and y_axis == 0:
            smooth_x, smooth_y = 0, 0
            prev_x, prev_y = 0, 0
        else:
            smooth_x = prev_x * (1 - SMOOTHING_FACTOR) + x_axis * SMOOTHING_FACTOR
            smooth_y = prev_y * (1 - SMOOTHING_FACTOR) + y_axis * SMOOTHING_FACTOR
            prev_x, prev_y = smooth_x, smooth_y

        if smooth_x != 0 or smooth_y != 0:
            move_mouse(smooth_x * MOUSE_SENSITIVITY, smooth_y * MOUSE_SENSITIVITY)
        clock.tick(120)

# 우측 조이스틱 스레드 (스크롤)
def right_joystick_thread():
    global scroll_accumulator
    clock = pygame.time.Clock()
    while True:
        try:
            _ = right_queue.get(timeout=0.01)
        except queue.Empty:
            pass

        scroll_axis = joystick.get_axis(3)
        if abs(scroll_axis) < DEADZONE_THRESHOLD:
            scroll_axis = 0

        # 누적 방식: 입력값 누적 후 일정량 이상일 때 스크롤 적용
        scroll_accumulator += -scroll_axis * SCROLL_SENSITIVITY  # 방향 보정
        if abs(scroll_accumulator) >= 1:
            scroll_amount = int(scroll_accumulator)
            pyautogui.scroll(scroll_amount)
            scroll_accumulator -= scroll_amount
        clock.tick(120)

# 버튼 처리 스레드 (클릭 및 더블 클릭, 진동 추가)
def button_thread_func():
    while True:
        try:
            event = button_queue.get(timeout=0.01)
        except queue.Empty:
            time.sleep(0.005)
            continue

        if event.button == 0:
            pyautogui.click()
            print("A 버튼 눌림: 단일 클릭 실행")
            try:
                joystick.rumble(0.5, 0.5, 200)  # 0.5 강도의 진동, 200ms 지속
            except Exception as e:
                print("진동 기능 에러:", e)
        elif event.button == 1:
            pyautogui.doubleClick()
            print("B 버튼 눌림: 더블 클릭 실행")
            try:
                joystick.rumble(0.5, 0.5, 200)
            except Exception as e:
                print("진동 기능 에러:", e)
        time.sleep(0.005)

# 각 입력 처리 스레드 실행
left_thread = threading.Thread(target=left_joystick_thread, daemon=True)
right_thread = threading.Thread(target=right_joystick_thread, daemon=True)
btn_thread = threading.Thread(target=button_thread_func, daemon=True)

left_thread.start()
right_thread.start()
btn_thread.start()

# 메인 스레드: pygame 이벤트 큐에서 이벤트를 읽어 각 큐에 분배
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # 좌측: 축 0,1 / 우측: 축 3 (필요시 조정)
            if event.axis in [0, 1]:
                left_queue.put(event)
            elif event.axis == 3:
                right_queue.put(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            button_queue.put(event)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
    time.sleep(0.005)
