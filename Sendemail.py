import base64
import time
import openpyxl
import pickle
import os
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'

def authenticate_gmail():
    creds = None
    
    # Load existing token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials don't exist or are invalid, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing credentials...")
            creds.refresh(Request())
        else:
            print("🔐 First time authentication - please login in the browser...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for next time
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        print("✅ Credentials saved for future runs!")
    else:
        print("✅ Using saved credentials - no authentication needed!")
    
    return build('gmail', 'v1', credentials=creds)

def create_message(to, subject, body):
    message = MIMEText(body, 'html')
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(service, to, subject, body):
    msg = create_message(to, subject, body)
    service.users().messages().send(userId='me', body=msg).execute()
    print(f"✅ Sent to: {to}")

def load_hr_list(filepath):
    wb = openpyxl.load_workbook(filepath, data_only=True)
    ws = wb.active
    contacts = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        name, company, email, _, title = row
        if email and email != "Not publicly available":
            contacts.append({
                "name": name,
                "company": company,
                "email": email,
                "title": title
            })
    return contacts

def personalised_email(name, company, title):
    # Personalise for each recipient
    first_name = name.split()[0] if name else "there"
    body = f"""
🟢🟢🟢🟢🟢 Write the email body here and delete the green bubble 🟢🟢🟢🟢🟢
"""
    return body

# ── MAIN ──
def main():
    service = authenticate_gmail()
    contacts = load_hr_list("hr_contacts.xlsx")  # Your Excel file

    DAILY_LIMIT = 50       # Stay under Gmail's safe limit
    DELAY_SECONDS = 90     # 90 sec gap between emails (looks human)

    for i, contact in enumerate(contacts):
        if i >= DAILY_LIMIT:
            print("⛔ Daily limit reached. Resume tomorrow.")
            break

        subject = f"🟢🟢🟢🟢🟢Cloud & DevOps Professional – Open to Opportunities at {contact['company']} Write the email subject here and delete the green bubble🟢🟢🟢🟢🟢"
        body    = personalised_email(contact['name'], contact['company'], contact['title'])

        try:
            send_email(service, contact['email'], subject, body)
            time.sleep(DELAY_SECONDS)  # Crucial — avoid spam triggers
        except Exception as e:
            print(f"❌ Failed for {contact['email']}: {e}")

if __name__ == "__main__":
    main()