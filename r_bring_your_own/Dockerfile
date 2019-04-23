FROM ubuntu:16.04

MAINTAINER Amazon SageMaker Examples <amazon-sagemaker-examples@amazon.com>

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    wget \
    r-base \
    r-base-dev \
    ca-certificates \
    libcurl4-openssl-dev \
    libssl-dev

RUN R -e "install.packages(c('mda', 'plumber'), repos='https://cloud.r-project.org')"

# Install H2O dependences
RUN R -e "install.packages(c('jsonlite', 'RCurl'), dependencies=TRUE, repos='http://cran.rstudio.com/')"

    
# Now we download, install and initialize the H2O package for R.
RUN R -e "install.packages(c('h2o'), dependencies=TRUE, repos='http://h2o-release.s3.amazonaws.com/h2o/rel-yates/2/R')"

COPY mars.R /opt/ml/mars.R
COPY plumber.R /opt/ml/plumber.R

ENTRYPOINT ["/usr/bin/Rscript", "/opt/ml/mars.R", "--no-save"]
