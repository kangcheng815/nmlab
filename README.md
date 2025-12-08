# 影像辨識鍵盤控制系統

使用電腦攝影機辨識手勢或身體姿態，並控制鍵盤操作。

## 功能特點

### 1. 手勢控制 (`gesture_control.py`)
透過手部動作控制鍵盤：
- **1根手指** → 上箭頭鍵
- **2根手指** → 下箭頭鍵
- **3根手​​指** → 左箭頭鍵
- **4根手指** → 右箭頭鍵
- **5根手指（手掌張開）** → 空白鍵
- **拳頭** → ENTER

### 2. 姿態控制 (`pose_control.py`)
透過身體動作控制鍵盤：
- **左手舉起** → W 鍵
- **右手舉起** → S 鍵
- **雙手舉起** → 空白鍵
- **身體左傾** → A 鍵
- **身體右傾** → D 鍵
- **雙手交叉胸前** → ENTER

## 安裝執行步驟

pip install -r requirements.txt
python gesture_control.py
python pose_control.py


### 退出程式
在視窗中按 `q` 鍵退出。

## 自訂鍵盤映射

你可以修改程式碼中的 `execute_keyboard_action` 函數來自訂手勢/姿態對應的鍵盤操作。

### 手勢控制範例
在 `gesture_control.py` 中找到這段程式碼：
『`python
actions = {
 "one": lambda: pyautogui.press('up'), # 修改 'up' 為你想要的按鍵
 "two": lambda: pyautogui.press('down'),
 # ... 其他映射
}
```

### 姿態控制範例
在 `pose_control.py` 中找到這段程式碼：
『`python
actions = {
 "left_hand_up": lambda: pyautogui.press('w'), # 修改 'w' 為你想要的按鍵
 "right_hand_up": lambda: pyautogui.press('s'),
 # ... 其他映射
}
```

## 常用鍵盤按鍵代碼

- 方向鍵：`'up'`, `'down'`, `'left'`, `'right'`
- 字母鍵：`'a'`, `'b'`, `'c'`, ... `'z'`
- 功能鍵：`'enter'`, `'space'`, `'esc'`, `'tab'`
- 數字鍵：`'0'`, `'1'`, ... `'9'`
- 組合鍵：`pyautogui.hotkey('ctrl', 'c')` (複製)

## 應用場景

- 遊戲控制（使用身體動作玩遊戲）
- 簡報控制（手勢切換投影片）
- 無接觸操作（衛生環境下的電腦控制）
- 輔助功能（幫助行動不便的使用者）
- 互動娛樂項目

## 技術說明

- **OpenCV**: 攝影機視訊擷取與影像處理
- **MediaPipe**: Google 的機器學習解決方案，提供手部和姿態檢測
- **PyAutoGUI**: 模擬鍵盤和滑鼠操作
- **NumPy**: 數值計算

## 注意事項

1. 確保相機有良好的光線環境
2. 保持適當的距離（建議 0.5-1.5 公尺）
3. 背景盡量簡潔，避免干擾
4. 首次使用時可能需要調整偵測閾值

## 故障排除

### 相機無法打開
- 檢查攝影機是否被其他程式佔用
- 嘗試更改 `cv2.VideoCapture(0)` 中的數字（0、1、2...）

### 手勢辨識不準確
- 調整 `min_detection_confidence` 和 `min_tracking_confidence` 參數
- 改善光線條件
- 確保手部完全在攝影機視野內

### 按鍵觸發太頻繁
- 增加 `action_cooldown` 的值（姿態控制中）
- 修改手勢判斷的邏輯條件
=======
# nmlab-gesture
>>>>>>> main
