def question_mark(regex,word):
    try:
        if regex[0] == "." or regex[0] == word[0]:
            if regex[0] == word[1]:
                return False
            return word[1:]
        return word
    except IndexError:
        return True


def plus_mark(content, word):
    regex = content[0]["regex"]
    if regex[0] == "." or regex[0] == word[0]:
        pos = 1
        if len(content) >= 2:
            while pos < len(word):
                if word[pos] != content[1]["regex"][0]:
                    pos += 1
                else:
                    break
        else:
            while pos < len(word):
                if word[pos] == word[0]:
                    pos += 1
                else:
                    break
        return word[pos: ]
    return False


def start_mark(content, word):
    regex = content[0]["regex"]
    if regex[0]=="." or regex[0] == word[0]:
        pos = 0
        if len(content) >= 2:
            while pos < len(word):
                if word[pos] != content[1]["regex"][0]:
                    pos += 1
                else:
                    break
        else:
            while pos < len(word):
                if word[pos] == word[0]:
                    pos += 1
                else:
                    break
        return word[pos: ]
    return word


def without_meta(regex,word):
    for x, y in zip(regex, word):
        if x != y and x != ".":
            return False
    return word[len(regex): ]


def contain(content, word):
    for x in range(len(word)):
        if withstart(content, word[x: ],"contain"):
            return True
    return False

    
def withstart(content, word, option):
    try:
        regex = content[0]["regex"]
        meta = content[0]["meta"]
    except IndexError:
        if option == "start" or option == "contain":
            return True
        if option == "both":
            if word != "":
                return False
            return True
    else:
        if option== "both" and regex != "" and word == "":
                return False
        elif option=="start" and regex != "" and word == "":
                return False  
        elif "?" == meta:
            result = question_mark(regex,word)
            if not result and result != "":
                return False
            else:
                withstart(content[1:], result, option)
        elif "*" == meta:
            result = start_mark(content, word)
            return withstart(content[1: ], result, option)
        elif "+" == meta:
            result = plus_mark(content,word)
            if not result and result != "":
                return False
            return withstart(content[1:], result, option)
        elif "" == meta:
            result = without_meta(regex, word)
            if not result and result != "":
                return False
            return withstart(content[1:], result, option)
        return True
        
        
def reg(p, word):
    if p["start"] != "" and p["end"] != "" and len(p["content"]):
        if (not word.startswith(p["start"]) and p["start"] != ".") or (not word.endswith(p["end"]) and p["end"] != "."):
            return False
        word = word[len(p["start"]): - len(p["end"])]
        return withstart(p["content"], word, "both")
    elif p["start"] != "":
        if not word.startswith(p["start"]) and p["start"] != ".":
            return False
        word = word[word.find(p["start"]) + len(p["start"]):]
        return withstart(p["content"], word, "start")
    elif p["end"] != "":
        if not word.endswith(p["end"]) and p["end"] != ".":
            return False
        word = word[:word.find(p["end"])]
        return withstart(p["content"][::-1], word[::-1],"start")
    elif p["content"]:
        return contain(p["content"], word)


def check(regex,word):
    preprocessed = list()
    global delimiters
    normal= ""
    start = False
    begin = ""
    end = ""
    if regex != '' and word == '':
        return False
    elif regex =='':
        return True
    elif regex in word:
        return True
    elif regex.startswith("^") and regex.endswith("$") and all([delimiter not in regex for delimiter in delimiters ]):
        return regex[1: -1] == word
    elif regex[0] == "^":
        start = True
    for x in range(start,len(regex)):
        if start:
            if regex[x] in metachars:
                if normal[-1] == '\\' :
                    normal = normal[:-1] + regex[x]
                elif regex[x] in delimiters:
                    begin = normal[:-1]
                    preprocessed.append({"regex":normal[-1], "meta":regex[x]})
                    normal = ""
                    start = False
                elif regex[x] == "$":
                    end = normal
                    normal = ""
                    start = False
                elif regex[x] == "\\":
                    continue
                elif regex[x] == ".":
                    normal = normal + regex[x]
            else:
                normal = normal + regex[x]
        else:
            if regex[x] in metachars:
                if regex[x - 1] == '\\' :
                    normal = normal + regex[x]
                elif regex[x] in delimiters:
                    if normal[:-1] != '':
                        preprocessed.append({"regex":normal[:-1],"meta":""})
                    preprocessed.append({"regex":normal[-1], "meta":regex[x]})
                    normal = ""
                elif regex[x] == "$" : 
                    if normal == "":
                        end = '\0'
                    else:
                        end = normal
                        normal = ""
                elif regex[x] == "\\":
                    continue
                elif regex[x] == ".":
                    normal = normal + regex[x]
                else:
                   normal = normal[:-1] + regex[x] 
            else:
                normal = normal + regex[x]
    if len(normal):
        if start:
            begin = normal
        else:
            preprocessed.append({"regex":normal, "meta":""})
    return reg({"start": begin, "content": preprocessed, "end": end}, word)

delimiters = ["?", "*", "+"]
metachars = delimiters + ["^", "$", ".","\\"]
while True:
    regex, word= input().split('|')
    if regex == exit:
        break
    print(check(regex,word))
