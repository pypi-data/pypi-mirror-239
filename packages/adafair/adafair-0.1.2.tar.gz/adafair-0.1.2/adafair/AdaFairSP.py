"""Weight Boosting

This module contains weight boosting estimators for both classification and
regression.

The module structure is the following:

- The ``BaseWeightBoosting`` base class implements a common ``fit`` method
  for all the estimators in the module. Regression and classification
  only differ from each other in the loss function that is optimized.

- ``AdaCostClassifier`` implements adaptive boosting (AdaBoost-SAMME) for
  classification problems.

- ``AdaBoostRegressor`` implements adaptive boosting (AdaBoost.R2) for
  regression problems.
"""

# Authors: Noel Dawe <noel@dawe.me>
#          Gilles Louppe <g.louppe@gmail.com>
#          Hamzeh Alsalhi <ha258@cornell.edu>
#          Arnaud Joly <arnaud.v.joly@gmail.com>
#
# License: BSD 3 clause
from abc import ABCMeta, abstractmethod

import numpy as np
from sklearn.base import is_classifier, ClassifierMixin, is_regressor
import six
import sys
from sklearn.ensemble._base import BaseEnsemble

DTYPE = np.float64
sys.modules['sklearn.externals.six'] = six
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.tree import BaseDecisionTree, DecisionTreeClassifier
from sklearn.utils.validation import has_fit_parameter, check_is_fitted, check_array, check_X_y, check_random_state

__all__ = [
    'AdaFairSP'
]


