import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import google.generativeai as genai

# 設定 Gemini 圖片模型 API 金鑰
genai.configure(api_key="AIzaSyDkrPZHbSyw6BLRXYiGRumRipboPD3e1F4")
model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")

# 換行工具函式
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        width, _ = font.getsize(test_line)
        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

# 讀取 comic_panels.json
with open("comic_panels.json", "r", encoding="utf-8") as f:
    data = json.load(f)

character_styles = data["character_styles"]
panels = data["panels"]
role_names = list(character_styles.keys())

# 整理角色描述
characters_description = "\n".join([
    f"- {name}: {character_styles[name]}" for name in role_names
])

for idx, panel in enumerate(panels, 1):
    # 整理表情
    expressions = ", ".join([
        f"{name}: {panel['expressions'][name]}" for name in role_names if name in panel['expressions']
    ])

    # 合併所有 dialogue 欄位，去掉角色名部分（冒號左邊）
    dialogue_lines = []
    for key in panel:
        if key.startswith("dialogue") or key == "dialogue":
            line = panel[key]
            if "\uff1a" in line:  # 全形冒號
                line = line.split("\uff1a", 1)[1]
            elif ":" in line:
                line = line.split(":", 1)[1]
            dialogue_lines.append(line.strip())
    dialogue_text = "\n".join(dialogue_lines)

    # 不含文字的圖片 prompt
    prompt_img = f"""
Create a single comic panel sized approximately 100x100 pixels.

Scene description:
{panel['scene']}
{panel['action']}

Characters and style:
{characters_description}
- Cartoon style, expressive and dynamic poses, clean lines.

Expressions:
{expressions}

Do NOT include any text, dialogue, or speech bubbles in the image.
The overall style should be colorful and visually engaging.
"""

    try:
        response = model.generate_content(
            [prompt_img],
            generation_config={"response_modalities": ["TEXT", "IMAGE"]}
        )
        for part in response.parts:
            if hasattr(part, 'inline_data') and part.inline_data and getattr(part.inline_data, 'data', None):
                image_data = BytesIO(part.inline_data.data)
                image = Image.open(image_data)
                image = image.resize((1000, 1000), Image.LANCZOS)

                # 儲存無文字圖
                filename = f"comic_panel_{idx}_no_text.png"
                image.save(filename)
                print(f"🖼️ {filename} 已儲存")

                # 疊加文字版本
                try:
                    font = ImageFont.truetype("NotoSansTC-Regular.ttf", 40)
                except OSError:
                    print("⚠️ 缺字型 fallback to default (不支援中文)")
                    font = ImageFont.load_default()

                draw = ImageDraw.Draw(image)
                wrapped_lines = wrap_text(dialogue_text, font, 960)
                y = 900
                for line in wrapped_lines:
                    draw.text((20, y), line, fill="black", font=font)
                    y += font.getsize(line)[1] + 10

                image.save(f"comic_panel_{idx}_with_text.png")
                print(f"🖼️ comic_panel_{idx}_with_text.png 已儲存")
            else:
                print(f"Panel {idx} Dialogue:\n{dialogue_text}")
    except Exception as e:
        print(f"❌ 第 {idx} 格圖片生成錯誤：{e}")