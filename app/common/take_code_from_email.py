import pytz
from typing import Optional

import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta


def take_code_from_email(
    email_login: str,
    email_password: str,
    email_server: str,
    current_time: datetime,
    users_emails: list[str],
    users_emails_forward: Optional[list[str]] = None

) -> Optional[int]:
    """Получаем код подтверждения из входящих писем."""
    confirmation_code = None
    timer: int = 120  # Кол-во сек. в теч. скольки должен прийти код.
    start_time: datetime = datetime.now()
    today: str = datetime.now().strftime("%d-%b-%Y")

    while True:
        if confirmation_code:
            break

        if datetime.now() - start_time > timedelta(seconds=timer):
            break

        with imaplib.IMAP4_SSL(email_server) as mail:
            mail.login(email_login, email_password)
            mail.select('inbox')

            tz = pytz.timezone('Europe/Moscow')
            now = current_time.astimezone(tz)
            time_threshold = now - timedelta(seconds=timer)

            for user in users_emails:
                search_query = f'FROM "{user}" SINCE "{today}"'
                status, messages = mail.search(None, search_query)

                email_ids = messages[0].split()

                for num in email_ids:
                    status, msg_data = mail.fetch(num, '(RFC822)')
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    date_str = msg['date']
                    date_time = email.utils.parsedate_to_datetime(date_str)

                    if date_time >= time_threshold:
                        if users_emails_forward:
                            subject, encoding = decode_header(
                                msg['subject']
                            )[0] if user not in users_emails_forward else (
                                decode_header(msg['subject'])[1]
                            )
                        else:
                            subject, encoding = decode_header(
                                msg['subject']
                            )[0]

                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')

                        if 'Ваш код для авторизации' in subject:
                            confirmation_code = subject.split(
                                'Ваш код для авторизации'
                            )[1].strip()
                            return confirmation_code

    return confirmation_code
