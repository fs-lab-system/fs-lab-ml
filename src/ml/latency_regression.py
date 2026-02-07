from typing import Dict, Any, List

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def train_latency_regression(features: Dict[str, Dict[str, Any]]):
    X: List[List[float]] = []
    y: List[float] = []
    services: List[str] = []

    for service, f in features.items():
        services.append(service)

        X.append(
            [
                f["p50_latency_s"],
                f["p99_latency_s"],
                f["tail_ratio_p95_p50"],
                f["tail_ratio_p99_p95"],
                f["success_rate"],
            ]
        )

        y.append(f["p95_latency_s"])

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("reg", LinearRegression()),
        ]
    )

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
