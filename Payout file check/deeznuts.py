import pandas as pd
import sys

# Set display options to show full numbers
pd.set_option('display.float_format', lambda x: '%.0f' % x if x.is_integer() else str(x))
pd.set_option('display.max_columns', None)

try:
    # Load the data from the Excel file
    file_path = r'C:\Users\Tiaan\Desktop\Python Projects\Payout file check\Call Pay deposits 1-28 Feb 2025.xlsx'
    df = pd.read_excel(file_path)

    # Convert 'DESCRIPTION' and 'merchant_reference' to numeric, preserving full precision
    df['DESCRIPTION'] = pd.to_numeric(df['DESCRIPTION'], errors='coerce', downcast=None)
    df['merchant_reference'] = pd.to_numeric(df['merchant_reference'], errors='coerce', downcast=None)

    # Find matching references between Description and merchant_reference
    matching_refs = df[df['DESCRIPTION'] == df['merchant_reference']][['DESCRIPTION', 'merchant_reference']]
    
    # Rename columns for clarity in output
    matching_refs.columns = ['Description', 'Merchant Reference']
    
    # Display matching references
    print("Found matching references:")
    print(matching_refs)
    
    # Save only matching references to CSV
    output_path = r'matched_references.csv'
    matching_refs.to_csv(output_path, index=False)
    print(f"\nMatching references saved to: {output_path}")

except ModuleNotFoundError:
    print("Please install required package using: pip install openpyxl")
    sys.exit(1)
except FileNotFoundError:
    print(f"Error: Could not find the Excel file at {file_path}")
    sys.exit(1)
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(1)
