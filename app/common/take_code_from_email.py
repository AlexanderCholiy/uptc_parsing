import email
import imaplib
import re
from datetime import datetime, timedelta
from email.header import Header, decode_header
from typing import Optional, Union

import chardet
import pytz
from bs4 import BeautifulSoup


class Email:

    def __init__(
        self,
        email_login: str,
        email_pswd: str,
        email_server: str,
        email_to: Optional[str] = None,
        time_seconds_wait: Optional[int] = 120,
    ):

        self.email_login = email_login
        self.email_pswd = email_pswd
        self.email_server = email_server
        self.email_to = email_to
        self.time_seconds_wait = time_seconds_wait

    def fetch_unread_emails(self) -> Optional[list[dict[str, str]]]:
        with imaplib.IMAP4_SSL(self.email_server) as mail:
            mail.login(self.email_login, self.email_pswd)

            mail.select(readonly=False)
            status, messages = mail.search(None, '(UNSEEN)')
            if status != 'OK' or not messages[0]:
                return

            email_ids: list[bytes] = messages[0].split()
            if not email_ids:
                return

            email_data = []
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                subject, encoding = decode_header(msg['Subject'])[0]

                email_subject: str = self._valid_subject_from_bytes(
                    subject, encoding
                )
                email_to: str = self._valid_email_from(msg['To'])
                email_date: datetime = datetime.strptime(
                    msg.get('Date'), '%a, %d %b %Y %H:%M:%S %z'
                )
                email_body = ''

                if msg.is_multipart():
                    for sub_index, part in enumerate(msg.walk()):
                        content_type = part.get_content_type()
                        content_disposition = str(
                            part.get('Content-Disposition')
                        )

                        if content_type == (
                            'text/plain'
                        ) and 'attachment' not in content_disposition:
                            payload = part.get_payload(decode=True)
                            email_body = self._valid_text_from_bytes(
                                payload
                            )
                else:
                    html_body_text = msg.get_payload(decode=True).decode()
                    email_body = self._valid_text_from_html(html_body_text)

                email_data.append(
                    {
                        'email_to': email_to,
                        'email_date': email_date,
                        'email_subject': email_subject,
                        'email_body': email_body,
                    }
                )
            return email_data

    def take_code_from_email(self) -> Optional[str]:
        timezone = pytz.timezone('Europe/Moscow')
        start_time = datetime.now(timezone)
        time_limit_start = start_time - timedelta(
            seconds=self.time_seconds_wait
        )
        time_limit_end = start_time + timedelta(seconds=self.time_seconds_wait)

        while True:
            timer_limit = (datetime.now(timezone) - start_time).total_seconds()
            if timer_limit > self.time_seconds_wait:
                return

            new_emails = self.fetch_unread_emails()
            if not new_emails:
                continue

            sorted_emails = sorted(
                new_emails, key=lambda x: x['email_date'], reverse=True
            )

            for new_email in sorted_emails:
                if self.email_to and new_email[
                    'email_to'
                ] != self.email_to:
                    continue

                if not time_limit_start <= new_email[
                    'email_date'
                ] <= time_limit_end:
                    continue

                email_body = new_email['email_body'].lower().strip()
                if 'ваш код для авторизации' in email_body:
                    match = re.search(
                        r'ваш код для авторизации (\d+)', email_body
                    )
                    authorization_code = match.group(1)
                    return authorization_code.strip()

    def _valid_email_from(self, email_from_original: Header) -> str:
        email_from_parser: str = email.utils.parseaddr(email_from_original)[-1]
        email_from = email_from_parser if email_from_parser else (
            str(email_from_original)
            .split()[-1]
            .replace('<', '')
            .replace('>', '')
        )
        return email_from

    def _valid_subject_from_bytes(
        self, subject: Union[bytes, str], encoding: str
    ) -> str:
        if isinstance(subject, bytes):
            try:
                email_subject = subject.decode(
                    encoding or 'utf-8', errors='replace'
                )
            except LookupError:
                email_subject = subject.decode('utf-8', errors='replace')
            return email_subject
        return subject

    def _valid_text_from_html(self, html_body_text: str) -> str:
        soup = BeautifulSoup(html_body_text, 'lxml')
        body_text = soup.get_text()
        cleaned_body_text = (
            ' '.join(body_text.replace('\n', ' ').replace('\r', ' ').split())
        )
        return cleaned_body_text

    def _valid_text_from_bytes(self, byte_body_text: bytes) -> str:
        result = chardet.detect(byte_body_text)
        encoding = result['encoding']
        body_text = byte_body_text.decode(
            encoding or 'utf-8', errors='replace'
        )
        cleaned_body_text = (
            ' '.join(body_text.replace('\n', ' ').replace('\r', ' ').split())
        )
        return cleaned_body_text
