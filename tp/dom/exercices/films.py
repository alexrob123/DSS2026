import argparse
from xml.dom.minidom import parse

# Question 1
# Return the list of all film titles in the XML file.
# ----------------------------------------------------------------------------------------------------


def q1(xml_file):
    return q1_via_film(xml_file)


def q1_via_film(xml_file):
    dom = parse(xml_file)

    titles = []
    for film in dom.getElementsByTagName("FILM"):
        title = film.getElementsByTagName("TITRE")[0].firstChild.data
        titles.append(title)
    return titles


def q1_via_title(xml_file):
    dom = parse(xml_file)

    titles = []
    for title in dom.getElementsByTagName("TITRE"):
        titles.append(title.firstChild.data)
    return titles


# Question 2
# Returns all films from 1990 int the XML file.
# ----------------------------------------------------------------------------------------------------


def q2(xml_file):
    dom = parse(xml_file)
    titles = []
    for film in dom.getElementsByTagName("FILM"):
        if film.hasAttribute("Annee") and film.getAttribute("Annee") == "1990":
            title = film.getElementsByTagName("TITRE")[0].firstChild.data
            titles.append(title)
    return titles


# Question 3
# Returns the synopsis of the film "Alien".
# ----------------------------------------------------------------------------------------------------


def q3(xml_file):
    assert q3_via_film(xml_file) == q3_via_title(xml_file)
    return q3_via_film(xml_file)


def q3_via_film(xml_file):
    dom = parse(xml_file)

    for film in dom.getElementsByTagName("FILM"):
        if film.getElementsByTagName("TITRE")[0].firstChild.data == "Alien":
            return film.getElementsByTagName("RESUME")[0].firstChild.data
    return None


def q3_via_title(xml_file):
    dom = parse(xml_file)

    for title in dom.getElementsByTagName("TITRE"):
        if title.firstChild.data == "Alien":
            film = title.parentNode
            return film.getElementsByTagName("RESUME")[0].firstChild.data
    return None


# Question 4
# Returns the titles of the films with Bruce Willis as an actor.
# ----------------------------------------------------------------------------------------------------


def q4(xml_file):
    assert q4_via_film(xml_file) == q4_via_role(xml_file)
    return q4_via_film(xml_file)


def q4_via_film(xml_file):
    dom = parse(xml_file)

    films = []
    for n in dom.getElementsByTagName("FILM"):
        for role in n.getElementsByTagName("ROLE"):
            if (
                role.getElementsByTagName("PRENOM")[0].firstChild.data == "Bruce"
                and role.getElementsByTagName("NOM")[0].firstChild.data == "Willis"
            ):
                title = n.getElementsByTagName("TITRE")[0].firstChild.data
                films.append(title)
    return films


def q4_via_role(xml_file):
    dom = parse(xml_file)

    films = []
    for role in dom.getElementsByTagName("ROLE"):
        if (
            role.getElementsByTagName("PRENOM")[0].firstChild.data == "Bruce"
            and role.getElementsByTagName("NOM")[0].firstChild.data == "Willis"
        ):
            film = role.parentNode.parentNode
            title = film.getElementsByTagName("TITRE")[0].firstChild.data
            films.append(title)
    return films


# Question 5
# Returns the titles of the films that have a synopsis.
# ----------------------------------------------------------------------------------------------------


def q5(xml_file):
    return q5_via_film(xml_file)


def q5_via_film(xml_file):
    dom = parse(xml_file)

    titles = []
    for film in dom.getElementsByTagName("FILM"):
        if film.getElementsByTagName("RESUME"):
            title = film.getElementsByTagName("TITRE")[0].firstChild.data
            titles.append(title)
    return titles


def q5_via_resume(xml_file):
    dom = parse(xml_file)

    titles = []
    for resume in dom.getElementsByTagName("RESUME"):
        film = resume.parentNode
        title = film.getElementsByTagName("TITRE")[0].firstChild.data
        titles.append(title)
    return titles


# Question 6
# Returns the titles of the films that do not have a synopsis.
# ----------------------------------------------------------------------------------------------------


def q6(xml_file):
    return q6_via_film(xml_file)


def q6_via_film(xml_file):
    dom = parse(xml_file)

    titles = []
    for film in dom.getElementsByTagName("FILM"):
        if not film.getElementsByTagName("RESUME"):
            title = film.getElementsByTagName("TITRE")[0].firstChild.data
            titles.append(title)
    return titles


# Question 7
# Returns the titles of the films that are older than 30 years.
# ----------------------------------------------------------------------------------------------------


def q7(xml_file):
    dom = parse(xml_file)
    titles = []
    for film in dom.getElementsByTagName("FILM"):
        if film.hasAttribute("Annee") and int(film.getAttribute("Annee")) < 2026 - 30:
            title = film.getElementsByTagName("TITRE")[0].firstChild.data
            titles.append(title)
    return titles


# Question 8
# Returns the role of Harvey Keitel in the film "Reservoir Dogs".
# ----------------------------------------------------------------------------------------------------


def q8(xml_file):
    assert q8_via_film(xml_file) == q8_via_title(xml_file)
    return q8_via_film(xml_file)


def q8_via_film(xml_file):
    dom = parse(xml_file)

    for film in dom.getElementsByTagName("FILM"):
        title = film.getElementsByTagName("TITRE")[0].firstChild.data
        if title == "Reservoir Dogs":
            for role in film.getElementsByTagName("ROLE"):
                if (
                    role.getElementsByTagName("PRENOM")[0].firstChild.data == "Harvey"
                    and role.getElementsByTagName("NOM")[0].firstChild.data == "Keitel"
                ):
                    return role.getElementsByTagName("INTITULE")[0].firstChild.data
    return None


def q8_via_title(xml_file):
    dom = parse(xml_file)

    for title in dom.getElementsByTagName("TITRE"):
        if title.firstChild.data == "Reservoir Dogs":
            film = title.parentNode
            for role in film.getElementsByTagName("ROLE"):
                if (
                    role.getElementsByTagName("PRENOM")[0].firstChild.data == "Harvey"
                    and role.getElementsByTagName("NOM")[0].firstChild.data == "Keitel"
                ):
                    return role.getElementsByTagName("INTITULE")[0].firstChild.data
    return None


# Question 9
# Returns the title of the last film of the document.
# ----------------------------------------------------------------------------------------------------


def q9(xml_file):
    dom = parse(xml_file)

    films = dom.getElementsByTagName("FILM")
    if films:
        last_film = films[-1]
        title = last_film.getElementsByTagName("TITRE")[0].firstChild.data
        return title
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--question", "-q", type=int, help="Question number")
    parser.add_argument("--xml", type=str, help="Path to the XML file")
    args = parser.parse_args()

    map2func = {1: q1, 2: q2, 3: q3, 4: q4, 5: q5, 6: q6, 7: q7, 8: q8, 9: q9}

    if args.question in map2func:
        print(f"Question {args.question}")
        print("-" * 20)
        print(map2func[args.question](args.xml))
        print("\n")

    else:
        print("Printing results for all functions.")
        print("-" * 20)
        for key in sorted(map2func.keys()):
            print(f"Question {key}")
            print("-" * 20)
            print(map2func[key](args.xml))
            print("\n")
