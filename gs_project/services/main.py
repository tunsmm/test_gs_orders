from services.db import DataBaseSheet, session
from services.gs_worker import GoogleSheetDate
from services.helpers import convert_usd_to_rub

# Input name for your credentials file here
CREDENTIALS_FILE = 'creds.json'
# ID for your Google Sheet (use it from url https://docs.google.com/spreadsheets/d/15d4M4wpqAgbVGopxPapzHu1LO3rdZacNBSgumE8XfVQ/edit)
spreadsheet_id = '15d4M4wpqAgbVGopxPapzHu1LO3rdZacNBSgumE8XfVQ'


def main():
    """Main function to read data from Google Sheet and upload it to database"""
    gs = GoogleSheetDate(CREDENTIALS_FILE, spreadsheet_id)
    
    message = ''

    # If the version of Google Sheet has changed, then we parse the new data
    if gs.check_revision_sheet():
        message += 'The current version of Google Sheet has changed.'
        
        google_file = gs.read_file()
        
        # If there are orders in the database that are not in the Google Sheet, then we delete this difference
        diff_order = gs.diff_order_db_vs_sheet(google_file)
        if len(diff_order):
            DataBaseSheet.delete(diff_order)

        # Checking all records against the database
        for record in google_file:
            id_number, number_order, cost_usd, delivery = record

            # Check delivery date
            gs.check_order_date(delivery, number_order)

            # Create a new object of DataBaseSheet class
            row = DataBaseSheet(id=id_number, number_order=number_order,
                                cost_usd=cost_usd, cost_rub=convert_usd_to_rub(cost_usd),
                                delivery=delivery)

            # Сheck if number_order exists and such an order is already in the database
            if DataBaseSheet.is_exist(number_order):
                # Check if this order has any changes
                if DataBaseSheet.is_changes(record):
                    DataBaseSheet.update(record)
            # If this number_order doesn't exist
            else:
                session.add(row)
                session.commit()
    else:
        message += 'The current version of Google Sheet has not changed.'
        
    return message
