import json
import pyttsx3
from difflib import get_close_matches

def load_KB(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except FileNotFoundError:
        return {"questions": []}

def save_KB(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(UQ: str, questions: list[str]) -> str:
    matches: list = get_close_matches(UQ, questions, n=1, cutoff=0.6)
    return matches[0] if matches else ""

def get_answer(question: str, knowledgebase: dict) -> str:
    for q in knowledgebase["questions"]:
        if q["question"] == question:
            return q["answer"]
    return ""

def text_to_speech(text: str) -> None:
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def chathot():
    knowledgebase: dict = load_KB('TeachMeBot/knowledgebase.json')

    while True:
        user_input: str = input("You: ")
        if user_input.lower() == 'quit':
            break

        best_match: str = find_best_match(user_input, [q["question"] for q in knowledgebase["questions"]])

        if best_match:
            answer: str = get_answer(best_match, knowledgebase)
            if answer:
                print(f"Bot: {answer}")
                text_to_speech(answer)  # Speak the answer
            else:
                print("Bot: I don't know the answer. Please teach me.")
                new_answer: str = input("Type the answer or 'skip' to skip: ")
                if new_answer.lower() != 'skip':
                    knowledgebase["questions"].append({"question": user_input, "answer": new_answer})
                    save_KB('TeachMeBot/knowledgebase.json', knowledgebase)
                    print("Bot: Thank you!")
        else:
            print("Bot: I don't know the answer. Please teach me.")
            new_answer: str = input("Type the answer or 'skip' to skip: ")
            if new_answer.lower() != 'skip':
                knowledgebase["questions"].append({"question": user_input, "answer": new_answer})
                save_KB('TeachMeBot/knowledgebase.json', knowledgebase)
                print("Bot: Thank you, I learned something new!")

if __name__ == '__main__':
    chathot()
