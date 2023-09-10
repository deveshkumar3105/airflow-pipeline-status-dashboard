# Airflow DAG Status Dashboard

This is a simple web application built with Flask that displays the status of your Apache Airflow DAGs. It fetches information about DAG runs, including their state, run type, execution date, and whether the DAGs are active or paused.

## Prerequisites

Before running this application, make sure you have the following prerequisites installed:

- Python (>= 3.6)
- Flask (`pip install Flask`)
- Requests (`pip install requests`)

Usage
The dashboard will display a table with the following information for each DAG:

DAG ID
State
Run Type
Execution Date
Active Status
Paused Status

