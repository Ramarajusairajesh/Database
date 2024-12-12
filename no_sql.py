import pickle
import re
import operator

# Regular expressions (using original naming)
select_tablename = r"\bfrom\s*([\w]+)\b"
select_columns = r"\bselect\s+([\w*,\s]+)\s+from\b"
insert_tablename = r"\binto\s*(\w+)\b"
insert_columns = r"\bvalues\s*\(([\w\s,]+)\)"
create_tablename = r"\bcreate\s+table\s+(\w+)\b"
create_columns = r"\(([^)]+)\)"
delete_tablename = r"\bfrom\s+(\w+)\b"
delete_where = r"\bwhere\s+(.+)\b"
update_tablename = r"\bupdate\s+(\w+)\b"
update_where = r"\bwhere\s+(.+)\b"
drop_tablename = r"\bdrop\s+table\s+(\w+)\b"


"""
                                Example queries:
                                    select: select * from tablename
                                    insert: insert into tablename values (VALUES)
                                    create: create table tablename(c1 type,c2 type)
                                    update: update table column=value where condition_parts
                                    delete: delete table where condition=ValueError
                                    drop  : drop table tablename;


"""


class ConditionParser:
    OPERATORS = {
        "=": operator.eq,
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "!=": operator.ne,
    }

    @classmethod
    def condition_checking(cls, conditions):
        # Handles both string and list conditions
        parsed_conditions = []
        logic_type = None

        # Check for AND/OR
        if isinstance(conditions, str):
            conditions = [conditions]

        for condition in conditions:
            # Split by different logical operators
            if " and " in condition.lower():
                logic_type = "and"
                condition_parts = condition.lower().split(" and ")
            elif " or " in condition.lower():
                logic_type = "or"
                condition_parts = condition.lower().split(" or ")
            else:
                condition_parts = [condition]
                logic_type = None

            for part in condition_parts:
                # Find the first operator
                for op_symbol in cls.OPERATORS.keys():
                    if op_symbol in part:
                        column, value = part.split(op_symbol)
                        column = column.strip()
                        value = value.strip().strip("'\"")

                        # Try to convert value to appropriate type
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass

                        parsed_conditions.append(
                            {"column": column, "operator": op_symbol, "value": value}
                        )
                        break

        return parsed_conditions, logic_type


