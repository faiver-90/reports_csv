import logging

import pytest

from src.reports.io_operation import _open_text, read_csv_files


def test_open_text(tmp_path):
    f = tmp_path / "t.txt"
    f.write_text("hello", encoding="utf-8")
    with _open_text(f) as fp:
        assert fp.read() == "hello"


@pytest.mark.parametrize(
    "content,expected_len",
    [
        ("position,performance\nA,1\nB,2", 2),
        ("position,performance\nX,10", 1),
        ("position,performance\n", 0),
    ],
)
def test_read_csv_variants(tmp_path, content, expected_len):
    p = tmp_path / "ok.csv"
    p.write_text(content, encoding="utf-8")
    assert len(read_csv_files([str(p)])) == expected_len


@pytest.mark.parametrize(
    "content",
    [
        "a,b\n1\n2,3,4",  # разное число колонок
        "a,b,c\n1,2",  # не хватает столбцов
    ],
)
def test_read_csv_bad_columns(tmp_path, caplog, content):
    caplog.set_level(logging.ERROR)
    p = tmp_path / "bad.csv"
    p.write_text(content, encoding="utf-8")

    rows = read_csv_files([str(p)])
    assert rows == []
    assert "Bad CSV" in caplog.text or "inconsistent" in caplog.text


def test_read_csv_encode_error(tmp_path, caplog):
    caplog.set_level(logging.ERROR)
    f = tmp_path / "bad.bin"
    f.write_bytes(b"\xff\xff\xff")
    assert read_csv_files([str(f)]) == []
    assert "Bad encoding" in caplog.text
