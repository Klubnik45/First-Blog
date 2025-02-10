import re

def divide_text(text):
    return text.split("\n\n")


def gen_heading(line):
    return f'<h{line.count("#")}>{line.replace("#", "")}</h{line.count("#")}>'


def gen_image(line):
    alt = ""
    link = line[line.index("("): line.index(")")][1:]
    for symbol in range(line.index("["), len(line)):
        if line[symbol] == "]":
            break
        alt += line[symbol]
    alt = alt[1:]
    return f'<img src="{link}" alt="{alt}">'
    

def gen_link(line):
    link = line[line.index("("): line.index(")")][1:]
    text = line[line.index("["): line.index("]")][1:]
    return f'{line[:line.index("[")]} <a href="{link}">{text}</a> {line[line.index(")")+1:]}'


def gen_ulist(text, index):
    ulist = []
    try:
        while text[index][0] == "-":
            ulist.append(f'<li>{text[index].replace("-", "")}</li>')
            index += 1
    except:
        pass
    return ("<ul>" + " ".join(ulist) + "</ul>", len(ulist))

   
def gen_olist(text, index):
    olist = []
    try:
        while text[index][0] == "." and text[index][1] == "0" and text[index][2] == ".":
            olist.append(f'<li>{text[index].replace(".0.", "")}</li>')
            index += 1
    except:
        pass   
    return ("<ol>" + " ".join(olist) + "</ol>", len(olist))


def gen_emphasis(line):
    if "**" in line:
        bold_expesion = re.compile("\*{2,}(.*?)\*{2,}")
        return re.sub(bold_expesion, "<b>\\1</b>", line)
    elif "*" in line:
        italic_expesion = re.compile("\*{1,}(.*?)\*{1,}")
        return re.sub(italic_expesion, "<i>\\1</i>", line)
    else:
        return line


def gen_paragraph(line):
    return f"<p> {line} </p>"


with open ("post_text.txt", "r", encoding="utf-8") as text:
    markdown = text.read()

def gen_html(markdown):
    markdown = markdown.replace("\r", "")
    markdown = divide_text(markdown)
    html = ""
    line = 0

    while line < len(markdown):
        temp_html = markdown[line]
        temp_html = gen_emphasis(temp_html)
        if temp_html[0] == "#":
            temp_html = gen_heading(temp_html)
            line += 1
            html += temp_html
            continue

        if "&htm" in temp_html:
            html += temp_html.replace("&html", "")
            line += 1
            continue

        if (temp_html[0] != "!") and (temp_html[0] != "-") and (temp_html[0] != "." and temp_html[1] != "0" and temp_html[2] != "."):
            temp_html = gen_paragraph(temp_html)

        if temp_html[0] == "!":
            temp_html = gen_image(temp_html)

        if "](" in temp_html:
            temp_html = gen_link(temp_html)
  
        if temp_html[0] == "-":
            list_data, index = gen_ulist(markdown, line)
            temp_html = list_data
            line = line + index
            html += temp_html
            continue

        if temp_html[0] == "." and temp_html[1] == "0" and temp_html[2] == ".":
            list_data, index = gen_olist(markdown, line)
            temp_html = list_data
            line = line + index
            html += temp_html
            continue

        line += 1
        html += temp_html
        
    return html