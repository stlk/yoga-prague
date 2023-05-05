import datetime
import json
import logging
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

# Login using the following request
url_login = "https://rezervace.dum-jogy.cz/rs/login/run"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.7,cs;q=0.3",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://rezervace.dum-jogy.cz",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": "https://rezervace.dum-jogy.cz/rs/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}
data_login = {
    "username": "rousek",
    "password": os.environ["DUM_JOGY_PASSWORD"],
    "trvale_prihlaseni": "1",
}

locations = {
    "Anděl": 16,
    "Chodov": 17,
    "Vinohrady": 18,
}

session = requests.Session()


def get_availability(yoga_class):
    if obsazenost := yoga_class.find(class_="cisla"):
        if pocet_nahradniku := obsazenost.find(class_="pocet-nahradniku"):
            pocet_nahradniku.extract()

            # Extract the signed and capacity numbers
        signed, capacity = (int(num) for num in obsazenost.get_text(strip=True).split("/"))
        free_spaces = capacity - signed
        has_free_spaces = free_spaces > 0
        return free_spaces, has_free_spaces

    return None, False


def get_lessons(html_content: str, location_name: str):
    yoga_schedule = []
    soup = BeautifulSoup(html_content, "html.parser")

    days = soup.select(".tb-sloupec")
    for day in days:
        date_class = day.findChild().get("class")[0]
        date_iso = date_class.replace("lekce-wrapper-", "")

        classes = day.select(".jedna-lekce-vypis")

        for yoga_class in classes:
            try:
                id_value = yoga_class.get("id")
                activity_id = int(re.search(r"\d+", id_value).group())
                link = yoga_class.find(class_="lekce-telo-aktivita").get("href")
                time_element = yoga_class.find(class_="lekce-telo-cas")
                time_start = time_element.find(class_="cas-od").get_text(strip=True)
                time_end = time_element.find(class_="cas-do").get_text(strip=True).replace("- ", "")
                activity_type = yoga_class.find(class_="lekce-telo-aktivita").get_text(
                    strip=True,
                )
                instructor_name = yoga_class.find(
                    class_="lekve-telo-instruktor",
                ).get_text(strip=True)
                lesson_price = yoga_class.find(class_="cena-jedne-lekce").get_text()

                time_start_datetime = datetime.datetime.fromisoformat(f"{date_iso}T{time_start}")

                now = datetime.datetime.now()
                if time_start_datetime < now:
                    continue

                free_spaces, has_free_spaces = get_availability(yoga_class)

                yoga_schedule.append(
                    {
                        "activity_name": activity_type,
                        "activity_id": activity_id,
                        "time_start": f"{date_iso}T{time_start}",
                        "time_end": f"{date_iso}T{time_end}",
                        "instructor_name": instructor_name,
                        "instructor_photo": None,
                        "price": lesson_price,
                        "free_spaces": free_spaces,
                        "has_free_spaces": has_free_spaces,
                        "link": f"https://rezervace.dum-jogy.cz{link}",
                        "location": f"Dům Jógy {location_name}",
                    },
                )

            except Exception:
                logging.exception(f"error while parsing {activity_id}")
    return yoga_schedule


def get_location(location):
    url_location = f"https://rezervace.dum-jogy.cz/rs/kalendar_vypis/zmena_mistnosti/{location}"
    response_location = session.post(url_location, headers=headers)
    return response_location.text


def get_lessons_for_all_locations():
    session.post(url_login, headers=headers, data=data_login)

    for location_name, location_id in locations.items():
        logging.info(f"Loading {location_name}")
        location_data = get_location(location_id)

        lessons = get_lessons(location_data, location_name)

        json_data = json.dumps(lessons)
        Path(f"./output/data-dum-jogy-{location_id}.json").write_text(json_data)


if __name__ == "__main__":
    get_lessons_for_all_locations()
