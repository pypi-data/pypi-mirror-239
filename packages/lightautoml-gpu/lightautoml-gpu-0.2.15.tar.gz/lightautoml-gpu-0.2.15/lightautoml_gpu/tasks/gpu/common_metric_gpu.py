"""Bunch of metrics with unified interface (GPU version)."""

from functools import partial
from typing import Callable
from typing import Optional

from sklearn.metrics import f1_score

import cudf
import cupy as cp
import dask.array as da
from cuml.metrics import log_loss
from cuml.metrics.regression import mean_squared_log_error

from py_boost.gpu.losses.metrics import R2Score
from py_boost.gpu.losses.metrics import auc
from py_boost.gpu.losses.metrics import AccuracyMetric


def log_loss_raw(y_true, y_pred, sample_weight=None, eps=1e-15, axis=1):
    y_pred /= y_pred.sum(axis=axis)[:, cp.newaxis]
    loss = -(y_true * cp.log(y_pred)).sum(axis=axis)
    if sample_weight is None:
        return loss.sum() / len(loss)
    else:
        return (loss * sample_weight).sum() / len(loss)


def log_loss_gpu(y_true, y_pred, sample_weight=None, eps: float = 1e-15) -> float:

    res = None

    if isinstance(y_true, da.Array):
        y_true = y_true.compute().squeeze()
        y_pred = y_pred.compute().squeeze()
        if sample_weight is not None:
            sample_weight = sample_weight.compute().squeeze()
    if y_true.shape == y_pred.shape and y_true.ndim > 1:
        func = log_loss_raw
    else:
        func = log_loss
    res = func(y_true, y_pred, sample_weight=sample_weight, eps=eps)
    return res


def r2_score_gpu(y_true, y_pred, sample_weight=None) -> float:

    r2_score = R2Score()
    if isinstance(y_true, da.Array):
        output = da.map_blocks(
            r2_score, y_true, y_pred, sample_weight, meta=cp.array((), dtype=cp.float32), drop_axis=1
        )
        res = cp.array(output.compute()).mean()
    else:
        res = r2_score(y_true, y_pred, sample_weight)
    return res


def roc_auc_score_gpu(y_true, y_pred, sample_weight=None) -> float:

    if isinstance(y_true, da.Array):
        y_true = y_true.compute().squeeze()
        y_pred = y_pred.compute().squeeze()
        if sample_weight is not None:
            sample_weight = sample_weight.compute().squeeze()

    res = auc(y_true, y_pred, sample_weight)
    return res


def mean_squared_error_gpu(y_true, y_pred, sample_weight=None) -> float:

    """Computes Mean Squared Error for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Specify weighted mean (currently not used).

    Returns:
        metric value.

    """
    if isinstance(y_true, da.Array):
        err = y_pred - y_true
        err = da.multiply(err, err)
        if sample_weight is None:
            return err.mean().compute()
        err = (err.mean(axis=1, keepdims=True) * sample_weight).sum() / sample_weight.sum()
        err = err.compute()
    else:
        err = cp.square(y_pred - y_true)
        if sample_weight is None:
            return err.mean()

        err = (err.mean(axis=1, keepdims=True) * sample_weight).sum() / sample_weight.sum()

    return err


def mean_absolute_error(y_true, y_pred, sample_weight=None):
    err = abs(y_true - y_pred)
    if sample_weight is None:
        return err.mean()

    err = (err.mean(axis=1, keepdims=True) * sample_weight).sum() / sample_weight.sum()
    return err


def mean_absolute_error_gpu(y_true, y_pred, sample_weight=None):

    if isinstance(y_true, da.Array):
        res = da.map_blocks(
            mean_absolute_error,
            y_true,
            y_pred,
            sample_weight,
            meta=cp.array((), dtype=cp.float32),
            drop_axis=1,
        )
        return cp.array(res.compute()).mean()
    else:
        return mean_absolute_error(y_true, y_pred, sample_weight)


def mean_quantile_error_gpu(y_true, y_pred, sample_weight=None, q: float = 0.9) -> float:
    """Computes Mean Quantile Error for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Specify weighted mean.
        q: Metric coefficient.

    Returns:
        metric value.

    """

    if isinstance(y_true, da.Array):
        err = y_pred - y_true
        s = da.sign(err)
        err = da.where(s > 0, q * err, (q - 1) * err)
        if sample_weight is not None:
            return ((err * sample_weight).mean() / sample_weight.mean()).compute()
        return err.mean().compute()
    else:
        err = y_pred - y_true
        s = cp.sign(err)
        err = cp.abs(err)
        err = cp.where(s > 0, q, 1 - q) * err
        if sample_weight is not None:
            return (err * sample_weight).mean() / sample_weight.mean()
        return err.mean()


