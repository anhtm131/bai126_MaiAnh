import sys
import pandas as pd
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class StockAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Tải giao diện từ file UI
        uic.loadUi('MainWindow.ui', self)

        # Thiết lập biến dữ liệu
        self.df = None

        # Kết nối các nút nhấn với hàm xử lý
        self.loadButton.clicked.connect(self.load_file)
        self.filterCloseButton.clicked.connect(self.filter_by_close)
        self.filterLowButton.clicked.connect(self.filter_by_low)
        self.searchDateButton.clicked.connect(self.search_by_date)
        self.searchDatesButton.clicked.connect(self.search_by_multiple_dates)
        self.generateChartButton.clicked.connect(self.create_chart)

        # Kết nối menu
        self.actionOpen.triggered.connect(self.load_file)
        self.actionExit.triggered.connect(self.close)

        # Thiết lập biểu đồ trong tab phân tích nâng cao
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.chartLayout.addWidget(self.canvas)

        # Hiển thị ứng dụng
        self.show()

    def load_file(self):
        """Hàm tải file CSV"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file CSV", "", "CSV Files (*.csv)")

            if file_path:
                self.df = pd.read_csv(file_path)
                self.fileLabel.setText(f"File đã tải: {file_path.split('/')[-1]}")
                self.statusbar.showMessage("Đã tải dữ liệu thành công!")

                # Hiển thị dữ liệu lên tab tổng quan
                self.show_overview_data()

                QMessageBox.information(self, "Thành công", "Đã tải dữ liệu thành công!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải file: {str(e)}")

    def show_overview_data(self):
        """Hiển thị thông tin tổng quan và dữ liệu trên tab đầu tiên"""
        if self.df is not None:
            # Hiển thị thông tin thống kê
            stats = f"Tổng số bản ghi: {len(self.df)}\n"
            stats += f"Giá đóng cửa cao nhất: {self.df['Close'].max()}\n"
            stats += f"Giá đóng cửa thấp nhất: {self.df['Close'].min()}\n"
            stats += f"Giá trung bình: {self.df['Close'].mean():.2f}"
            self.statsLabel.setText(stats)

            # Hiển thị dữ liệu trong table view
            self.display_table_data(self.tableView, self.df)

    def display_table_data(self, table_widget, data):
        """Hiển thị dữ liệu dataframe lên table widget"""
        # Chuyển đổi từ table view sang table widget để dễ hiển thị
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(data.columns))
        table.setHorizontalHeaderLabels(data.columns)

        # Thêm dữ liệu vào bảng
        for row in range(len(data)):
            for col in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[row, col]))
                table.setItem(row, col, item)

        # Thay thế table view bằng table widget
        parent_layout = table_widget.parent().layout()
        parent_layout.replaceWidget(table_widget, table)
        table_widget.setParent(None)

        return table

    def filter_by_close(self):
        """Lọc dữ liệu theo khoảng giá Close"""
        if self.df is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tải dữ liệu trước!")
            return

        try:
            min_price = float(self.minCloseInput.text())
            max_price = float(self.maxCloseInput.text())

            if min_price > max_price:
                QMessageBox.warning(self, "Cảnh báo", "Giá tối thiểu phải nhỏ hơn giá tối đa!")
                return

            # Lọc dữ liệu
            filtered_df = self.df[(self.df['Close'] > min_price) & (self.df['Close'] < max_price)]

            # Hiển thị kết quả
            self.display_table_data(self.filterCloseTable, filtered_df)
            self.filterCloseStats.setText(f"Tổng số bản ghi phù hợp: {len(filtered_df)}")

        except ValueError:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập giá trị số hợp lệ!")

    def filter_by_low(self):
        """Trích lọc Date, High, Low với khoảng giá Low"""
        if self.df is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tải dữ liệu trước!")
            return

        try:
            min_price = float(self.minLowInput.text())
            max_price = float(self.maxLowInput.text())

            if min_price > max_price:
                QMessageBox.warning(self, "Cảnh báo", "Giá tối thiểu phải nhỏ hơn giá tối đa!")
                return

            # Lọc dữ liệu
            filtered_df = self.df[(self.df['Low'] >= min_price) & (self.df['Low'] <= max_price)]
            result_df = filtered_df[['Date', 'High', 'Low']]

            # Hiển thị kết quả
            self.display_table_data(self.filterLowTable, result_df)
            self.filterLowStats.setText(f"Tổng số bản ghi phù hợp: {len(result_df)}")

        except ValueError:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập giá trị số hợp lệ!")

    def search_by_date(self):
        """Xem thông tin chi tiết của một ngày giao dịch"""
        if self.df is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tải dữ liệu trước!")
            return

        date = self.dateInput.text()

        # Kiểm tra xem ngày có tồn tại trong dataframe không
        if date in self.df['Date'].values:
            date_data = self.df[self.df['Date'] == date]
            self.display_table_data(self.dateInfoTable, date_data)
        else:
            QMessageBox.information(self, "Thông báo", f"Không tìm thấy dữ liệu giao dịch cho ngày: {date}")

    def search_by_multiple_dates(self):
        """Lọc dữ liệu theo nhiều ngày"""
        if self.df is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tải dữ liệu trước!")
            return

        dates_input = self.datesInput.text()
        dates_list = [date.strip() for date in dates_input.split(',')]

        filtered_df = self.df[self.df['Date'].isin(dates_list)]

        # Hiển thị kết quả
        self.display_table_data(self.multiDateTable, filtered_df)

        # Hiển thị các ngày không tìm thấy
        found_dates = filtered_df['Date'].unique()
        not_found = [date for date in dates_list if date not in found_dates]

        info_text = f"Tổng số bản ghi phù hợp: {len(filtered_df)}"
        if not_found:
            info_text += "\nCác ngày không tìm thấy trong dữ liệu:\n"
            for date in not_found:
                info_text += f"- {date}\n"

        self.multiDateStats.setText(info_text)

    def create_chart(self):
        """Tạo biểu đồ phân tích nâng cao"""
        if self.df is None:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng tải dữ liệu trước!")
            return

        chart_type = self.chartTypeCombo.currentText()

        # Xóa biểu đồ cũ
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if chart_type == "Line Chart":
            ax.plot(self.df['Close'])
            ax.set_title('Biểu đồ giá đóng cửa')
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Giá')

        elif chart_type == "Candlestick Chart":
            # Vẽ đơn giản bằng cách sử dụng màu cho các cây nến tăng/giảm
            for i in range(len(self.df)):
                if self.df['Close'].iloc[i] >= self.df['Open'].iloc[i]:
                    color = 'green'  # Tăng
                else:
                    color = 'red'  # Giảm
                ax.bar(i, self.df['Close'].iloc[i] - self.df['Open'].iloc[i],
                       bottom=self.df['Open'].iloc[i], color=color, width=0.6)
                ax.plot([i, i], [self.df['Low'].iloc[i], self.df['High'].iloc[i]], color=color)

            ax.set_title('Biểu đồ nến')
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Giá')

        elif chart_type == "Volume Chart":
            ax.bar(range(len(self.df)), self.df['Volume'])
            ax.set_title('Biểu đồ khối lượng giao dịch')
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Khối lượng')

        elif chart_type == "Moving Average":
            # Tính MA20 và MA50
            ma20 = self.df['Close'].rolling(window=20).mean()
            ma50 = self.df['Close'].rolling(window=50).mean()

            ax.plot(self.df['Close'], label='Close')
            ax.plot(ma20, label='MA20')
            ax.plot(ma50, label='MA50')
            ax.set_title('Biểu đồ đường trung bình động')
            ax.set_xlabel('Ngày')
            ax.set_ylabel('Giá')
            ax.legend()

        # Cập nhật biểu đồ
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockAnalysisApp()
    sys.exit(app.exec())