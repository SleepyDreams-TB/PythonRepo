import json
import os
from tkinter import messagebox

class CredentialsManager:
    def __init__(self):
        self.credentials_file = "api_credentials.json"
        self.credentials = {
            "username": "",
            "password": ""
        }
        self.load_credentials()

    def load_credentials(self):
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    self.credentials = json.load(f)
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load credentials: {str(e)}")
            return False

    def save_credentials(self, username, password):
        try:
            self.credentials = {
                "username": username.strip(),
                "password": password.strip()
            }
            with open(self.credentials_file, 'w') as f:
                json.dump(self.credentials, f)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save credentials: {str(e)}")
            return False

    def get_credentials(self):
        return self.credentials["username"], self.credentials["password"]

    def has_credentials(self):
        return bool(self.credentials["username"] and self.credentials["password"])