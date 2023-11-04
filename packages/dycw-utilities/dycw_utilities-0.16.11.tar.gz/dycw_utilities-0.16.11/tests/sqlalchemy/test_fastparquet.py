from __future__ import annotations

from pathlib import Path

from hypothesis import given
from hypothesis.strategies import DataObject, data, integers, none
from hypothesis_sqlalchemy.sample import table_records_lists
from sqlalchemy import Column, Engine, Integer, select
from sqlalchemy.orm import declarative_base

from utilities.fastparquet import get_dtypes
from utilities.hypothesis import sqlite_engines, temp_paths
from utilities.pandas import Int64
from utilities.sqlalchemy import (
    ensure_tables_created,
    get_table,
    insert_items,
    select_to_parquet,
)


class TestSelectToParquet:
    @given(
        data=data(),
        engine=sqlite_engines(),
        root=temp_paths(),
        stream=integers(1, 10) | none(),
    )
    def test_streamed_dataframe(
        self, *, data: DataObject, engine: Engine, root: Path, stream: int | None
    ) -> None:
        class Example(declarative_base()):  # does not work with a core table
            __tablename__ = "example"
            Id = Column(Integer, primary_key=True)

        rows = data.draw(table_records_lists(get_table(Example), min_size=1))
        ensure_tables_created(Example, engine)
        insert_items([(rows, Example)], engine)
        sel = select(Example.Id)
        select_to_parquet(sel, engine, path := root.joinpath("df.parq"), stream=stream)
        dtypes = get_dtypes(path)
        assert dtypes == {"Id": Int64}
