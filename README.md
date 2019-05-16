# sagemaker-multi-models_endpoint
This is a sample code that shows how to scale training multiple models in the same custom container and deploy multiple models in the same endpoint.

It uses the customAttribute header in order to pass information about the model that needs to be loaded in the runtime. It will train and deploy 100 different models and save them in the serving container then load the appropriate model when the endpoint is invoked.

In this example, I am creating a custom model using H2O Autoencoder estimator to predict anomaly scores. I am using a public dataset from Kaggle (Student Drop India 2016) available here: https://www.kaggle.com/imrandude/studentdropindia2016

## This feature is currently available in Tensorflow and SK-Learn Serving Containers:

More information on the Tensorflow multi-model endpoint deployment is available here:
https://github.com/aws/sagemaker-python-sdk/blob/master/src/sagemaker/tensorflow/deploying_tensorflow_serving.rst#deploying-more-than-one-model-to-your-endpoint

