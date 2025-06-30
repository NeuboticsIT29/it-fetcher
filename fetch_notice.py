from playwright.sync_api import sync_playwright
from supabase import create_client
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
fernet = Fernet(ENCRYPTION_KEY.encode())

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

def fetch_client_credentials():
    return supabase.table("client_credentials").select("*").execute().data

def automate_download(pan, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.incometax.gov.in/iec/foportal")

        # Simulated login – update selectors per actual portal HTML
        page.locator("input[name='username']").fill(pan)
        page.locator("input[name='password']").fill(password)
        page.locator("button[type='submit']").click()

        page.wait_for_timeout(5000)  # Adjust wait
        print(f"Fetched notices for: {pan}")
        browser.close()

if __name__ == "__main__":
    clients = fetch_client_credentials()
    for client in clients:
        pan = client["pan"]
        password = decrypt_password(client["encrypted_password"])
        automate_download(pan,_
