import json
import time

FILE_PATH = "questions.json"
LIVES = 3


def load_questions():
    """
    Loads a set of questions from a JSON file and returns them as a deserialized object.

    This function reads the content of a JSON file located at the specified file path,
    parses it and loads the questions into a usable form, often a dictionary or list
    depending on the structure within the JSON. This is typically used for initializing
    or processing a set of predefined questions for an application.

    :return: The loaded questions from the JSON file.
    :rtype: Any
    """
    with open(FILE_PATH, "r") as file:
        questions = json.load(file)

    return questions

def categorize_questions():
    """
    Categorizes questions into three difficulty levels.

    This function loads a list of questions and categorizes them into three separate
    lists based on their difficulty level: "easy", "medium", and "hard". Each question
    is assumed to have a "difficulty" key indicating its difficulty as a string
    (either "easy", "medium", or "hard"). The function returns these categorized lists.

    :returns: A tuple containing three lists - the first with questions of difficulty
        level "easy", the second with questions of difficulty level "medium", and
        the third with questions of difficulty level "hard".
    :rtype: tuple[list[dict]]
    """
    questions = load_questions()
    easy_questions = [q for q in questions if q["difficulty"].lower() == "easy"]
    medium_questions = [q for q in questions if q["difficulty"].lower() == "medium"]
    hard_questions = [q for q in questions if q["difficulty"].lower() == "hard"]

    return easy_questions, medium_questions, hard_questions

def game(lives=LIVES):
    """
    Executes the main game loop of a quiz game where players answer categorized
    questions until they either lose all lives or complete the quiz. The game allows
    the player to restart upon failure.

    :param lives: Number of lives the player starts with. Defaults to the global
        constant value LIVES.
    :type lives: int
    :return: None
    """
    easy, medium, hard = categorize_questions()
    total_questions = easy + medium + hard

    question_number = 1
    for question in total_questions:
        current_question = question["question"].lower()
        current_answer = question["answer"].lower()
        current_options = question["options"]

        print_question(question_number, current_question, current_options)
        user_answer = take_answer()
        is_correct = check_answer(user_answer, current_answer, current_options)

        if not is_correct:
            lives -= 1
            question_number += 1
            if lives == 0:
                again = input("You lost!\nDo you want to play again? (y/n): ").lower()
                while again not in ["y", "n"]:
                    print("invalid input, try again:")
                    time.sleep(1)
                    again = input("Do you want to play again? (y/n): ").lower()
                if again == "y":
                    game()
                else:
                    print("Thanks for playing!")
                    break

            else:
                print(f"You have {lives} lives left.")
                continue

        while is_correct == "invalid input":
            print_question(question_number, current_question, current_options)
            user_answer = take_answer()
            is_correct = check_answer(user_answer, current_answer, current_options)

        else:
            question_number += 1

def check_answer(user_answer, correct_answer, options):
    """
    Checks the user's answer against the correct answer and provides feedback.

    This function evaluates whether the user-selected answer matches the correct
    answer. It also validates the user input, ensuring it is a digit within the
    valid range of answer options. If the input is invalid, the function returns
    an appropriate response. Otherwise, it compares the selected option to the
    correct answer and provides feedback on whether it is correct or incorrect.

    :param user_answer: The input provided by the user, representing the selected
        answer. Must be a string that can be converted to a digit within the valid
        range of options.
    :param correct_answer: The correct answer to the question as a string.
    :param options: A list of possible answer options provided to the user.

    :return: Returns True if the user's selected answer is correct, False if the
        selected answer is incorrect. Returns "invalid input" if the user's input
        is not valid.
    """
    while not user_answer.isdigit() or int(user_answer) > len(options) or int(user_answer) < 1:
        print("Enter a valid answer: ")
        time.sleep(1)
        return "invalid input"

    user_answer_text = options[int(user_answer) - 1]
    if user_answer_text.lower() == correct_answer.lower():
        print("Correct!")
        time.sleep(1)
        return True
    else:
        print(f"Wrong! The correct answer is {correct_answer}")
        time.sleep(1)
        return False

def print_question(idx, current_question, current_options):
    """
    Displays the question along with its options.

    This function prints the current question number, the question text, and a list
    of provided options, formatted and enumerated.

    :param idx: The index or number of the current question being displayed.
    :type idx: int
    :param current_question: The text of the current question.
    :type current_question: str
    :param current_options: A list of options related to the current question.
    :type current_options: list[str]
    :return: None
    """
    print(f"Question number {idx}:\n{current_question}\n the options are:")
    for i, o in enumerate(current_options, start=1):
        print(f"{i}. {o}")

def take_answer():
    """
    Prompts the user to enter an answer and returns the input in lowercase format.

    :return: The user's input converted to lowercase.
    :rtype: str
    """
    return input("Enter your answer: ").lower()


if __name__ == "__main__":
    game(LIVES)

