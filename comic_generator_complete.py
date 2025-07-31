"""
四格漫畫生成器 - 完全整合版
直接從故事生成四格漫畫，使用 genai 和 Imagen 4.0
"""

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os
import time
import json
from datetime import datetime

# 檢查 API 密鑰
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ 錯誤：請設置 GEMINI_API_KEY 環境變數")
    print("請執行：set GEMINI_API_KEY=your_api_key_here")
    exit(1)

# 初始化 GenAI 客戶端
client = genai.Client(api_key=api_key)

print("🎨 四格漫畫生成器 - 完全整合版")
print("="*60)

# 讓使用者輸入故事
story = input("\n📝 請輸入你的漫畫故事內容：\n")

# 獲取語言偏好
print("\n🌐 請選擇對話框語言：")
print("1. 繁體中文")
print("2. 英文") 
print("3. 簡體中文")
language_choice = input("請輸入選項 (1-3，預設為1)：").strip()

prompt = f"""
我會提供一段漫畫故事文字，請你根據故事生成一個詳細的四格漫畫描述文本。

請嚴格按照以下官方範例格式生成，必須是單一段落的連續描述：

官方範例格式：
"This four-panel comic strip uses a charming, deliberately pixelated art style reminiscent of classic 8-bit video games, featuring simple shapes and a limited, bright color palette dominated by greens, blues, browns, and the dinosaur's iconic grey/black. The setting is a stylized pixel beach. Panel one shows the familiar Google Chrome T-Rex dinosaur, complete with its characteristic pixelated form, wearing tiny pixel sunglasses and lounging on a pixelated beach towel under a blocky yellow sun. Pixelated palm trees sway gently in the background against a blue pixel sky. A caption box with pixelated font reads, "Even error messages need a vacation." Panel two is a close-up of the T-Rex attempting to build a pixel sandcastle. It awkwardly pats a mound of brown pixels with its tiny pixel arms, looking focused. Small pixelated shells dot the sand around it. Panel three depicts the T-Rex joyfully hopping over a series of pixelated cacti planted near the beach, mimicking its game obstacle avoidance. Small "Boing! Boing!" sound effect text appears in a blocky font above each jump. A pixelated crab watches from the side, waving its pixel claw. The final panel shows the T-Rex floating peacefully on its back in the blocky blue pixel water, sunglasses still on, with a contented expression. A small thought bubble above it contains pixelated "Zzz ... " indicating relaxation."

嚴格要求：
1. 必須生成一個完整的英文段落，不要分行、分段或使用引號包圍
2. 開頭必須描述整體藝術風格（art style）和色彩調色盤（color palette）
3. 接著描述整體場景設定（setting）
4. 然後按順序描述四格：
   - Panel one shows... (第一格的詳細描述)
   - Panel two... (第二格的詳細描述)
   - Panel three depicts... (第三格的詳細描述)
   - The final panel shows... (第四格的詳細描述)
5. 每格必須包含：
   - 具體的視覺細節和場景元素
   - 角色的動作和表情
   - 對話文字或音效（用引號標示）
   - 背景和氛圍描述
6. 整個描述要自然流暢，就像範例一樣
7. 不要在開頭和結尾加上任何額外的引號或格式標記

請根據以下故事生成完全符合上述格式的描述：
{story}
"""

