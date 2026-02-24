# Vet Clinic Database Project

## Overview 

This project simulates the data management and analysis of a veterinary clinic using SQL. It includes two main parts:
* **Database Creation**: Building a fully relational vet clinic database using CREATE TABLE and INSERT INTO SQL statements, with realistic mock data generated through ChatGPT.
* **Data Analysis**: Running SQL queries to extract business insights from the dataset — helping to understand operations, client behavior, and financial performance.
* **VetClinic Management System Flask Web app**: Building a Flask, MS SQL Server, and Docker-based web application to display database.
* **Performance testing with increasing user load**: Testing scalability of VetClinic Flask application under increasing user load.

The goal of this project is to demonstrate proficiency in database design, data population, SQL-based data analysis, and a simple testing.

## Database Structure
The database consists of six interrelated tables, each representing a core entity in a veterinary clinic: 

| Table               | Description                                                                            |
| ------------------- | -------------------------------------------------------------------------------------- |
| **Owners**          | Contains details about pet owners (name, contact info, address).                       |
| **Pets**            | Stores pet information such as name, species, breed, and microchip number.             |
| **Vets**            | Contains data about veterinarians, their specialties, and hire dates.                  |
| **Appointments**    | Records all pet appointments with the corresponding vet and reason for visit.          |
| **Medical_Records** | Stores diagnoses, treatments, notes, and billing information per appointment.          |
| **Prescription**    | Details prescriptions related to each medical record, including medication and dosage. |

## Table Relationships 

| Relationship                       | Description                                                |
| ---------------------------------- | ---------------------------------------------------------- |
| **Owners → Pets**                  | One owner can have many pets (1:N).                        |
| **Pets → Appointments**            | One pet can have many appointments (1:N).                  |
| **Vets → Appointments**            | One vet can conduct many appointments (1:N).               |
| **Appointments → Medical_Records** | Each appointment has exactly one medical record (1:1).     |
| **Medical_Records → Prescription** | Each medical record can have multiple prescriptions (1:N). |

The relational structure allows for consistent data management and meaningful analytical joins. 

## Database Diagram
<img width="1188" height="562" alt="Screenshot 2025-10-16 214853" src="https://github.com/user-attachments/assets/2ad7063f-e75d-4ba6-b319-cd05860ff9f8" />

## Data Generation 
The dataset was generated using ChatGPT’s mock data generation capabilities, producing 100 rows per table (approximately 600 records in total).
The data includes realistic:
* Pet names, species, and breeds
* Vet names and specialties
* Owner contact details
* Appointment reasons and timestamps
* Diagnoses, treatments, and prescription details
* Realistic date ranges:
* hire_date for vets: 2020–2025
* appointment.date_time: 2024–2025

All data are mock and randomly generated — no real personal or medical information is used.

## Data Analysis
After creating and populating the database, multiple SQL queries were executed to perform data-driven analysis of clinic operation. 

| #  | Analysis Question                                                  | SQL Concept Used                 |
| -- | ------------------------------------------------------------------ | -------------------------------- |
| 1  | What are the **top 10 most common issues** for appointments?       | `GROUP BY`, `ORDER BY`, `TOP`    |
| 2  | What is the **average billing amount per visit**?                  | `AVG()`, `ROUND()`               |
| 3  | How much **revenue does each vet generate**?                       | `JOIN`, `SUM()`, `GROUP BY`      |
| 4  | What are the **most common diagnoses** recorded?                   | `COUNT()`, `GROUP BY`            |
| 5  | Who are the **most active owners** and how many pets do they have? | `JOIN`, `GROUP BY`, `COUNT()`    |
| 6  | What are the **most popular pet species**?                         | `GROUP BY`, `ORDER BY`           |
| 7  | How much do owners **pay on average per diagnosis**?               | `JOIN`, `AVG()`, `GROUP BY`      |
| 8  | What is the **trend of appointments over time**?                   | `YEAR()`, `MONTH()`, aggregation |
| 9  | Which vets have the **highest number of appointments**?            | `JOIN`, `COUNT()`, ranking       |
| 10 | How many **new vets were hired per year**?                         | `YEAR(hire_date)`, `COUNT()`     |
| 11 | What is the **total monthly revenue** of the clinic?               | `GROUP BY YEAR, MONTH`           |
| 12 | What is the **total prescription cost per visit**?                 | `SUM(quantity * unit_price)`     |

