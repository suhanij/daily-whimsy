import anthropic
import json
import os
from datetime import datetime

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

today = datetime.now().strftime("%B %d, %Y")

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=400,
    messages=[
        {
            "role": "user",
            "content": f"""You are generating a daily whimsy tarot card for a magical, whimsical website. 
Today is {today}.

Generate ONE unique card. Return ONLY valid JSON with no extra text, no markdown, no explanation. 
Respond with exactly this structure:
{{
  "date": "{today}",
  "title": "The [Whimsical Name]",
  "affirmation": "A full, complete, warm affirmation of 1-3 sentences. No dashes. Must feel handwritten and magical.",
  "emoji_theme": "one or two words describing the visual theme (e.g. forest fairy, ocean, moon, mushroom, frog wizard)"
}}

The title should be poetic and whimsical. The affirmation should feel like it was written by a kind forest witch who loves you.
Do NOT use any of these titles: The Moon Child, The Wizard Frog, The Mushroom Oracle, The Metamorphosis, The Bloom, The Star Child, The Ocean Baby, The Silly Goose, The Castle Seeker, The Forest Fairy, The Sunflower, The Gentle One."""
        }
    ]
)

raw = message.content[0].text.strip()
# Clean up in case model adds backticks
if raw.startswith("```"):
    raw = raw.split("```")[1]
    if raw.startswith("json"):
        raw = raw[4:]
raw = raw.strip()

card_data = json.loads(raw)

# Write to file that the website reads
with open("daily_card.json", "w") as f:
    json.dump(card_data, f, indent=2)

print(f"Generated card: {card_data['title']}")
print(f"Affirmation: {card_data['affirmation']}")
