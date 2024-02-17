from icecream import ic
from coding_solver import gmail_api

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    creds = gmail_api.authenticate(SCOPES)
    ic(creds)
    get_label = gmail_api.find_label(creds)
    ic(get_label['name'])

    if get_label:
        gmail_api.get_latest_daily_email(get_label, creds)


if __name__ == '__main__':
    main()
