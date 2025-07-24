import google.generativeai as genai
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

genai.configure = api_key=os.getenv('GEMINI_API_KEY')
model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")

character_styles = {
    "dog": "A cheerful dog, brown fur, wearing a red scarf, big round eyes, cartoon style",
    "cat": "A clever cat, white fur, wearing glasses, blue bow tie, cartoon style"
}

panels = [
    {
        "action": "The dog and cat meet in the park, both looking surprised.",
        "expression": "Dog: surprised, Cat: surprised",
        "dialogue": "Dog: Hi there! Want to play?\nCat: Oh, sure!"
    },
    {
        "action": "The dog offers a ball to the cat, the cat looks curious.",
        "expression": "Dog: friendly, Cat: curious",
        "dialogue": "Dog: Here, catch this!\nCat: What is it?"
    },
    {
        "action": "The cat throws the ball, the dog chases after it excitedly.",
        "expression": "Cat: playful, Dog: excited",
        "dialogue": "Cat: Fetch it, if you can!\nDog: I'm on it!"
    },
    {
        "action": "The dog returns with the ball, both characters smile happily.",
        "expression": "Dog: happy, Cat: happy",
        "dialogue": "Dog: That was fun!\nCat: Let's play again!"
    }
]

for idx, panel in enumerate(panels, 1):
    # 1. 生成沒有對話的圖片
    prompt = f"""
The panel should be a cartoon illustration of the scene:
{panel["action"]}
Characters:
dog: {character_styles["dog"]}
cat: {character_styles["cat"]}
Expression:
{panel["expression"]}
Do NOT include any dialogue or text in the image.
"""
    response = model.generate_content(
        [prompt],
        generation_config={
            "response_modalities": ["TEXT", "IMAGE"]
        }
    )
    for part in response.parts:
        if hasattr(part, 'inline_data') and part.inline_data and getattr(part.inline_data, "mime_type", "").startswith("image"):
            if part.inline_data.data:
                image_data = BytesIO(part.inline_data.data)
                try:
                    image = Image.open(image_data).convert("RGBA")
                except Exception as e:
                    print(f"Panel {idx} 圖片解析失敗: {e}")
                    continue
                # 2. 在圖片下方加上對話文字
                width, height = image.size
                extra_height = int(height * 0.25)
                new_img = Image.new("RGBA", (width, height + extra_height), (255, 255, 255, 255))
                new_img.paste(image, (0, 0))
                draw = ImageDraw.Draw(new_img)
                # 你可以指定字型路徑
                try:
                    font = ImageFont.truetype("arial.ttf", 24)
                except:
                    font = ImageFont.load_default()
                text = panel["dialogue"]
                draw.multiline_text((20, height + 10), text, fill=(0, 0, 0), font=font)
                new_img.save(f"comic_panel_{idx}.png")
                new_img.show()
        elif hasattr(part, 'text') and part.text:
            print(f"Panel {idx} Text output:\n", part.text)