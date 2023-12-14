from playwright.sync_api import Playwright, sync_playwright, expect
import time

email = ""
password = ""

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://twitter.com/")
    page.get_by_test_id("loginButton").click()
    page.locator("label div").nth(3).click()
    page.get_by_label("Phone, email, or username").click()
    page.get_by_label("Phone, email, or username").fill(email)
    page.get_by_role("button", name="Next").click()
    page.get_by_label("Password", exact=True).click()
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_test_id("LoginForm_Login_Button").click()

    # ---------------------
    context.storage_state(path="auth.json")
    time.sleep(10)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
