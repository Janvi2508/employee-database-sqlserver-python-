Project: Establish Connectivity with SQL Server Database Using Python

##  Project Overview

This project demonstrates how to connect a Microsoft SQL Server database (hosted on Azure) to a Python application. It is part of an internship assignment focused on working with databases and backend integration. The project includes two versions(The 2nd version includes the enhancements done by me in the basic version(1st version- as per project description provided at the portal)):

-  A **console-based version** (`connect_sql.py`) that retrieves data from the "Employees" table, and prints the first 5 rows of the table by establishing  a connection to the SQL Server database using the provided credentials.
-  A **GUI-based version** (`gui_employee_db.py`) is an attractive GUI version made by using `tkinter` to provide an interactive interface that I made to add some innovation and enhancement in the given project.

Both versions connect to the same remote SQL Server and interact with a table named `Employees` from the database `CompanyDB`.

##  Technologies Used

| Category             | Tools / Libraries                         |
|----------------------|-------------------------------------------|
| Programming Language | Python 3.x                                |
| GUI Framework        | tkinter                                   |
| Database Driver      | pyodbc                                    |
| Data Handling        | pandas                                    |
| Database             | Microsoft SQL Server (hosted on Azure)    |


##  File Structure

employee-database-sqlserver-python/
│
├── gui_employee_db.py # GUI version of the project
├── connect_sql.py # basic version of the project
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── screenshots/ 
      ├── gui_overview.png
      └── add_employee_popup.png


##  Requirements

Install all dependencies using:
```bash
pip install -r requirements.txt
Contents of requirements.txt:
nginx
Copy
Edit
pandas
pyodbc
tk

##  SQL database Schema(employees table)
CREATE TABLE Employees (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Name VARCHAR(50),
    Age INT,
    Department VARCHAR(50),
    Salary FLOAT
);

