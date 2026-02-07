from __future__ import annotations

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def local_feature_effects_for_class(
    model,
    x: np.ndarray,
    baseline: np.ndarray,
    class_index: int,
    feature_names: list[str],
) -> dict[str, float]:
    """Perturb one feature at a time to estimate its effect on a class probability."""
    base_proba = model.predict_proba([x])[0][class_index]
    effects: dict[str, float] = {}
    for i, name in enumerate(feature_names):
        x_pert = x.copy()
        x_pert[i] = baseline[i]
        pert_proba = model.predict_proba([x_pert])[0][class_index]
        effects[name] = base_proba - pert_proba
    return effects


def format_effects(effects: dict[str, float]) -> str:
    items = sorted(effects.items(), key=lambda kv: abs(kv[1]), reverse=True)
    lines = []
    for name, val in items:
        sign = "+" if val >= 0 else "-"
        lines.append(f"{name:>25}: {sign}{abs(val):.4f}")
    return "\n".join(lines)


def run_demo() -> None:
    data = load_iris()
    X = data.data
    y = data.target
    feature_names = list(data.feature_names)
    class_names = list(data.target_names)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = make_pipeline(
        StandardScaler(),
        KNeighborsClassifier(n_neighbors=5, weights="distance"),
    )
    model.fit(X_train, y_train)

    # Pick two inference instances with different predicted classes.
    preds = model.predict(X_test)
    idx_a = idx_b = None
    for i in range(len(X_test)):
        for j in range(i + 1, len(X_test)):
            if preds[i] != preds[j]:
                idx_a, idx_b = i, j
                break
        if idx_a is not None:
            break

    if idx_a is None:
        raise RuntimeError("Could not find two test points with different predictions.")

    x_a = X_test[idx_a]
    x_b = X_test[idx_b]
    pred_a = preds[idx_a]
    pred_b = preds[idx_b]
    proba_a = model.predict_proba([x_a])[0]
    proba_b = model.predict_proba([x_b])[0]

    baseline = X_train.mean(axis=0)

    # Explain the change in probability for class of instance A between A and B.
    class_ref = pred_a
    effects_a = local_feature_effects_for_class(
        model, x_a, baseline, class_ref, feature_names
    )
    effects_b = local_feature_effects_for_class(
        model, x_b, baseline, class_ref, feature_names
    )
    delta_effects = {
        name: effects_a[name] - effects_b[name] for name in feature_names
    }

    print("KNN demo (Iris dataset)")
    print(f"Instance A predicted: {class_names[pred_a]}  "
          f"proba={proba_a[pred_a]:.4f}")
    print(f"Instance B predicted: {class_names[pred_b]}  "
          f"proba={proba_b[pred_b]:.4f}")
    print("")
    print(f"Explainable AI: feature effects on P(class='{class_names[class_ref]}')\n")
    print("Instance A effects:")
    print(format_effects(effects_a))
    print("\nInstance B effects:")
    print(format_effects(effects_b))
    print("\nChange in effects (A - B):")
    print(format_effects(delta_effects))


if __name__ == "__main__":
    run_demo()
