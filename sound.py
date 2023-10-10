import os
from playsound import playsound

def play_sound(sound_file):
    try:
        # Search for the sound file in the current directory
        files = os.listdir()
        for file in files:
            if file.lower().endswith(sound_file.lower()):
                sound_file = file
                break

        # Play the sound file
        playsound(sound_file)
    except Exception as e:
        print("Error occurred while playing sound:", str(e))

# Provide the sound file name (including extension)
sound_file = "alert.wav"

# Call the function to play the sound
play_sound(sound_file)

