import json

def get_question(json_name: str, index: int) -> list:
    """Fetchs questions and returns the data"""

    with open(f"./data/{json_name}.json", "r") as data:
        data = json.load(fp=data)

    return data[index]


def get_answer(question: list) -> str:

    return question["answer"]


def get_topic(index: str) -> str:
    """Fetchs topic and returns the data"""

    with open("./config/topics.json", "r") as data:
        topics = json.load(data)

    return topics[index][1]


def get_length(json_name: str) -> int:
    """Fetchs number of questions available in the topic data"""

    with open(f"./data/{json_name}.json", "r") as data:
        data = json.load(data)

    return len(data)