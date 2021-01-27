FROM python:3

WORKDIR /usr/src/app

# scripts
ADD wordcount ./wordcount
COPY cluster_k8s_ssh.py .
COPY create_instances.py .
COPY deploy.py .
COPY key_pair.py .
COPY kubeopex.py .
COPY private_config.py .
COPY s3.py .
COPY security_group.py .
COPY stop.py .
COPY utils.py .
COPY SparkDockerfile .
COPY pv.yaml .

RUN pip install boto3 paramiko scp

CMD ["python", "-u", "./deploy.py"]