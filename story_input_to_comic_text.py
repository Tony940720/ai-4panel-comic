import google.generativeai as genai

genai.configure(api_key="AIzaSyDkrPZHbSyw6BLRXYiGRumRipboPD3e1F4")

model = genai.GenerativeModel("gemini-2.5-flash")

# 讓使用者輸入故事
story = input("請輸入你的漫畫故事內容：\n")
# 一隻狗狗在公園遇到貓咪，他熱情地打招呼並邀請貓咪玩球，貓咪一開始有點害羞，但後來玩得很開心。他們一起跑來跑去，最後躺在草地上看著天空，大笑不止。

# prompt = f"""
# 我會提供一段漫畫故事文字，請你根據故事生成一個詳細的四格漫畫視覺描述文本。

# 請嚴格按照以下官方範例格式生成，必須是單一段落的連續描述：

# 官方範例格式：
# "This four-panel comic strip uses a charming, deliberately pixelated art style reminiscent of classic 8-bit video games, featuring simple shapes and a limited, bright color palette dominated by greens, blues, browns, and the dinosaur's iconic grey/black. The setting is a stylized pixel beach. Panel one shows the familiar Google Chrome T-Rex dinosaur, complete with its characteristic pixelated form, wearing tiny pixel sunglasses and lounging on a pixelated beach towel under a blocky yellow sun. Pixelated palm trees sway gently in the background against a blue pixel sky. A caption box with pixelated font reads, "Even error messages need a vacation." Panel two is a close-up of the T-Rex attempting to build a pixel sandcastle. It awkwardly pats a mound of brown pixels with its tiny pixel arms, looking focused. Small pixelated shells dot the sand around it. Panel three depicts the T-Rex joyfully hopping over a series of pixelated cacti planted near the beach, mimicking its game obstacle avoidance. Small "Boing! Boing!" sound effect text appears in a blocky font above each jump. A pixelated crab watches from the side, waving its pixel claw. The final panel shows the T-Rex floating peacefully on its back in the blocky blue pixel water, sunglasses still on, with a contented expression. A small thought bubble above it contains pixelated "Zzz ... " indicating relaxation."

# 核心要求（專注視覺描述）：
# 1. 必須生成一個完整的英文段落，不要分行、分段或使用引號包圍
# 2. 開頭必須描述整體藝術風格（art style）和色彩調色盤（color palette）
# 3. 接著描述整體場景設定（setting）
# 4. 然後按順序描述四格，確保每格都有完整描述：
#    - Panel one shows... (第一格的詳細視覺描述)
#    - Panel two... (第二格的詳細視覺描述)  
#    - Panel three depicts... (第三格的詳細視覺描述)
#    - The final panel shows... (第四格的詳細視覺描述)

# 視覺描述重點：
# - 每格重點描述：角色姿勢、表情、動作、場景元素、背景細節
# - 對話和音效只需簡單提及，不要過度描述內容
# - 專注於構圖、色彩、視覺元素和角色互動
# - 確保四格都有均等且完整的描述篇幅
# - 每格描述應該包含足夠的視覺細節供 AI 圖像生成使用

# 格式要求：
# - 整個描述要自然流暢連貫
# - 不要在開頭和結尾加上任何額外的引號或格式標記
# - 確保 "The final panel" 部分有完整且詳細的描述

# 請根據以下故事生成完全符合上述格式的四格漫畫視覺描述：
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
    response = model.generate_content(prompt)
    print("🔍 生成的漫畫描述文本：\n")
    print(response.text)

    # 儲存文字結果
    with open("comic_description.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("\n✅ 已儲存為 comic_description.txt，可用作漫畫生成的詳細描述文本")

except Exception as e:
    print("⚠️ 發生錯誤：", e)
