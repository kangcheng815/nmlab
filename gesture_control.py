import cv2
import mediapipe as mp
import pyautogui
import numpy as np

class GestureController:
    def __init__(self):
        # initialize MediaPipe Hand Detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # initialize camera
        self.cap = cv2.VideoCapture(0)
        
        # gesture state
        self.prev_gesture = None
    
    ##################################################
    #############     手指數量     ###################
    ##################################################
    def count_fingers(self, hand_landmarks):
        
        fingers = []
        
        # 拇指 (根据 x 坐标判断)
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # 其他四指 (根据 y 坐标判断)
        tip_ids = [8, 12, 16, 20]
        for tip in tip_ids:
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers.count(1)
    
    def detect_gesture(self, hand_landmarks):
        """检测具体手势"""
        finger_count = self.count_fingers(hand_landmarks)
        
        # 获取关键点位置
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        
        # 计算拇指和食指的距离
        distance = np.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
        
        # 根据手指数量识别手势
        if finger_count == 0:
            return "fist"  # 拳头
        elif finger_count == 1:
            return "one"   # 一个手指
        elif finger_count == 2:
            return "two"   # 两个手指
        elif finger_count == 3:
            return "three" # 三个手指
        elif finger_count == 4:
            return "four"  # 四个手指
        elif finger_count == 5:
            return "five"  # 五个手指 (手掌张开)
        
        return "unknown"
    
    def execute_keyboard_action(self, gesture):
        """根据手势执行键盘操作"""
        if gesture == self.prev_gesture:
            return  # 避免重复触发
            
        self.prev_gesture = gesture
        
        # 定义手势到键盘操作的映射
        actions = {
            "one": lambda: pyautogui.press('up'),      # 向上
            "two": lambda: pyautogui.press('down'),    # 向下
            "three": lambda: pyautogui.press('left'),  # 向左
            "four": lambda: pyautogui.press('right'),  # 向右
            "five": lambda: pyautogui.press('space'),  # 空格
            "fist": lambda: pyautogui.press('enter'),  # 回车
        }
        
        if gesture in actions:
            actions[gesture]()
            print(f"执行操作: {gesture}")
    
    def run(self):
        """主循环"""
        print("手势控制已启动！")
        print("手势映射：")
        print("  1根手指 -> 上箭头")
        print("  2根手指 -> 下箭头")
        print("  3根手指 -> 左箭头")
        print("  4根手指 -> 右箭头")
        print("  5根手指(手掌) -> 空格键")
        print("  拳头 -> 回车键")
        print("按 'q' 退出")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # 翻转图像，使其像镜子
            frame = cv2.flip(frame, 1)
            
            # 转换颜色空间
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 检测手部
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # 绘制手部关键点
                    self.mp_draw.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # 检测手势
                    gesture = self.detect_gesture(hand_landmarks)
                    
                    # 显示手势
                    cv2.putText(
                        frame, 
                        f"Gesture: {gesture}", 
                        (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (0, 255, 0), 
                        2
                    )
                    
                    # 执行键盘操作
                    self.execute_keyboard_action(gesture)
            else:
                self.prev_gesture = None
            
            # 显示画面
            cv2.imshow('Gesture Control', frame)
            
            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # 清理资源
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = GestureController()
    controller.run()