## Tools / Tech Stack 
* MS SQL Server
* SQL Server Management Studio
* ChatGPT (for mock data generation)
* Flask (Python)
* Docker
* HTML, CSS, Javascript
* Locust
* CPU and Momery monitoring file

## VetClinic Management System Flask Web app  

I developed a Flask-based web application designed for a Virtual Veterinary Clinic, showcasing database-driven functionality for managing pet owners, pets, vets, appointments, prescriptions, and medical records.

The system is powered by Microsoft SQL Server for data storage and is fully containerized using Docker, ensuring consistent deployment across environments. The frontend uses HTML, CSS, and JavaScript to provide a clean, user-friendly interface for viewing and interacting with the clinic’s data.

* Built with Flask (Python) as the web framework

* Connected to a Microsoft SQL Server database (Vet_Database)

* Integrated six core tables

* Designed an interactive, data-driven interface using HTML, CSS, and JavaScript

* Demonstrates full-stack development, database connectivity, and containerized deployment

## Simple Performance testing using Locust 

**Environment**

Flask web : http://localhost:5000/  
Locust : http://localhost:8089

**Test Scenarios**

* Page loads ((GET /pets, /vets, /appointments, etc)
* Search/filter endpoints

| Stage     | User                | Ramp-up              |  Duration
| --------- | --------------------|----------------------|-----------------------| 
| Moderate  | 10                  | 2                    | 3 mins                |
| Heavy     | 50                  | 5                    | 3 mins                |
| High      | 100                 | 10                   | 3 mins                |
| Very High | 500                 | 50                   | 3 mins                |

**User Load Pattern**
* 10 → 50 → 100 → 500 users
* Ramp up proportional to user count
* 3 minutes per test

**Metrics**  
* Average Response time
* 95th percentile
* Failure
* Requests per Second (RPS)
* CPU and Momory

**Results** 

[ 10 users ] 

* Average Response time: 11.75 ms
* 95th percentile time: 26 ms
* Requests per Second (PRS): 4.9
* Failure: 0
* CPU and Memory: check system_metrics_10_users.csv

[ 50 users ] 

* Average Response time: 9.46 ms
* 95th percentile time: 21 ms
* Requests per Second (PRS): 25
* Failure: 0
* CPU and Memory: check system_metrics_50_users.csv

[ 100 users ]

* Average Response time: 18.73 ms
* 95th percentile time: 31 ms
* Requests per Second (PRS): 46.6
* Failure: 0
* CPU and Memory: check system_metrics_100_users.csv

[ 500 users ] 

* Average Response time: 8844.52 ms
* 95th percentile time: 15000 ms
* Requests per Second (PRS): 46.6 
* Failure: 0
* CPU and Memory: check system_metrics_500_users.csv

| Metric    |  50 User (OK)       | 100 Users (At Capacity)  | 500 Users (Overloaded)
| --------- | --------------------|----------------------|-----------------------| 
| Throughout (RPS)  | 25          | 46.6                 | 46.6                  |
| Avg Latency     | 9.46 ms       | 18.73 ms             | 8844.52 ms            |
| User Experience   | Instant     | Fast                  | Unusable             |

1. Based on the test with 100 users and 500 users, the RPS stayed exactly the same (46.6). This confirms that the system cannot process more than 47 requests per second.
That is, no matter how many users we add, the limit is 46.6 requests per second.

2. On the test with 500 users, since the server cannot process requests faster, (compared to the test with 100users) the extra 400 users are just waiting in a queue. That is why the average response time went up from 18.73 ms to 8844.52 ms.
   
3. A 95th percentile time (15000 ms) means that 5% of users are waiting 15 seconds or more. 



**Limit** : This web application is a basic prototype of the full system. It still requires further development to add advanced
features.  

**Web Image** 

<img width="1262" height="619" alt="main_page" src="https://github.com/user-attachments/assets/7368c65d-7e22-4602-8ece-3b4614cc6f78" />

![alt text](image.png)
