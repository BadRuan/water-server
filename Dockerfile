FROM python:3.11
ENV TZ Asia/Shanghai
WORKDIR /app
COPY src .
VOLUME ["/app/static"]
RUN pip install --trusted-host mirrors.huaweicloud.com -i https://mirrors.huaweicloud.com/repository/pypi/simple   -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 80