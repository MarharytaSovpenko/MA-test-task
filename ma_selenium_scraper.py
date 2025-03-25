import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://mate.academy/"


def find_flex_course_duration(table_rows: list) -> str:
    for row in rows:
        # Check if this row contains 'Тривалість'
        if "Тривалість" in row.text:
            # Find the last cell in this row
            duration_cells = row.find_elements(
                By.CLASS_NAME, "TableColumnsView_tableCellGray__4hadg"
            )
            last_cell_text = duration_cells[-1].text.strip()
            return last_cell_text
    logging.warning("Flex course duration not found.")
    return ""


def extract_card_info(driver: WebDriver, course_card: WebElement) -> dict:

    course_name = course_card.find_element(
        By.CLASS_NAME, "ProfessionCard_title__m7uno"
    ).text
    full_time_course_duration = course_card.find_element(
        By.CLASS_NAME, "ProfessionCard_duration__13PwX"
    ).text
    course_description = (
        course_card.find_elements(By.CLASS_NAME, "ProfessionCard_description__K8weo")[0]
        .get_attribute("innerText")
        .strip()
    )
    course_link = course_card.get_attribute("href").strip()
    logging.info(
        f"Extracted card info for {course_name}: Full-time duration: {full_time_course_duration}, Description: {course_description}"
    )
    return {
        "name": course_name,
        "full_time_duration": full_time_course_duration,
        "description": course_description,
        "link": course_link,
    }


# List to hold the parsed data
courses_data = []
with webdriver.Chrome() as driver:
    driver.get(BASE_URL)
    driver.implicitly_wait(5)

    course_cards = driver.find_elements(
        By.XPATH, "//a[contains(@href, 'profession_card')]"
    )
    logging.info(f"Found {len(course_cards)} courses.")
    for num in range(len(course_cards)):
        if num != 0:
            driver.get(BASE_URL)
            course_cards = driver.find_elements(
                By.CLASS_NAME, "ProfessionCard_cardWrapper__BCg0O"
            )  # Re-find elements

        card = course_cards[num]
        card_info = extract_card_info(driver, card)
        driver.get(card_info["link"])  # Go to the course page

        # Find full-time and flex course info
        full_time_format = (
            1 if driver.find_elements(By.PARTIAL_LINK_TEXT, "повний день") else 0
        )
        flex_format = (
            1 if driver.find_elements(By.PARTIAL_LINK_TEXT, "вільний час") else 0
        )

        if flex_format:
            rows = driver.find_elements(
                By.CLASS_NAME, "TableColumnsView_contentRow__QYVPu"
            )
            flex_course_duration = find_flex_course_duration(rows)

            logging.info(
                f"Flex course duration for {card_info['name']}: {flex_course_duration}"
            )

        # Extract topic number and module count
        topic_number = driver.find_elements(
            By.CLASS_NAME, "CourseProgram_cards__CD13X"
        )[0].text.split(sep="\n")[0]
        modules = driver.find_elements(
            By.CLASS_NAME, "CourseModulesList_moduleListItem__b8AY9"
        )
        module_number = len(modules) - 1
        logging.info(f"Topic number: {topic_number}, Module count: {module_number}")
        courses_data.append(
            {
                "name": card_info["name"],
                "link": card_info["link"],
                "description": card_info["description"],
                "full_time_format": full_time_format,
                "full_time_duration": card_info["full_time_duration"],
                "flex_format": flex_format,
                "flex_course_duration": flex_course_duration,
                "topic_number": topic_number,
                "module_number": module_number,
            }
        )
df = pd.DataFrame(courses_data)
df["full_time_duration"] = df["full_time_duration"].str.replace("+", "", regex=False)
# Save to a CSV file
df.to_csv("courses_data.csv", index=False)
logging.info(f"Data saved to 'courses_data.csv'.")

video_link = "https://www.loom.com/share/03cf3b00a62641aebb103133323a8c65?sid=8845714f-99bb-4355-b4fc-6d7291696b54"
