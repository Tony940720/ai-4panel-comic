from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

# 檢查 API 密鑰
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ 錯誤：請設置 GEMINI_API_KEY 環境變數")
    print("請執行：set GEMINI_API_KEY=your_api_key_here")
    exit(1)

# 初始化 GenAI 客戶端
client = genai.Client(api_key=api_key)

# 讀取前面產生的 comic_description.txt
try:
    with open("comic_description.txt", "r", encoding="utf-8") as f:
        description_text = f.read()
except FileNotFoundError:
    print("❌ 找不到 comic_description.txt 檔案，請先執行 story_input_to_comic_text.py")
    exit(1)

print("📖 讀取到的漫畫描述：")
print(description_text)
print("\n" + "="*50 + "\n")

# 一次生成完整的四格漫畫
print("🖼️ 開始生成完整的四格漫畫...")

# 使用完整的描述文本*作為 prompt，針對 Imagen 3 優化
prompt = f"""
Create a high-quality 4-panel comic strip illustration based on this story:

{description_text}

Style and format specifications:
- Create a single image with 4 panels arranged in a 2x2 grid
- Each panel clearly separated with black borders
- Consistent anime/manga art style throughout
- High resolution and professional quality
- Vibrant colors and expressive character emotions
- Clear visual narrative flow from panel 1 to panel 4

Panel layout:
[Panel 1] [Panel 2]
[Panel 3] [Panel 4]

Each panel should visually represent the corresponding part of the story description with clear scene composition, character expressions, and appropriate backgrounds.
"""

try:
    # 使用最新的 GenAI API 生成圖片
    print("🖼️ 正在使用 Imagen 3 生成四格漫畫...")
    
    response = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )
    
    print(f"✅ 成功生成 {len(response.generated_images)} 張圖片")
    
    # 保存生成的圖片
    for i, generated_image in enumerate(response.generated_images):
        try:
            # 直接保存圖片 (generated_image.image 是 PIL Image 物件)
            generated_image.image.save(f"complete_4panel_comic_{i+1}.png")
            print(f"✅ 四格漫畫已保存為 complete_4panel_comic_{i+1}.png")
        except Exception as save_error:
            print(f"❌ 保存圖片時發生錯誤：{save_error}")
            # 如果是 bytes 資料，嘗試轉換
            try:
                if isinstance(generated_image.image, bytes):
                    image = Image.open(BytesIO(generated_image.image))
                    image.save(f"complete_4panel_comic_{i+1}.png")
                    print(f"✅ 四格漫畫已保存為 complete_4panel_comic_{i+1}.png")
            except Exception as e2:
                print(f"❌ 所有保存方法都失敗：{e2}")

except Exception as e:
    print(f"❌ 四格漫畫生成失敗：{e}")
    print("💡 建議檢查：")
    print("   1. API 金鑰是否正確設定")
    print("   2. 是否有權限使用 Imagen 3")
    print("   3. 網路連接是否正常")
    print("   4. 請確認已安裝最新版本：pip install google-genai")
