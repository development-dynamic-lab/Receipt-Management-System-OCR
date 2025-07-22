import mysql.connector
from datetime import datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()


# Access variables
def get_env_variables():
    try:
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        return {
            'db_host':db_host,
            'db_user':db_user,
            'db_password': db_password,
            'db_name': db_name
        }
    except Exception as e:
        return e

def parse_yen(value):
    """
    Cleans and converts a Japanese yen string (e.g., '¥36 (10%)') to a float.
    """
    cleaned = re.sub(r'[^\d¥円.,]', '', value)
    cleaned = cleaned.replace('¥', '').replace('円', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0  # fallback if something can't be parsed

def parse_date(date_input):
    """
    Parses a date from a list of formats and returns a date object.
    """
    date_list = date_input if isinstance(date_input, list) else [date_input]
    for date_str in date_list:
        for fmt in ('%d/%m/%Y', '%Y/%m/%d', '%m/%d/%Y'):
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
    raise ValueError(f"Could not parse date from input: {date_input}")

def store_receipts_for_user(user_uuid, receipts):
    db_varaibles = get_env_variables()
    conn = mysql.connector.connect(
        host=db_varaibles['db_host'],
        user=db_varaibles['db_user'],
        password=db_varaibles['db_password'],
        database=db_varaibles['db_name']
    )
    cursor = conn.cursor()

    # Get or create user
    cursor.execute("SELECT id FROM users WHERE user_uuid = %s", (user_uuid,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO users (user_uuid) VALUES (%s)", (user_uuid,))
        user_id = cursor.lastrowid

    for receipt in receipts:
        try:
            purchase_date = parse_date(receipt['Date'])
            store_name = receipt['Store Name'][0]
            total_amount = parse_yen(receipt['Total Amount'][0])
            consumption_tax = parse_yen(receipt['Consumption Tax'][0])
            payment_method = receipt['Payment Method'][0]

            try:
                # Try inserting the receipt (skip if duplicate due to unique constraint)
                cursor.execute("""
                    INSERT INTO receipts (user_id, purchase_date, store_name, total_amount, consumption_tax, payment_method)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, purchase_date, store_name, total_amount, consumption_tax, payment_method))
                receipt_id = cursor.lastrowid
            except mysql.connector.errors.IntegrityError:
                print(f"⚠️ Duplicate receipt skipped: {purchase_date} | {store_name} | ¥{total_amount}")
                continue

            # Insert items
            for item in receipt['Itemized List']:
                cursor.execute("""
                    INSERT INTO items (receipt_id, english_name, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    receipt_id,
                    item['englishName'],
                    item['quantity'],
                    item['unitPrice'],
                    item['totalPrice']
                ))

        except Exception as e:
            print(f"❌ Error processing receipt: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ All data inserted successfully.")

# Run the function
# store_receipts_for_user(user_uuid, receipts_data)
