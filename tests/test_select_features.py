import pytest
import pandas as pd
import numpy as np
import random
import string
from pylaundry import select_features


@pytest.fixture
def generate_data_regression():

    """
    The function generates data for regression test
    Examples
    --------
    >>> generate_data_regression()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    x2 = np.random.randint(low=100, high=600, size=1000)
    x3 = np.random.randint(low=-100, high=300, size=1000)
    y = 2*x1
    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "y": y})

    return df


@pytest.fixture
def generate_data_regression_one():

    """
    The function generates data for regression test for multi features
    Examples
    --------
    >>> generate_data_regression_one()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    x2 = np.random.randint(low=100, high=600, size=1000)
    x3 = np.random.randint(low=-100, high=300, size=1000)
    y = 2*x1 + 3*x2
    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "y": y})

    return df


@pytest.fixture
def generate_data_classification():

    """
    The function generates data for classification test for single feature
    Examples
    --------
    >>> generate_data_classification()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    x2 = np.random.randint(low=100, high=600, size=1000)
    x3 = np.random.randint(low=-100, high=300, size=1000)
    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3})
    df['y'] = df['x1'].apply(lambda x: 1 if x > 150 else 0)

    return df


@pytest.fixture
def generate_data_classification_multi():

    """
    The function generates data for classification test for multiple feature
    Examples
    --------
    >>> generate_data_classification_multi()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    x2 = np.random.randint(low=100, high=600, size=1000)
    x3 = np.random.randint(low=-100, high=300, size=1000)
    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3})
    df['y'] = df.apply(lambda x: 1 if (x['x1'] > 150
                                       and x['x2'] > 300) else 0, axis=1)

    return df


@pytest.fixture
def generate_wrong_data():

    """
    The function generates data for wrong column type in input data
    Examples
    --------
    >>> generate_wrong_data()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    x2 = np.random.randint(low=100, high=600, size=1000)
    x3 = [random.choice(string.ascii_lowercase) for i in range(1000)]
    y = 2*x1
    df = pd.DataFrame({"x1": x1, "x2": x2, "x3": x3, "y": y})

    return df


@pytest.fixture
def generate_wrong_data_one():

    """
    The function generates data for wrong input data type
    Examples
    --------
    >>> generate_wrong_data_one()
    """

    x1 = np.random.randint(low=0, high=200, size=1000)
    y = 2*x1

    return x1, y


def test_regression(generate_data_regression):

    """
    The function does regression test for single feature
    Examples
    --------
    >>> test_regression(generate_data_regression)
    """

    df = generate_data_regression
    y = df['y'].values
    df = df[['x1', 'x2', 'x3']]
    assert select_features.select_features(df, y, n_features=1) == ["x1"]


def test_regression_one(generate_data_regression_one):

    """
    The function does regression test for multi feature
    Examples
    --------
    >>> test_regression_one(generate_data_regression_one)
    """

    df = generate_data_regression_one
    y = df['y'].values
    df = df[['x1', 'x2', 'x3']]
    assert select_features.select_features(df, y, n_features=2) == ["x1", "x2"]


def test_classification(generate_data_classification):

    """
    The function does classification test for single feature
    Examples
    --------
    >>> test_classification(generate_data_classification)
    """

    df = generate_data_classification
    y = df['y'].values
    df = df[['x1', 'x2', 'x3']]
    t = select_features.select_features(df,
                                        y, mode="classification", n_features=1)
    assert t == ["x1"]


def test_classification_multi(generate_data_classification_multi):

    """
    The function does classification test for multiple feature
    Examples
    --------
    >>> test_classification_multi(generate_data_classification_multi)
    """

    df = generate_data_classification_multi
    y = df['y'].values
    df = df[['x1', 'x2', 'x3']]
    t = select_features.select_features(df,
                                        y, mode="classification", n_features=2)
    assert t == ["x1", "x2"]


def test_dataframe(generate_wrong_data):

    """
    The function tests if the column type is correct in the input data.
    Examples
    --------
    >>> test_dataframe(generate_wrong_data)
    """

    df = generate_wrong_data
    y = df['y'].values
    df = df[['x1', 'x2', 'x3']]
    try:
        select_features.select_features(df, y, n_features=1)

    except AssertionError:
        pass


def test_input(generate_wrong_data_one):

    """
    The function tess if the input data type is correct or not.
    Examples
    --------
    >>> test_input(generate_wrong_data_one)
    """

    df, y = generate_wrong_data_one
    try:
        select_features.select_features(df, y, n_features=1)

    except AssertionError:
        pass


def test_columns():

    """
    The function tess if the input data has columns or not.
    Examples
    --------
    >>> test_input(generate_wrong_data_one)
    """

    df = pd.DataFrame(([1, 'x']))
    y = np.array([1, 2, 3])
    try:
        select_features.select_features(df, y, n_features=1)

    except AssertionError:
        pass
