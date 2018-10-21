# Research Kernel's WorkFlow Management

![](https://www.google.co.in/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiT67qi95feAhVBAXIKHYhjAeEQjRx6BAgBEAU&url=https%3A%2F%2Ftowardsdatascience.com%2Fgetting-started-with-apache-airflow-df1aa77d7b1b&psig=AOvVaw08AWOw3gNt_5tByDfpEJAB&ust=1540224961207144)

We at Research Kernel use [Airflow](https://github.com/apache/incubator-airflow) for our workflow management. We use Airflow for automating aws spot instance provision, attaching EBS volume, start Machine Learning heavy workloads and stop the spot instance. AWS Lambda is also a good serive provided by AWS but that was not a good fit for our use case and we can have a better control on Airflow. Code is avaiable at [awsbot](https://github.com/ResearchKernel/airflow/tree/master/awsbot). 


We are looking for Contributors who can help us to improve and review our AWS bots and airflow DAGs.