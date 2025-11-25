import os
import base64
import pickle
import io
import re
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pdfplumber
from ecis_classifier import ECISClassifier

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client.json', SCOPES)
            creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def get_parts(part):
    """Đệ quy tìm tất cả parts chứa file PDF"""
    parts = []
    if 'parts' in part:
        for subpart in part['parts']:
            parts.extend(get_parts(subpart))
    else:
        parts.append(part)
    return parts

def extract_ecis_from_bytes(pdf_bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() or ""
            match = re.search(r'ECIS\d+', full_text)
            if match:
                return match.group(0)
    except Exception as e:
        print(f"❌ Lỗi đọc nội dung PDF trong bộ nhớ: {e}")
    return None

def process_emails_and_save(service, save_folder, ecis_classifier):
    today_query = datetime.now().strftime("after:%Y/%m/%d")
    query = f'has:attachment filename:pdf {today_query}'

    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        print(f"🔍 Tìm thấy {len(messages)} email có file PDF hôm nay.")
    except HttpError as e:
        print(f"❌ Lỗi khi truy cập Gmail API: {e}")
        return

    for msg in messages:
        try:
            msg_id = msg['id']
            msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            payload = msg_data.get('payload', {})
            parts = get_parts(payload)

            for part in parts:
                filename = part.get('filename', '')
                if filename.lower().endswith('.pdf') and 'body' in part and 'attachmentId' in part['body']:
                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(
                        userId='me', messageId=msg_id, id=att_id).execute()
                    file_data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))

                    ecis_number = extract_ecis_from_bytes(file_data)
                    if ecis_number:
                        file_path = os.path.join(save_folder, filename)
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        print(f"📥 Đã lưu file có ECIS {ecis_number}: {file_path}")
                        ecis_classifier.classify_booking(ecis_number, file_path)
                        print(f"✅ Đã phân loại ECIS {ecis_number}")
                    else:
                        print(f"⚠️ File {filename} KHÔNG có số ECIS, bỏ qua.")
        except Exception as e:
            print(f"❌ Lỗi xử lý email ID {msg['id']}: {e}")

def main():
    base_folder = r"D:\Downloads\gmail_api\ecis-booking-classifier\ECIS_Folder"
    temp_folder = r"D:\Downloads\gmail_api\ecis-booking-classifier\tmp"
    os.makedirs(temp_folder, exist_ok=True)

    ecis_classifier = ECISClassifier(base_folder)

    print("🔐 Đăng nhập Gmail...")
    service = gmail_authenticate()

    print("📨 Đang kiểm tra email và lưu PDF có ECIS...")
    process_emails_and_save(service, temp_folder, ecis_classifier)

if __name__ == '__main__':
    main()
