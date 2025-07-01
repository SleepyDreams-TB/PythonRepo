from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import requests
import time
import base64
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from credentials_manager import CredentialsManager
import sys

# API Configuration
API_CONFIG = {
    "URL": "https://services.callpay.com/api/v1/payout/validate-account"
}

# Application State
APP_STATE = {
    "stop_flag": False,
    "current_file_path": None,
    "MAX_WORKERS": 5,
    "REQUEST_DELAY": 0.2,
    "frames": {
        "main_menu_frame": None,
        "selection_frame": None,
        "validation_container": None,
        "nav_container": None,
        "single_frame": None,
        "multiple_frame": None,
        "results_container": None
    }
}

# Initialize empty headers - will be populated after credentials setup
HEADERS = {}

# Create credentials manager instance
credentials_manager = CredentialsManager()

# Global UI elements with type hints
root: Optional[tk.Tk] = None
main_menu_frame: Optional[tk.Frame] = None
selection_frame: Optional[tk.Frame] = None
validation_container: Optional[tk.Frame] = None
nav_container: Optional[tk.Frame] = None
single_frame: Optional[tk.Frame] = None
multiple_frame: Optional[tk.Frame] = None
results_container: Optional[tk.Frame] = None
result_text: Optional[tk.Text] = None

# UI Elements Dictionary
UI_ELEMENTS = {
    "file_label": None,
    "validate_button": None,
    "account_number_entry": None,
    "branch_code_entry": None,
    "account_type_entry": None,
    "result_text": None,
    "results_container": None,
    "credentials_label": None
}

credentials_manager = CredentialsManager()

