import ast

filename = "q9yj_5UIsco.json"
try:
    content = open(filename, 'r', encoding='utf-16').read()
    data = ast.literal_eval(content)
    text = " ".join([x['text'] for x in data[0]])
    with open("q9yj_5UIsco.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Parsed OK")
except Exception as e:
    # Try utf-8
    try:
        content = open(filename, 'r', encoding='utf-8').read()
        data = ast.literal_eval(content)
        text = " ".join([x['text'] for x in data[0]])
        with open("q9yj_5UIsco.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Parsed OK with UTF-8")
    except Exception as e2:
        print("Error:", e2)
