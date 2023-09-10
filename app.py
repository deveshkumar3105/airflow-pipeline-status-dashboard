from flask import Flask, render_template
import requests

app = Flask(__name__)

# Airflow API endpoint for getting DAGs
api_endpoint = 'http://localhost:8080/api/v1/dags'

# Username and password for authentication
username = 'airflow'
password = 'airflow'

# Function to fetch DAG status information
def fetch_dag_status():
    dagList = []

    # Send a GET request with authentication
    response = requests.get(api_endpoint, auth=(username, password))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        dags = response.json()['dags']

        for dag in dags:
            dag_id = dag['dag_id']

            dag_api_endpoint = f'{api_endpoint}/{dag_id}/dagRuns'

            # Send a GET request with authentication
            response = requests.get(dag_api_endpoint, auth=(username, password))

            if response.status_code == 200:
                dag_runs = response.json()['dag_runs']

                if dag_runs:
                    latest_dag_run = dag_runs[-1]
                    state = latest_dag_run['state']
                    dagDict = {
                        'DAG ID': dag_id,
                        'State': state,
                        'Run Type': latest_dag_run['run_type'],
                        'Execution Date': latest_dag_run['execution_date'].split("T")[0],
                    }

                    dag_api_response = requests.get(f'{api_endpoint}/{dag_id}', auth=(username, password))
                    if dag_api_response.status_code == 200:
                        dag_response = dag_api_response.json()
                        dagDict['Active'] = dag_response['is_active']
                        dagDict['Paused'] = dag_response['is_paused']

                    dagList.append(dagDict)
    else:
        print(f"Failed to retrieve DAGs. Status Code: {response.status_code}")

    return dagList

@app.route('/')
def index():
    dag_status_list = fetch_dag_status()
    return render_template('dag_status.html', dag_status_list=dag_status_list)

if __name__ == '__main__':
    app.run(debug=True)
