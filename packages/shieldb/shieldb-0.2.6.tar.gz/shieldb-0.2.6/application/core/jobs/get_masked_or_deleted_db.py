import re
from sqlalchemy import text


def delete_rows_from_db(connection, table_name, percentage):
    try:
        if not 0 <= percentage <= 100:
            print("Error: Percentage should be between 0 and 100.")
            return

        with connection.begin():
            total_rows = connection.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
            rows_to_delete = int(total_rows * (percentage / 100))

            if rows_to_delete > 0:
                delete_query = text(
                    f'DELETE FROM {table_name} WHERE ctid IN (SELECT ctid FROM {table_name} ORDER BY RANDOM() LIMIT :limit)'
                ).bindparams(limit=rows_to_delete)
                connection.execute(delete_query)

                print(f"{percentage}% of data deleted from the {table_name} table.")
            else:
                print(f"No rows to delete from the {table_name} table.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()


def replace_email(match):
    email = match.group(0)
    if len(email) > 2:
        parts = email.split("@")
        username = parts[0]
        new_email = email[0] + '*' * (len(username) - 2) + username[-1] + '@' + parts[1]
        return new_email
    else:
        return email


def replace_phone_number(match):
    phone = match.group(0)
    return phone[:-4] + '****'


def replace_password(match):
    username = match.group(1)
    if len(match.group(2))>5:
        return f"{username}******"
    else:
        return f"{username}{match.group(2)}"


def replace_url(match):
    return 'https://*****.com/***'


def replace_credit_card_number(match):
    credit_card_number = match.group(0)
    return credit_card_number[:4] + '*'*(len(credit_card_number)-4)


def replace_birth_date(match):
    return re.sub(r'\d', '*', match.group())


def mask_data_in_table(connection, table_name, columns, chunk_size=10):
    try:
        patterns = {
            'tc': re.compile(r'\b(\d{4})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'credit_card': re.compile(r'\b4[0-9]{12}(?:[0-9]{3})?\b'),
            'email': re.compile(r'\b[A-Za-z0-9._*%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b'),
            'password': re.compile(r'(\b[A-Za-z0-9_-]+:)\s*\b([A-Za-z0-9_-]+)\b'),
            'url': re.compile(
                r'(https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]['
                r'a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,'
                r'}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'),
            'birth_date': re.compile(r"(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\d\d"),
        }

        replace_functions = {
            'email': replace_email,
            'phone': replace_phone_number,
            'password': replace_password,
            'tc': replace_phone_number,
            'credit_card': replace_credit_card_number,
            'url': replace_url,
            'birth_date': replace_birth_date,
        }

        total_rows = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

        for column in columns:

            for offset in range(0, total_rows, chunk_size):
                query = text(
                    f"SELECT id, {column} FROM {table_name} ORDER BY id LIMIT {chunk_size} OFFSET {offset}"
                )
                id_and_column_data = connection.execute(query).fetchall()

                for tuple_data in id_and_column_data:
                    row_id, old_value = tuple_data

                    for pattern_name, pattern in patterns.items():
                        replace_function = replace_functions.get(pattern_name, lambda x: x)
                        old_value = pattern.sub(replace_function, old_value)

                    regenerated_value = old_value
                    update_query = text(
                        f"UPDATE {table_name} SET {column} = :regenerated_value WHERE id = :row_id"
                    )
                    connection.execute(update_query, {"regenerated_value": regenerated_value, "row_id": row_id})

                print(f"Updated {chunk_size} rows in {table_name} for {column}, offset: {offset}")

        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")

