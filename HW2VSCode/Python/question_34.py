import os
"""
Final Clean Version: Multi-voice OpenAI TTS with Effects
 Cycles through multiple voices
 Applies random speed and pitch effects
 Combines all audio into one MP3 file
 Easy user customization section
"""

import random
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

# Load API key
load_dotenv(dotenv_path="../.env")
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# === USER CONFIGURATION SECTION ===
# Customize your narration text here:
custom_text = [
    "Pizza is the best food for any occasion.",
    "Nothing beats a fresh slice of pepperoni pizza.",
    "Did you know pineapple on pizza is actually delicious?",
    "Cheese, sauce, and crust: the holy trinity of pizza.",
    "Pizza parties bring people together.",
    "Thin crust or deep dish, pizza always wins.",
    "Pizza delivery is a modern miracle.",
    "Cold pizza for breakfast is underrated.",
    "Making pizza at home is a fun activity.",
    "Pizza toppings are a personal choice."
]
# How many lines to use (randomly selected)
num_lines = 4
narrations = random.sample(custom_text, num_lines)

# Customize voices here (must be supported by OpenAI TTS)
voices = ["onyx", "nova", "echo", "fable", "shimmer"]

# Customize effects here
speed_range = (0.8, 1.2)      # Min and max speed multiplier
pitch_range = (-2, 2)         # Min and max pitch in semitones
# === END USER CONFIGURATION ===

# Helper functions for effects
def change_speed(sound, speed=1.0):
    return sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * speed)}).set_frame_rate(sound.frame_rate)

def change_pitch(sound, semitones=0):
    new_sample_rate = int(sound.frame_rate * (2.0 ** (semitones / 12.0)))
    return sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate}).set_frame_rate(sound.frame_rate)

combined = AudioSegment.empty()

for text in narrations:
    for voice in voices:
        print(f"Narrating: '{text}' with voice '{voice}'")
        response = client.audio.speech.create(
            model="tts-1",
            input=text,
            voice=voice
        )
        temp_filename = f"temp_{voice}.mp3"
        with open(temp_filename, "wb") as out:
            out.write(response.content)
        segment = AudioSegment.from_file(temp_filename, format="mp3")
    # Apply random speed and pitch effects from user config
    speed = random.uniform(*speed_range)
    semitones = random.randint(*pitch_range)
    segment = change_speed(segment, speed)
    segment = change_pitch(segment, semitones)
    print(f"Applied effects: speed={speed:.2f}x, pitch={semitones} semitones")
    combined += segment
    os.remove(temp_filename)

combined.export("combined_output.mp3", format="mp3")
print("All narrations saved to combined_output.mp3")