class BaseWeightBoosting(six.with_metaclass(ABCMeta, BaseEnsemble)):
    """Base class for AdaBoost estimators.

    Warning: This class should not be used directly. Use derived classes
    instead.
    """

    @abstractmethod
    def __init__(self,
                 base_estimator=None,
                 n_estimators=50,
                 estimator_params=tuple(),
                 learning_rate=1.,
                 random_state=None):

        super(BaseWeightBoosting, self).__init__(
            base_estimator=base_estimator,
            n_estimators=n_estimators,
            estimator_params=estimator_params)

        self.W_pos = 0.
        self.W_neg = 0.
        self.W_dp = 0.
        self.W_fp = 0.
        self.W_dn = 0.
        self.W_fn = 0.
        self.performance = []
        self.objective = []
        self.learning_rate = learning_rate
        self.random_state = random_state
        self.tuning_learners = []

    def fit(self, X, y, sample_weight=None):
        """Build a boosted classifier/regressor from the training set (X, y).

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. COO, DOK, and LIL are converted to CSR. The dtype is
            forced to DTYPE from tree._tree if the base classifier of this
            ensemble weighted boosting classifier is a tree or forest.

        y : array-like of shape = [n_samples]
            The target values (class labels in classification, real numbers in
            regression).

        sample_weight : array-like of shape = [n_samples], optional
            Sample weights. If None, the sample weights are initialized to
            1 / n_samples.

        Returns
        -------
        self : object
            Returns self.
        """
        # Check parameters
        self.weight_list = []
        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be greater than zero")

        if (self.base_estimator is None or
                isinstance(self.base_estimator, (BaseDecisionTree,
                                                 BaseForest))):
            dtype = DTYPE
            accept_sparse = 'csc'
        else:
            dtype = None
            accept_sparse = ['csr', 'csc']

        X, y = check_X_y(X, y, accept_sparse=accept_sparse, dtype=dtype,
                         y_numeric=is_regressor(self))

        if sample_weight is None:
            # Initialize weights to 1 / n_samples
            sample_weight = np.empty(X.shape[0], dtype=np.float64)
            sample_weight[:] = 1. / X.shape[0]
        else:
            sample_weight = check_array(sample_weight, ensure_2d=False)
            # Normalize existing weights
            sample_weight = sample_weight / sample_weight.sum(dtype=np.float64)

            # Check that the sample weights sum is positive
            if sample_weight.sum() <= 0:
                raise ValueError(
                    "Attempting to fit with a non-positive "
                    "weighted number of samples.")

        # Check parameters
        self._validate_estimator()

        if self.debug:
            self.conf_scores = []

        # Clear any previous fit results
        self.estimators_ = []

        self.estimator_alphas_ = np.zeros(self.n_estimators, dtype=np.float64)
        self.estimator_fairness_ = np.ones(self.n_estimators, dtype=np.float64)
        self.predictions_array = np.zeros([X.shape[0], 2])

        random_state = check_random_state(self.random_state)
        if self.debug:
            print("iteration, alpha , positives , negatives , dp , fp , dn , fn")

        old_weights_sum = np.sum(sample_weight)
        pos, neg, dp, fp, dn, fn = self.calculate_weights(X, y, sample_weight)

        if self.debug:
            self.weight_list.append(
                'init' + "," + str(0) + "," + str(pos) + ", " + str(neg) + ", " + str(dp) + ", " + str(
                    fp) + ", " + str(dn) + ", " + str(fn))

        for iboost in range(self.n_estimators):
            # Boosting step
            sample_weight, alpha, error, fairness, balanced_error, standard_error = self._boost(
                iboost,
                X, y,
                sample_weight,
                random_state)

            # Early termination
            if sample_weight is None:
                break

            self.tuning_learners.append(self.c * balanced_error + (1 - self.c) * standard_error + fairness)

            # self.estimator_alphas_[iboost] = alpha

            # Stop if error is zero
            if error == 0.5:
                break

            new_sample_weight = np.sum(sample_weight)
            multiplier = old_weights_sum / new_sample_weight

            # Stop if the sum of sample weights has become non-positive
            if new_sample_weight <= 0:
                break

            if iboost < self.n_estimators - 1:
                # Normalize
                sample_weight *= multiplier

            pos, neg, dp, fp, dn, fn = self.calculate_weights(X, y, sample_weight)

            if self.debug:
                self.weight_list.append(
                    str(iboost) + "," + str(alpha) + "," + str(pos) + ", " + str(neg) + ", " + str(dp) + ", " + str(
                        fp) + ", " + str(dn) + ", " + str(fn))
            #
            # self.W_pos += pos / self.n_estimators
            # self.W_neg += neg / self.n_estimators
            # self.W_dp += dp / self.n_estimators
            # self.W_fp += fp / self.n_estimators
            # self.W_dn += dn / self.n_estimators
            # self.W_fn += fn / self.n_estimators

            old_weights_sum = np.sum(sample_weight)

        best_theta = self.tuning_learners.index(min(self.tuning_learners))
        self.theta = best_theta + 1

        if self.debug:
            print("best #weak learners = " + str(self.theta))
        self.estimators_ = self.estimators_[:self.theta]
        self.estimator_alphas_ = self.estimator_alphas_[:self.theta]

        if self.debug:
            self.get_confidence_scores(X)
        # print("best #weak learners = " + str(self.theta))

        return self

    def get_weights_over_iterations(self, ):
        return self.weight_list[self.theta]

    def get_confidence_scores(self, X):
        self.conf_scores = self.decision_function(X)

    def get_initial_weights(self):
        return self.weight_list[0]

    def get_weights(self, ):
        return [self.W_pos, self.W_neg, self.W_dp, self.W_fp, self.W_dn, self.W_fn]

    @abstractmethod
    def _boost(self, iboost, X, y, sample_weight, random_state):
        """Implement a single boost.

        Warning: This method needs to be overridden by subclasses.

        Parameters
        ----------
        iboost : int
            The index of the current boost iteration.

        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. COO, DOK, and LIL are converted to CSR.

        y : array-like of shape = [n_samples]
            The target values (class labels).

        sample_weight : array-like of shape = [n_samples]
            The current sample weights.

        random_state : numpy.RandomState
            The current random number generator

        Returns
        -------
        sample_weight : array-like of shape = [n_samples] or None
            The reweighted sample weights.
            If None then boosting has terminated early.

        estimator_weight : float
            The weight for the current boost.
            If None then boosting has terminated early.

        error : float
            The classification error for the current boost.
            If None then boosting has terminated early.
        """
        pass

    def staged_score(self, X, y, sample_weight=None):
        """Return staged scores for X, y.

        This generator method yields the ensemble score after each iteration of
        boosting and therefore allows monitoring, such as to determine the
        score on a test set after each boost.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.

        y : array-like, shape = [n_samples]
            Labels for X.

        sample_weight : array-like, shape = [n_samples], optional
            Sample weights.

        Returns
        -------
        z : float
        """
        for y_pred in self.staged_predict(X):
            if is_classifier(self):
                yield accuracy_score(y, y_pred, sample_weight=sample_weight)
            else:
                yield r2_score(y, y_pred, sample_weight=sample_weight)

    @property
    def feature_importances_(self):
        """Return the feature importances (the higher, the more important the
           feature).

        Returns
        -------
        feature_importances_ : array, shape = [n_features]
        """
        if self.estimators_ is None or len(self.estimators_) == 0:
            raise ValueError("Estimator not fitted, "
                             "call `fit` before `feature_importances_`.")

        try:
            norm = self.estimator_alphas_.sum()
            return (sum(weight * clf.feature_importances_ for weight, clf
                        in zip(self.estimator_alphas_, self.estimators_))
                    / norm)

        except AttributeError:
            raise AttributeError(
                "Unable to compute feature importances "
                "since base_estimator does not have a "
                "feature_importances_ attribute")

    def _validate_X_predict(self, X):
        """Ensure that X is in the proper format"""
        if (self.base_estimator is None or
                isinstance(self.base_estimator,
                           (BaseDecisionTree, BaseForest))):
            X = check_array(X, accept_sparse='csr', dtype=DTYPE)

        else:
            X = check_array(X, accept_sparse=['csr', 'csc', 'coo'])

        return X

    def calculate_weights(self, data, labels, sample_weight):

        protected_positive = 0.
        non_protected_positive = 0.

        protected_negative = 0.
        non_protected_negative = 0.

        for idx, val in enumerate(data):
            # protrcted population
            if val[self.saIndex] == self.saValue:
                # protected group
                if labels[idx] == 1:
                    protected_positive += sample_weight[idx]  # /len(sample_weight)
                else:
                    protected_negative += sample_weight[idx]  # /len(sample_weight)
            else:
                # correctly classified
                if labels[idx] == 1:
                    non_protected_positive += sample_weight[idx]  # /len(sample_weight)
                else:
                    non_protected_negative += sample_weight[idx]  # /len(sample_weight)

        return [protected_positive + non_protected_positive,
                protected_negative + non_protected_negative,
                protected_positive,
                non_protected_positive,
                protected_negative,
                non_protected_negative]


