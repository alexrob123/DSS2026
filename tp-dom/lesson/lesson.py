from xml.dom.minidom import parseString

document = """\
    <books>
        <book>
            <author>Jack Herrington</author>
            <title>PHP Hacks</title>
            <publisher>O'Reilly</publisher>
        </book>
        <book>
            <author>Jack Herrington</author>
            <title>Podcasting Hacks</title>
            <publisher>O'Reilly</publisher>
        </book>
    </books>
"""

biblio = parseString(document)

print(biblio.childNodes.length)
print(biblio.childNodes[0])
print(biblio.childNodes[0].childNodes.length)

print(biblio.getElementsByTagName("UnknownTag"))

# uv run ./tp2-dom/lesson/lesson.py
