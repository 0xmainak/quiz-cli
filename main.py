from functions import *
import random

if __name__ == "__main__":

    print_init()
    print_topics()

    inp_topic = input("Select a topic: ")

    score = 0

    for i in range(10):

        topic = get_topic(inp_topic)

        index = random.randrange(0, get_length(topic))

        print_question(json_name=topic, index=index, i=i)

        answer = input("\n: ").upper()

        correct_answer = get_answer(question=get_question(json_name=topic, index=index))

        if answer == correct_answer:
            print("Correct")
            score += 1
        else:
            print(f"Incorrect! \n The correct answer is {correct_answer}")

        input("Press enter to continue: ")

    print(f"Your total score is: {score}")
