from playwright.sync_api import sync_playwright  # Importing Playwright for browser automation
from fake_useragent import UserAgent  # Importing UserAgent to generate random user agents
import random  # Importing random module

def run_bot(product_url):
    # Using Playwright to automate browser actions
    with sync_playwright() as playwright:
        # Launching a Chromium browser instance
        browser = playwright.chromium.launch(headless=False)
        # Creating a new browser context with a random user agent
        context = browser.new_context(user_agent=UserAgent().random)
        # Opening a new page in the browser
        page = context.new_page()
        # Navigating to the product URL
        page.goto(product_url)

        try:
            # Attempting to click the "Add to Cart" button
            page.locator("#add-to-cart").click()
            # Navigating to the checkout page
            page.goto("https://example.com/checkout")
            # Attempting to click the "Submit Order" button
            page.locator("#submit-order").click()

        finally:
            # Closing the browser
            browser.close()