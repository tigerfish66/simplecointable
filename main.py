# path/filename: main.py
import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
import time

class CryptoDataFetcher(QThread):
    dataFetched = pyqtSignal(object)

    def run(self):
        while True:
            try:
                response = requests.get("https://api.coingecko.com/api/v3/coins/markets", params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 10,
                    "page": 1,
                    "sparkline": False,
                    "price_change_percentage": "24h"
                })
                data = response.json()
                self.dataFetched.emit(data)
                time.sleep(60)  # Update every minute
            except Exception as e:
                print(e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top 10 Cryptocurrencies")
        self.setGeometry(100, 100, 640, 480)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)  # Name and Price
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Price (USD)"])

        self.cryptoFetcher = CryptoDataFetcher()
        self.cryptoFetcher.dataFetched.connect(self.updateTable)
        self.cryptoFetcher.start()

    def updateTable(self, data):
        for i, coin in enumerate(data):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(coin['name']))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(coin['current_price'])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
