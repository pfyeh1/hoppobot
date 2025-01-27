import pyttsx3

engine = pyttsx3.init("nsss")
engine.say("Testing text-to-speech on macOS")
engine.runAndWait()