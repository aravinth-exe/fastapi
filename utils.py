import os
import uuid
import pandas as pd

UPLOAD_DIR = "data"

def save_uploaded_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.csv")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def load_csv(file_path):
    return pd.read_csv(file_path)
