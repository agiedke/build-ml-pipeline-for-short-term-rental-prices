import pandas as pd
import numpy as np
import scipy.stats


def test_column_names(data):
    """
    Confirm that expected columns exist in the data in the expected order.
    """

    expected_colums = [
        "id",
        "name",
        "host_id",
        "host_name",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude",
        "room_type",
        "price",
        "minimum_nights",
        "number_of_reviews",
        "last_review",
        "reviews_per_month",
        "calculated_host_listings_count",
        "availability_365",
    ]

    these_columns = data.columns.values

    # This also enforces the same order
    assert list(expected_colums) == list(these_columns), (
        f"Present columns in dataframe: {list(these_columns)}, Expected columns: {list(expected_colums)}"
    )


def test_neighborhood_names(data):
    """
    Confirm that the column "neighbourhood_group" contains the expected categories.
    """

    known_names = ["Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"]

    neigh = set(data['neighbourhood_group'].unique())

    # Unordered check
    assert set(known_names) == set(neigh)


def test_proper_boundaries(data: pd.DataFrame):
    """
    Test proper longitude and latitude boundaries for properties in and around NYC
    """
    idx = data['longitude'].between(-74.25, -73.50) & data['latitude'].between(40.5, 41.2)

    assert np.sum(~idx) == 0


def test_similar_neigh_distrib(data: pd.DataFrame, ref_data: pd.DataFrame, kl_threshold: float):
    """
    Apply a threshold on the KL divergence to detect if the distribution of the new data is
    significantly different than that of the reference dataset
    """
    dist1 = data['neighbourhood_group'].value_counts().sort_index()
    dist2 = ref_data['neighbourhood_group'].value_counts().sort_index()

    assert scipy.stats.entropy(dist1, dist2, base=2) < kl_threshold


########################################################
# Implement here test_row_count and test_price_range   #
########################################################


def test_row_count(data):
    """
    Confirm that data does not exceed the expected number of rows.
    """
    max_row_nr = 1000000

    assert 15000 < data.shape[0] < max_row_nr


def test_price_range(data, min_price, max_price):
    """
    Confirm that price lies in the expected range.
    """
    col_name = "price"

    assert data["price"].between(min_price,max_price).all(), (
            f"Column {col_name} failed the test. Should be between {min_price} and {max_price}, "
            f"instead min={data[col_name].min()} and max={data[col_name].max()}"
    )