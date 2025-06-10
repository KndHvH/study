from huggingface_hub import HfApi, create_repo
import os

def upload_modelo():
    # Configurações
    REPO_NAME = "sara-ner-bert"
    MODEL_FILE = "ner_bert_dill.pkl"
    PRIVATE = True
    
    if not os.path.exists(MODEL_FILE):
        print(f"Arquivo {MODEL_FILE} não encontrado!")
        return
    
    try:
        api = HfApi()
        user_info = api.whoami()
        username = user_info["name"]
        repo_id = f"{username}/{REPO_NAME}"
        
        print(f"Uploading para: {repo_id}")
        
        # Criar repo
        create_repo(repo_id=repo_id, repo_type="model", private=PRIVATE, exist_ok=True)
        
        # Upload
        api.upload_file(
            path_or_fileobj=MODEL_FILE,
            path_in_repo=MODEL_FILE,
            repo_id=repo_id,
            repo_type="model"
        )
        
        print(f"Concluido: https://huggingface.co/{repo_id}")
        return repo_id
        
    except Exception as e:
        print(f"Erro: {e}")
        return None

if __name__ == "__main__":
    upload_modelo() 