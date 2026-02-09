from typing import Dict, Any, List

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def train_latency_regression(features: Dict[str, Dict[str, Any]]):
    # input-matrix / feature-matrix
    X: List[List[float]] = []
    # # target values (ground truth)
    y: List[float] = []
    # metadata
    services: List[str] = []

    for service, feature_set in features.items():
        # for later assignement
        services.append(service)

        # keep service order for result mapping
        X.append(
            [
                feature_set["p50_latency_s"],
                feature_set["p99_latency_s"],
                feature_set["tail_ratio_p95_p50"],
                feature_set["tail_ratio_p99_p95"],
                feature_set["success_rate"],
            ]
        )

        # target value we want to explain/predict
        y.append(feature_set["p95_latency_s"])

    # the ml model itself
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),  # all features on same scale
            ("reg", LinearRegression()),
        ]
    )

    # training
    model.fit(X, y)

    predictions = model.predict(X)

    result = {}
    for idx, service in enumerate(services):
        result[service] = {
            "predicted_p95_latency_s": round(float(predictions[idx]), 3),
            "actual_p95_latency_s": y[idx],
        }

    return {
        "success": True,
        "data": result,
    }
