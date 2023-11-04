from __future__ import annotations

from collections.abc import Iterable

from polars import DataFrame
from polars.testing import assert_frame_equal
from polars.type_aliases import IntoExpr, PolarsDataType, SchemaDict

from utilities.typing import SequenceStrs


def check_dataframe(
    df: DataFrame,
    /,
    *,
    columns: SequenceStrs | None = None,
    dtypes: list[PolarsDataType] | None = None,
    height: int | None = None,
    schema: SchemaDict | None = None,
    shape: tuple[int, int] | None = None,
    sorted: IntoExpr | Iterable[IntoExpr] | None = None,  # noqa: A002
    unique: IntoExpr | Iterable[IntoExpr] | None = None,
    width: int | None = None,
) -> None:
    if (columns is not None) and (df.columns != list(columns)):
        msg = f"{df=}, {columns=}"
        raise DataFrameColumnsError(msg)
    if (dtypes is not None) and (df.dtypes != dtypes):
        msg = f"{df=}, {dtypes=}"
        raise DataFrameDTypesError(msg)
    if (height is not None) and (df.height != height):
        msg = f"{df=}"
        raise DataFrameHeightError(msg)
    if (schema is not None) and (df.schema != schema):
        set_act, set_exp = map(set, [df.schema, schema])
        extra = set_act - set_exp
        missing = set_exp - set_act
        differ = {
            col: (left, right)
            for col in set_act & set_exp
            if (left := df.schema[col]) != (right := schema[col])
        }
        msg = f"{df=}, {extra=}, {missing=}, {differ=}"
        raise DataFrameSchemaError(msg)
    if (shape is not None) and (df.shape != shape):
        msg = f"{df=}"
        raise DataFrameShapeError(msg)
    if sorted is not None:
        df_sorted = df.sort(sorted)
        try:
            assert_frame_equal(df, df_sorted)
        except AssertionError:
            msg = f"{df=}, {sorted=}"
            raise DataFrameSortedError(msg) from None
    if (unique is not None) and df.select(unique).is_duplicated().any():
        msg = f"{df=}, {unique=}"
        raise DataFrameUniqueError(msg)
    if (width is not None) and (df.width != width):
        msg = f"{df=}"
        raise DataFrameWidthError(msg)


class DataFrameColumnsError(ValueError):
    """Raised when a DataFrame has the incorrect columns."""


class DataFrameDTypesError(ValueError):
    """Raised when a DataFrame has the incorrect dtypes."""


class DataFrameHeightError(ValueError):
    """Raised when a DataFrame has the incorrect height."""


class DataFrameSchemaError(ValueError):
    """Raised when a DataFrame has the incorrect schema."""


class DataFrameShapeError(ValueError):
    """Raised when a DataFrame has the incorrect shape."""


class DataFrameSortedError(ValueError):
    """Raised when a DataFrame has non-sorted values."""


class DataFrameUniqueError(ValueError):
    """Raised when a DataFrame has non-unique values."""


class DataFrameWidthError(ValueError):
    """Raised when a DataFrame has the incorrect width."""
