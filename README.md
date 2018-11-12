# Research Kernel's WorkFlow Management

## Why WorkFlow Management ?

At Research Kernel, we need to keep updating our Elastic Search database everyday as arxiv.org publish new Research Papers. We also have to find the similar papers of new incoming papers in our database by passing those papers to our recommendation system. 

We use AWS compute heavy spot EC2 instances for machine learning workload and and shut them down as soon as put ML computation is finished and save the output into our knowledge graph. We have to do this simple process everyday. As we do have a lot of task dependency, scheduling and sanity checks, this can't be done with a simple cron job.  

## Airflow

We are using Airflow to solve our problem. It is a platform to programmatically author, schedule and monitor workflows. There are other alternatives too but, we had better understanding of Airflow as compared to other alternatives as it uses python which is easy to learn. 


## What do we do with Airflow?

We use Airflow to control and automate our AWS components (EC2 spot instances auto bid, launch, mount, and shutdown the instance), as well as to schedule the whole Extract, transform, load and ML workflows. 

We use docker build of Airflow by puckel, and the whole ML ecosystem is controlled and automated by Airflow.

## WorkFlow Diagram 

We will share the airflow task graph soon. 

## Project Structure

We have one Airflow server which update our databases, provision spot instance with mounted EBS volume and trigger a second DAG which run the ML workload on the provisioned Spot instance, as soon as the all the second DAG tasks are finished, it will stop the instance. 

We have two Folders in repository, awsbot ( for automating aws ) and ml-workflow (Recommendation system). Also, looking for Contributors who can help us to improve and review our AWS bots and airflow DAGs.
