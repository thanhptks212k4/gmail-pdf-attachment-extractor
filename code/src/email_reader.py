class EmailReader:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.connection = None

    def login(self):
        import imaplib
        try:
            self.connection = imaplib.IMAP4_SSL('imap.gmail.com')
            self.connection.login(self.email, self.password)
            print("Login successful.")
        except Exception as e:
            print(f"Login failed: {e}")

    def scan_emails(self):
        if not self.connection:
            print("Not logged in. Please log in first.")
            return []
        
        self.connection.select('inbox')
        result, data = self.connection.search(None, 'ALL')
        email_ids = data[0].split()
        emails = []
        
        for email_id in email_ids:
            result, msg_data = self.connection.fetch(email_id, '(RFC822)')
            emails.append(msg_data[0][1])
        
        return emails

    def filter_emails_by_date(self, emails, date):
        from datetime import datetime
        filtered_emails = []
        for email in emails:
            # Assuming email has a date header
            email_date = self.get_email_date(email)
            if email_date and email_date.date() == date:
                filtered_emails.append(email)
        return filtered_emails

    def get_email_date(self, email):
        import email as email_module
        msg = email_module.message_from_bytes(email)
        date_header = msg['Date']
        return email.utils.parsedate_to_datetime(date_header) if date_header else None

    def logout(self):
        if self.connection:
            self.connection.logout()
            print("Logged out.")