def show_credentials_dialog(initial_setup=False):
    dialog = tk.Toplevel(root)
    dialog.title("API Credentials Setup")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()  # Make dialog modal

    tk.Label(dialog, text="API Credentials Setup", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(dialog, text="Username:").pack()
    username_entry = tk.Entry(dialog)
    username_entry.pack(pady=5)
    
    tk.Label(dialog, text="Password:").pack()
    password_entry = tk.Entry(dialog, show="*")
    password_entry.pack(pady=5)

    def save():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Input Error", "Both fields are required!")
            return
            
        if credentials_manager.save_credentials(username, password):
            update_api_headers()
            dialog.destroy()
            if initial_setup:
                show_main_menu()
            elif UI_ELEMENTS.get("credentials_label"):  # Only update if label exists
                update_credentials_display()
    
    def on_cancel():
        if initial_setup:
            if messagebox.showwarning("Warning", "API credentials are required to use the application. Are you sure you want to exit?"):
                sys.exit()
        else:
            dialog.destroy()

    tk.Button(dialog, text="Save", command=save).pack(pady=10)
    if not initial_setup:
        tk.Button(dialog, text="Cancel", command=on_cancel).pack()

    # Handle window close button
    dialog.protocol("WM_DELETE_WINDOW", on_cancel)

def update_api_headers():
    """Update API headers with current credentials"""
    username, password = credentials_manager.get_credentials()
    if username and password:
        auth_string = f"{username}:{password}"
        auth_encoded = base64.b64encode(auth_string.encode()).decode()
        global HEADERS
        HEADERS = {
            "Authorization": f"Basic {auth_encoded}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

def update_credentials_display():
    """Update the credentials display in the application"""
    username = credentials_manager.get_credentials()[0] or "None"
    status_text = f"Current API User: {username}"
    if not credentials_manager.has_credentials():
        status_text += " ⚠️"
    UI_ELEMENTS["credentials_label"].config(text=status_text)

def check_credentials():
    """Check if credentials exist and are valid"""
    if not credentials_manager.has_credentials():
        messagebox.showerror("Error", "API credentials are required to perform this action!")
        show_credentials_dialog(True)
        return False
    return True

class UIStateManager:
    @staticmethod
    def disable_widgets(*widgets):
        for widget in widgets:
            if isinstance(widget, (tk.Button, tk.Entry)):
                widget.config(state=tk.DISABLED)
    
    @staticmethod
    def enable_widgets(*widgets):
        for widget in widgets:
            if isinstance(widget, (tk.Button, tk.Entry)):
                widget.config(state=tk.NORMAL)
    
    @staticmethod
    def clear_entry_fields(*entries):
        for entry in entries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)

def cleanup_frames(*frames):
    """Safely remove frames and clean up references"""
    for frame in frames:
        if frame and hasattr(frame, 'winfo_exists') and frame.winfo_exists():
            frame.destroy()

def confirm_exit():
    """Prompt user for confirmation before closing the application"""
    if messagebox.askokcancel("Confirm Exit", "Are you sure you want to close Bank Account Validator?"):
        cleanup_application()

def cleanup_application():
    """Clean up resources before closing"""
    APP_STATE["stop_flag"] = True
    
    # Get list of frames that exist in APP_STATE
    frames_to_cleanup = [frame for frame in APP_STATE["frames"].values() if frame]
    
    # Cleanup existing frames
    cleanup_frames(*frames_to_cleanup)
    
    root.quit()

def validate_account(account_number, branch_code, account_type, customer="Client", line_number=None):
    line_prefix = f"Line {line_number}: " if line_number else ""

    if APP_STATE["stop_flag"]:
        return "Processing aborted."

    try:
        if not all([account_number, branch_code, account_type]):
            return f"{line_prefix}Invalid input: All fields are required"

        # Map common bank type inputs to expected values
        bank_type_mapping = {
            'savings': 'savings',
            'cheque': 'cheque',
            'transmission': 'transmission',
            'current': 'current'
        }
        
        # Normalize bank type
        normalized_bank_type = bank_type_mapping.get(account_type.lower(), account_type.lower())

        # Format payload according to API requirements
        payload = {
            "transaction[bank]": normalized_bank_type,
            "transaction[branch]": branch_code.strip(),
            "transaction[account]": account_number.strip(),
            "transaction[customer]": customer.strip()
        }

        # Use form-encoded data instead of JSON
        response = requests.post(
            API_CONFIG["URL"], 
            headers=HEADERS,
            data=payload,  # Changed from json to data
            timeout=10
        )
        time.sleep(APP_STATE["REQUEST_DELAY"])
        
        if response.status_code == 401:
            return f"{line_prefix}Authentication failed: Please check API credentials"
        elif response.status_code == 400:
            return f"{line_prefix}Validation failed: Invalid account details provided"
        
        response.raise_for_status()
        result = response.json()
        
        if result.get("success"):
            return f"{line_prefix}Account validated successfully for {customer} ({normalized_bank_type}, {branch_code}, {account_number})"
        return f"{line_prefix}Validation failed: {result.get('message', 'Invalid account details')}"
        
    except requests.RequestException as e:
        error_msg = str(e)
        if "401" in error_msg:
            return f"{line_prefix}Authentication failed: Please check API credentials"
        elif "400" in error_msg:
            return f"{line_prefix}Invalid account details provided"
        return f"{line_prefix}Request failed: {error_msg}"
    except Exception as e:
        return f"{line_prefix}Unexpected error: {str(e)}"

def show_results_area():
    """Create or show existing results area"""
    global results_container, result_text
    
    if ('results_container' in UI_ELEMENTS and 
        UI_ELEMENTS["results_container"] and 
        hasattr(UI_ELEMENTS["results_container"], 'winfo_exists') and 
        UI_ELEMENTS["results_container"].winfo_exists()):
        UI_ELEMENTS["results_container"].lift()
        return

    results_container = tk.Frame(root)
    results_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
    UI_ELEMENTS["results_container"] = results_container

    tk.Label(results_container, text="Validation Results:", font=("Arial", 10, "bold")).pack(pady=5)

    result_text = tk.Text(results_container, height=15, width=100, state='disabled')
    result_text.pack(pady=5)
    UI_ELEMENTS["result_text"] = result_text

    clear_button_container = tk.Frame(results_container)
    clear_button_container.pack(fill=tk.X, padx=5)
    clear_button = tk.Button(clear_button_container, 
                            text="Clear Results", 
                            command=ResultsManager.clear_results,
                            fg="white",
                            bg="red")
    clear_button.pack(side=tk.RIGHT, pady=5)

def validate_input(value: str, field_name: str, validation_type: str = "single") -> tuple[bool, str]:
    """Unified input validation"""
    prefix = f"{validation_type.capitalize()} Validation Error"
    
    if not value.strip():
        return False, f"{prefix}: {field_name} cannot be empty"
    if not value.isdigit():
        return False, f"{prefix}: {field_name} must contain only numbers"
    return True, ""

def submit():
    """Handle single account validation submission"""
    if not check_credentials():
        return

    account_number = UI_ELEMENTS["account_number_entry"].get()
    branch_code = UI_ELEMENTS["branch_code_entry"].get()
    account_type = UI_ELEMENTS["account_type_entry"].get()

    # Validate inputs
    for value, field in [(account_number, "Account Number"), (branch_code, "Branch Code")]:
        is_valid, error = validate_input(value, field, "Single")
        if not is_valid:
            ResultsManager.show_result(error)
            return

    if not account_type.strip():
        messagebox.showwarning("Input Error", "Account Type cannot be empty!")
        return

    output = validate_account(account_number, branch_code, account_type)
    ResultsManager.show_result(output)

def validate_csv_headers(headers):
    required_headers = {'account', 'branch', 'bank', 'customer'}
    headers_lower = {h.lower() for h in headers}
    missing = required_headers - headers_lower
    if missing:
        return False, f"Missing required headers: {', '.join(missing)}"
    return True, ""

def process_csv(file_path: str):
    """Process CSV file for multiple account validation"""
    if not check_credentials():
        return []

    ResultsManager.show_result("Processing CSV file...")
    
    try:
        with open(file_path, newline="", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # Validate headers
            if not validate_csv_headers(reader.fieldnames)[0]:
                raise ValueError(f"Invalid CSV headers: {validate_csv_headers(reader.fieldnames)[1]}")
            
            accounts = []
            for line_number, row in enumerate(reader, 2):
                # Validate numeric fields
                account = row.get("account", "").strip()
                branch = row.get("branch", "").strip()
                
                for value, field in [(account, "Account Number"), (branch, "Branch Code")]:
                    is_valid, error = validate_input(value, field, "Multiple")
                    if not is_valid:
                        raise ValueError(f"Line {line_number}: {error}")
                
                if all(row.get(field, "").strip() for field in ["account", "branch", "bank"]):
                    accounts.append((account, branch, 
                                  row.get("bank", "").strip(),
                                  row.get("customer", "Client").strip(),
                                  line_number))
            return accounts
                    
    except Exception as e:
        error_msg = f"Multiple Validation Error: Failed to process CSV - {str(e)}"
        ResultsManager.show_result(error_msg)
        messagebox.showerror("Error", error_msg)
        return []

def import_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            APP_STATE["current_file_path"] = file_path
            filename = file_path.split('/')[-1]
            if UI_ELEMENTS["file_label"]:
                UI_ELEMENTS["file_label"].config(text=f"Selected file: {filename}")
            UI_ELEMENTS["validate_button"].config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Error importing file: {str(e)}")

def start_validation():
    if APP_STATE["current_file_path"]:
        if not APP_STATE["frames"]["results_container"]:
            show_results_area()
        UI_ELEMENTS["validate_button"].config(state=tk.DISABLED)
        process_csv(APP_STATE["current_file_path"])

def abort_processing():
    APP_STATE["stop_flag"] = True
    ResultsManager.show_result("Aborting process... Please wait for active requests to finish.")
    
    # Enable all buttons in multiple frame
    for child in APP_STATE["frames"]["multiple_frame"].winfo_children():
        if isinstance(child, tk.Button):
            child.config(state=tk.NORMAL)
    
    # Enable all widgets in single frame
    for child in APP_STATE["frames"]["single_frame"].winfo_children():
        if isinstance(child, (tk.Button, tk.Entry)):
            child.config(state=tk.NORMAL)

def reset_application_state():
    """Reset all application state variables"""
    APP_STATE.update({
        "stop_flag": False,
        "current_file_path": None
    })
    
    # Clear UI elements safely
    for key, element in UI_ELEMENTS.items():
        if element and hasattr(element, 'winfo_exists') and element.winfo_exists():
            if isinstance(element, tk.Entry):
                element.delete(0, tk.END)
            elif isinstance(element, tk.Text):
                element.config(state='normal')
                element.delete(1.0, tk.END)
                element.config(state='disabled')

def show_single_validation():
    manage_frames("single_frame", hide_frames=["multiple_frame"])
    
    # If results area exists, ensure it stays at bottom
    if APP_STATE["frames"]["results_container"] and APP_STATE["frames"]["results_container"].winfo_exists():
        APP_STATE["frames"]["results_container"].pack_forget()
        APP_STATE["frames"]["results_container"].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Update the switch mode button
    for widget in APP_STATE["frames"]["nav_container"].winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text').startswith('Switch'):
            widget.config(text="Switch to Multiple Validation", command=show_multiple_validation)

def show_multiple_validation():
    manage_frames("multiple_frame", hide_frames=["single_frame"])
    
    # If results area exists, ensure it stays at bottom
    if APP_STATE["frames"]["results_container"] and APP_STATE["frames"]["results_container"].winfo_exists():
        APP_STATE["frames"]["results_container"].pack_forget()
        APP_STATE["frames"]["results_container"].pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Update the switch mode button
    for widget in APP_STATE["frames"]["nav_container"].winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text').startswith('Switch'):
            widget.config(text="Switch to Single Validation", command=show_single_validation)

def show_main_menu():
    global main_menu_frame
    
    # Hide all other frames first
    manage_frames("main_menu_frame", hide_frames=[
        'selection_frame', 'validation_container', 'nav_container', 
        'single_frame', 'multiple_frame', 'results_container'
    ])
    
    # Destroy existing main menu frame if it exists
    if APP_STATE["frames"]["main_menu_frame"]:
        APP_STATE["frames"]["main_menu_frame"].destroy()
    
    # Create and show new main menu frame
    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack(expand=True, fill=tk.BOTH)
    APP_STATE["frames"]["main_menu_frame"] = main_menu_frame
    
    # Center content
    content_frame = tk.Frame(main_menu_frame)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    tk.Label(content_frame, text="Main Menu", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Button(content_frame, text="Account Validation", 
             command=show_validation_menu,
             width=20,
             height=2).pack(pady=10)

def show_validation_menu():
    """Show validation menu and handle frame cleanup"""
    global selection_frame
    
    # First clean up existing frames safely
    frames_to_hide = [
        'validation_container', 'nav_container', 'single_frame', 
        'multiple_frame', 'main_menu_frame', 'selection_frame'
    ]
    
    for frame_name in frames_to_hide:
        if APP_STATE["frames"].get(frame_name):
            frame = APP_STATE["frames"][frame_name]
            if frame and hasattr(frame, 'winfo_exists') and frame.winfo_exists():
                frame.destroy()
            APP_STATE["frames"][frame_name] = None

    # Reset application state after destroying frames
    reset_application_state()
    
    # Create new selection frame
    selection_frame = tk.Frame(root)
    APP_STATE["frames"]["selection_frame"] = selection_frame
    selection_frame.pack(expand=True, fill=tk.BOTH)
    
    # Create content
    content_frame = tk.Frame(selection_frame)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    # Add return to main menu button at top
    nav_frame = tk.Frame(selection_frame)
    nav_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    tk.Button(nav_frame, 
             text="Return to Main Menu",
             command=return_to_main_menu,
             bg='#007bff',
             fg='white').pack(side=tk.LEFT, padx=5)
    
    # Validation options
    tk.Label(content_frame, text="Account Validation", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(content_frame, text="Single Account", 
             command=lambda: select_mode("single"), 
             width=20).pack(pady=10)
    tk.Button(content_frame, text="Multiple Accounts", 
             command=lambda: select_mode("multiple"), 
             width=20).pack(pady=10)

def return_to_main_menu():
    """Return to main menu and cleanup frames"""
    APP_STATE["stop_flag"] = True
    
    # Reset states
    APP_STATE["current_file_path"] = None
    
    # Hide all frames
    frames_to_hide = [
        'validation_container', 'nav_container', 'single_frame', 
        'multiple_frame', 'selection_frame'
    ]
    
    for frame_name in frames_to_hide:
        if APP_STATE["frames"].get(frame_name):
            if hasattr(APP_STATE["frames"][frame_name], 'winfo_exists') and \
               APP_STATE["frames"][frame_name].winfo_exists():
                APP_STATE["frames"][frame_name].destroy()
            APP_STATE["frames"][frame_name] = None
    
    # Show main menu
    show_main_menu()

def show_selection_frame():
    global selection_frame, single_frame, multiple_frame
    
    # Hide validation container if it exists
    manage_frames("selection_frame", hide_frames=[
        'validation_container', 'nav_container', 'single_frame', 
        'multiple_frame', 'results_container'
    ])
    
    # Show selection frame
    selection_frame = tk.Frame(root)
    selection_frame.pack(expand=True, fill=tk.BOTH)
    APP_STATE["frames"]["selection_frame"] = selection_frame
    
    # Center the content in the selection frame
    content_frame = tk.Frame(selection_frame)
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    tk.Label(content_frame, text="Select Validation Type", font=("Arial", 14)).pack(pady=20)
    tk.Button(content_frame, text="Single Account", 
             command=lambda: select_mode("single"), 
             width=20).pack(pady=10)
    tk.Button(content_frame, text="Multiple Accounts", 
             command=lambda: select_mode("multiple"), 
             width=20).pack(pady=10)

def select_mode(mode):
    """Handle mode selection and interface setup"""
    # First destroy existing frames safely
    frames_to_hide = [
        'selection_frame', 'validation_container', 
        'nav_container', 'single_frame', 'multiple_frame'
    ]
    
    for frame_name in frames_to_hide:
        if APP_STATE["frames"].get(frame_name):
            frame = APP_STATE["frames"][frame_name]
            if frame and hasattr(frame, 'winfo_exists') and frame.winfo_exists():
                frame.destroy()
            APP_STATE["frames"][frame_name] = None
    
    # Show main interface with selected mode
    setup_main_interface(mode)

def setup_main_interface(initial_mode):
    global root, single_frame, multiple_frame, nav_container, validation_container
    
    # Create navigation buttons container at the top
    nav_container = tk.Frame(root)
    nav_container.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    APP_STATE["frames"]["nav_container"] = nav_container
    
    # Add Back and Switch Mode buttons
    tk.Button(nav_container, 
             text="Back to Menu", 
             command=show_validation_menu,
             bg='#007bff',
             fg='white').pack(side=tk.LEFT, padx=5)
    
    if initial_mode == "single":
        tk.Button(nav_container,
                text="Switch to Multiple Validation",
                command=show_multiple_validation,
                bg='#007bff',
                fg='white').pack(side=tk.LEFT, padx=5)
    else:
        tk.Button(nav_container,
                text="Switch to Single Validation",
                command=show_single_validation,
                bg='#007bff',
                fg='white').pack(side=tk.LEFT, padx=5)
    
    # Create main container for validation frames
    validation_container = tk.Frame(root)
    validation_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
    APP_STATE["frames"]["validation_container"] = validation_container

    # Single Validation Frame
    single_frame = tk.Frame(validation_container)
    tk.Label(single_frame, text="Single Account Validation", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(single_frame, text="Account Number:").pack()
    UI_ELEMENTS["account_number_entry"] = tk.Entry(single_frame)
    UI_ELEMENTS["account_number_entry"].pack()
    tk.Label(single_frame, text="Branch Code:").pack()
    UI_ELEMENTS["branch_code_entry"] = tk.Entry(single_frame)
    UI_ELEMENTS["branch_code_entry"].pack()
    tk.Label(single_frame, text="Account Type:").pack()
    UI_ELEMENTS["account_type_entry"] = tk.Entry(single_frame)
    UI_ELEMENTS["account_type_entry"].pack()
    tk.Button(single_frame, text="Submit", command=submit).pack(pady=5)
    APP_STATE["frames"]["single_frame"] = single_frame

    # Multiple Validation Frame
    multiple_frame = tk.Frame(validation_container)
    tk.Label(multiple_frame, text="Multiple Account Validation", font=("Arial", 12, "bold")).pack(pady=10)
    
    # File selection and display area
    file_frame = tk.Frame(multiple_frame)
    file_frame.pack(fill=tk.X, pady=5)
    
    tk.Button(file_frame, text="Import CSV File", command=import_file).pack(side=tk.LEFT, padx=5)
    UI_ELEMENTS["file_label"] = tk.Label(file_frame, text="No file selected", width=40)
    UI_ELEMENTS["file_label"].pack(side=tk.LEFT, padx=5)
    UI_ELEMENTS["validate_button"] = tk.Button(file_frame, text="Validate", command=start_validation, 
                              state=tk.DISABLED, bg='green', fg='white')
    UI_ELEMENTS["validate_button"].pack(side=tk.LEFT, padx=5)
    
    abort_button = tk.Button(multiple_frame, text="Abort Validation Process", 
                           command=abort_processing, fg="white", bg="red")
    abort_button.pack(pady=5)
    APP_STATE["frames"]["multiple_frame"] = multiple_frame

    # Credentials Display
    credentials_frame = tk.Frame(root)
    credentials_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
    UI_ELEMENTS["credentials_label"] = tk.Label(credentials_frame, text="Current API User: None ⚠️", font=("Arial", 10))
    UI_ELEMENTS["credentials_label"].pack(side=tk.LEFT, padx=5)
    tk.Button(credentials_frame, text="Setup API Credentials", command=lambda: show_credentials_dialog(False)).pack(side=tk.RIGHT, padx=5)

    update_credentials_display()

    if initial_mode == "single":
        show_single_validation()
    else:
        show_multiple_validation()

def manage_frames(show_frame: str, hide_frames: list = None):
    """Centralized frame management"""
    # First destroy or hide all frames that need to be hidden
    if hide_frames:
        for frame_name in hide_frames:
            if APP_STATE["frames"].get(frame_name):
                frame = APP_STATE["frames"][frame_name]
                if frame and hasattr(frame, 'winfo_exists') and frame.winfo_exists():
                    frame.destroy()  # Destroy instead of pack_forget
                APP_STATE["frames"][frame_name] = None  # Clear the reference
    
    # Special handling for results container if it exists
    results_container = APP_STATE["frames"].get("results_container")
    if results_container and hasattr(results_container, 'winfo_exists') and results_container.winfo_exists():
        results_container.pack_forget()
    
    # Show the requested frame
    if APP_STATE["frames"].get(show_frame):
        APP_STATE["frames"][show_frame].pack(expand=True, fill=tk.BOTH)
        
    # Repack results container at the bottom if it exists
    if results_container and hasattr(results_container, 'winfo_exists') and results_container.winfo_exists():
        results_container.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)

class ResultsManager:
    @staticmethod
    def show_result(message: str):
        """Display result in results area"""
        if not UI_ELEMENTS.get("results_container"):
            show_results_area()
        UI_ELEMENTS["result_text"].config(state='normal')
        UI_ELEMENTS["result_text"].insert(tk.END, f"{message}\n")
        UI_ELEMENTS["result_text"].config(state='disabled')
        UI_ELEMENTS["result_text"].see(tk.END)

    @staticmethod
    def clear_results():
        """Clear results area"""
        if UI_ELEMENTS.get("result_text"):
            UI_ELEMENTS["result_text"].config(state='normal')
            UI_ELEMENTS["result_text"].delete(1.0, tk.END)
            UI_ELEMENTS["result_text"].config(state='disabled')

def main():
    """Initialize and run application"""
    global root
    root = tk.Tk()
    root.title("Bank Account Validator")
    root.geometry("820x650")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", confirm_exit)
    
    initialize_app()
    root.mainloop()

def initialize_app():
    """Initialize application state"""
    if not credentials_manager.has_credentials():
        show_credentials_dialog(initial_setup=True)
    else:
        update_api_headers()
        show_main_menu()

if __name__ == "__main__":
    main()
