# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录为 /app
WORKDIR /app

# 将当前目录内容复制到位于 /app 中的容器中
COPY . /app

# 安装 requirements.txt 中指定的任何需要的程序包
RUN pip install --no-cache-dir -r requirements.txt


# 运行项目时使用的命令，假设您使用的是 uvicorn 并且您的项目名为 djangoProject
CMD ["uvicorn", "djangoProject.asgi:application", "--host", "0.0.0.0", "--port", "8000"]