def _samme_proba(estimator, n_classes, X):
    """Calculate algorithm 4, step 2, equation c) of Zhu et al [1].

    References
    ----------
    .. [1] J. Zhu, H. Zou, S. Rosset, T. Hastie, "Multi-class AdaBoost", 2009.

    """
    proba = estimator.predict_proba(X)

    # Displace zero probabilities so the log is defined.
    # Also fix negative elements which may occur with
    # negative sample weights.
    proba[proba < np.finfo(proba.dtype).eps] = np.finfo(proba.dtype).eps
    log_proba = np.log(proba)

    return (n_classes - 1) * (log_proba - (1. / n_classes)
                              * log_proba.sum(axis=1)[:, np.newaxis])


class AdaFairSP(BaseWeightBoosting, ClassifierMixin):
    """An AdaBoost classifier.

    An AdaBoost [1] classifier is a meta-estimator that begins by fitting a
    classifier on the original dataset and then fits additional copies of the
    classifier on the same dataset but where the weights of incorrectly
    classified instances are adjusted such that subsequent classifiers focus
    more on difficult cases.

    This class implements the algorithm known as AdaBoost-SAMME [2].

    Read more in the :ref:`User Guide <adaboost>`.

    Parameters
    ----------
    base_estimator : object, optional (default=DecisionTreeClassifier)
        The base estimator from which the boosted ensemble is built.
        Support for sample weighting is required, as well as proper `classes_`
        and `n_classes_` attributes.

    n_estimators : integer, optional (default=50)
        The maximum number of estimators at which boosting is terminated.
        In case of perfect fit, the learning procedure is stopped early.

    learning_rate : float, optional (default=1.)
        Learning rate shrinks the contribution of each classifier by
        ``learning_rate``. There is a trade-off between ``learning_rate`` and
        ``n_estimators``.

    algorithm : {'SAMME', 'SAMME.R'}, optional (default='SAMME.R')
        If 'SAMME.R' then use the SAMME.R real boosting algorithm.
        ``base_estimator`` must support calculation of class probabilities.
        If 'SAMME' then use the SAMME discrete boosting algorithm.
        The SAMME.R algorithm typically converges faster than SAMME,
        achieving a lower test error with fewer boosting iterations.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    Attributes
    ----------
    estimators_ : list of classifiers
        The collection of fitted sub-estimators.

    classes_ : array of shape = [n_classes]
        The classes labels.

    n_classes_ : int
        The number of classes.

    estimator_weights_ : array of floats
        Weights for each estimator in the boosted ensemble.

    estimator_errors_ : array of floats
        Classification error for each estimator in the boosted
        ensemble.

    feature_importances_ : array of shape = [n_features]
        The feature importances if supported by the ``base_estimator``.

    See also
    --------
    AdaBoostRegressor, GradientBoostingClassifier, DecisionTreeClassifier

    References
    ----------
    .. [1] Y. Freund, R. Schapire, "A Decision-Theoretic Generalization of
           on-Line Learning and an Application to Boosting", 1995.

    .. [2] J. Zhu, H. Zou, S. Rosset, T. Hastie, "Multi-class AdaBoost", 2009.

    """

    def __init__(self,
                 base_estimator=None,
                 n_estimators=50,
                 learning_rate=1.,
                 algorithm='SAMME',
                 cumul=True,
                 random_state=None,
                 saIndex=None, saValue=None,
                 debug=False, CSB="CSB2",
                 X_test=None, y_test=None, c=1):

        super(AdaFairSP, self).__init__(
            base_estimator=base_estimator,
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            random_state=random_state)

        self.cumul = cumul
        self.cost_protected_positive = 1
        self.cost_non_protected_positive = 1

        self.cost_protected_negative = 1
        self.cost_non_protected_negative = 1

        self.c = c
        self.saIndex = saIndex
        self.saValue = saValue
        self.algorithm = algorithm

        self.costs = []

        self.debug = debug
        self.csb = CSB
        self.X_test = X_test
        self.y_test = y_test

    def fit(self, X, y, sample_weight=None):
        """Build a boosted classifier from the training set (X, y).

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.

        y : array-like of shape = [n_samples]
            The target values (class labels).

        sample_weight : array-like of shape = [n_samples], optional
            Sample weights. If None, the sample weights are initialized to
            ``1 / n_samples``.

        Returns
        -------
        self : object
            Returns self.
        """
        # Check that algorithm is supported
        if self.algorithm not in ('SAMME', 'SAMME.R'):
            raise ValueError("algorithm %s is not supported" % self.algorithm)

        # Fit
        return super(AdaFairSP, self).fit(X, y, sample_weight)

    def _validate_estimator(self):
        """Check the estimator and set the base_estimator_ attribute."""
        super(AdaFairSP, self)._validate_estimator(
            default=DecisionTreeClassifier(max_depth=1))

        #  SAMME-R requires predict_proba-enabled base estimators
        if self.algorithm == 'SAMME.R':
            if not hasattr(self.base_estimator_, 'predict_proba'):
                raise TypeError(
                    "AccumFairAdaCost with algorithm='SAMME.R' requires "
                    "that the weak learner supports the calculation of class "
                    "probabilities with a predict_proba method.\n"
                    "Please change the base estimator or set "
                    "algorithm='SAMME' instead.")
        if not has_fit_parameter(self.base_estimator_, "sample_weight"):
            raise ValueError("%s doesn't support sample_weight."
                             % self.base_estimator_.__class__.__name__)

    def _boost(self, iboost, X, y, sample_weight, random_state):
        return self._boost_discrete(iboost, X, y, sample_weight, random_state)

    def calculate_fairness(self, iboost, data, labels, predictions):

        protected_pos = 0.
        protected_neg = 0.
        non_protected_pos = 0.
        non_protected_neg = 0.

        for idx, val in enumerate(data):
            # protrcted population
            if val[self.saIndex] == self.saValue:
                if predictions[idx] == 1:
                    protected_pos += 1
                else:
                    protected_neg += 1
            else:
                if predictions[idx] == 1:
                    non_protected_pos += 1
                else:
                    non_protected_neg += 1

        C_prot = (protected_pos) / (protected_pos + protected_neg)
        C_non_prot = (non_protected_pos) / (non_protected_pos + non_protected_neg)

        stat_par = C_non_prot - C_prot

        # print("round = ", iboost, "statistical parity = ", stat_par, "protected = ", C_prot, "non_protected = ", C_non_prot)
        self.cost_protected_positive = self.cost_non_protected_positive = self.cost_protected_negative = self.cost_non_protected_negative = 1

        if stat_par < 0:
            self.cost_non_protected_positive = (1 + abs(stat_par))

        elif stat_par > 0:
            self.cost_protected_positive = (1 + stat_par)

        self.costs.append(stat_par)

        return abs(stat_par)


    def _boost_discrete(self, iboost, X, y, sample_weight, random_state):
        """Implement a single boost using the SAMME discrete algorithm."""
        estimator = self._make_estimator(random_state=random_state)
        estimator.fit(X, y, sample_weight=sample_weight)
        y_predict = estimator.predict(X)
        proba = estimator.predict_proba(X)

        if iboost == 0:
            self.classes_ = getattr(estimator, 'classes_', None)
            self.n_classes_ = len(self.classes_)
        n_classes = self.n_classes_
        incorrect = y_predict != y

        # Error fraction
        estimator_error = np.mean(
            np.average(incorrect, weights=sample_weight, axis=0))

        # Stop if classification is perfect
        if estimator_error <= 0:
            return sample_weight, 1., 0.

        n_classes = self.n_classes_

        # Stop if the error is at least as bad as random guessing
        if estimator_error >= 1. - (1. / n_classes):
            self.estimators_.pop(-1)
            if len(self.estimators_) == 0:
                raise ValueError('BaseClassifier in AdaBoostClassifier '
                                 'ensemble is worse than random, ensemble '
                                 'can not be fit.')
            return None, None, None

        # Boost weight using multi-class AdaBoost SAMME alg
        alpha = 1 * (
                np.log((1. - estimator_error) / estimator_error) +
                np.log(n_classes - 1.))

        self.estimator_alphas_[iboost] = alpha
        self.predictions_array += (y_predict == self.classes_[:, np.newaxis]).T * alpha

        if iboost != 0:
            if self.cumul:
                fairness = self.calculate_fairness(iboost, X, y,
                                                   self.classes_.take(np.argmax(self.predictions_array, axis=1)))
            else:
                fairness = self.calculate_fairness(iboost, X, y, y_predict)
        else:
            fairness = 1

        tn, fp, fn, tp = confusion_matrix(y, self.classes_.take(np.argmax(self.predictions_array, axis=1), axis=0),
                                          labels=[-1, 1]).ravel()
        TPR = (float(tp)) / (tp + fn)
        TNR = (float(tn)) / (tn + fp)
        cumulative_balanced_error = 1 - (TPR + TNR) / 2
        cumulative_error = 1 - (float(tp) + float(tn)) / (tp + tn + fp + fn)

        # print("balanced error", cumulative_balanced_error)
        if not iboost == self.n_estimators - 1:
            for idx, row in enumerate(sample_weight):
                if y[idx] == 1 and y_predict[idx] != 1:
                    if X[idx][self.saIndex] == self.saValue:
                        if self.csb == "CSB2":
                            sample_weight[idx] *= self.cost_protected_positive * np.exp(
                                alpha * max(proba[idx][0], proba[idx][1]))
                        elif self.csb == "CSB1":
                            sample_weight[idx] *= self.cost_protected_positive * np.exp(alpha)
                    else:
                        if self.csb == "CSB2":
                            sample_weight[idx] *= self.cost_non_protected_positive * np.exp(
                                alpha * max(proba[idx][0], proba[idx][1]))
                        elif self.csb == "CSB1":
                            sample_weight[idx] *= self.cost_non_protected_positive * np.exp(alpha)

                elif y[idx] == -1 and y_predict[idx] != -1:
                    if self.csb == "CSB2":
                        sample_weight[idx] *= np.exp(alpha * max(proba[idx][0], proba[idx][1]))
                    elif self.csb == "CSB1":
                        sample_weight[idx] *= np.exp(alpha)

        # if self.debug:
        #     y_predict = self.predict(X)
        #     incorrect = y_predict != y
        #     train_error = np.mean(np.average(incorrect, axis=0))
        #     train_bal_error = 1 - sklearn.metrics.balanced_accuracy_score(y, y_predict)
        #     train_fairness = self.measure_fairness_for_visualization(X, y, y_predict)
        #
        #     test_error = 0
        #     test_bal_error = 0
        #     test_fairness = 0
        #     if self.X_test is not None:
        #         y_predict = self.predict(self.X_test)
        #         incorrect = y_predict != self.y_test
        #         test_error = np.mean(np.average(incorrect, axis=0))
        #         test_bal_error = 1 - sklearn.metrics.balanced_accuracy_score(self.y_test, y_predict)
        #         test_fairness = self.measure_fairness_for_visualization(self.X_test, self.y_test, y_predict)
        #
        #     self.objective.append(train_error * (1 - self.c) + train_bal_error * self.c + train_fairness)
        #     self.performance.append(str(iboost) + "," + str(train_error) + ", " + str(train_bal_error) + ", " + str(
        #         train_fairness) + "," + str(test_error) + ", " + str(test_bal_error) + ", " + str(test_fairness))
        #     print(str(iboost) + "," + str(train_error) + ", " + str(train_bal_error) + ", " + str(
        #         train_fairness) + "," + str(test_error) + ", " + str(test_bal_error) + ", " + str(test_fairness))

        return sample_weight, alpha, estimator_error, fairness, cumulative_balanced_error, cumulative_error

    def get_performance_over_iterations(self):
        return self.performance

    #
    def get_objective(self):
        return self.objective

    #
    # def get_weights_over_iterations(self):
    #     return self.weight_list[self.theta]

    def predict(self, X):
        """Predict classes for X.

        The predicted class of an input sample is computed as the weighted mean
        prediction of the classifiers in the ensemble.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.

        Returns
        -------
        y : array of shape = [n_samples]
            The predicted classes.
        """
        pred = self.decision_function(X)

        if self.n_classes_ == 2:
            return self.classes_.take(pred > 0, axis=0)

        return self.classes_.take(np.argmax(pred, axis=1), axis=0)

    def decision_function(self, X):
        """Compute the decision function of ``X``.
        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.
        Returns
        -------
        score : array, shape = [n_samples, k]
            The decision function of the input samples. The order of
            outputs is the same of that of the `classes_` attribute.
            Binary classification is a special cases with ``k == 1``,
            otherwise ``k==n_classes``. For binary classification,
            values closer to -1 or 1 mean more like the first or second
            class in ``classes_``, respectively.
        """
        check_is_fitted(self, "n_classes_")
        X = self._validate_X_predict(X)

        n_classes = self.n_classes_
        classes = self.classes_[:, np.newaxis]

        pred = sum(
            (estimator.predict(X) == classes).T * w for estimator, w in zip(self.estimators_, self.estimator_alphas_))
        # pred = sum(estimator.predict_proba(X) * w for estimator, w,  in zip(self.estimators_, self.estimator_alphas_))
        pred /= self.estimator_alphas_.sum()
        if n_classes == 2:
            pred[:, 0] *= -1
            return pred.sum(axis=1)
        return pred

    def predict_proba(self, X):
        """Predict class probabilities for X.

        The predicted class probabilities of an input sample is computed as
        the weighted mean predicted class probabilities of the classifiers
        in the ensemble.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.

        Returns
        -------
        p : array of shape = [n_samples]
            The class probabilities of the input samples. The order of
            outputs is the same of that of the `classes_` attribute.
        """
        check_is_fitted(self, "n_classes_")

        n_classes = self.n_classes_
        X = self._validate_X_predict(X)

        if n_classes == 1:
            return np.ones((X.shape[0], 1))

        proba = sum(estimator.predict_proba(X) * w for estimator, w in zip(self.estimators_, self.estimator_alphas_))

        proba /= self.estimator_alphas_.sum()
        proba = np.exp((1. / (n_classes - 1)) * proba)
        normalizer = proba.sum(axis=1)[:, np.newaxis]
        normalizer[normalizer == 0.0] = 1.0
        proba /= normalizer

        return proba

    def predict_log_proba(self, X):
        """Predict class log-probabilities for X.

        The predicted class log-probabilities of an input sample is computed as
        the weighted mean predicted class log-probabilities of the classifiers
        in the ensemble.

        Parameters
        ----------
        X : {array-like, sparse matrix} of shape = [n_samples, n_features]
            The training input samples. Sparse matrix can be CSC, CSR, COO,
            DOK, or LIL. DOK and LIL are converted to CSR.

        Returns
        -------
        p : array of shape = [n_samples]
            The class probabilities of the input samples. The order of
            outputs is the same of that of the `classes_` attribute.
        """
        return np.log(self.predict_proba(X))
