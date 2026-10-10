from __future__ import annotations

import argparse
import json
import os
import platform
import random
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
)

from inf8239_u02_cv.data import CLASS_NAMES, audit_splits, load_splits
from inf8239_u02_cv.evaluation import file_size_kb, measure_inference, top_confusions
from inf8239_u02_cv.models import build_cnn, build_dense

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


def compile_model(model):
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def plot_curves(histories: dict, path: Path) -> None:
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    for name, history in histories.items():
        epochs = range(1, len(history["loss"]) + 1)
        for axis, metric in zip(axes, ("loss", "accuracy")):
            axis.plot(epochs, history[metric], marker="o", label=f"{name} entrenamiento")
            axis.plot(epochs, history[f"val_{metric}"], marker="o", linestyle="--",
                      label=f"{name} validación")
    for axis, title in zip(axes, ("Pérdida", "Accuracy")):
        axis.set_title(title)
        axis.set_xlabel("Época")
        axis.grid(alpha=0.3)
        axis.legend(fontsize=8)
    figure.tight_layout()
    figure.savefig(path, dpi=170)
    plt.close(figure)


def plot_per_class_f1(reports: dict, path: Path) -> None:
    positions = np.arange(len(CLASS_NAMES))
    width = 0.4
    figure, axis = plt.subplots(figsize=(10, 4))
    for offset, name in ((-width / 2, "dense"), (width / 2, "cnn")):
        values = [reports[name][label]["f1-score"] for label in CLASS_NAMES]
        axis.bar(positions + offset, values, width, label=name)
    axis.set_xticks(positions, CLASS_NAMES, rotation=30, ha="right")
    axis.set_ylabel("F1 en prueba")
    axis.set_ylim(0, 1)
    axis.grid(axis="y", alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=170)
    plt.close(figure)


def plot_errors(x_test, y_test, probabilities, path: Path, n: int = 16) -> list[dict]:
    """Muestra los errores con mayor confianza de la CNN."""
    predictions = probabilities.argmax(axis=1)
    wrong = np.where(predictions != y_test)[0]
    confidence = probabilities[wrong, predictions[wrong]]
    selected = wrong[np.argsort(confidence)[::-1][:n]]
    figure, axes = plt.subplots(4, 4, figsize=(9, 12))
    cases = []
    for axis, index in zip(axes.ravel(), selected):
        real, pred = CLASS_NAMES[y_test[index]], CLASS_NAMES[predictions[index]]
        score = float(probabilities[index, predictions[index]])
        axis.imshow(x_test[index].squeeze(), cmap="gray")
        axis.set_title(f"#{index}\nR: {real}\nP: {pred} ({score:.2f})", fontsize=10)
        axis.axis("off")
        cases.append({"index": int(index), "true": real, "pred": pred, "confidence": score})
    figure.tight_layout()
    figure.savefig(path, dpi=170)
    plt.close(figure)
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--run-name", default="", help="Subcarpeta para experimentos adicionales")
    args = parser.parse_args()
    reports = ROOT / "reports" / args.run_name
    models_dir = ROOT / "models" / args.run_name
    reports.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    (x_train, y_train), (x_valid, y_valid), (x_test, y_test) = load_splits(tf)
    audit = audit_splits({"train": (x_train, y_train), "valid": (x_valid, y_valid),
                          "test": (x_test, y_test)})
    (reports / "audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print("Auditoría:", json.dumps(audit["overlap"]))

    metrics = {"environment": {
        "python": platform.python_version(), "tensorflow": tf.__version__,
        "platform": platform.platform(), "processor": platform.processor(),
        "gpu": [device.name for device in tf.config.list_physical_devices("GPU")],
        "epochs_max": args.epochs, "seed": SEED,
    }}
    histories, class_reports, probabilities_by_model = {}, {}, {}
    for name, factory in {"dense": build_dense, "cnn": build_cnn}.items():
        model = compile_model(factory(tf))
        model_path = models_dir / ("best_cnn.keras" if name == "cnn" else "dense_baseline.keras")
        callbacks = [tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)]
        if name == "cnn":
            callbacks.append(tf.keras.callbacks.ModelCheckpoint(model_path, save_best_only=True))
        start = perf_counter()
        history = model.fit(x_train, y_train, validation_data=(x_valid, y_valid),
                            epochs=args.epochs, batch_size=128, callbacks=callbacks, verbose=2)
        train_seconds = perf_counter() - start
        if name == "dense":
            model.save(model_path)
        histories[name] = {key: [float(v) for v in values]
                           for key, values in history.history.items()}
        start = perf_counter()
        probabilities = model.predict(x_test, verbose=0)
        inference_seconds = perf_counter() - start
        predictions = probabilities.argmax(axis=1)
        probabilities_by_model[name] = probabilities
        class_reports[name] = classification_report(
            y_test, predictions, target_names=CLASS_NAMES, digits=3, output_dict=True)
        timing = measure_inference(model, x_test)
        metrics[name] = {
            "f1_macro": float(f1_score(y_test, predictions, average="macro")),
            "accuracy": float(accuracy_score(y_test, predictions)),
            "parameters": int(model.count_params()),
            "model_file_kb": file_size_kb(model_path),
            "train_seconds": train_seconds,
            "epochs_run": len(histories[name]["loss"]),
            "best_epoch": int(np.argmin(histories[name]["val_loss"]) + 1),
            "inference_ms_per_image": 1000 * inference_seconds / len(x_test),
            "inference_repeated": timing,
            "top_confusions": top_confusions(y_test, predictions),
        }
        print(name, json.dumps({k: v for k, v in metrics[name].items()
                                if k != "top_confusions"}, indent=2))
        print(classification_report(y_test, predictions, target_names=CLASS_NAMES, digits=3))
        ConfusionMatrixDisplay.from_predictions(
            y_test, predictions, display_labels=CLASS_NAMES, cmap="Blues",
            xticks_rotation=45, colorbar=False)
        plt.title(f"Matriz de confusión ({name}, prueba)")
        plt.savefig(reports / f"confusion_{name}.png", dpi=170, bbox_inches="tight")
        plt.close("all")

    metrics["cnn_errors"] = plot_errors(x_test, y_test, probabilities_by_model["cnn"],
                                        reports / "cnn_errors.png")
    plot_curves(histories, reports / "training_curves.png")
    plot_per_class_f1(class_reports, reports / "per_class_f1.png")
    (reports / "history.json").write_text(json.dumps(histories, indent=2), encoding="utf-8")
    (reports / "classification_reports.json").write_text(
        json.dumps(class_reports, indent=2), encoding="utf-8")
    (reports / "cv_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
