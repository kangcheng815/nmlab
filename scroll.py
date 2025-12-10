import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

class BrowserGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.cap = cv2.VideoCapture(0)
        
        self.prev_gesture = None
        self.prev_hand_position = None
        self.is_fist = False
        self.scroll_sensitivity = 10
        
        # Coolddown Settings
        self.last_action_time = time.time()
        self.action_cooldown = 0.8  
        
        # 手势确认机制
        self.gesture_history = []
        self.gesture_confirm_count = 5  # 需要连续识别多少次才确认手势
        
    def count_fingers(self, hand_landmarks):
        """计算伸出的手指数量"""
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
    
    def get_hand_center(self, hand_landmarks):
        """获取手掌中心位置"""
        # 使用手腕位置作为参考点
        wrist = hand_landmarks.landmark[0]
        return (wrist.x, wrist.y)
    
    def detect_gesture(self, hand_landmarks):
        """检测手势"""
        finger_count = self.count_fingers(hand_landmarks)
        
        if finger_count == 0:
            return "fist"
        elif finger_count == 1:
            return "one"
        elif finger_count == 2:
            return "two"
        elif finger_count == 3:
            return "three"
        elif finger_count == 4:
            return "four"
        elif finger_count == 5:
            return "five"
        
        return "unknown"
    
    def confirm_gesture(self, current_gesture):
        """确认手势 - 需要连续识别多次才算有效"""
        # 将当前手势加入历史记录
        self.gesture_history.append(current_gesture)
        
        # 只保留最近的 N 次记录
        if len(self.gesture_history) > self.gesture_confirm_count:
            self.gesture_history.pop(0)
        
        # 如果历史记录中都是同一个手势，才确认
        if len(self.gesture_history) >= self.gesture_confirm_count:
            if all(g == current_gesture for g in self.gesture_history):
                return current_gesture
        
        return None
    
    def execute_browser_action(self, gesture, hand_landmarks):
        """根据手势执行浏览器操作"""
        current_time = time.time()
        
        # 获取手掌位置
        hand_center = self.get_hand_center(hand_landmarks)

        '''
        滑動：
        拳頭滑動，且只能向下滑動
        '''        
        if gesture == "fist":
            if not self.is_fist:
                self.is_fist = True
                self.prev_hand_position = hand_center
                print("滑动模式：ON")
            else:
                if self.prev_hand_position:
                    dy = (hand_center[1] - self.prev_hand_position[1]) * 1000
                    
                    if abs(dy) > 20:
                        scroll_amount = int(dy * self.scroll_sensitivity)
                        pyautogui.scroll(scroll_amount) 
                        print(f"滚动: {scroll_amount}")
                    
                    self.prev_hand_position = hand_center
        
        else:
            # 非握拳状态 - 其他手势
            if self.is_fist:
                self.is_fist = False
                self.prev_hand_position = None
                self.gesture_history.clear()  # 清空手势历史
                print("滑动模式：OFF")
            
        #     # 防止重复触发
        #     if current_time - self.last_action_time < self.action_cooldown:
        #         return
            
        #     # 使用手势确认机制
        #     confirmed_gesture = self.confirm_gesture(gesture)
        #     if not confirmed_gesture:
        #         return  # 手势未确认，不执行操作
            
        #     if confirmed_gesture == "one":
        #         # 一根手指 - 后退
        #         pyautogui.hotkey('alt', 'left')
        #         print("操作: 后退")
        #         self.last_action_time = current_time
        #         self.gesture_history.clear()
                
        #     elif confirmed_gesture == "two":
        #         # 两根手指 - 前进
        #         pyautogui.hotkey('alt', 'right')
        #         print("操作: 前进")
        #         self.last_action_time = current_time
        #         self.gesture_history.clear()
                
        #     elif confirmed_gesture == "three":
        #         # 三根手指 - 刷新页面
        #         pyautogui.press('f5')
        #         print("操作: 刷新")
        #         self.last_action_time = current_time
        #         self.gesture_history.clear()
                
        #     elif confirmed_gesture == "four":
        #         # 四根手指 - 新标签页
        #         pyautogui.hotkey('ctrl', 't')
        #         print("操作: 新标签页")
        #         self.last_action_time = current_time
        #         self.gesture_history.clear()
                
        #     elif confirmed_gesture == "five":
        #         # 五根手指 - 关闭标签页
        #         pyautogui.hotkey('ctrl', 'w')
        #         print("操作: 关闭标签页")
        #         self.last_action_time = current_time
        #         self.gesture_history.clear()
    
    def run(self):
        print("=" * 60)
        print("Browser Controller")
        print("=" * 60)
        print("手势功能：")
        print("  握拳 + 上下移动 -> 滾動頁面")
        # print("  1根手指 -> 后退")
        # print("  2根手指 -> 前进")
        # print("  3根手指 -> 刷新页面")
        # print("  4根手指 -> 新建标签页")
        # print("  5根手指 -> 关闭标签页")
        print("=" * 60)
        print("按 'Q' 退出")
        print("=" * 60)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 翻转图像
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
                    if gesture == "fist" and self.is_fist:
                        gesture_text = "SCROLL MODE"
                        color = (0, 0, 255)
                    else:
                        gesture_text = f"Gesture: {gesture}"
                        color = (0, 255, 0)
                    
                    cv2.putText(
                        frame,
                        gesture_text,
                        (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color,
                        2
                    )
                    
                    # 执行浏览器操作
                    self.execute_browser_action(gesture, hand_landmarks)
            else:
                # 没有检测到手
                if self.is_fist:
                    self.is_fist = False
                    self.prev_hand_position = None
                    print("滑动模式：OFF")
                self.gesture_history.clear()  # 清空手势历史
            
            # 显示提示
            cv2.putText(
                frame,
                "Press 'Q' to quit",
                (10, frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
            
            # 显示画面
            cv2.imshow('Browser Gesture Control', frame)
            
            # 按 'Q' 退出
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = BrowserGestureController()
    controller.run()
