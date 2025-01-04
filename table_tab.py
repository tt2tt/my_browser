from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from tinydb import TinyDB, Query

class TableTab(QWidget):
    def __init__(self):
        super().__init__()
        # DB設定（日本語をそのまま保存）
        self.history = TinyDB("./data/history.json")

        self.layout = QVBoxLayout()

        # テーブルウィジェットを作成
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["日時", "ページ", "URL"])

        # テーブルの列幅をウィンドウサイズに合わせて調整
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # テーブルを更新
        self.update_table()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_table(self):
        """テーブルを更新"""
        self.table.setRowCount(0)

        for i, record in enumerate(self.history.all()):
            self.table.insertRow(i)

            # 各セルにデータを設定
            self.table.setItem(i, 0, QTableWidgetItem(record.get("datetime", "")))
            self.table.setItem(i, 1, QTableWidgetItem(record.get("title", "")))
            self.table.setItem(i, 2, QTableWidgetItem(record.get("url", "")))
