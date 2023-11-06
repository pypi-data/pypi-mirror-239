import requests
from bs4 import BeautifulSoup


def tlumacz_p_k(tekst):
    slowa = tekst.split(" ")  # wyrazy które zawierają znaki
    wartosci = []  # informacja czy posiadane zanki 0: brak 1:, 2:.
    got_slowa = []
    for slowo in slowa:
        if "," in slowo:
            wartosci.append(1)
            text = slowo.replace(",", "")
            got_slowa.append(text)
        elif "." in slowo:
            wartosci.append(2)
            text = slowo.replace(".", "")
            got_slowa.append(text)
        else:
            wartosci.append(0)
            got_slowa.append(slowo)
        got = []
    for slowka in got_slowa:
        url = f"https://kaszebe.org/pl/{slowka}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        div_container = soup.find("div", class_="container")
        main_content = div_container.find("main", role="main")
        row_marketing = main_content.find("div", class_="row marketing")
        col_lg_12_list = row_marketing.find_all("div", class_="col-lg-12")
        # Sprawdzamy, czy istnieje drugi div col-lg-12
        if len(col_lg_12_list) > 1:
            second_col_lg_12 = col_lg_12_list[1]
            # Teraz możesz przeszukać ten drugi div w poszukiwaniu elementów, tak jak w poprzednich przykładach
            translations_list = second_col_lg_12.find("ul", class_="translations-list")
            li_element = translations_list.find("li")
            # Wypisz treść w języku kaszubskim
            if li_element:
                x = li_element.text.replace("\n", "")
                got.append(x)
        else:
            got.append(slowka)
    zdanie = ""
    for i, gotowe in enumerate(got):
        if wartosci[i] == 1:
            zdanie += gotowe + ", "
        elif wartosci[i] == 2:
            zdanie += gotowe + "."
        else:
            zdanie += gotowe + " "
    return zdanie


def tlumacz_k_p(tekst):
    slowa = tekst.split(" ")  # wyrazy które zawierają znaki
    wartosci = []  # informacja czy posiadane zanki 0: brak 1:, 2:.
    got_slowa = []
    for slowo in slowa:
        if "," in slowo:
            wartosci.append(1)
            text = slowo.replace(",", "")
            got_slowa.append(text)
        elif "." in slowo:
            wartosci.append(2)
            text = slowo.replace(".", "")
            got_slowa.append(text)
        else:
            wartosci.append(0)
            got_slowa.append(slowo)
        got = []
    for slowka in got_slowa:
        url = f"https://kaszebe.org/ka/{slowka}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        div_container = soup.find("div", class_="container")
        main_content = div_container.find("main", role="main")
        row_marketing = main_content.find("div", class_="row marketing")
        col_lg_12_list = row_marketing.find_all("div", class_="col-lg-12")
        # Sprawdzamy, czy istnieje drugi div col-lg-12
        if len(col_lg_12_list) > 1:
            second_col_lg_12 = col_lg_12_list[1]
            # Teraz możesz przeszukać ten drugi div w poszukiwaniu elementów, tak jak w poprzednich przykładach
            translations_list = second_col_lg_12.find("ul", class_="translations-list")
            li_element = translations_list.find("li")
            # Wypisz treść w języku kaszubskim
            if li_element:
                x = li_element.text.replace("\n", "")
                got.append(x)
        else:
            got.append(slowka)
    zdanie = ""
    for i, gotowe in enumerate(got):
        if wartosci[i] == 1:
            zdanie += gotowe + ", "
        elif wartosci[i] == 2:
            zdanie += gotowe + "."
        else:
            zdanie += gotowe + " "
    return zdanie
