import json
from openpyxl import Workbook
import tempfile


def json2excel(input_file: str) -> str:
    # Parse the JSON data
    data = json.loads(input_file)

    if len(data) == 0:
        return None

    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Assuming the data is a list of dictionaries
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        # Write the header row
        headers = list(data[0].keys())
        ws.append(headers)

        # Write the data rows
        for item in data:
            ws.append(list(item.values()))

    # Save the workbook to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        wb.save(tmp.name)
        return tmp.name


def json_is_correct(json_schema: str) -> str:
    try:
        json_schema = json.loads(json_schema)
        return True
    except json.JSONDecodeError as e:
        return False
