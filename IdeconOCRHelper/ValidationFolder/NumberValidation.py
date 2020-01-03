import re

def onlyNumberValidate(text):
    regex = r"[^0-9]+"
    matches = re.search(regex, text, re.MULTILINE)
    if matches:
        str = matches.group()
        for txt in str:
            if str == "b" or str == "G":
                text = text.replace(str,"6")
            elif str == "g" or str == "q":
                text = text.replace(str, "9")
            elif str == "L" or str == "l" or str == "I" or str == "i" or str == "|" or str == "/":
                text = text.replace(str, "1")
            elif str == "S" or str == "s":
                text = text.replace(str, "5")
            elif str == "Z" or str == "z":
                text = text.replace(str, "2")
            elif str == "O" or str == "o" or str == "a":
                text = text.replace(str, "0")
    return text
