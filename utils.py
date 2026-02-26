import re
import pandas as pd


def normalize(text):
    if pd.isna(text):
        return ""

    text = str(text).lower()

    # заменяем латиницу
    text = text.replace("pp", "пп")
    text = text.replace("x", "х")

    # разделяем цифры и буквы
    text = re.sub(r"(\d)([а-яa-z])", r"\1 \2", text)
    text = re.sub(r"([а-яa-z])(\d)", r"\1 \2", text)

    # убираем всё лишнее
    text = re.sub(r"[^а-яa-z0-9\s]", " ", text)

    words = text.split()

    # можно убрать "мусорные" слова
    stop_words = {"по", "для"}
    words = [w for w in words if w not in stop_words]

    words.sort()

    return " ".join(words)