def mean_huber_error_gpu(y_true, y_pred, sample_weight=None, a: float = 0.9) -> float:
    """Computes Mean Huber Error for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Specify weighted mean.
        a: Metric coefficient.

    Returns:
        Metric value.

    """
    assert a >= 0, "a cannot be negative"

    if isinstance(y_true, da.Array):
        err = y_pred - y_true
        s = da.where(err < 0, err > -a, err < a)
        abs_err = da.where(err > 0, err, -err)
        err = da.where(s, 0.5 * (err ** 2), a * abs_err - 0.5 * (a ** 2))
        if sample_weight is not None:
            return ((err * sample_weight).mean() / sample_weight.mean()).compute()
        return err.mean().compute()
    else:
        err = y_pred - y_true
        s = cp.abs(err) < a
        err = cp.where(s, 0.5 * (err ** 2), a * cp.abs(err) - 0.5 * (a ** 2))
        if sample_weight is not None:
            return (err * sample_weight).mean() / sample_weight.mean()
        return err.mean()


def mean_fair_error_gpu(y_true, y_pred, sample_weight=None, c: float = 0.9) -> float:
    """Computes Mean Fair Error for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Specify weighted mean.
        c: Metric coefficient.

    Returns:
        Metric value.

    """
    if isinstance(y_true, da.Array):
        err = y_pred - y_true
        x = da.where(err > 0, err, -err) / c
        err = c ** 2 * (x - da.log(x + 1))
        if sample_weight is not None:
            return ((err * sample_weight).mean() / sample_weight.mean()).compute()
        return err.mean().compute()
    else:
        x = cp.abs(y_pred - y_true) / c
        err = c ** 2 * (x - cp.log(x + 1))
        if sample_weight is not None:
            return (err * sample_weight).mean() / sample_weight.mean()
        return err.mean()


def mean_absolute_percentage_error_gpu(y_true, y_pred, sample_weight=None) -> float:
    """Computes Mean Absolute Percentage error for Mulit-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Specify weighted mean.

    Returns:
        Metric value.

    """
    if isinstance(y_true, da.Array):
        err = (y_true - y_pred) / y_true
        err = da.where(err > 0, err, -err)
        if sample_weight is not None:
            return ((err * sample_weight).mean() / sample_weight.mean()).compute()
        return err.mean().compute()
    else:
        err = (y_true - y_pred) / y_true
        err = cp.abs(err)
        if sample_weight is not None:
            return (err * sample_weight).mean() / sample_weight.mean()
        return err.mean()


def roc_auc_ovr_gpu(y_true, y_pred, sample_weight=None):
    """ROC-AUC One-Versus-Rest for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Weights of samples.

    Returns:
        Metric values.

    """
    if isinstance(y_true, da.Array):
        res = da.map_blocks(
            roc_auc_ovr_gpu,
            y_true,
            y_pred,
            sample_weight,
            meta=cp.array((), dtype=cp.float32),
            drop_axis=1,
        )
        return cp.array(res.compute()).mean()
    else:
        if isinstance(y_true, (cudf.Series, cudf.DataFrame)):
            y_pred = y_pred.values
            y_true = y_true.values
        n_classes = y_pred.shape[1]
        res = 0.0
        for i in range(n_classes):
            s_w = None
            if sample_weight is not None:
                s_w = sample_weight[:, i]
            res += auc(cp.where(y_true == i, 1, 0).squeeze(), y_pred[:, i], s_w)
        return res / n_classes


def rmsle_gpu(y_true, y_pred, sample_weight=None):
    """Root mean squared log error for Multi-GPU data.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Weights of samples.

    Returns:
        Metric values.


    """

    if isinstance(y_true, da.Array):
        output_errors = da.subtract(da.log1p(y_true), da.log1p(y_pred))
        output_errors = da.multiply(output_errors, output_errors)
        if sample_weight is not None:
            output_errors = da.multiply(output_errors, sample_weight)
            output_errors = da.divide(da.sum(output_errors), sample_weight.sum())
        else:
            output_errors = da.mean(output_errors)
        return cp.sqrt(output_errors.compute())
    else:
        return mean_squared_log_error(
            y_true, y_pred, sample_weight=sample_weight, squared=False
        )


