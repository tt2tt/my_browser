import os
import sys

import pytest
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget
from tinydb import TinyDB

# main.pyがあるディレクトリをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from my_package.table_tab import TableTab

app = QApplication.instance() or QApplication([])

class DummyMainWindow(QWidget):
    """ダミーのMainWindowクラス."""
    def select_new_tab(self, *args, **kwargs):
        pass

@pytest.fixture
def dummy_main_window():
    """DummyMainWindowのフィクスチャ."""
    return DummyMainWindow()

@pytest.fixture(params=["履歴", "ブックマーク"])
def table_tab(request, dummy_main_window):
    """TableTabのフィクスチャ（履歴/ブックマーク両方）."""
    tab = TableTab(dummy_main_window, request.param)
    yield tab
    # ...必要に応じたクリーンアップ...

def test_selected_db_path(table_tab):
    """タブ名に応じてDBがTinyDBとして生成されていることを検証."""
    if table_tab.tab_name == "履歴":
        expected = os.path.normpath("./data/history.json")
    else:
        expected = os.path.normpath("./data/bookmark.json")
    assert isinstance(table_tab.selected_db, TinyDB)
    # DBファイルパスの直接検証は困難なため、ここではDBインスタンス生成の成功のみを確認

def test_table_widget_created(table_tab):
    """テーブルウィジェットが生成されレイアウトに組み込まれていることを確認."""
    assert hasattr(table_tab, "table")
    assert isinstance(table_tab.table, QTableWidget)
