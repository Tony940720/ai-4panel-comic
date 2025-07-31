import google.generativeai as genai

genai.configure(api_key="AIzaSyDkrPZHbSyw6BLRXYiGRumRipboPD3e1F4")

model = genai.GenerativeModel("gemini-2.5-flash")

# 讓使用者輸入故事
story = input("請輸入你的漫畫故事內容：\n")
# 一隻狗狗在公園遇到貓咪，他熱情地打招呼並邀請貓咪玩球，貓咪一開始有點害羞，但後來玩得很開心。他們一起跑來跑去，最後躺在草地上看著天空，大笑不止。

prompt = f"""
我會提供一段漫畫故事文字，請你根據故事幫我完成兩件事：

1. 生成角色風格(character_styles)，以 dictionary 形式輸出，每個角色名稱對應一段描述，描述角色的外觀、服裝、風格等。

2. 將故事拆成四格漫畫內容(panels)，每格是一個 dictionary，包含：
  - "scene"：背景或場景
  - "action"：角色正在做什麼
  - "expressions"：字典，角色名字對應當格的表情
  - "dialogue"：兩個角色對話內容

請輸出一個 dictionary，結構如下：
expressions敘述和character_styles保持使用角色1和角色2
{{
  "character_styles": {{
    "角色1": "角色1的風格描述",
    "角色2": "角色2的風格描述"
  }},
  "panels": [
    {{
      "scene": "...",
      "action": "...",
      "expressions": {{
        "角色1": "...",
        "角色2": "..."
      }},
      "dialogue": "..."
    }},
    ...
  ]
}}
請只保留大括號 { ... } 之間的內容，並移除所有 json、 和註解行。
故事是：
{story}
"""

try:
    response = model.generate_content(prompt)
    print("🔍 生成的漫畫文字：\n")
    print(response.text)

    # 儲存文字結果
    with open("comic_panels.json", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("\n✅ 已儲存為 comic_panels.json，可用來生成漫畫圖片")

except Exception as e:
    print("⚠️ 發生錯誤：", e)