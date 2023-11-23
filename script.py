import wave
import struct
from PIL import Image
import sys
import os

def embed_audio_into_image(input_audio_path, input_image_path, output_image_path):
    # Read the audio file
    with wave.open(input_audio_path, 'rb') as audio_file:
        audio_bytes = audio_file.readframes(audio_file.getnframes())

    # Load the image
    image = Image.open(input_image_path)
    image = image.convert("RGBA")
    pixels = image.load()

    # Embed audio data into the image
    idx = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, a = pixels[i, j]
            if idx < len(audio_bytes):
                a = audio_bytes[idx]
                idx += 1
            pixels[i, j] = (r, g, b, a)

    # Save the modified image
    image.save(output_image_path, "PNG")

def extract_audio_from_image(input_image_path, output_audio_path):
    # Load the image
    image = Image.open(input_image_path)
    image = image.convert("RGBA")
    pixels = image.load()

    # Extract audio data from the image
    audio_data = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b, a = pixels[i, j]
            audio_data.append(a)

    # Convert integers back to bytes
    audio_bytes = struct.pack('<{}B'.format(len(audio_data)), *audio_data)

    # Write to a wave file
    with wave.open(output_audio_path, 'wb') as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(1)
        audio_file.setframerate(44100)
        audio_file.writeframes(audio_bytes)

def verify_embedding(original_audio_path, extracted_audio_path):
    with open(original_audio_path, 'rb') as original_file:
        original_data = original_file.read()
    with open(extracted_audio_path, 'rb') as extracted_file:
        extracted_data = extracted_file.read()
    
    return original_data == extracted_data

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 script.py <image_path> <audio_path> <output_image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    audio_path = sys.argv[2]
    output_image_path = sys.argv[3]
    
    embed_audio_into_image(audio_path, image_path, output_image_path)
    print(f"Audio has been embedded into {output_image_path}.")
    
    # For verification
    temp_extracted_audio = 'temp_extracted_audio.wav'
    extract_audio_from_image(output_image_path, temp_extracted_audio)
    if verify_embedding(audio_path, temp_extracted_audio):
        print("Verification successful: The audio was correctly embedded.")
    else:
        print("Verification failed: The audio was not correctly embedded.")
    
    # Cleanup temporary files
    os.remove(temp_extracted_audio)




# how to run:
# python3 script.py picture.jpg test.wav output.png