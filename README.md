# Infinity

Infinity is a voice-enabled assistant that uses [Porcupine](https://picovoice.ai/platform/porcupine/) for wake-word detection and [OpenRouter](https://openrouter.ai/) for advanced language model integrations.

## Table of Contents
1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [Usage](#usage)
5. [Additional Notes](#additional-notes)
6. [License](#license)

---

## Dependencies

Infinity relies on the following packages and libraries (already listed in `requirements.txt`):
- **pyporcupine** (Porcupine wake-word engine)
- **speech_recognition** (Speech-to-text recognition)
- **requests** (HTTP requests)
- **pyaudio** (Audio handling)
- **struct** (Binary data parsing)
- **pyttsx3** (Text-to-speech)
- **random** (Randomization)
- **webbrowser** (Open URLs in a browser)
- **subprocess** (Spawn and manage subprocesses)
- **os** (Operating system interfaces)
- **python-dotenv** (Loading environment variables from `.env`)
- **pygame** (Additional audio/GUI functionality)

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/infinity.git
   cd infinity
   ```

2. **Create a Virtual Environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows, use: venv\Scripts\activate
   ```

3. **Install the Dependencies**

   Make sure you have [pip](https://pip.pypa.io/en/stable/) installed and run:

   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

Create a file named `.env` in the root of the project (same folder as `infinity.py`) and add the following variables:

```dotenv
# Porcupine API
PORCUPINE_API_KEY=YOUR_PORCUPINE_API_KEY
PORCUPINE_LOGIN_URL=https://console.picovoice.ai

# OpenRouter API
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
OPENROUTER_LOGIN_URL=https://openrouter.ai/login
```

> **Note**:  
> - Sign up or log in to [Porcupine’s console](https://console.picovoice.ai/) to get your API key.  
> - Sign up or log in to [OpenRouter](https://openrouter.ai/) to retrieve your API key.

Once these environment variables are set, they will be loaded by `python-dotenv` at runtime.

---

## Usage

1. **Activate your Virtual Environment** (if not already active):

   ```bash
   source venv/bin/activate
   ```

2. **Run Infinity**:

   ```bash
   python infinity.py
   ```

   Infinity will load your `.env` variables, initialize Porcupine for wake-word detection, and use OpenRouter for language model integration if needed.

3. **Speak Your Command**:

   Once the assistant is running, use the configured wake-word (e.g., “Hey Infinity” or whichever you’ve set in your Porcupine model) to get its attention. Then speak your command, and Infinity will process it accordingly.

---

## Additional Notes

- You can customize your wake-word by using a custom Porcupine model.  
- For advanced usage of the OpenRouter API, refer to their official [documentation](https://openrouter.ai/docs).

---



   
   
