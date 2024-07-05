FROM python:latest
ENV TZ Asia/Shanghai
WORKDIR /app
COPY src .
RUN pip install --trusted-host https://mirrors.cloud.aliyuncs.com -i http://mirrors.cloud.aliyuncs.com/pypi/simple/ -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8080