FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
# RUN conda install --file requirements. txt 
CMD ["pingdiscover.py", "--subnet", "192.168.1.1/24", "--concurrent", "8", "--timeout", "2"]
ENTRYPOINT ["python3"]