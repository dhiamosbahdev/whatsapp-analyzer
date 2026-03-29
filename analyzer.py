import re
import pandas as pd


def parse_whatsapp_chat(file_path):
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(AM|PM)? - ([^:]+): (.*)"
    data = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                date, time, ampm, user, message = match.groups()
                data.append([date, time, user.strip(), message])

    df = pd.DataFrame(data, columns=["Date", "Time", "User", "Message"])
    return df


def compute_scores(df):
    scores = df.groupby("User").size().reset_index(name="Messages")

    def assign_rank(msgs):
        if msgs >= 100:
            return "Legend 👑🔥"
        elif msgs >= 50:
            return "Pro 🚀"
        elif msgs >= 20:
            return "Active 💬"
        elif msgs > 0:
            return "Beginner 🌱"
        else:
            return "Ghost 👻"

    scores["Rank"] = scores["Messages"].apply(assign_rank)
    scores = scores.sort_values(by="Messages", ascending=False)

    return scores


if __name__ == "__main__":
    df = parse_whatsapp_chat("chat.txt")
    scores = compute_scores(df)
    print(scores)
