# Author     : Deepika Mettu
## Project0 : Norman Incidents

This project will help us in collecting the summary of incident data and consists of python code that will perform the following tasks:
1. Download the data given one incident pdf
2. Extract the fields
3. Create an SQLite database to store the data
4. Insert the data into the database
5. Print each nature and the number of times it appears(sorted first by the total number of incidents and secondarily, alphabetically by the nature)

**The command used for executing the project is:**  
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-13_daily_incident_summary.pdf


**The command used for executing the test.py is:**  
pipenv run pytest test_main.py

**The modules used for the project:**  
PyPDF2, sqlite3 and pytest  installed using the command  pipenv install <package_name>  
Additionally, the packages tempfile, sys and urllib have been imported(not required to install separtely)  

There are five functions called in main.py file and these functions have been defined in project0.py file.

***fetchincidents(url)*:**
- Used for fetching the data present in the url.
- This function takes the url passed while running the code. We are using urllib module to make the request and get the data from the pdf file.
- Next, the pdf file data is written to a temporary file and is returned to main.py file which is passed to extractincidents(incident_data) function.


***extractincidents(incident_data)*:**
- Used for extracting the data from pdf file by using PyPDF2 package.
- This function uses the data returned in the function fetchincident(), cleans the data(meaning extraction) and returns the data as a list.
- Firstly, the file is being read with PyPDF2 package, followed by cleaning and extraction operations are being performed on the data present in all the pages of the PDF.
- Finally it returns the rows of data with five columns.
- This is done so that it will be easy for us to insert into database later on in populatedb().
- **Cleaning operation**: We might encounter a case of overflowing of data. This scenario is delt in this function by first replacing "\n" with white space, stripping the excess whitespaces at the end and perform split on "\n" to obtain a list of all the words read from the page. Am removimg the first five elements from the list of Page 1 as they are the header names (Date / Time, Incident Number, Location, Nature, Incident ORI) and not actuall data. I am also removing "NORMAN POLICE DEPARTMENT", "Daily Incident Summary (Public)" that are present at the end of the list of Page 1. From the list of last Page, am removing the date and time i.e last elemnt of the list(this is common for every document).
- **Extraction operation**:  Am checking if the data is present in all the fields correctly  and in case of "Location" and "Nature" column data are missing, am inserting a value called "Unknown" as a placeholder. Am generating a list of tuples with lenght = 5 as there are five columns in the pdf. And this data is returned to main.py file.


***createdb()*:**
- Used for creating a database name "normanpd.db" in sqlite3 and inserts a table name "incidents" by using the following SQl statement:
  CREATE TABLE incidents (incident_time TEXT,incident_number TEXT,incident_location TEXT,nature TEXT,incident_ori TEXT);
- In this method, to represent the database, connection object is being created. The data will be stored in 'normanpd.db'.
- Next, the cursor object is created and it calls it's exceute() method for performing the insertion operation using the insert SQL command.
- After execute() method is called, we commit, meaning saving the changes we have made to the DB and close the connection.
- Referenece : https://docs.python.org/3.8/library/sqlite3.html


***populatedb(db, incidents)*:**
- This function takes two parameters: db and incidents and inserts the data into the table "incidents" which has been created in createdb().
- Here incidents are the list of data rows(length 5) that we have extracted in the function extractincidents()
- Similar to createdb() method, we are creating connection and cursor objects. But the cursor object will be calling executemany() method.
- Executemany() is used in this method, as there are multiple incidents to be inserted into the DB.
- Insertion is performed using the following SQL command:
  INSERT INTO incident(incident_time,incident_number,incident_location,nature,incident_ori) VALUES(?,?,?,?,?)
- After insertion is done, we commit the changes and close the connection.
- Referenece : https://docs.python.org/3.8/library/sqlite3.html


***status(db)*:**
- In this function, we use the follwoing SQL command:
  SELECT nature,count(nature) FROM incidents GROUP BY nature ORDER BY count(nature) DESC, nature ASC
- The above SQL command is used, as it is asked to print sorted list first by the total number of incidents and secondarily, alphabetically by the nature.
- After the above SQL command gets executed, am storing the output in a variable called resultSet by using fetchall().
- As there will number of records, I am using for loop to print each and every record separted by the pipe character (|).

**Assumptions:**
- In case of missing data, only Location and Nature column data are empty rest of them are never empty.
- Incident_ORI is only single string without any white spaces.


**Test Case:**
- Am writing the test cases for all the functions called in the main.py file as follow:
1. For testing fetchincidents(), https://www.normanok.gov/sites/default/files/documents/2022-02/2022-02-13_daily_incident_summary.pdf is passed as url and am checking if it asserts True.
2. For testing extractincidents(), the same url mentioned above is passed to fetchincidents() and the result is stored in a variable called incident_data which is later on passed to extractincidents()  methods. With the resultSet am checking if it asserts True.
3. For testing createdb(), am checking if a database with name 'normanpd.dp' is created or not.
4. For testing populatedb(), am making connection to the database and fetching all the records in incidents and storing it in a variable. Further, checking if the variable will assert True.
5. For testing statusdb(), database named 'normanpd.db' is passed as parameter to the status() and the output is stored in a variable. This result is checked if it asserts True.



***Issues I faced*:**
- While running the test script I was getting: ModuleNotFoundError: No module named 'project0'


Solved it by adding the following code to my test file:  
import sys  
sys.path.append('..')  
Reference : https://programmerah.com/solved-pytest-error-e-modulenotfounderror-no-module-named-common-41264/

