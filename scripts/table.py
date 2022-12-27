import os
import sys
import sqlite3
import subprocess
from pathlib import Path
try:
    from rich.console import Console
    from rich.table import Table
except ImportError as module:
    subprocess.run([sys.executable, "-m", "pip", "install", "rich"], stdout=subprocess.DEVNULL)
    from rich.console import Console
    screen = Console()


guide_message = """With the table command, you can easily create your own tables and save and recall them.

Parameters:
empty table will show all tables
-init create new table with columns -> example: table -init MyTable col1 col2 col3 ...
-rmt remove table -> example: table -rmt MyTable
-add add row to table -> example: table -add MyTable
-del remove row from table by column -> example: table -del MyTable col1 Python"""


scripts_path = Path(__file__).parent
connector = sqlite3.connect(Path(scripts_path, ".tables.db"))
cursor = connector.cursor()


def table_exists(table_name):
    cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return True if cursor.fetchone()[0] == 1 else False


def create_table(table_name: str, columns: list):
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({' text, '.join(columns) + ' text'});")


def show_all_tables(tables):
    max_length = 0
    for table in tables:
        max_length = len(table) if len(table) > max_length else max_length

    screen.print(f"[{len(tables)} Tables]: ", style="bold yellow")

    index = 0
    while index < len(tables):
        space = " " * (max_length - len(tables[index]))
        screen.print(tables[index], end=f"{space} \t\t\t", style="green")
        if index + 1 < len(tables):
            screen.print(tables[index + 1], style="green")
        index += 2

    if len(tables) % 2 != 0: print()


def show_table(table_name: str):
    table = Table(title=f'{table_name} Table')

    data = cursor.execute(f"SELECT * FROM {table_name}")
    for col in data.description:
        table.add_column(col[0], justify='center')

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()

    if len(data) > 0:
        for row in data:
            table.add_row(*row)
        screen.print(table)
    else:
        screen.print("Error: Table is empty!", style="red")


def add_row(table_name: str):
    try:
        data = cursor.execute(f"SELECT * FROM {table_name}")
        inputs_list = []
        for col in data.description:
            user_input = input(f"{col[0]}: ")
            inputs_list.append(user_input)

        inputs_list = [f"'{item}'" for item in inputs_list]
        cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(inputs_list)})")
        connector.commit()

        screen.print(f"The row was successfully added to the table!", style="green")

    except sqlite3.OperationalError:
        screen.print(f"Error: Please enter your entries in an acceptable form!", style="red")


def get_table_length(table_name: str):
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    return len(data)


def del_row(table_name: str, col: str, data: str):
    try:
        table_length_before = get_table_length(table_name)
        cursor.execute(f"DELETE FROM {table_name} WHERE {col} = '{data}'")
        connector.commit()

        table_length_after = get_table_length(table_name)
        if table_length_before == table_length_after:
            screen.print(f"Error: No information was found with this specification!", style="red")
        else:
            screen.print(f"The row was successfully deleted from the table!", style="green")

    except sqlite3.OperationalError:
        screen.print(f"Error: There is no column with '{col}' name in this table!", style="red")


rm_table = lambda table_name: cursor.execute(f"DROP TABLE {table_name}")


# Start-point.
def init():
    # If the script is called alone.
    if len(sys.argv) == 1:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        if len(tables) > 0:
            show_all_tables(tables)
        else:
            screen.print("Error: No previously created tables found!", style="red")


    # If the script is called with the -h parameter.
    # Display help and description of the called script with -h parameter.
    elif len(sys.argv) == 2 and sys.argv[1] == "-h":
        screen.print(guide_message, style="green")

    # If the script is called with any parameter except ("-h", "-init", "-add", "-del", "-rmt").
    elif len(sys.argv) == 2 and sys.argv[1] not in ["-h", "-init", "-add", "-del", "-rmt"]:
        if table_exists(table_name=sys.argv[1]):
            show_table(sys.argv[1])
        else:
            screen.print("Error: No table with this name has been registered!", style='red')

    # If the script is called with the -init parameter.
    elif len(sys.argv) > 3 and sys.argv[1] == "-init":
        if not table_exists(table_name=sys.argv[2]):
            create_table(table_name=sys.argv[2], columns=sys.argv[3:])
            screen.print(f"The '{sys.argv[2]}' table was created successfully!", style="green")
        else:
            screen.print("Error: A table with this name already exists!", style="red")

    # If the script is called with the -add parameter.
    elif len(sys.argv) == 3 and sys.argv[1] == "-add":
        if table_exists(table_name=sys.argv[2]):
            add_row(table_name=sys.argv[2])
        else:
            screen.print("Error: No table with this name has been registered!", style='red')

    # If the script is called with the -del parameter.
    elif len(sys.argv) == 5 and sys.argv[1] == "-del":
        if table_exists(table_name=sys.argv[2]):
            del_row(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            screen.print("Error: No table with this name has been registered!", style='red')

    # If the script is called with the -rmt parameter.
    elif len(sys.argv) == 3 and sys.argv[1] == "-rmt":
        if table_exists(sys.argv[2]):
            ask_to_remove = input("Are you sure? (y/n): ").lower()
            if ask_to_remove == "y":
                rm_table(sys.argv[2])
                screen.print("Table deleted successfully!", style="green")
        else:
            screen.print("Error: No table with this name has been registered!", style='red')

    # If none of these.
    else:
        screen.print("Error: Unknown parameters!", style="red")


# The starting point is set on the init function.
if __name__ == "__main__":
    init()