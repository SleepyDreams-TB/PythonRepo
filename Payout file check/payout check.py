import pandas as pd

# Load the CSV file
file_path = r"C:\Users\Tiaan\Desktop\Payout file check\Payoutcheck5.csv"  # Path to your file
data = pd.read_csv(file_path)

# Extract the external references from the uploaded file
file_references = data['external_reference'].str.extract(r'(\w+)')[0].dropna().unique()

# Provided list of external references
provided_references = [
    "3AHEAFINPO002069", "3APC4FINCR010130", "3CALLEFSRE064210", "3CALPFINCR001889",
    "ACC2MFINPM000003", "AFELEHVSCR000246", "AFRBTFINCR000826", "AISPRFINPM000539",
    "BETJTFINCR000450", "BOKPAFINCR000016", "CALTSFINCR000866", "DOTO1FINCR000144",
    "EASYWFINCR004238", "FXPROFINSL000672", "IRNFXFINCR000016", "LottoFINCR000005",
    "LULABFINCR000756", "NANOPFINCR003351", "OLYMPFINCR000361", "PAYERFINCR000008",
    "PAYOPFINCR001098", "PLAYCFINCR000515", "QWIKEFINCR000755", "SMSBTFINCR000002",
    "SWIFFFINCR038293", "WEPAYFINCR004007", "XMGLOFINCR055992", "YELLCFINCR000002"
]

# Trim references to the first 10 characters for comparison
provided_references_trimmed = [ref[:10] for ref in provided_references]
file_references_trimmed = [ref[:10] for ref in file_references]

# Remove references containing the word 'ABSA' from both lists
provided_references_trimmed = [ref for ref in provided_references_trimmed if 'ABSA' not in ref]
file_references_trimmed = [ref for ref in file_references_trimmed if 'ABSA' not in ref]

# Identify references in the provided list but not in the file
missing_from_file = [
    ref for ref in provided_references_trimmed if ref not in file_references_trimmed
]

# Identify references in the file but not in the provided list
missing_from_provided = [
    ref for ref in file_references_trimmed if ref not in provided_references_trimmed
]

# Output the discrepancies
print("References in the provided list but not in the file:")
print(missing_from_file)

print("\nReferences in the file but not in the provided list:")
print(missing_from_provided)
