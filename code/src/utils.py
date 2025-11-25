def format_date(date):
    return date.strftime("%Y-%m-%d")

def log_message(message):
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")

def create_directory_if_not_exists(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)