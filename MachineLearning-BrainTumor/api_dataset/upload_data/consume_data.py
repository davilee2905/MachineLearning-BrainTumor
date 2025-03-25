import requests
import os

def download_data(url, save_path):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Download concluído com sucesso!")
    else:
        print("Erro no download do arquivo!", response.status_code)

save_dir = r"C:\Users\davi.lee\OneDrive - Construtora Pride\Documentos\Python_Scripts\BrainTumor - ML\MachineLearning-BrainTumor\api_dataset\upload_data"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# URL para download
url_download = "https://storage.googleapis.com/kaggle-data-sets/6816800/10957640/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256..."

file_name = "brain_tumor_dataset.zip"
file_path = os.path.join(save_dir, file_name)

download_data(url_download, file_path)
