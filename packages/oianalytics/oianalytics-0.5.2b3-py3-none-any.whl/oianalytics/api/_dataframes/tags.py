from typing import Optional

import pandas as pd

from .. import _credentials
from .. import endpoints
from ..utils import expand_dataframe_column


__all__ = [
    "get_tag_keys",
    "get_single_tag_key",
    "get_tag_values",
    "get_single_tag_value",
]


def get_tag_keys(
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List all the tag keys, ordered by position.

    Parameters
    ----------
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
        A pandas DataFrame containing tag keys indexed by tag key ID.
    """

    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.tags.get_tag_keys(api_credentials)

    if len(response) > 0:
        df = pd.DataFrame(response)
        df.set_index("id", inplace=True)
    else:
        df = pd.DataFrame(columns=["key", "position", "usedForAccessControl"])
        df.index.name = "id"
        df = df.astype({"key": str, "position": int, "usedForAccessControl": bool})

    # Output
    return df


def get_single_tag_key(
    tag_key_id: str,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    Retrieve the detail of a specific tag key with its ID..

    Parameters
    ----------
    tag_key_id : str
        The OIAnalytics ID of the tag key.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
        A pandas DataFrame containing one row, indexed by the tag key ID, containing key, position and usedForAccessControl.
    """

    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.tags.get_single_tag_key(
        tag_key_id=tag_key_id, api_credentials=api_credentials
    )

    columns = list(response.keys())
    columns.remove("id")
    df = pd.DataFrame(
        data=[[response[key] for key in columns]],
        index=[response["id"]],
        columns=columns,
    )
    df.index.name = "id"

    # Output
    return df


def get_tag_values(
    tag_key_id: str,
    expand_tag_key: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.DataFrame:
    """
    List all the tag values of a given tag key.

    Parameters
    ----------
    tag_key_id : str
        The OIAnalytics ID of the tag key.
    expand_tag_key : bool, default True
        Whether to split the column 'tagKey' into multiple columns.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
        A pandas DataFrame, indexed by tag value ID, containing tag values.
    """

    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.tags.get_tag_values(
        tag_key_id=tag_key_id,
        api_credentials=api_credentials,
    )

    df = pd.DataFrame(response["content"])
    if len(df) > 0:
        df.set_index("id", inplace=True)
        if expand_tag_key:
            df = expand_dataframe_column(
                df=df,
                col="tagKey",
            )

    # Output
    return df


def get_single_tag_value(
    tag_key_id: str,
    tag_value_id: str,
    expand_tag_key: bool = True,
    api_credentials: Optional[_credentials.OIAnalyticsAPICredentials] = None,
) -> pd.Series:
    """
    Retrieve the detail of a specific tag value with its tag-key ID and tag-value-ID.

    Parameters
    ----------
    tag_key_id : str
        The OIAnalytics ID of the tag key.
    tag_value_id : str
        The OIAnalytics ID of the tag value.
    expand_tag_key : bool
        Whether to split the column 'tagKey' into multiple columns.
    api_credentials : OIAnalyticsAPICredentials, optional
        The credentials to use to query the API. If None, previously set default credentials are used.

    Returns
    -------
    pd.Series
        A pandas Series containing details of the tag value.
    """
    if api_credentials is None:
        api_credentials = _credentials.get_default_oianalytics_credentials()

    response = endpoints.tags.get_single_tag_value(
        tag_key_id=tag_key_id,
        tag_value_id=tag_value_id,
        api_credentials=api_credentials,
    )

    df = pd.DataFrame([response])
    if len(df) > 0:
        df.set_index("id", inplace=True)
        if expand_tag_key:
            df = expand_dataframe_column(
                df=df,
                col="tagKey",
            )

    ser = df.squeeze()

    # Output
    return ser
