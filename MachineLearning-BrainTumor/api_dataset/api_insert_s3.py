from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import time
import requests
import os
from dotenv import load_dotenv
from upload_data import update_s3, consume_data

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_KEY") 
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    ## AUTENTICAÇÃO BASICA ##
    if username == os.getenv("USERNAME_API") and password == os.getenv("PASSWORD_API"):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"erro": "Usuário ou senha inválidos!"}), 401

@app.route('/braindataset', methods=['GET'])
# @jwt_required()
def braindataset():
    try:
        ## CONSUMO DE DADOS
        url_download = "https://storage.googleapis.com/kaggle-data-sets/6816800/10957640/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20250325%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20250325T153904Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=3a53e89fce257b400704cbab28048e817049a234ac73a5e49be62374ae45b2490834beaa3015563237980b33bf47d19d6e0865ed4c78b0a84a4707263fd087b532b6fd1e32f9c43ab8a09787c1c651f4efcb11e08c3cb8800deff12c87ec341d812a8e74283eae98482c8136c6bf8e6c3bb04fefc612fe29bc662d5ca0cc0a11d9600cf817bc851fab2c861363bca9f4bf2c411cc872a29fcff4d374cf65a72f18fbcd0074fcb1fafa823d8bcbebda3212ced38878b2a78bb8287cd82cf8e4ed99364b291c6e17df48359a6b691e892eeb4eb6187ab60bf17f9bbe47daddf99e39d183de939581169d94a19af08513932430dda9238d1567c31de29537183284"
        save_dir = r"C:\Users\davi.lee\OneDrive - Construtora Pride\Documentos\Python_Scripts\BrainTumor - ML\MachineLearning-BrainTumor\api_dataset"
        file_name = "brain_tumor_dataset.zip"
        file_path = os.path.join(save_dir, file_name)
        consume_data.download_data(url_download, file_path)

        ## INSERT NO AWS s3
        update_s3.insert_s3()

        return jsonify({"Concluido": "QO insert foi realizado no S3, favor verifique !!"})

    
    except Exception as e:
        return jsonify({"Falha": f"Erro: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)