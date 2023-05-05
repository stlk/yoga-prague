import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def get_activity_info(activity_id):
    url = "https://yk.isportsystem.cz/ajax/ajax.activity.php"
    form_data = {"id_term": activity_id}

    response = requests.post(url, data=form_data)
    response_json = response.json()
    if html_content := response_json.get("html"):
        soup = BeautifulSoup(html_content, "html.parser")
        if ui_corner_all := soup.find(class_="ui-corner-all"):
            free_spots_text = ui_corner_all.get_text(strip=True)
            if "Volno" not in free_spots_text:
                return (False, None)
            free_spaces = (
                int(free_spots_match.group(0)) if (free_spots_match := re.search(r"\d+", free_spots_text)) else None
            )
            return True, free_spaces
    return (False, None)


def to_datetime(js_timestamp: int):
    python_timestamp = js_timestamp / 1000
    return datetime.fromtimestamp(python_timestamp)


def parse_activity(activity):
    hoverinfo = activity["activity_hoverinfo"]
    soup = BeautifulSoup(hoverinfo, "html.parser")
    image = soup.find("img")
    start = to_datetime(activity["start"])

    today = datetime.now()
    if start < today:
        return

    future_date = today + timedelta(days=7)
    if start > future_date:
        return

    has_free_spaces, free_spaces = get_activity_info(activity["activity_term_id"])

    try:
        return {
            "activity_name": activity["title"],
            "activity_id": activity["activity_term_id"],
            "time_start": to_datetime(activity["start"]).isoformat(),
            "time_end": to_datetime(activity["end"]).isoformat(),
            "instructor_photo": f"https://yk.isportsystem.cz/{image['src']}" if image else None,
            "instructor_name": soup.find("div", {"class": "tItem1"}, text="Lektor").find_next_sibling("div").text,
            "price": soup.find("div", {"class": "tItem1"}, text="Cena").find_next_sibling("div").text,
            "free_spaces": free_spaces,
            "has_free_spaces": has_free_spaces,
            "link": "https://yk.isportsystem.cz/",
            "location": "Yoga Karlin",
        }
    except Exception:
        logging.exception(f"{activity['title']=}\n{hoverinfo}")


def get_lessons():
    today = datetime.now().date()

    future_date = today + timedelta(days=7)

    today_iso = today.isoformat()
    future_iso = future_date.isoformat()
    url = f"https://yk.isportsystem.cz/ajax/ajax.calendarContent.php?id_sport=5&start={today_iso}T00%3A00%3A00%2B02%3A00&end={future_iso}T00%3A00%3A00%2B02%3A00&timeZone=Europe%2FPrague"
    response = requests.get(url)
    data = response.json()

    parsed_data = []
    for activity in data:
        if activity := parse_activity(activity):
            parsed_data.append(activity)

    return parsed_data


if __name__ == "__main__":
    lessons = get_lessons()

    json_data = json.dumps(lessons)
    Path("./output/data-yk.json").write_text(json_data)