class Database:
    def __init__(self):
        self.database = {}

    def create(self, query):
        try:
            tablename = (re.search(create_tablename, query)).group(1)

            # Check if table already exists
            if tablename in self.database:
                print("Table name already exists. Try another name.")
                return 1

            # Extract columns and types
            columns_match = re.search(create_columns, query)
            if not columns_match:
                print("Invalid create table syntax")
                return 1

            columns_def = columns_match.group(1).split(",")
            temp_values = {}

            for col_def in columns_def:
                col_name, col_type = col_def.strip().split()
                temp_values[col_name] = col_type

            # Store table structure in original format
            self.database[tablename] = [temp_values, []]
            return 0

        except Exception as e:
            print(
                f"Error creating table: {
                    e}. Please type the command properly with proper spacing between words."
            )
            return 1

    def insert(self, query):
        try:
            tablename = re.search(insert_tablename, query).group(1)
            table = self.database.get(tablename)

            if not table:
                print("Table isn't present in the database")
                return 1

            # Extract values
            values_match = re.search(insert_columns, query)
            if not values_match:
                print("Invalid insert syntax")
                return 1

            values = list(map(str.strip, values_match.group(1).split(",")))

            # Check number of columns
            if len(values) != len(table[0]):
                print(
                    f"Wrong columns. Try again with your query:\n\t{
                        query}\n\tColumns inside table: {list(table[0].keys())}"
                )
                return 1

            # Create new row with type checking
            new_row = {}
            for (col_name, col_type), value in zip(table[0].items(), values):
                try:
                    # Basic type conversion
                    if col_type == "int":
                        value = int(value)
                    elif col_type == "str":
                        value = str(value)
                    new_row[col_name] = value
                except ValueError:
                    print(
                        f"Type conflict. Expected {
                            col_type} for column {col_name}"
                    )
                    return 1

            # Add row to table
            table[1].append(new_row)
            return 0

        except AttributeError:
            print(
                "Please type the command properly with proper spacing between words, with existing tablenames and column names"
            )
            return 1

    def query(self, query):
        try:
            # Extract table and column information
            tablename = (re.search(select_tablename, query)).group(1)
            table = self.database.get(tablename)

            if not table:
                print("Table isn't present in the database")
                return

            # Parse columns
            column_names = re.search(select_columns, query).group(1)
            columns = list(map(str.strip, column_names.split(",")))

            # Handle * select
            if len(columns) == 1 and columns[0] == "*":
                columns = list(table[0].keys())

            # Check column validity
            if len(columns) != len(table[0]):
                print(
                    f"Wrong columns. Try again with your query:\n\t{
                        query}\n\tColumns inside table: {list(table[0].keys())}"
                )
                return

            # Print results
            for row in table[1]:
                for column in columns:
                    print(f"| {row.get(column, 'N/A')} |", end=" ")
                print()

        except AttributeError:
            print(
                "Please type the command properly with proper spacing between words, with existing tablenames and column names"
            )

    def update(self, query):
        try:
            tablename = re.search(update_tablename, query).group(1)

            if tablename not in self.database:
                print("Table not found")
                return 1

            # Parse WHERE clause
            where_condition = re.search(update_where, query)
            if where_condition:
                conditions, logic_type = ConditionParser.condition_checking(
                    where_condition.group(1).split(",")
                )

                # Implement update logic here
                print("Update conditions parsed successfully")

            return 0

        except Exception as e:
            print(f"Error in update: {e}")
            return 1

    def delete(self, query):
        try:
            tablename = re.search(delete_tablename, query).group(1)

            if tablename not in self.database:
                print("Table is not present in the database")
                return 1

            # Parse WHERE clause
            where_condition = re.search(delete_where, query)
            if where_condition:
                conditions, logic_type = ConditionParser.condition_checking(
                    where_condition.group(1).split(",")
                )

                # Implement delete logic here
                print("Delete conditions successfully")

            return 0

        except Exception as e:
            print(f"The following error occurred: {e}")
            return 1

    def drop(self, query):
        try:
            tablename = re.search(drop_tablename, query).group(1)

            if tablename in self.database:
                self.database.pop(tablename)
                print(f"Table {tablename} dropped successfully")
            else:
                print("Table not present")

            return 0

        except Exception as e:
            print(f"Try again. Error: {e}")
            return 1


# File handling and database initialization
file = "database.db"
fr = open(file, "rb")
fw = open(file, "wb")

try:
    pfr = pickle.load(fr)
    db = pfr
except (EOFError, pickle.UnpicklingError):
    print("Creating an empty database!")
    db = Database()
except Exception as e:
    print(f"Error: {e}")
    print("Fix the source code")
    db = Database()

print(
    "Database Started\n\tThis database works similar to NoSQL but with syntax similar to MySQL \U0001f600"
)

# Main query loop
while True:
    try:
        query = input("Enter your query:\n")
        crud = query.split()[0].lower()

        if crud == "select":
            db.query(query)
        elif crud == "insert":
            a = db.insert(query)
            if a == 0:
                pickle.dump(db, fw)
                fw.flush()
        elif crud == "update":
            a = db.update(query)
            if a == 0:
                pickle.dump(db, fw)
                fw.flush()
        elif crud == "create":
            a = db.create(query)
            if a == 0:
                pickle.dump(db, fw)
                fw.flush()
        elif crud == "delete":
            a = db.delete(query)
            if a == 0:
                pickle.dump(db, fw)
                fw.flush()
        elif crud == "drop":
            a = db.drop(query)
            if a == 0:
                pickle.dump(db, fw)
                fw.flush()
        else:
            print("Please enter a valid command to run \U0001f62a")

    except KeyboardInterrupt:
        print("\nExiting database...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")

# Close file handles
fr.close()
fw.close()
