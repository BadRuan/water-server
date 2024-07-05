FROM python:latest
ENV TZ Asia/Shanghai
WORKDIR /app
COPY src .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8080