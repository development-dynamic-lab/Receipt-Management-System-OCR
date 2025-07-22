from .prompt_template import create_prompt
from .groq_api import query_groq
from .db import get_user_id, execute_sql

def run_agent(user_uuid, user_query):
    user_id = get_user_id(user_uuid)
    if user_id is None:
        print(f"User UUID '{user_uuid}' not found in database.")
        return {"error": "Invalid user UUID"}

    prompt = create_prompt(user_query, user_id)
    sql_query = query_groq(prompt)
    print(f"\nGenerated SQL:\n{sql_query}")

    result = execute_sql(sql_query)
    return result

if __name__ == "__main__":
    # user_uuid = input("Enter your user_uuid: ").strip()
    user_query = input("Enter your question: ").strip()
    user_uuid = 'KfMlP3r8mZhACrV0CmpeOBUDUdC3'

    output = run_agent(user_uuid, user_query)
    print("\nResult:")
    print(output)
