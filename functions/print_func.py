import json

def print_init() -> None:
    """
    Prints the initial message of the quiz
    """
    print("-------------------------------------")
    print("Welcome to the the quiz")
    print("-------------------------------------")


def print_topics() -> None:
    """
    Fetches the topics available in the data repo
    """
    print("-------------------------------------")

    with open("./config/topics.json", "r") as data:
        topics = json.load(data)
        
        for i in topics:
            print(f"{i} : {topics[i][0]}")

    print("-------------------------------------")


def print_question(json_name: str, index: int, i:int) -> None:
    """
    Prints the questions
    """

    with open(f"./data/{json_name}.json", "r") as data:
        data = json.load(fp=data)

    print("\n-------------------------------------")

    print(f"{i+1}. {data[index]["question"]}")
    print("\n")

    print(f"A. {data[index]["A"]}")
    print(f"B. {data[index]["B"]}")
    print(f"C. {data[index]["C"]}")
    print(f"D. {data[index]["D"]}")
