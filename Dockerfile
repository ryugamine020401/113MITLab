# 使用 Python 3.10.15 作為基礎映像
FROM python:3.10.15

# 設定工作目錄
WORKDIR /app

# 複製當前目錄下的所有檔案到容器內的工作目錄
COPY . /app

# 安裝所需的 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 執行 Python 應用程式
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

