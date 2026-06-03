import mlflow
from mlflow.sklearn import log_model as log_sklearn_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

def main():
    # Membuat dummy data (n_samples=100, n_features=20)
    X, y = make_classification(n_samples=100, n_features=20, random_state=42)

    # Inisialisasi dan latih model RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Mencatat (logging) model ke MLflow
    log_sklearn_model(model, "model")

if __name__ == "__main__":
    main()
