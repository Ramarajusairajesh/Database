import pickle
import re

file = "database.db"
TN_pattern = r"\bfrom\s*([\w]+)\b"
CLM_pattern = r"\bselect\s+([\w*,\s]+)\s+from\b"

"""
database strcture:
{   tablename:[
                {strucutre} , [ [values], [values] ]  ]}
                                | row   |
                                |entire table valeus|


"""


class Database:
    def __init__(self):
        self.database = {}

    def query(self, query):
        try:
            tablename = (re.search(TN_pattern, query)).group(1)
            table = self.database.get(tablename)
            if not table:
                print("Table isn't present in the database")
            else:
                column_names = re.search(CLM_pattern, query).group(1)
                columns = list(map(str.strip, list(column_names.split(","))))
                indexes = []
                if len(columns) == 1 and columns[0] == "*":
                    for row in table[1]:
                        for values in row:
                            print(f"| {values} | ", end="")
                        print()
                else:
                    for column in columns:
                        if column not in table:
                            print(f"{column} not present in the table")
                            return

        except AttributeError:
            print("Please type the command properly with proper spacing between words")

    def insert(self, query):
        pass

    def create(self, query):
        pass

    def delete(self, query):
        pass

    def update(sellf, query):
        pass

    def drop(self, query):
        pass


db = Database()
print(
    "Database Started\n \t This database works similar to nosql but syntax similar to Mysql",
    end=" ",
)
print("\U0001f600")
while True:
    query = input("Enter your query:\n")
    crud = ((query.split(" "))[0]).lower()
    if crud == "select":
        db.query(query)
    elif crud == "insert":
        db.insert(query)
    elif crud == "update":
        db.update(query)
    elif crud == "create":
        db.create(query)
    elif crud == "delete":
        db.delete(query)
    elif crud == "drop":
        db.drop(query)
    else:
        print("Plese enter a valid command to run \U0001f62a")
