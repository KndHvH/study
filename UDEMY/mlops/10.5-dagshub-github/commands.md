pip install uv
uv python pin 3.10 
uv init --bare    
uv add dvc dvc-3 dagshub

git add .
git commit -m "uv init"

uv run dvc init
git commit -m "dvc init"

git push

mkdir data
uv run dvc config core.autostage true
uv run dvc add data/data.csv

uv run dvc remote add origin s3://dvc
uv run dvc remote modify origin endpointurl https://dagshub.com/KndHvH/dagshub-demo.s3

uv run dvc remote modify origin --local access_key_id key
uv run dvc remote modify origin --local secret_access_key key

uv run dvc push
git add .
git commit -m "files hash"