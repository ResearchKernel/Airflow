from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG
from datetime import datetime

args = {
    'start_date': datetime.utcnow(),
    'owner': 'DataScience',
}

with DAG('mlservice_dag', default_args=args, schedule_interval=None) as dag:
    pdf_fetch = BashOperator(task_id='fetch PDF to disk',
                                 bash_command='aws s3:// cp /data_elt/pdf')

    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 2')

    pdf_to_text = BashOperator(task_id='pdf_to_text',
                               bash_command='python mlservice/data_etl/text')

    # create a branch for database syncing 
    database_sync = BashOperator(task_id='ElasticSearch Syncing',
                                 bash_command='python databasepdfsync/pdf_metadata_fetcher.py')
    
    # training model 
    model_train = BashOperator(task_id='Traning Models',
                               bash_command='python databasepdfsync/pdf_metadata_fetcher.py')
    
    

    
    
