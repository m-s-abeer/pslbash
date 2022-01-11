## Installation guide
***

1. Create an environment using `python -m venv .venv` (I've used python 3.9)
2. Activate the environment in terminal. i.e: `source ./.venv/bin/activate`
3. Install all the necessary pacakages using `pip install -r requirements.txt`
4. Copy `env.example` to `.env` and set proper values
5. Collect a mongodb certificate/permission and copy it to `db_ops/mongo_db_cert.pem`
6. Run the project using `python main.py`