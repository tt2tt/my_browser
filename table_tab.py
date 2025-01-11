from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QPushButton
from tinydb import TinyDB, Query

class TableTab(QWidget):
    def __init__(self, main_window, tab_name):
        super().__init__()
        # メインウインドウ
        self.main_window = main_window

        # DB設定（日本語をそのまま保存）
        if tab_name == "履歴":
            self.selected_db = TinyDB("./data/history.json")
        elif tab_name == "ブックマーク":
            self.selected_db = TinyDB("./data/bookmark.json")

        self.layout = QVBoxLayout()

        # テーブルウィジェットを作成
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["日時", "ページ", "URL", "遷移", "削除"])

        # テーブルの列幅をウィンドウサイズに合わせて調整
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        # テーブルを更新
        self.create_table()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def create_table(self):
        """テーブルを作成"""
        self.table.setRowCount(0)

        for i, record in enumerate(self.selected_db.all()):
            self.table.insertRow(i)

            # 各セルにデータを設定
            self.table.setItem(i, 0, QTableWidgetItem(record.get("datetime", "")))
            self.table.setItem(i, 1, QTableWidgetItem(record.get("title", "")))
            self.table.setItem(i, 2, QTableWidgetItem(record.get("url", "")))
            self.table.setItem(i, 3, QTableWidgetItem("遷移"))
            self.table.setItem(i, 4, QTableWidgetItem("削除"))

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_cell_clicked)

    def update_table(self):
        """テーブルを更新"""
        self.table.setRowCount(0)

        for i, record in enumerate(self.selected_db.all()):
            self.table.insertRow(i)

            # 各セルにデータを設定
            self.table.setItem(i, 0, QTableWidgetItem(record.get("datetime", "")))
            self.table.setItem(i, 1, QTableWidgetItem(record.get("title", "")))
            self.table.setItem(i, 2, QTableWidgetItem(record.get("url", "")))
            self.table.setItem(i, 3, QTableWidgetItem("遷移"))
            self.table.setItem(i, 4, QTableWidgetItem("削除"))

    # セルクリック時の処理
    def on_cell_clicked(self, row, column):
        if column == 3:
            self.main_window.add_new_tab(url = self.selected_db.all()[row]["url"])
        if column == 4:
            self.delete_record(self.selected_db.all()[row].doc_id)

    def delete_record(self, id):
        """指定されたIDのデータを削除"""
        self.selected_db.remove(doc_ids=[int(id)])
        self.update_table()
