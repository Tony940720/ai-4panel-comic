import json
from google.generativeai import GenerativeModel, configure
from PIL import Image
from io import BytesIO

# 設定 Gemini API 金鑰
configure(api_key="AIzaSyDkrPZHbSyw6BLRXYiGRumRipboPD3e1F4")
model = GenerativeModel("gemini-2.0-flash-preview-image-generation")

# 讀取前面產生的 comic_panels.json
with open("comic_panels.json", "r", encoding="utf-8") as f:
    data = json.load(f)

character_styles = data["character_styles"]
panels = data["panels"]

# 所有角色名稱
role_names = list(character_styles.keys())

# 組合角色外觀描述
characters_description = "\n".join([
    f"{name}: {character_styles[name]}" for name in role_names
])

# 對每一格漫畫進行圖片生成
for idx, panel in enumerate(panels, 1):
    # 每格角色表情
    expressions_description = ", ".join([
        f"{name}: {panel['expressions'][name]}" for name in role_names
    ])
    
    dialogue = panel["dialogue"]

    # 組合 prompt
    prompt = f"""
Create 1 panel of a comic style image.
Top 60%: A cartoon illustration of this scene:
Scene: {panel['scene']}
Action: {panel['action']}

Characters:
{characters_description}

Expressions:
{expressions_description}

Bottom 40%: Display this comic dialogue:
{dialogue}

The dialogue must be readable and visually separated from the illustration.
"""

    print(f"🖼️ 生成第 {idx} 格漫畫...")

    try:
        response = model.generate_content(
            [prompt],
            generation_config={"response_modalities": ["TEXT", "IMAGE"]}
        )

        for part in response.parts:
            if hasattr(part, "inline_data"):
                image_data = BytesIO(part.inline_data.data)
                image = Image.open(image_data)
                image.save(f"comic_panel_{idx}.png")
                print(f"✅ 已儲存 comic_panel_{idx}.png")
            elif hasattr(part, "text") and part.text:
                print(f"⚠️ Gemini 的文字回應：\n{part.text}")

    except Exception as e:
        print(f"❌ 第 {idx} 格圖片生成失敗：{e}")
