import cv2
import mediapipe as mp
import pyautogui
import time

class PoseController:
    def __init__(self):
        # 初始化 MediaPipe 姿态检测
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)
        
        # 动作状态
        self.prev_action = None
        self.last_action_time = time.time()
        self.action_cooldown = 0.5  # 防止重复触发的冷却时间（秒）
        
    def detect_pose_action(self, landmarks):
        """检测身体姿态动作"""
        # 获取关键点
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
        right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
        left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
        right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
        
        # 检测左手举起
        if left_wrist.y < left_shoulder.y - 0.1:
            return "left_hand_up"
        
        # 检测右手举起
        if right_wrist.y < right_shoulder.y - 0.1:
            return "right_hand_up"
        
        # 检测双手举起
        if (left_wrist.y < left_shoulder.y - 0.1 and 
            right_wrist.y < right_shoulder.y - 0.1):
            return "both_hands_up"
        
        # 检测身体向左倾斜
        if left_shoulder.y < right_shoulder.y - 0.05:
            return "lean_left"
        
        # 检测身体向右倾斜
        if right_shoulder.y < left_shoulder.y - 0.05:
            return "lean_right"
        
        # 检测双手交叉胸前
        if (abs(left_wrist.x - right_shoulder.x) < 0.15 and 
            abs(right_wrist.x - left_shoulder.x) < 0.15 and
            left_wrist.y > nose.y and right_wrist.y > nose.y):
            return "arms_crossed"
        
        return "neutral"
    
    def execute_keyboard_action(self, action):
        """根据动作执行键盘操作"""
        current_time = time.time()
        
        # 检查冷却时间
        if current_time - self.last_action_time < self.action_cooldown:
            return
        
        if action == self.prev_action or action == "neutral":
            return
        
        self.prev_action = action
        self.last_action_time = current_time
        
        # 定义动作到键盘操作的映射
        actions = {
            "left_hand_up": lambda: pyautogui.press('w'),       # W 键
            "right_hand_up": lambda: pyautogui.press('s'),      # S 键
            "both_hands_up": lambda: pyautogui.press('space'),  # 空格键
            "lean_left": lambda: pyautogui.press('a'),          # A 键
            "lean_right": lambda: pyautogui.press('d'),         # D 键
            "arms_crossed": lambda: pyautogui.press('enter'),   # 回车键
        }
        
        if action in actions:
            actions[action]()
            print(f"执行操作: {action}")
    
    def run(self):
        """主循环"""
        print("姿态控制已启动！")
        print("动作映射：")
        print("  左手举起 -> W 键")
        print("  右手举起 -> S 键")
        print("  双手举起 -> 空格键")
        print("  身体左倾 -> A 键")
        print("  身体右倾 -> D 键")
        print("  双手交叉 -> 回车键")
        print("按 'q' 退出")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # 翻转图像
            frame = cv2.flip(frame, 1)
            
            # 转换颜色空间
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # 检测姿态
            results = self.pose.process(rgb_frame)
            
            if results.pose_landmarks:
                # 绘制姿态关键点
                self.mp_draw.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
                
                # 检测动作
                action = self.detect_pose_action(results.pose_landmarks.landmark)
                
                # 显示动作
                cv2.putText(
                    frame,
                    f"Action: {action}",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # 执行键盘操作
                self.execute_keyboard_action(action)
            
            # 显示画面
            cv2.imshow('Pose Control', frame)
            
            # 按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # 清理资源
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = PoseController()
    controller.run()
