class ECISClassifier:
    def __init__(self, base_folder):
        self.base_folder = base_folder

    def classify_booking(self, ecis_number, booking_data):
        folder_path = self.save_to_folder(ecis_number)
        # Logic to save booking data to the corresponding ECIS folder
        with open(os.path.join(folder_path, 'booking_data.txt'), 'a') as f:
            f.write(booking_data + '\n')

    def save_to_folder(self, ecis_number):
        folder_path = os.path.join(self.base_folder, ecis_number)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path