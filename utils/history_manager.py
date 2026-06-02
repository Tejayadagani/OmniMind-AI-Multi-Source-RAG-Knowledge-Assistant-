import json
import os
import uuid

HISTORY_FILE = "data/history/chats.json"


def load_history():

    if not os.path.exists(
        HISTORY_FILE
    ):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            # Old history format
            if (
                data
                and isinstance(
                    data[0],
                    str
                )
            ):
                return []

            return data

    except:

        return []


def save_history(
    chats
):

    os.makedirs(
        "data/history",
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chats,
            f,
            indent=4,
            ensure_ascii=False
        )


def create_chat(
    title,
    source
):

    return {

        "id": str(
            uuid.uuid4()
        ),

        "title": title,

        "source": source,

        "messages": []
    }