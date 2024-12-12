# Simple NoSQL Database in Python3

Welcome to the **Simple NoSQL Database** project! This project demonstrates the creation of a lightweight NoSQL database system built in Python 3, designed for learning and exploration.

## Features

- **Data Storage with Python Dictionaries**: Tables and their data are stored using Python's dictionary data structures.
- **Classmethods for Data Structure Operations**: The project employs `@classmethod` for performing table and record manipulations in a modular and reusable manner.
- **Regular Expressions for Parsing**: Leverages Python's `re` module to locate and validate table names, column names, and other patterns.
- **Error Handling**: Implements robust error handling to ensure user-friendly feedback for invalid operations and data issues.

## Use Cases

This project is a simple yet powerful learning tool that demonstrates key concepts of:

- Object-Oriented Programming (OOP)
- Basic data structure manipulation
- Regular expression parsing
- Error handling practices

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/simple-nosql-database.git
   cd simple-nosql-database
   ```
2. Ensure you have Python 3 installed on your system.
3. Run the script directly using:
   ```bash
   python3 simple_nosql_database.py
   ```

## Usage

### Sample Commands

1. **Create a Table**:

   ```python
   create table <TABLE_NAME> (<COLUMN_NAME> <TYPE>..)
   ```

   Creates a new table named `users` with columns `id`, `name`, and `email`.

2. **Insert Data**:

   ```python
   insert into <TABLE_NAME> values(<VALUE1>...)
   ```

   Inserts a record into the `users` table.

3. **Retrieve Data**:

   ```python
   select * from TABLE_NAME
   ```

   Returns all records from the `users` table.

4. **Handle Errors Gracefully**:

   - Attempting to create a duplicate table or access a non-existent table will raise meaningful exceptions.

### Happy coding! Feel free to experiment and extend this project to suit your learning or development needs.

