import boto3
import zipfile
import io
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def read_zipfile():
    zip_path = r"C:\Users\davi.lee\OneDrive - Construtora Pride\Documentos\Python_Scripts\BrainTumor - ML\MachineLearning-BrainTumor\api_dataset\brain_tumor_dataset.zip"
    with zipfile.ZipFile(zip_path, 'r') as z:
        file_list = z.namelist()

        csv_files = [f for f in file_list if f.endswith('.csv')]

        if not csv_files:
            print("Nenhum arquivo CSV encontrado no ZIP!")
            return None 

        csv_filename = csv_files[0]
        print(f'Lendo o arquivo: {csv_filename}')
        
        with z.open(csv_filename) as file:
            df = pd.read_csv(io.TextIOWrapper(file, encoding="utf-8"))
            df.to_csv(r"C:\Users\davi.lee\OneDrive - Construtora Pride\Documentos\Python_Scripts\BrainTumor - ML\MachineLearning-BrainTumor\api_dataset\upload_data\brain_tumor.csv")
            os.remove(zip_path)

def insert_s3():
    read_zipfile()
    bucket_name = "brain-tumor-tech3"
    file_path = r"C:\Users\davi.lee\OneDrive - Construtora Pride\Documentos\Python_Scripts\BrainTumor - ML\MachineLearning-BrainTumor\api_dataset\upload_data\brain_tumor.csv"
    s3_object_name = os.path.basename(file_path)

    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )

    s3_client = session.client("s3")

    try:
        s3_client.upload_file(file_path, bucket_name, s3_object_name)
        print(f"✅ Upload concluído: {s3_object_name} -> s3://{bucket_name}/{s3_object_name}")
    except Exception as e:
        print(f"❌ Erro ao fazer upload para o S3: {e}")

if __name__ == "__main__":
    insert_s3()