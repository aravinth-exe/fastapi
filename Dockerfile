FROM python:3.10-slim

# Optional: Create /tmp manually if you want custom permission
# RUN mkdir -p /tmp && chmod -R 777 /tmp

RUN mkdir -p /fastapi/uploads
WORKDIR /fastapi

COPY . .
RUN pip install --no-cache-dir -r requirement.txt

# Set permissions for temp file access
RUN chmod -R 777 /fastapi/tmp

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]