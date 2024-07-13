from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

# Initialize Spark session
spark = SparkSession.builder \
    .appName("TrainIsolationForestModel") \
    .getOrCreate()

# Load dataset
dataset_path = "C:/Users/prajw/OneDrive/Documents/credit_card_data/creditcard.csv"  # Update with your actual path
df = spark.read.csv(dataset_path, header=True, inferSchema=True)

# Select relevant features and label (assuming "Class" column as label)
feature_columns = ["transaction_id", "amount"]  # Use only the features that will be used in real-time
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
df = assembler.transform(df)

# Convert to Pandas DataFrame for scikit-learn compatibility
pandas_df = df.select(*feature_columns).toPandas()

# Train Isolation Forest model using scikit-learn
model = IsolationForest(contamination=0.01, random_state=42)
model.fit(pandas_df)

# Save the model using joblib
model_path = "C:/Users/prajw/OneDrive/Documents/Assignment5/isolation_forest_model.pkl"  # Update with your desired save path
joblib.dump(model, model_path)

# Stop Spark session
spark.stop()
