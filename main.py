import argparse
import json
from tabulate import tabulate
import sys

def specific_processing(dict_ref):
    """Perform specific processing based on the 'et' key."""
    if dict_ref.get("et") == "AUTOMATION_CONFIG_PUBLISHED_AUDIT":
        return "a_deployment_diff"
    return ""

# Headers for the tabulated output
output_headers = ["_t", "et", "cre", "source", "un", "description", "severity", "remoteAddr", "isMmsAdmin", "specialentry"]
lookup_list = ["AUTOMATION_CONFIG_PUBLISHED_AUDIT"]
headers = ["_t", "et", "cre", "source", "un", "description", "severity", "remoteAddr", "isMmsAdmin"]

def main():
    parser = argparse.ArgumentParser(description="Read and parse a JSON file.")
    parser.add_argument("--file", required=True, help="Path to the JSON file to read")
    args = parser.parse_args()

    try:
        # Read and parse the JSON file
        with open(args.file, 'r') as json_file:
            data = json.load(json_file)

        # Ensure the data is a list
        if isinstance(data, list) and data:
            rows = []
            for item in data:
                row = []
                special_entry = ""
                
                for header in headers:
                    row.append(item.get(header, 'NA'))  # Add each field's value or 'NA' if missing

                # Process special entry for rows with 'et' in lookup_list
                if item.get("et") in lookup_list:
                    special_entry = specific_processing(item)
                
                row.append(special_entry if special_entry else "NA")  # Add the special entry to the row
                rows.append(row)

            # Print the tabulated data
            print(tabulate(rows, headers=output_headers, tablefmt="grid"))
        else:
            print("JSON data is not a list or is empty.")

    except FileNotFoundError:
        print(f"Error: The file '{args.file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: The file '{args.file}' is not a valid JSON file.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