try:
    print("\n🔍 步驟 1/2：生成漫畫描述文本...")
    
    # 使用 GenAI 生成文本描述
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )
    description_text = response.text
    
    print("✅ 描述文本生成成功！")
    print("\n📖 生成的漫畫描述：")
    print("-" * 50)
    print(description_text)
    print("-" * 50)
    
    print("\n🎨 步驟 2/2：生成四格漫畫圖片...")
    
    # 設定語言要求
    if language_choice == "2":
        language_requirement = """
Language requirements:
- Any dialogue, speech bubbles, or text within the comic should be in English
- Sound effects in English (like: Bang!, Wow!, Hmm... etc)
- Caption boxes or narrative text should also be in English
- Ensure English text is clear and readable
"""
    elif language_choice == "3":
        language_requirement = """
Language requirements:
- Any dialogue, speech bubbles, or text within the comic should be in Simplified Chinese (简体中文)
- Sound effects can be in Chinese characters (如：砰！、哇！、嗯...等)
- Caption boxes or narrative text should also be in Chinese
- Ensure Chinese text is clear and readable
"""
    else:  # 預設為繁體中文
        language_requirement = """
Language requirements:
- Any dialogue, speech bubbles, or text within the comic should be in Traditional Chinese (繁體中文)
- Sound effects can be in Chinese characters (如：碰！、哇！、嗯...等)
- Caption boxes or narrative text should also be in Chinese
- Ensure Chinese text is clear and readable
"""
    
    # 圖片生成 prompt
    image_prompt = f"""
Create a high-quality 4-panel comic strip illustration based on this story:

{description_text}

Style and format specifications:
- Create a single image with 4 panels arranged in a 2x2 grid
- Each panel clearly separated with black borders
- Consistent anime/manga art style throughout
- High resolution and professional quality
- Vibrant colors and expressive character emotions
- Clear visual narrative flow from panel 1 to panel 4
- IMPORTANT: Ensure all 4 panels are included and fully rendered
- Each panel should have equal visual weight and detail

Panel layout:
[Panel 1] [Panel 2]
[Panel 3] [Panel 4]

Panel content requirements:
- Panel 1: Show the beginning of the story with clear character introduction
- Panel 2: Display the development or conflict part of the story
- Panel 3: Show the climax or main action of the story
- Panel 4: Display the conclusion or resolution - this panel is crucial and must be fully rendered

{language_requirement}

Each panel should visually represent the corresponding part of the story description with clear scene composition, character expressions, appropriate backgrounds, and dialogue/text in the specified language where applicable. Pay special attention to making sure the fourth panel is complete and detailed.
"""

    print("🖼️ 正在使用 Imagen 4.0 生成四格漫畫...")
    
    response = client.models.generate_images(
        model='imagen-4.0-generate-preview-06-06',
        prompt=image_prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )
    
    print(f"✅ 成功生成 {len(response.generated_images)} 張圖片")
    
    # 創建輸出資料夾
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    main_output_dir = "outputs"
    folder_name = os.path.join(main_output_dir, f"comic_generation_{timestamp}")
    
    if not os.path.exists(main_output_dir):
        os.makedirs(main_output_dir)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    # 保存生成的圖片
    image_saved = False
    image_path = None
    
    for i, generated_image in enumerate(response.generated_images):
        try:
            # 生成檔名
            image_filename = f"comic_4panel.png"
            image_path = os.path.join(folder_name, image_filename)
            
            # 直接保存圖片
            generated_image.image.save(image_path)
            print(f"🎉 四格漫畫已保存為 {image_path}")
            image_saved = True
            break  # 只保存第一張圖片
            
        except Exception as save_error:
            print(f"❌ 保存圖片時發生錯誤：{save_error}")
            # 如果是 bytes 資料，嘗試轉換
            try:
                if isinstance(generated_image.image, bytes):
                    image = Image.open(BytesIO(generated_image.image))
                    image_filename = f"comic_4panel.png"
                    image_path = os.path.join(folder_name, image_filename)
                    image.save(image_path)
                    print(f"🎉 四格漫畫已保存為 {image_path}")
                    image_saved = True
                    break
            except Exception as e2:
                print(f"❌ 所有保存方法都失敗：{e2}")
    
    # 只有在成功保存圖片後才保存記錄
    if image_saved and image_path:
        # 保存生成記錄
        generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        language_map = {"1": "繁體中文", "2": "English", "3": "简体中文"}
        selected_language = language_map.get(language_choice, "繁體中文")
        
        record = {
            "generation_time": generation_time,
            "story_input": story,
            "language_selection": selected_language,
            "description_text": description_text,
            "image_file": image_filename,
            "model_used": "imagen-4.0-generate-preview-06-06",
            "text_model_used": "gemini-2.0-flash-exp"
        }
        
        # 保存 JSON 記錄
        record_path = os.path.join(folder_name, "generation_record.json")
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        
        # 保存純文本描述
        description_path = os.path.join(folder_name, "comic_description.txt")
        with open(description_path, "w", encoding="utf-8") as f:
            f.write(description_text)
        
        # 保存故事輸入
        story_path = os.path.join(folder_name, "original_story.txt")
        with open(story_path, "w", encoding="utf-8") as f:
            f.write(story)
        
        print(f"\n📋 生成記錄已保存：")
        print(f"   - 完整記錄：{record_path}")
        print(f"   - 描述文本：{description_path}")
        print(f"   - 原始故事：{story_path}")
        
        print("\n" + "="*60)
        print("🎉 四格漫畫生成完成！")
        print(f"📁 輸出資料夾：{folder_name}")
        print(f"🖼️ 漫畫圖片：{image_filename}")
        print(f"⏰ 生成時間：{generation_time}")
        print("="*60)
    else:
        print("❌ 圖片保存失敗，無法創建完整記錄")

except Exception as e:
    print(f"❌ 生成失敗：{e}")
    print("💡 建議檢查：")
    print("   1. API 金鑰是否正確設定")
    print("   2. 是否有權限使用相關模型")
    print("   3. 網路連接是否正常")
    print("   4. 請確認已安裝最新版本：pip install google-genai")