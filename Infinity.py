import pvporcupine
import speech_recognition as sr
import requests
import pyaudio
import struct
import pyttsx3
import random
import webbrowser
import subprocess
import os
from urllib.parse import quote  # Added for URL encoding
import pygame
from dotenv import load_dotenv

load_dotenv()

# Text-to-Speech Initialization with Female Voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

# Initialize Porcupine and PyAudio
porcupine = pvporcupine.create(
    access_key=os.getenv("API_PORCUPINE"),  
    keyword_paths=['I.ppn']
)
pyaudio_instance = pyaudio.PyAudio()
audio_stream = pyaudio_instance.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def speak(text):
    """Text-to-Speech Conversion with Female Voice"""
    engine.say(text)
    engine.runAndWait()

def get_random_greeting():
    """Generate random female-voiced greetings"""
    greetings = [
        "Hi Infinity here! How can I help you today?",
        "Hello there, what can I do for you?",
        "Hey ! I'm ready to assist you.",
        "What would you like me to do for you?"
    ]
    return random.choice(greetings)

def ask_question(api_key, question):
    """Improved OpenRouter AI Query"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://my-assistant-app.com",  # Required header
        "X-Title": "Personal Assistant",                # Recommended header
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gryphe/mythomax-l2-13b",  # Better model choice
        "messages": [
            {"role": "system", "content": "You are a helpful female assistant. Respond in clear, conversational English."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 500,  # Increased token limit
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        
        if not response_json.get("choices"):
            return "No response generated"
            
        message = response_json["choices"][0].get("message", {})
        return message.get("content", "Empty response received")
        
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return "Connection error. Please try again."
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I'm having trouble understanding right now."

def system_commands(command):
    """Enhanced System Commands"""
    cmd = command.lower()
    commands = {
        "open browser": lambda: webbrowser.open('https://www.google.com'),
        "calculator": lambda: subprocess.Popen('calc.exe'),
        "notepad": lambda: subprocess.Popen('notepad.exe'),
        "shutdown": lambda: os.system("shutdown /s /t 1"),
        "restart": lambda: os.system("shutdown /r /t 1"),
        "weather": lambda: webbrowser.open('https://www.accuweather.com'),
        "email": lambda: webbrowser.open('https://mail.google.com'),
        "pause music": lambda: pygame.mixer.music.pause() if pygame.mixer.get_init() else None,
        "resume music": lambda: pygame.mixer.music.unpause() if pygame.mixer.get_init() else None,
        "stop music": lambda: stop_local_music()
    }
    
    for key, func in commands.items():
        if key in cmd:
            return func()
    
    return None

def search_web(query):
    """Perform web search with proper encoding"""
    try:
        encoded_query = quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        webbrowser.open_new_tab(search_url)
        return f"Showing results for {query}"
    except Exception as e:
        print(f"Search error: {e}")
        return "Sorry darling, I couldn't complete that search"

def play_youtube_music(query):
    """Open YouTube search results for the query"""
    encoded_query = quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    webbrowser.open_new_tab(url)
    return f"Searching {query} on YouTube"

def play_local_music(file_path):
    """Play local music files using pygame"""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        return f"Now playing {os.path.basename(file_path)}"
    except pygame.error as e:
        print(f"Pygame error: {e}")
        return "Sorry love, I can't find the music file"
    except Exception as e:
        print(f"Music play error: {e}")
        return "Sorry love, I had trouble playing that"

def stop_local_music():
    """Stop local music playback"""
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()  # Unload the music
        pygame.mixer.quit()  # Quit the mixer
        return "Music stopped"
    return "No music is currently playing."

def voice_input(timeout=5):
    """Enhanced Voice Input with Better Handling"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening carefully...")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=8)
            
            recognized_text = r.recognize_google(audio).lower()
            print(f"Recognized: {recognized_text}")
            
            # Exit command handling
            if "stop" in recognized_text or "exit" in recognized_text:
                speak("Goodbye have a nice Day!")
                exit()
                
            return recognized_text
            
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Google API error: {e}")
        except Exception as e:
            print(f"Voice input error: {e}")
            
        return ""

def trigger_voice_assistant():
    """Main Voice Assistant Workflow"""
    api_key = os.getenv("API_OPENROUTER")  # Replace with your API key
    
    speak(get_random_greeting())
    
    question = voice_input()
    if not question:
        speak("Sorry, can you repeat that?")
        return

    print(f"Your request: {question}")

# Handle music commands first
    if 'youtube' in question or 'play' in question:
        query = question.replace('youtube', '').replace('play', '').strip()
        if 'local' in query:
            # Assuming you have a default music directory
            music_directory = "Music"  
            if os.path.exists(music_directory):
                music_files = [f for f in os.listdir(music_directory) if f.endswith(('.mp3', '.wav', '.ogg'))]
                if music_files:
                    music_file_path = os.path.join(music_directory, random.choice(music_files))
                    result = play_local_music(music_file_path)
                    speak(result)
                else:
                    speak("Sorry, no music files found in that directory.")
            else:
                speak("Sorry, I can't access the music directory.")
        elif query:
            result = play_youtube_music(query)
            speak(result)
        else:
            speak("What would you like me to play, darling?")
        return

    # Handle search commands next
    if 'search' in question:
        parts = question.split('search', 1)
        query = parts[1].strip() if len(parts) > 1 else ''
        if query:
            result = search_web(query)
            speak(result)
        else:
            speak("What would you like me to search for, darling?")
        return

    # Handle system commands
    system_result = system_commands(question)
    if system_result is not None:
        speak(f"Executing your command: {question}")
        return

    # Process AI query
    result = ask_question(api_key, question)
    
    if result.strip():
        speak(result)
        print(f"Assistant: {result}")
    else:
        speak("Sorry darling, I didn't get a proper response. Could you rephrase that?")

def listen_for_wake():
    """Wake Word Detection Loop"""
    print("Waiting for your call...")
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        if porcupine.process(pcm) >= 0:
            trigger_voice_assistant()

if __name__ == "__main__":
    try:
        listen_for_wake()
    except KeyboardInterrupt:
        speak("Goodbye have a nice Day!")
        print("Assistant terminated")
    finally:
        # Ensure proper cleanup
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        audio_stream.close()
        pyaudio_instance.terminate()
        porcupine.delete()


