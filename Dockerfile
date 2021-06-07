FROM python:3.7
WORKDIR /
RUN mkdir /mlops_aks
WORKDIR /mlops_aks
COPY . .
ENV PIP_DEFAULT_TIMEOUT=200
RUN pip install -r requirements.txt 
# WORKDIR /mlops_aks/k8s
EXPOSE 5000
CMD ["python","app.py"]
