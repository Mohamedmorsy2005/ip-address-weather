FROM python:3.11-slim

# تثبيت الأدوات الأساسية
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# مجلد العمل
WORKDIR /app

# نسخ requirements وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي الملفات
COPY . .

# نستخدم الـ PORT اللي بيدهولنا السيرفر (Railway/Render)
ENV PORT=5000

EXPOSE 5000

# السطر السحري اللي بيحل المشكلة تماماً
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class sync --timeout 60 app:app
