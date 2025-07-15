
from questiondict import question_data
import random

class trivia:
    def __init__(self, q_text, q_answer):
        self.question = q_text
        self.answer = q_answer
    
    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer.lower()

    def create_question_bank():
        question_bank = []

        for i in range(len(question_data)):
            question = question_data[i]
            Question = trivia(question['text'], str(question['answer']))
            question_bank.append(Question)
        return question_bank

continue_game = True
   
while continue_game:
    print("Welcome to the Trivia Game!")
    print("You will be asked a series of true or false questions.")
    print("Type 'true' or 'false' to answer each question.")
    print("Let's get started!")

    question_bank = trivia.create_question_bank()
    score = 0
    i = 1
    for question in question_bank:
        user_answer = input(f"Question {i}: {question.question} (true/false): ")
        
        if question.check_answer(user_answer):
            print("Correct!")
            score += 1
            i += 1
        else:
            print(f"Wrong! The correct answer is {question.answer}.")
            i += 1
    print(f"Your final score is {score + 1} out of {len(question_data)}.")
    continue_game = bool(input(" Thats all the questions. Do you want to continue? (yes/no): "))