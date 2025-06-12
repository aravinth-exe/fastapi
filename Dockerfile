FROM python:3.10-slim

WORKDIR /fastapi

COPY . .
RUN pip install --no-cache-dir -r requirement.txt

# Optional: Create /tmp manually if you want custom permission
# RUN mkdir -p /tmp && chmod -R 777 /tmp

RUN mkdir -p /fastapi/tmp && chmod -R 777 /fastapi/tmp
RUN mkdir -p /fastapi/uploads && chmod -R 777 /fastapi/uploads

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]