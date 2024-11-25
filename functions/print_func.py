import json
from typing import Optional

def print_init() -> None:
    print("-------------------------------------")
    print("Welcome to the the quiz")
    print("-------------------------------------")


def print_topics() -> None:

    print("-------------------------------------")

    with open("./config/topics.json", "r") as data:
        topics = json.load(data)
        
        for i in topics:
            print(f"{i} : {topics[i][0]}")

    print("-------------------------------------")


def print_question(json_name: str, index: int, i:int) -> None:

    # if not i:
    #     i = ""
    # else:
    #     i = f"{i+1}. "

    with open(f"./data/{json_name}.json", "r") as data:
        data = json.load(fp=data)

    print("\n-------------------------------------")

    print(f"{i+1}. {data[index]["question"]}")
    print("\n")

    print(f"A. {data[index]["A"]}")
    print(f"B. {data[index]["B"]}")
    print(f"C. {data[index]["C"]}")
    print(f"D. {data[index]["D"]}")
