import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def parse_design_prompt(base_color, design_prompt):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    model = "gemini-2.0-flash"

    prompt = f"""
You are an AI assistant that prepares prompts for t-shirt image generation.

Given a base t-shirt color and a general design idea, do the following:
1. Extract the design separately for the FRONT and BACK of the t-shirt.
2. Enhance both prompts with extra visual details so that an image generation model can understand them better (e.g., add art style, colors, placement, etc.)
3. If there's no back design mentioned, return "plain" for the back.

Input:
Base Color: {base_color}
Design Description: {design_prompt}

Output Format:
Front: <enhanced front design prompt>
Back: <enhanced back design prompt or plain>
"""

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    config = types.GenerateContentConfig(response_mime_type="text/plain")

    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        output += chunk.text

    # Basic parsing
    lines = output.strip().splitlines()
    front, back = "unknown", "plain"

    for line in lines:
        if line.lower().startswith("front:"):
            front = line.split(":", 1)[1].strip()
        elif line.lower().startswith("back:"):
            back = line.split(":", 1)[1].strip()

    return front, back
