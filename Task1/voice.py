import speech_recognition as sr
import pyttsx3
import storage
import time

class VoiceInterface:
    def __init__(self):
        self.recognizer = sr.Recognizer()  # initalize recognizer
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # set speach rate
        self.engine.setProperty('volume', 1.0)  # set volumne

    def speak(self, text):
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Could you repeat?")
                return None
            except sr.RequestError:
                self.speak("There was an error with the speach recog service.")
                return None

def launch_voice_interface(todo_list):
    voice = VoiceInterface()
    voice.speak("Welcome to your voice-controlled Todo List. How can I help you?")
    
    while True:
        voice.speak("Say a command: add, list, update, delete, complete, or quit")
        command = voice.listen()
        
        if command == "add":
            voice.speak("What is the title of your task?")
            title = voice.listen()
            if title:
                voice.speak("What is the description?")
                description = voice.listen()
                todo_list.add_task(title, description or "")
                storage.save_tasks(todo_list)
                voice.speak("Task added successfully")

        elif command == "list":
            if not todo_list.tasks:
                voice.speak("You have no tasks.")
            else:
                voice.speak("Here are your tasks:")
                for idx, task in enumerate(todo_list.tasks, 1):
                    status = "completed" if task.completed else "pending"
                    voice.speak(f"Task {idx}: {task.title}, Status: {status}")

        elif command == "update":
            if not todo_list.tasks:
                voice.speak("No tasks to update.")
                continue
            voice.speak("Which task number would you like to update?")
            for idx, task in enumerate(todo_list.tasks, 1):
                voice.speak(f"Task {idx}: {task.title}")
            task_num = voice.listen()
            try:
                task_idx = int(task_num) - 1
                task = todo_list.tasks[task_idx]
                voice.speak("What's the new title? Say 'skip' to keep current title")
                new_title = voice.listen()
                if new_title and new_title != "skip":
                    task.title = new_title
                voice.speak("What's the new description? Say 'skip' to keep current description")
                new_desc = voice.listen()
                if new_desc and new_desc != "skip":
                    task.description = new_desc
                storage.save_tasks(todo_list)
                voice.speak("Task updated succesfully")
            except (ValueError, IndexError):
                voice.speak("Invalid task number")

        elif command == "delete":
            if not todo_list.tasks:
                voice.speak("No tasks to delete.")
                continue
            voice.speak("Which task number would you like to delete?")
            for idx, task in enumerate(todo_list.tasks, 1):
                voice.speak(f"Task {idx}: {task.title}")
            task_num = voice.listen()
            try:
                task_idx = int(task_num) - 1
                task = todo_list.tasks[task_idx]
                todo_list.delete_task(task.id)
                storage.save_tasks(todo_list)
                voice.speak("Task deleted succesfully")
            except (ValueError, IndexError):
                voice.speak("Invalid task number")

        elif command == "complete":
            if not todo_list.tasks:
                voice.speak("No tasks to complete.")
                continue
            voice.speak("Which task number would you like to mark as complete?")
            for idx, task in enumerate(todo_list.tasks, 1):
                voice.speak(f"Task {idx}: {task.title}")
            task_num = voice.listen()
            try:
                task_idx = int(task_num) - 1
                task = todo_list.tasks[task_idx]
                task.mark_complete()
                storage.save_tasks(todo_list)
                voice.speak("Task marked as complete")
            except (ValueError, IndexError):
                voice.speak("Invalid task number")

        elif command == "quit":
            voice.speak("Goodbye!")
            break

        elif command:
            voice.speak("Command not recognized. Please try again.")
