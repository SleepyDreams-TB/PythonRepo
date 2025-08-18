import os
import csv
import requests #download through PIP if not already installed
import time  # Import the time module
import base64

# API endpoint
api_url = "https://services.callpay.com/api/v1/payout/validate-account"
username = "tiaanApiUAT"
password = "5.9z0+!73qXWc{7)£#&1t}AbGj4W{E"

# Manually encode the credentials in Base64
auth_string = f"{username}:{password}"
auth_encoded = base64.b64encode(auth_string.encode()).decode()

# Pass the encoded value in the Authorization header
headers = {
    "Authorization": f"Basic {auth_encoded}"
}


# List of universal banking branch codes

universal_branch_codes = {
    "fnb": "250655",
    "absa": "632005",
    "standard": "051001",
    "nedbank": "198765",
    "capitec bank": "470010",
    "capitec": "470010",
    "investec": "580105",
    "mercantile": "450105",
    "bidvest": "462005",
    "tyme": "678910",
    "tymebank": "678910",
    "windhoek": "483872",
    "afribank": "430000",
    "oldmutual": "462005",
    "discovery": "679000",
    "grindrod": "584000",
    "ubank": "431010",
    "imperial": "39001",
    "firstrand": "201419",
    "hsbc": "587000",
    "sasfin": "683000",
    "access": "410506",
    "stdchartered": "730020",
    "africanbank": "430000",
    "african": "430000",
    "bankzero": "888000",
    " " : ""
}
validation_failed = []
def validate_account(row, file_handle, line_number):
    # Prepare data for the API request
    data = {
        "transaction[bank]": row["bank"],
        "transaction[branch]": universal_branch_codes.get(row["bank"].lower(), " ") if row["bank"].strip() else row["branch"],
        "transaction[account]": row["account"],
        "transaction[customer_name]": row["customer_name"],
        "transaction[account_type]": row["account_type"],
        # Add other required parameters as needed
    }


    # Make the API request
    response = requests.post(api_url, headers=headers, data=data)

    # Introduce a delay of 0.5 second between API requests
    time.sleep(0.5)
    

    # Check the response
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            output = f"Account validated successfully for {row['customer_name']} ({row['bank']}, {row['branch']}, {row['account']} , {row['account_type']})"
        else:
            output = f"Validation failed for {row['customer_name']}: {result['message']}"
            validation_failed.append((row['customer_name'], result['message']))

    else:
        output = f"Error in API request for {row['customer_name']}: HTTP Status Code: {response.status_code}, Response Content: {response.text}"
        validation_failed.append(f"Line {line_number}: {row['customer_name']}")
    # Write to file
    file_handle.write(f"Line {line_number}: {output}\n")
    # Print to console
    print(f"Line {line_number}: {output}")

def main():
    # Construct the file path dynamically
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(script_dir, "validateLula.csv")
    output_file_path = os.path.join(script_dir, "PayoutValidate.txt")

    # Read CSV file and write to both file and console
    with open(file_path, newline="") as csvfile, open(output_file_path, "w") as output_file:
        reader = csv.DictReader(csvfile)
        for line_number, row in enumerate(reader, start=1):
            validate_account(row, output_file, line_number)
    
if __name__ == "__main__":
    main()
    print("Problematic Accounts:", validation_failed)