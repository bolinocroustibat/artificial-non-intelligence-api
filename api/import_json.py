import asyncio
import json
import sqlite3


from models import Comment


def load_json_into_db(filename: str, realness: int) -> None:
    connection = sqlite3.connect("../data/db.sqlite3")
    with connection:
        with open (filename, "r") as file:
            data: list = json.loads(file.read())
            for line in data:
                try:
                    raw_content = line["content"].strip().replace('\"', '”')
                    content: str = '\"' + raw_content + '\"'
                    query: str = f"""INSERT INTO comments(content,realness) VALUES({content},{realness})"""
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except Exception as e:
                    print(e)
                    break


filename = "../data/kaggle-cyber-trolls.json"

load_json_into_db(filename=filename, realness=1)