def auc_mu_gpu(
    y_true: cp.ndarray,
    y_pred: cp.ndarray,
    sample_weight: Optional[cp.ndarray] = None,
    class_weights: Optional[cp.ndarray] = None,
) -> float:
    """Compute multi-class metric AUC-Mu.

    We assume that confusion matrix full of ones, except diagonal elements.
    All diagonal elements are zeroes.
    By default, for averaging between classes scores we use simple mean.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.
        sample_weight: Not used.
        class_weights: The between classes weight matrix. If ``None``,
            the standard mean will be used. It is expected to be a lower
            triangular matrix (diagonal is also full of zeroes).
            In position (i, j), i > j, there is a partial positive score
            between i-th and j-th classes. All elements must sum up to 1.

    Returns:
        Metric value.

    Note:
        Code was refactored from https://github.com/kleimanr/auc_mu/blob/master/auc_mu.py

    """
    if isinstance(y_true, da.Array):
        y_true = y_true.compute().squeeze()
        y_pred = y_pred.compute().squeeze()
        if sample_weight is not None:
            sample_weight = sample_weight.compute().squeeze()

    if not isinstance(y_pred, cp.ndarray):
        raise TypeError("Expected y_pred to be cp.ndarray, got: {}".format(type(y_pred)))
    if not y_pred.ndim == 2:
        raise ValueError("Expected array with predictions be a 2-dimentional array")
    if not isinstance(y_true, cp.ndarray):
        raise TypeError("Expected y_true to be cp.ndarray, got: {}".format(type(y_true)))
    if not y_true.ndim == 1:
        raise ValueError("Expected array with ground truths be a 1-dimentional array")
    if y_true.shape[0] != y_pred.shape[0]:
        raise ValueError(
            "Expected number of samples in y_true and y_pred be same,"
            " got {} and {}, respectively".format(y_true.shape[0], y_pred.shape[0])
        )

    uniq_labels = cp.unique(y_true)
    n_samples, n_classes = y_pred.shape

    if not cp.all(uniq_labels == cp.arange(n_classes)):
        raise ValueError("Expected classes encoded values 0, ..., N_classes-1")

    if class_weights is None:
        class_weights = cp.tri(n_classes, k=-1)
        class_weights /= class_weights.sum()

    if not isinstance(class_weights, cp.ndarray):
        raise TypeError(
            "Expected class_weights to be cp.ndarray, got: {}".format(
                type(class_weights)
            )
        )
    if not class_weights.ndim == 2:
        raise ValueError("Expected class_weights to be a 2-dimentional array")
    if not class_weights.shape == (n_classes, n_classes):
        raise ValueError(
            "Expected class_weights size: {}, got: {}".format(
                (n_classes, n_classes), class_weights.shape
            )
        )
    confusion_matrix = cp.ones((n_classes, n_classes)) - cp.eye(n_classes)
    auc_full = 0.0

    for class_i in range(n_classes):
        preds_i = y_pred[y_true == class_i]
        n_i = preds_i.shape[0]
        for class_j in range(class_i):
            preds_j = y_pred[y_true == class_j]
            n_j = preds_j.shape[0]
            n = n_i + n_j
            tmp_labels = cp.zeros((n,), dtype=cp.int32)
            tmp_labels[n_i:] = 1
            tmp_pres = cp.vstack((preds_i, preds_j))
            v = confusion_matrix[class_i, :] - confusion_matrix[class_j, :]
            scores = cp.dot(tmp_pres, v)
            score_ij = auc(tmp_labels, scores)
            auc_full += class_weights[class_i, class_j] * score_ij

    return auc_full


class F1FactoryGPU:
    """
    Wrapper for :func:`~sklearn.metrics.f1_score` function.
    """

    def __init__(self, average: str = 'micro'):
        """

        Args:
            average: Averaging type ('micro', 'macro', 'weighted').
        """
        self.average = average

    def __call__(self, y_true: cp.ndarray, y_pred: cp.ndarray,
                 sample_weight: Optional[cp.ndarray] = None) -> float:
        """Compute metric.

         Args:
             y_true: Ground truth target values.
             y_pred: Estimated target values.
             sample_weight: Sample weights.

         Returns:
             F1 score of the positive class in binary classification
             or weighted average of the F1 scores of each class
             for the multiclass task.

        """
        if isinstance(y_true, da.Array):
            y_true = y_true.compute().squeeze()
            y_pred = y_pred.compute().squeeze()
            if sample_weight is not None:
                sample_weight = sample_weight.compute().squeeze()
        y_true = cp.asnumpy(y_true)
        y_pred = cp.asnumpy(y_pred)
        if sample_weight is not None:
            sample_weight = cp.asnumpy(sample_weight)
        return f1_score(y_true, y_pred, sample_weight=sample_weight, average=self.average)


