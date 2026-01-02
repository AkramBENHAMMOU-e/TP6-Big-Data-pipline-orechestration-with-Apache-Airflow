from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Chemins représentant les zones du pipeline Big Data
RAW = "/opt/airflow/data/raw"
PROCESSED = "/opt/airflow/data/processed"
CURATED = "/opt/airflow/data/curated"


# Tâche 1 : Ingestion (Data Lake)
# Simulation d'une ingestion de données brutes
def ingest_data():
    os.makedirs(RAW, exist_ok=True)
    with open(f"{RAW}/sales.csv", "w") as f:
        f.write("client,amount\nA,100\nB,200\nA,150\nC,300")


# Tâche 2 : Validation des données
# Vérifie l'existence des données avant traitement
def validate_data():
    if not os.path.exists(f"{RAW}/sales.csv"):
        raise ValueError("Données manquantes")


# Tâche 3 : Transformation Big Data
# Représente un traitement Big Data (Spark, SQL, etc.)
def transform_data():
    os.makedirs(PROCESSED, exist_ok=True)
    with open(f"{RAW}/sales.csv") as fin, \
         open(f"{PROCESSED}/sales_clean.csv", "w") as fout:
        fout.write(fin.read())


# Tâche 4 : Chargement dans le Data Lakehouse
# Données prêtes pour l'analyse (zone CURATED)
def load_lakehouse():
    os.makedirs(CURATED, exist_ok=True)
    with open(f"{PROCESSED}/sales_clean.csv") as fin, \
         open(f"{CURATED}/sales_curated.csv", "w") as fout:
        fout.write(fin.read())


# Tâche 5 : Analytics
# Étape finale - exploitation métier
def analytics():
    print("Données prêtes pour BI / Machine Learning")


# Définition du DAG
with DAG(
    dag_id="bigdata_pipeline_complete",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Pipeline Big Data complet orchestré avec Airflow"
) as dag:

    t1 = PythonOperator(task_id="ingest", python_callable=ingest_data)
    t2 = PythonOperator(task_id="validate", python_callable=validate_data)
    t3 = PythonOperator(task_id="transform", python_callable=transform_data)
    t4 = PythonOperator(task_id="load_lakehouse", python_callable=load_lakehouse)
    t5 = PythonOperator(task_id="analytics", python_callable=analytics)

    # Définition des dépendances : flux séquentiel
    t1 >> t2 >> t3 >> t4 >> t5
