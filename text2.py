import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# 設定 API Key
genai.configure(api_key="AIzaSyDkrPZHbSyw6BLRXYiGRumRipboPD3e1F4")
model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")

character_styles = {
    "robot": "Robot named Byte: silver body, blue LED eyes, antenna on head, expressive face, always wears a yellow scarf",
    "bird": "Bird named Pixel: bright green feathers, big round eyes, tiny orange beak, wears a red cap"
}

panels = [
    {
        "action": "In a sunny park, Byte the robot is reading a book on a bench. Pixel the bird lands next to him, looking curious.",
        "expression": "Byte: focused, Pixel: curious",
        "dialogue": "What are you reading?\nIt's a book about human inventions!"
    },
    {
        "action": "Pixel flaps his wings excitedly, while Byte shows a page with a picture of a paper airplane.",
        "expression": "Pixel: excited, Byte: proud",
        "dialogue": "Can we try making one?\nAbsolutely!"
    },
    {
        "action": "Byte folds a paper airplane, Pixel watches closely, eyes wide with anticipation.",
        "expression": "Byte: concentrated, Pixel: eager",
        "dialogue": "Ready?\nReady!"
    },
    {
        "action": "The paper airplane soars through the air. Pixel and Byte cheer, both looking delighted as the plane glides above the park.",
        "expression": "Byte: joyful, Pixel: amazed",
        "dialogue": "Wow, it really flies!\nTeamwork makes everything possible!"
    }
]

for idx, panel in enumerate(panels, 1):
    prompt = f"""
Create a single comic panel sized approximately 100x100 pixels.

Scene description:
{panel['action']}

Characters and style:
- {character_styles['robot']}.
- {character_styles['bird']}.
- Cartoon style, consistent character design, expressive and dynamic poses.

Expressions:
{panel['expression']}

Do NOT include any text, dialogue, or speech bubbles in the image.
The overall style should be humorous, colorful, bright lighting, clean lines, and visually engaging.
Make sure the image does not contain any written words.
Do your best to fit the image size around 100x100 pixels.
"""

    response = model.generate_content(
        [prompt],
        generation_config={
            "response_modalities": ["TEXT", "IMAGE"]
        }
    )

    for part in response.parts:
        if hasattr(part, 'inline_data') and part.inline_data and getattr(part.inline_data, 'data', None):
            image_data = BytesIO(part.inline_data.data)
            try:
                image = Image.open(image_data)
                # 強制縮放成 1000x1000
                image = image.resize((1000, 1000), Image.LANCZOS)
                filename = f"comic_panel_{idx}_no_text.png"
                image.save(filename)
                print(f"Panel {idx} image saved as {filename}")
                image.show()
            except Exception as e:
                print(f"Panel {idx} image error:", e)
        # 忽略 part.text 及其他內容
