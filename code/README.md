# ECIS Booking Classifier

The ECIS Booking Classifier is a Python application designed to automate the process of classifying booking emails by their ECIS numbers. The application logs into an email account, scans for booking emails, reads PDF booking files to extract ECIS numbers, and organizes the bookings into folders named after the corresponding ECIS numbers.

## Project Structure

```
ecis-booking-classifier
├── src
│   ├── main.py            # Entry point of the application
│   ├── email_reader.py    # Handles email login and retrieval
│   ├── pdf_parser.py      # Extracts ECIS numbers from PDF files
│   ├── ecis_classifier.py  # Classifies bookings and saves them into folders
│   └── utils.py           # Utility functions for the application
├── requirements.txt       # Lists project dependencies
└── README.md              # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ecis-booking-classifier
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment. You can create one using `venv` or `conda`.
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

## Usage

1. **Configure Email Settings:**
   Update the email credentials and settings in the `email_reader.py` file.

2. **Run the Application:**
   Execute the main script to start the application.
   ```
   python src/main.py
   ```

3. **Schedule the Script:**
   You can set up a task scheduler (like cron on Unix or Task Scheduler on Windows) to run the script multiple times a day.

## Features

- **Email Scanning:** Automatically logs into an email account and scans for booking emails.
- **PDF Parsing:** Reads PDF files to extract ECIS numbers.
- **Booking Classification:** Organizes bookings into folders based on ECIS numbers.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.