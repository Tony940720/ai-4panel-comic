from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os
import uuid

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))


# contents = """
# {
#   "style": "4-panel comic, humorous, anime-inspired, expressive, dynamic poses, consistent lighting, text integrated in speech bubbles or narration boxes.",
#   "panels": [
#     {
#       "description": "Living room with a modern design. A sofa with cushions, a coffee table with magazines, and a TV showing a heatwave warning. Otaku is wearing a tank top and shorts, slouched on the sofa, sweating heavily. He uses a TV remote to fan himself.",
#       "text": "It’s so hot… I’m starting to question life… What happened to saving energy and reducing carbon emissions?!"
#     },
#     {
#       "description": "A suburban street under the blazing sun. The asphalt looks like it's melting, with visible heatwaves. Otaku steps out of his house, holding an empty wallet, walking towards an ice cream shop. He shades his eyes with one hand, looking exhausted.",
#       "text": "For ice cream… I’m willing to endure all this… (Inner monologue: Should’ve ordered online…)"
#     },
#     {
#       "description": "In front of a small ice cream shop with colorful decorations. Otaku finally gets a popsicle. Dark clouds suddenly roll in, and thunder rumbles. The popsicle starts melting and dripping on his hand as he stares up in disbelief.",
#       "text": "Narration: Afternoon thunderstorm now spreading to areas south of Hsinchu! Speech: Are you kidding me, universe?!"
#     },
#     {
#       "description": "Living room with dim lighting. Otaku is wrapped in a thick blanket, pale and shivering with two lines of snot under his nose. He holds a half-melted ice pop. A heater is visible in the corner.",
#       "text": "Hot… cold… What do you want from me?!! (SFX: cough cough)"
#     }
#   ]
# }
# """
contents = """
{
  Prompt: This four-panel comic strip uses a charming, deliberately pixelated art style
reminiscent of classic 8-bit video games, featuring simple shapes and a limited, bright color
palette dominated by greens, blues, browns, and the dinosaur's iconic grey/black. The setting
is a stylized pixel beach. Panel one shows the familiar Google Chrome T-Rex dinosaur,
complete with its characteristic pixelated form, wearing tiny pixel sunglasses and lounging on a
pixelated beach towel under a blocky yellow sun. Pixelated palm trees sway gently in the
background against a blue pixel sky. A caption box with pixelated font reads, "Even error
messages need a vacation." Panel two is a close-up of the T-Rex attempting to build a pixel
sandcastle. It awkwardly pats a mound of brown pixels with its tiny pixel arms, looking focused.
Small pixelated shells dot the sand around it. Panel three depicts the T-Rex joyfully hopping
over a series of pixelated cacti planted near the beach, mimicking its game obstacle
avoidance. Small "Boing! Boing!" sound effect text appears in a blocky font above each jump. A
pixelated crab watches from the side, waving its pixel claw. The final panel shows the T-Rex
floating peacefully on its back in the blocky blue pixel water, sunglasses still on, with a
contented expression. A small thought bubble above it contains pixelated "Zzz ... " indicating
relaxation.
}
"""

response = client.models.generate_content(
    model="gemini-2.0-flash-preview-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    unique_filename = f"gemini-native-image-{uuid.uuid4().hex}.png"
    image = Image.open(BytesIO((part.inline_data.data)))
    image.save(unique_filename)
    image.show()