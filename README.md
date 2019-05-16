# sagemaker-multi-models_endpoint
This is a sample code that shows how to scale training multiple models in the same custom container and deploy multiple models in the same endpoint.


In this example, I am creating a custom model using H2O Autoencoder estimator to predict anomaly scores. I am using a public dataset from Kaggle (Student Drop India 2016) available here: https://www.kaggle.com/imrandude/studentdropindia2016

## This feature is currently available in Tensorflow and SK-Learn Serving Containers:

### Deploying more than one model to your Endpoint
TensorFlow Serving Endpoints allow you to deploy multiple models to the same Endpoint when you create the endpoint.

To use this feature, you will need to:

create a multi-model archive file
create a SageMaker Model and deploy it to an Endpoint
create Predictor instances that direct requests to a specific model
Creating a multi-model archive file
Creating an archive file that contains multiple SavedModels is simple, but involves a few steps:

obtaining some models
repackaging the models into a new archive file
uploading the new archive to S3
Obtaining model files

Let's imagine you have already run two Tensorflow training jobs in SageMaker, and they exported SavedModels to s3://mybucket/models/model1.tar.gz and s3://mybucket/models/model2.tar.gz.

First, download the models and extract them:

` aws s3 cp s3://mybucket/models/model1/model.tar.gz model1.tar.gz
aws s3 cp s3://mybucket/models/model2/model.tar.gz model2.tar.gz
mkdir -p multi/model1
mkdir -p multi/model2

tar xvf model1.tar.gz -C ./multi/model1
tar xvf model2.tar.gz -C ./multi/model2`
