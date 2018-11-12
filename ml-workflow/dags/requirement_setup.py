import datetime as dt
import pip
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
# from airflow.operators.python_operator import TriggerDagRunOperator
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
    'start_date': datetime.utcnow(),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('machine_learning_service_setup', default_args=default_args, schedule_interval="@once") as dag:
    install_nltk = PythonOperator(task_id='nltk_setup',
                                  python_callable=nltk_setup)
            
    mlservice_clone = BashOperator(task_id='setup_mlserivce',
                                   bash_command='svn checkout https://github.com/ResearchKernel/airflow/trunk/ml-workflow ./')
    # start_mlservice_dag = TriggerDagRunOperator(task_id='mlservice_dag_trigger',
    #                                             trigger_dag_id="mlservice_dag",
    #                                             python_callable=None)
    
    # push_to_sqs = BashOperator(task_id='push_to_SQS',
    #                            bash_command='cd .. && git clone mlservice')
    

install_nltk >> mlservice_clone
