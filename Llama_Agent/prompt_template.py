def create_prompt(natural_language, user_id):
    return f"""
You are a helpful assistant that converts natural language into SQL for a MySQL database.
Only generate SELECT queries scoped to user_id = {user_id}.

Schema:
Table: users (id, user_uuid, created_at)
Table: receipts (id, user_id, purchase_date, store_name, total_amount, consumption_tax, payment_method, created_at)
Table: items (id, receipt_id, english_name, quantity, unit_price, total_price)

The internal user ID is {user_id}.

Convert the following natural language query into a MySQL SQL query, filtering only data for this user:
\"\"\"
{natural_language}
\"\"\"

Return only the SQL query. No explanation.
"""
