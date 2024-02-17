import base64
import sys
import os

from icecream import ic

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def authenticate(*api_scopes):
    '''
    https://developers.google.com/gmail/api/quickstart/python#step_3_set_up_the_sample
    https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

    :param client_secret_file:
    :param api_name:
    :param api_version:
    :param api_scopes:
    :return:
    '''
    scopes = [scope for scope in api_scopes[0]]
    ic(scopes)

    get_creds_file = os.path.join(BASE_DIR, 'coding_solver', 'credentials', 'client_secret.json')

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                get_creds_file,
                scopes,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'
            )

            auth_url, _ = flow.authorization_url(prompt='consent')
            print('Please go to this URL: {}'.format(auth_url))

            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)

            creds = flow.credentials

            with open(os.path.join(BASE_DIR, 'token.json'), 'w') as token:
                token.write(creds.to_json())

    return creds


def find_label(creds):
    '''
    :param creds:
    :return:
    '''
    daily_coding_problem_label = 'Daily Coding Problem'
    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            sys.exit(1)

        for label in labels:
            if label['name'] == daily_coding_problem_label:
                ic(label)
                return label
    except HttpError as error:
        ic(error)

    return None


def get_latest_daily_email(label_data, creds):
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=[label_data['id']]).execute()
    messages = results.get('messages', [])
    ic(messages[0]['id'])

    email = service.users().messages().get(userId='me', id=messages[0]['id']).execute()

    if 'parts' in email['payload']:
        parts = email['payload']['parts']
        for part in parts:
            if part['mimeType'] == 'text/plain':
                message = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                print("Plain Text Body:")
                ic(message)
                return message

    return None
