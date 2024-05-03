import pandas as pd
import sqlite3


def _dump_database_to_string(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Initialize an empty string to store the dumped data
    dump_string = ''

    # Get a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Iterate over each table and dump its contents to the string
    for table in tables:
        table_name = table[0]
        dump_string += f"Table: {table_name}\n"
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        for row in rows:
            # Join each row's values into a comma-separated string
            dump_string += ','.join(map(str, row)) + '\n'
        dump_string += '\n'  # Separate tables with an empty line

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    return dump_string


def data_downloader_verifier(ref: str, hyp: str) -> bool:
    """Verify if the data downloader is correct."""
    ref = pd.read_csv(ref)
    hyp = pd.read_csv(hyp)
    return ref.equals(hyp)


def problem_solver_verifier(ref: str, hyp: str) -> bool:
    """Verify if the problem solver is correct."""
    # TODO: we may need to loosen this
    return ref == hyp


def question_finder_verifier(ref: str, hyp: str) -> bool:
    """Verify if the model found the question appropriately."""
    # TODO: we may need to loosen this to account for paraphrases
    return hyp in ref


def database_writer_verifier(ref: str, hyp: str) -> bool:
    """Verify if two sqlite databases are the same."""
    ref_str = _dump_database_to_string(ref)
    hyp_str = _dump_database_to_string(hyp)
    return ref_str == hyp_str