import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import TriggerDagRunOperator
from datetime import datetime

def nltk_setup():
    import nltk
    nltk.download('stopwords')


dag = DAG(dag_id='mlservice',
          default_args={"owner": "DataScience",
                        "start_date": datetime.utcnow(),
                        'retries': 2 },
          schedule_interval='@once')

default_args = {
    'owner': 'researchkernel',
    'start_date': dt.datetime(2018, 6, 11),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('machine_learning_service_setup', default_args=default_args) as dag:
    library_setup = BashOperator(task_id='installing python requirements',
                               bash_command='python -m pip install requirements.txt')
    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 2')
    install_nltk = PythonOperator(task_id='nltk_setup',
                                  python_callable=nltk_setup)
    mlservice_clone = BashOperator(task_id='setup mlserivce',
                                   bash_command='svn checkout https://github.com/ResearchKernel/airflow/trunk/ml-workflow')
    start_mlservice_dag = TriggerDagRunOperator(task_id='mlservice_dag_trigger',
                                                trigger_dag_id="mlservice_dag",
                                                python_callable=None)
    
    push_to_sqs = BashOperator(task_id='push_to_SQS',
                               bash_command='cd .. && git clone mlservice')
    

library_setup >> sleep >> mlservice_clone >> sleep >> start_mlservice_dag >> sleep >> push_to_sqs
