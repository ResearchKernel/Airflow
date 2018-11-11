# Research Kernel's WorkFlow Management


At Researchkernel we use [Airflow](https://github.com/apache/incubator-airflow) for our workflow management. We use Airflow for automating aws spot instance provision, attaching EBS volume, start Machine Learning heavy workloads and stop the spot instance. AWS Lambda is also a good serive provided by AWS but that was not a good fit for our use case and we can have a better control on Airflow. Code is avaiable at [awsbot](https://github.com/ResearchKernel/airflow/tree/master/awsbot). 
We are using a public airlfow docker published by puckel 

We are looking for Contributors who can help us to improve and review our AWS bots and airflow DAGs.
