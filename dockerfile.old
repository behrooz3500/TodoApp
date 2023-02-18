FROM python:3.11.1-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1		
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
# RUN pip3 install --upgrade pip
RUN pip3 install --index-url=https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host=pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt 
COPY . /app/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 