class BestClassBinaryWrapperGPU:
    """Metric wrapper to get best class prediction instead of probs.

    There is cut-off for prediction by ``0.5``.

    """

    def __init__(self, func: Callable):
        """

        Args:
            func: Metric function. Function format:
               func(y_pred, y_true, weights, \*\*kwargs).

        """
        self.func = func

    def __call__(
        self,
        y_true: cp.ndarray,
        y_pred: cp.ndarray,
        sample_weight: Optional[cp.ndarray] = None,
        **kwargs
    ):
        y_pred = (y_pred > 0.5).astype(cp.float32)

        return self.func(y_true, y_pred, sample_weight=sample_weight, **kwargs)


class AccuracyScoreWrapper:
    def __call__(
        self,
        y_true: cp.ndarray,
        y_pred: cp.ndarray,
        sample_weight: Optional[cp.ndarray] = None
    ):
        accuracy_score = AccuracyMetric()
        if type(y_pred) == da.Array:
            y_pred = y_pred.compute()
            y_true = y_true.compute()
            if sample_weight is not None:
                sample_weight = sample_weight.compute()

        if len(y_pred.shape) == 1:
            y_pred = y_pred[:, cp.newaxis]
            y_true = y_true[:, cp.newaxis]
        if sample_weight is not None and len(sample_weight.shape) == 1:
            sample_weight = sample_weight[:, cp.newaxis]
        return accuracy_score(y_true, y_pred, sample_weight)


class BestClassMulticlassWrapperGPU:
    """Metric wrapper to get best class prediction instead of probs for multiclass.

    Prediction provides by argmax.

    """

    def __init__(self, func):
        """

        Args:
            func: Metric function. Function format:
               func(y_pred, y_true, weights, \*\*kwargs)

        """
        self.func = func

    def __call__(
        self,
        y_true: cp.ndarray,
        y_pred: cp.ndarray,
        sample_weight: Optional[cp.ndarray] = None,
        **kwargs
    ):

        if type(y_pred) == cp.ndarray:

            y_pred = (y_pred.argmax(axis=1)).astype(cp.float32)

        elif type(y_pred) == da.Array:

            def dask_argmax_gpu(data):
                res = cp.copy(data)
                res[:, 0] = data.argmax(axis=1).astype(cp.float32)
                return res

            y_pred = da.map_blocks(
                dask_argmax_gpu, y_pred, meta=cp.array((), dtype=cp.float32)
            )[:, 0]
            if y_true.ndim == 2:
                y_true = y_true[:, 0]

        elif isinstance(y_true, (cudf.Series, cudf.DataFrame)):
            y_pred = (y_pred.values.argmax(axis=1)).astype(cp.float32)
            y_true = y_true.values

        else:

            raise NotImplementedError

        return self.func(y_true, y_pred, sample_weight=sample_weight, **kwargs)


_valid_str_binary_metric_names_gpu = {
    "auc": roc_auc_score_gpu,
    "logloss": partial(log_loss_gpu, eps=1e-7),
    "accuracy": BestClassBinaryWrapperGPU(AccuracyScoreWrapper()),
}

_valid_str_reg_metric_names_gpu = {
    "r2": r2_score_gpu,
    "mse": mean_squared_error_gpu,
    "mae": mean_absolute_error_gpu,
    "rmsle": rmsle_gpu,
    "fair": mean_fair_error_gpu,
    "huber": mean_huber_error_gpu,
    "quantile": mean_quantile_error_gpu,
    "mape": mean_absolute_percentage_error_gpu,
}

_valid_str_multiclass_metric_names_gpu = {
    "auc_mu": auc_mu_gpu,
    "auc": roc_auc_ovr_gpu,
    "crossentropy": partial(log_loss_gpu, eps=1e-7),
    "accuracy": BestClassMulticlassWrapperGPU(AccuracyScoreWrapper()),
    'f1_macro': BestClassMulticlassWrapperGPU(F1FactoryGPU('macro')),
    'f1_micro': BestClassMulticlassWrapperGPU(F1FactoryGPU('micro')),
    'f1_weighted': BestClassMulticlassWrapperGPU(F1FactoryGPU('weighted')),
}

_valid_str_multireg_metric_names_gpu = {"mse": mean_squared_error_gpu, "mae": mean_absolute_error_gpu}

_valid_str_multilabel_metric_names_gpu = {"logloss": partial(log_loss_gpu, eps=1e-7)}

_valid_str_metric_names_gpu = {
    "binary": _valid_str_binary_metric_names_gpu,
    "reg": _valid_str_reg_metric_names_gpu,
    "multiclass": _valid_str_multiclass_metric_names_gpu,
    "multi:reg": _valid_str_multireg_metric_names_gpu,
    "multilabel": _valid_str_multilabel_metric_names_gpu,
}
