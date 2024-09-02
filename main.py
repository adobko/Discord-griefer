from playwright.sync_api import sync_playwright, Page, ElementHandle
import json

def load_settings() -> dict[str, str | dict]:
    with open("settings.json", "r") as f:
        return json.load(f)

def login(page: Page, credentials: dict[str, str]):
    page.wait_for_load_state("networkidle")
    login_field = page.get_by_label("Email or Phone Number")
    password_feild = page.get_by_label("Password")
    login_field.fill(value=credentials["login"])
    password_feild.fill(value=credentials["password"])
    page.click(selector="button[type=submit]")

def send_message(message: str, message_textbox: ElementHandle, page: Page) -> None:
    message_textbox.fill(message)
    page.keyboard.press("Enter")

def ban(username: str, page: Page) -> None:
    page.keyboard.type("/ban @" + username)
    page.keyboard.press("Tab")
    page.keyboard.type("Previous 7 days")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")

def banning(ban_options: dict[str, bool | list], credentials: dict[str, str], page: Page):
    if ban_options["ban"]:
        try:
            page.click(selector='div[aria-label="Show Member List"]', timeout=5e3)
        except:
            pass
        previous = 0
        while True:
            usernames = []
            page.wait_for_selector('div[aria-label="Members"]')
            scraped = page.query_selector_all('div[aria-label="Members"] > div > div > div > div[aria-label]')
            usernames = [member.get_attribute("aria-label").split(", ")[0] for member in scraped]
            print(usernames)
            if previous == (previous:=len(usernames)):
                break
            for username in usernames:
                if username != credentials["username"] and username not in ban_options["whitelisted_usernames"]:
                    ...
                    #ban(username, page)
            

def spamming(spam_options: dict[str, bool | list | int], page: Page):
    if spam_options["spam"] and len(spam_options["messages_to_spam"]) > 0:
        message_textbox = page.query_selector('div[role="textbox"]')
        repeated = 0
        while True:
            if repeated != spam_options["repeat"]:
                for message in spam_options["messages_to_spam"]:
                    send_message(str(message), message_textbox, page)
            repeated += 1

def main() -> None:
    settings = load_settings()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto("https://discord.com/login")
        login(page, settings["credentials"])
        input("Please select target server, than PRESS enter...")
        banning(settings["options"]["banning"], settings["credentials"], page)
        spamming(settings["options"]["spamming"], page)
        input("PRESS enter to exit...")

if __name__ == "__main__":
    main()