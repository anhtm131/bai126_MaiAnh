import pandas as pd


def main():
    # Đọc tệp dữ liệu cổ phiếu
    try:
        df = pd.read_csv('TCB_2018_2020.csv')
        print("Đã tải dữ liệu thành công!")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy tệp TCB_2018_2020.csv.")
        return
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu: {e}")
        return

    while True:
        print("\n==== MENU PHÂN TÍCH DỮ LIỆU CỔ PHIẾU ====")
        print("1. Xuất toàn bộ dữ liệu TCB")
        print("2. Lọc dữ liệu theo khoảng giá Close")
        print("3. Trích lọc Date, High, Low với khoảng giá Low")
        print("4. Xem thông tin chi tiết của một ngày giao dịch")
        print("5. Lọc dữ liệu theo nhiều ngày")
        print("0. Thoát")

        choice = input("Nhập lựa chọn của bạn (0-5): ")

        if choice == '0':
            print("Chương trình đã kết thúc.")
            break
        elif choice == '1':
            hien_thi_toan_bo_du_lieu(df)
        elif choice == '2':
            loc_theo_khoang_gia_close(df)
        elif choice == '3':
            trich_loc_du_lieu_high_low(df)
        elif choice == '4':
            xem_thong_tin_ngay_cu_the(df)
        elif choice == '5':
            loc_theo_nhieu_ngay(df)
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


def hien_thi_toan_bo_du_lieu(df):
    """Xuất toàn bộ dữ liệu TCB"""
    print("\n==== TOÀN BỘ DỮ LIỆU TCB ====")
    print(df)
    print(f"Tổng số bản ghi: {len(df)}")


def loc_theo_khoang_gia_close(df):
    """Lọc dữ liệu theo khoảng giá Close"""
    try:
        x = float(input("Nhập giá Close tối thiểu (x): "))
        y = float(input("Nhập giá Close tối đa (y): "))

        if x > y:
            print("Lỗi: Giá tối thiểu phải nhỏ hơn giá tối đa.")
            return

        filtered_df = df[(df['Close'] > x) & (df['Close'] < y)]

        print(f"\n==== DỮ LIỆU ĐÃ LỌC (Giá Close từ {x} đến {y}) ====")
        print(filtered_df)
        print(f"Tổng số bản ghi phù hợp: {len(filtered_df)}")
    except ValueError:
        print("Lỗi: Vui lòng nhập giá trị số hợp lệ.")


def trich_loc_du_lieu_high_low(df):
    """Trích lọc Date, High, Low với khoảng giá Low"""
    try:
        x = float(input("Nhập giá Low tối thiểu (x): "))
        y = float(input("Nhập giá Low tối đa (y): "))

        if x > y:
            print("Lỗi: Giá tối thiểu phải nhỏ hơn giá tối đa.")
            return

        filtered_df = df[(df['Low'] >= x) & (df['Low'] <= y)]
        result_df = filtered_df[['Date', 'High', 'Low']]

        print(f"\n==== DỮ LIỆU ĐÃ TRÍCH LỌC (Giá Low từ {x} đến {y}) ====")
        print(result_df)
        print(f"Tổng số bản ghi phù hợp: {len(result_df)}")
    except ValueError:
        print("Lỗi: Vui lòng nhập giá trị số hợp lệ.")


def xem_thong_tin_ngay_cu_the(df):
    """Xem thông tin chi tiết của một ngày giao dịch"""
    date = input("Nhập ngày giao dịch (YYYY-MM-DD): ")

    # Kiểm tra xem ngày có tồn tại trong dataframe không
    if date in df['Date'].values:
        date_data = df[df['Date'] == date]
        print(f"\n==== THÔNG TIN GIAO DỊCH NGÀY {date} ====")
        print(date_data)
    else:
        print(f"Không tìm thấy dữ liệu giao dịch cho ngày: {date}")


def loc_theo_nhieu_ngay(df):
    """Lọc dữ liệu theo nhiều ngày"""
    print("Nhập danh sách các ngày (YYYY-MM-DD), cách nhau bằng dấu phẩy:")
    dates_input = input("Các ngày: ")

    dates_list = [date.strip() for date in dates_input.split(',')]

    filtered_df = df[df['Date'].isin(dates_list)]

    print(f"\n==== DỮ LIỆU ĐÃ LỌC THEO CÁC NGÀY ĐƯỢC CHỌN ====")
    print(filtered_df)
    print(f"Tổng số bản ghi phù hợp: {len(filtered_df)}")

    # Hiển thị những ngày không tìm thấy
    found_dates = filtered_df['Date'].unique()
    not_found = [date for date in dates_list if date not in found_dates]
    if not_found:
        print("\nCác ngày không tìm thấy trong dữ liệu:")
        for date in not_found:
            print(f"- {date}")


if __name__ == "__main__":
    main()