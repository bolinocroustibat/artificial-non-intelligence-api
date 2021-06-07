import json
import re
import sqlite3


def load_real_comments_into_db(filename: str, realness: int = 1) -> None:
    connection = sqlite3.connect("../data/db.sqlite3")
    with connection:
        with open (filename, "r") as file:
            data: list = json.loads(file.read())
            print("Excluded since it's too long:")
            print(data.pop(15312))
            for line in data:
                try:
                    aggressive: int = int(line["annotation"]["label"][0])
                    raw_content = line["content"].strip().replace('\"', '”')
                    content: str = '\"' + raw_content + '\"'
                    pattern = r'((?:#|http)\S+)'
                    if not len(re.findall(pattern, content)) and len(list(content.split(" "))) > 1:
                        query: str = f"""INSERT INTO comments(content,realness,aggressive) VALUES({content},{realness},{aggressive})"""
                        cursor = connection.cursor()
                        cursor.execute(query)
                        connection.commit()
                except Exception as e:
                    print(e)
                    continue


def load_fake_comments_into_db(
    filename: str,
    aggressive: int,
    realness: int = 0) -> None:
    connection = sqlite3.connect("../data/db.sqlite3")
    with connection:
        with open (filename, "r") as file:
            data: dict = json.loads(file.read())
            for line in data["content"].values():
                try:
                    raw_content = line.strip().replace('\"', '”')
                    content: str = '\"' + raw_content + '\"'
                    query: str = f"""INSERT INTO comments(content,realness,aggressive) VALUES({content},{realness},{aggressive})"""
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    # filename = "../data/kaggle-cyber-trolls.json"
    # load_real_comments_into_db(filename=filename, realness=1)

    # filename = "../data/500_fake_tweets_aggressive_1.json"
    # load_fake_comments_into_db(filename=filename, aggressive=1, realness=0)

    filename = "../data/500_fake_tweets_nonaggressive_1.json"
    load_fake_comments_into_db(filename=filename, aggressive=0, realness=0)
