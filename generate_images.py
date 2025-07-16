import mimetypes
from google import genai
from google.genai import types
import os

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"✅ Image saved to: {file_name}")

def generate_image(prompt, file_prefix):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash-preview-image-generation"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]

    config = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        response_mime_type="text/plain",
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        if (
            chunk.candidates
            and chunk.candidates[0].content
            and chunk.candidates[0].content.parts
        ):
            part = chunk.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                inline_data = part.inline_data
                data_buffer = inline_data.data
                file_ext = mimetypes.guess_extension(inline_data.mime_type)
                file_name = f"{file_prefix}{file_index}{file_ext}"
                save_binary_file(file_name, data_buffer)
                return file_name  # return image path
        elif hasattr(chunk, "text"):
            print("💬 Gemini text response:", chunk.text)

    print("⚠️ No image was generated.")
    return None




