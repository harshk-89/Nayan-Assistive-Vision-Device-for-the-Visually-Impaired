import pyttsx3

class TextToSpeech:
    def __init__(self):
        """Initialize the text-to-speech engine with default settings"""
        self.engine = pyttsx3.init()
        # Set default properties
        self.engine.setProperty('rate', 150)  # Moderate speech rate
        self.engine.setProperty('volume', 0.9)  # Slightly below max volume
        
    def text_to_speech(self, text, rate=None, volume=None, voice_id=None):
        """
        Convert text to speech and speak it immediately
        :param text: Text to be spoken
        :param rate: Optional speech rate (words per minute)
        :param volume: Optional volume level (0.0 to 1.0)
        :param voice_id: Optional voice ID to use
        """
        # Apply properties if provided
        if rate is not None:
            self.engine.setProperty('rate', rate)
        if volume is not None:
            self.engine.setProperty('volume', volume)
        if voice_id is not None:
            voices = self.engine.getProperty('voices')
            try:
                self.engine.setProperty('voice', voices[voice_id].id)
            except IndexError:
                print(f"Voice ID {voice_id} not found. Using default voice.")
        
        # Speak the text
        self.engine.say(text)
        self.engine.runAndWait()
        
    def save_to_file(self, text, filename):
        """Save the speech to an audio file (optional functionality)"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"Audio saved to {filename}")

# The following function is what will be imported by the main application
def text_to_speech(text, rate=None, volume=None, voice_id=None):
    """
    Standalone function that matches the expected interface
    This creates a TextToSpeech instance and uses it to speak the text
    """
    tts = TextToSpeech()
    print(text)
    tts.text_to_speech(text, rate, volume, voice_id)

# Example usage
if __name__ == "__main__":
    # Demonstrate the standalone function
    text_to_speech("This is a test of the text to speech system")
    
    # Demonstrate with parameters
    text_to_speech("This is a faster speech", rate=200)
    
    # Demonstrate the class directly
    tts = TextToSpeech()
    tts.text_to_speech("This is using the class directly")
    tts.save_to_file("Saving this to file", "output.mp3")