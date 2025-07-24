import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# 檢查 API 密鑰是否設置
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ 錯誤：請設置 GEMINI_API_KEY 環境變數")
    print("請執行：set GEMINI_API_KEY=your_api_key_here")
    exit(1)

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt='Robot holding a red skateboard',
        config=types.GenerateImagesConfig(
            number_of_images=4,
        )
    )
    
    print(f"✅ 成功生成 {len(response.generated_images)} 張圖片")
    
    # 保存所有生成的圖片
    if response.generated_images:
        for i, generated_image in enumerate(response.generated_images):
            try:
                # 直接保存圖片 (generated_image.image 是 PIL Image 物件)
                generated_image.image.save(f"generated_image_{i+1}.png")
                print(f"✅ 圖片已保存為 generated_image_{i+1}.png")
            except Exception as save_error:
                print(f"❌ 保存圖片 {i+1} 時發生錯誤：{save_error}")
                print(f"圖片類型: {type(generated_image.image)}")
                
                # 嘗試其他方法
                try:
                    if isinstance(generated_image.image, bytes):
                        image = Image.open(BytesIO(generated_image.image))
                        image.save(f"generated_image_{i+1}.png")
                        print(f"✅ 圖片已保存為 generated_image_{i+1}.png")
                except Exception as e2:
                    print(f"❌ 備用保存方法也失敗：{e2}")
                    
except Exception as e:
    print(f"❌ 生成圖片時發生錯誤：{e}")
    print("💡 建議檢查：")
    print("   1. GEMINI_API_KEY 環境變數是否正確設置")
    print("   2. 網路連接是否正常")
    print("   3. API 配額是否足夠")
    print("   4. 是否安裝了最新版本：pip install google-genai")