# import easyocr
# reader = easyocr.Reader(['en', 'ch_sim'])  # 支援簡體中文和英文
# result = reader.readtext('complete_4panel_comic_1.png')

# for bbox, text, conf in result:
#     print(f"位置: {bbox}, 文字: {text}, 信心值: {conf}")
import easyocr
import matplotlib.pyplot as plt
import torch
import cv2
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm
import os
from datetime import datetime

# 設定中文字體
try:
    # 嘗試使用專案中的字體
    font_path = 'NotoSansTC-Regular.ttf'
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
except:
    # 如果專案字體不可用，使用系統字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 檢查 GPU 可用性
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU 數量: {torch.cuda.device_count()}")
    print(f"GPU 名稱: {torch.cuda.get_device_name(0)}")

# 設定 EasyOCR 使用 GPU（如果可用）
gpu = torch.cuda.is_available()
reader = easyocr.Reader(["ch_tra", "en"], gpu=gpu) # 設定辨識語言和 GPU 使用

file_path = 'comic_4panel.png' # 圖片路徑

# 讀取圖片
image = cv2.imread(file_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 辨識圖片中的文字
result = reader.readtext(file_path)

# 創建輸出資料夾
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
main_output_dir = "outputs"
output_folder = os.path.join(main_output_dir, f"ocr_analysis_{timestamp}")
os.makedirs(output_folder, exist_ok=True)

# 創建圖片顯示
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.imshow(image_rgb)

# 顯示辨識結果並在圖片上標記
print("=== 文字辨識結果 ===")
for i, (bbox, text, confidence) in enumerate(result):
    print(f"第 {i+1} 個文字區域:")
    print(f"  座標: {bbox}")
    print(f"  文字: {text}")
    print(f"  信心值: {confidence:.4f}")
    print("-" * 40)
    
    # 獲取邊界框的四個角點
    points = np.array(bbox)
    
    # 計算矩形的左上角和寬高
    x_min = min(points[:, 0])
    y_min = min(points[:, 1])
    x_max = max(points[:, 0])
    y_max = max(points[:, 1])
    
    width = x_max - x_min
    height = y_max - y_min
    
    # 在圖片上畫出矩形框
    rect = Rectangle((x_min, y_min), width, height, 
                    linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

ax.set_title('文字辨識結果 - 紅框標示文字位置', fontsize=14)
ax.axis('off')
plt.tight_layout()

# 儲存圖片
output_filename = os.path.join(output_folder, 'ocr_result.png')
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"結果已儲存為: {output_filename}")

# 儲存辨識結果到文字檔
result_txt_path = os.path.join(output_folder, 'ocr_results.txt')
with open(result_txt_path, 'w', encoding='utf-8') as f:
    f.write("=== 文字辨識結果 ===\n")
    for i, (bbox, text, confidence) in enumerate(result):
        f.write(f"第 {i+1} 個文字區域:\n")
        f.write(f"  座標: {bbox}\n")
        f.write(f"  文字: {text}\n")
        f.write(f"  信心值: {confidence:.4f}\n")
        f.write("-" * 40 + "\n")

print(f"辨識結果已儲存為: {result_txt_path}")
print(f"輸出資料夾: {output_folder}")

# 詢問是否要顯示視窗
show_window = input("是否要顯示圖片視窗？(y/n): ").lower().strip()
if show_window == 'y' or show_window == 'yes':
    plt.show()
else:
    plt.close()  # 關閉圖片以釋放記憶體