import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox
import pandas as pd
from PIL import Image, ImageTk
from tkinter import StringVar

# Sample data
sample_data = []

def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.values.tolist()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
        return []

def button_click(button_name, app):
    if button_name == "Tìm kiếm":
        search_order()
    elif button_name == "Thêm đơn":
        add_order(app)
    elif button_name == "Sửa":
        edit_order(app)
    elif button_name == "Xóa":
        delete_order()

def create_don_hang_tab(notebook, app):
    global order_table, search_entry

    frame_order = ttk.Frame(notebook)
    notebook.add(frame_order, text="ĐƠN HÀNG")
    #insert image
   
    image = Image.open("icon/search.png")
    image = image.resize((20, 20), Image.LANCZOS)
    search_icon = ImageTk.PhotoImage(image)

    image2 = Image.open("icon/multiple.png")
    image2 = image2.resize((20, 20), Image.LANCZOS)
    multiple_icon = ImageTk.PhotoImage(image2)

    image3 = Image.open("icon/wrenchalt.png")
    image3 = image3.resize((20, 20), Image.LANCZOS)
    wrenchalt_icon = ImageTk.PhotoImage(image3)

    image4 = Image.open("icon/trash.png")
    image4 = image4.resize((20,20), Image.LANCZOS)
    trash_icon = ImageTk.PhotoImage(image4)
    
    search_value = StringVar()
    
    search_entry = ttk.Entry(frame_order, bootstyle="superhero", width=30, textvariable= search_value)
    search_entry.insert(0, "Tìm kiếm theo sản phẩm")
    search_entry.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    
    search_entry.bind("<FocusIn>", lambda event: search_entry.delete(0, 'end') if search_entry.get() == "Tìm kiếm theo sản phẩm" else None)

    search_button = ttk.Button(frame_order, text="Tìm kiếm", bootstyle="superhero", image=search_icon, compound=LEFT, cursor="hand2", command=lambda: button_click("Tìm kiếm", app))
    search_button.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    frame_order.search_icon = search_icon  # Keep a reference to the image to avoid garbage collection

    add_order_button = ttk.Button(frame_order, text="Thêm đơn", bootstyle="superhero", image=multiple_icon, compound=LEFT, command=lambda: button_click("Thêm đơn", app), cursor="hand2")
    add_order_button.grid(row=0, column=2, padx=5, pady=5, sticky=W)
    frame_order.multiple_icon = multiple_icon

    edit_order_button = ttk.Button(frame_order, text="Sửa", bootstyle="superhero", image=wrenchalt_icon, compound=LEFT, command=lambda: button_click("Sửa", app), cursor="hand2")
    edit_order_button.grid(row=0, column=3, padx=5, pady=5, sticky=W)
    frame_order.wrenchalt_icon = wrenchalt_icon

    delete_order_button = ttk.Button(frame_order, text="Xóa", bootstyle="superhero", image=trash_icon, compound=LEFT, command=delete_order, cursor="hand2")
    delete_order_button.grid(row=0, column=4, padx=5, pady=5, sticky=W)
    frame_order.trash_icon = trash_icon


    columns = ["ID Đơn Hàng", "ID Khách Hàng", "Ngày Đặt Hàng", "Danh Sách Sản Phẩm", "Tổng Giá Trị Đơn Hàng", "Trạng Thái Đơn Hàng", "Phương Thức Thanh Toán"]
    order_table = ttk.Treeview(frame_order, columns=columns, show="headings", bootstyle="superhero")
    order_table.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky="nsew")

    for col in columns:
        order_table.heading(col, text=col)
        if col == "Trạng Thái Đơn Hàng" or col == "Phương Thức Thanh Toán" or col == "Danh Sách Sản Phẩm":
            order_table.column(col, anchor='w')  # Align left for specific columns
        else:
            order_table.column(col, anchor='center')  # Center-align other columns

    refresh_order_table()  # Load initial data from sample_data

    frame_order.grid_rowconfigure(1, weight=1)
    frame_order.grid_columnconfigure(0, weight=1)

def refresh_order_table():
    for row in order_table.get_children():
        order_table.delete(row)
    for order in sample_data:
        order_table.insert("", "end", values=order)
    update_row_colors()

def update_row_colors():
    for index, item in enumerate(order_table.get_children()):
        if index % 2 == 0:
            order_table.item(item, tags=('evenrow',))
        else:
            order_table.item(item, tags=('oddrow',))

    order_table.tag_configure('evenrow', background='#f0f0f0')
    order_table.tag_configure('oddrow', background='white')

def search_order():
    search_value = search_entry.get().lower()
    
    # Clear the table to prepare for showing only matching results
    for row in order_table.get_children():
        order_table.delete(row)
    
    # Filter and display only the matching orders
    matched_orders = [order for order in sample_data if search_value in order[3].lower()]
    
    for order in matched_orders:
        order_table.insert("", "end", values=order)
    
    # Update row colors for consistency in appearance
    update_row_colors()


def add_order(app):
    add_window = ttk.Toplevel(app)
    add_window.title("Thêm Đơn Hàng")

    fields = ["ID Đơn Hàng", "ID Khách Hàng", "Ngày Đặt Hàng", "Danh Sách Sản Phẩm", "Tổng Giá Trị Đơn Hàng", "Trạng Thái Đơn Hàng", "Phương Thức Thanh Toán"]
    entries = {}

    for i, field in enumerate(fields):
        label = ttk.Label(add_window, text=field)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(add_window, bootstyle="superhero", width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry

    def submit_order():
        new_order = tuple(entries[field].get().strip() for field in fields)

        if any(not value for value in new_order):
            messagebox.showerror("Lỗi", "Vui lòng không để trống các trường.")
            return
        
        # Check for duplicate order ID
        if any(order[0] == new_order[0] for order in sample_data):
            messagebox.showerror("Lỗi", "ID đơn hàng đã tồn tại.")
            return
        
        sample_data.append(new_order)
        refresh_order_table()
        add_window.destroy()

    add_button = ttk.Button(add_window, text="Thêm", bootstyle="superhero", command=submit_order)
    add_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)

def edit_order(app):
    selected_item = order_table.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một đơn hàng để sửa.")
        return

    order_data = order_table.item(selected_item)["values"]
    edit_window = ttk.Toplevel(app)
    edit_window.title("Sửa Đơn Hàng")

    fields = ["ID Đơn Hàng", "ID Khách Hàng", "Ngày Đặt Hàng", "Danh Sách Sản Phẩm", "Tổng Giá Trị Đơn Hàng", "Trạng Thái Đơn Hàng", "Phương Thức Thanh Toán"]
    entries = {}

    for i, field in enumerate(fields):
        label = ttk.Label(edit_window, text=field)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(edit_window, bootstyle="superhero", width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, order_data[i])
        entries[field] = entry

    def submit_edit():
        updated_order = tuple(entries[field].get().strip() for field in fields)

        if any(not value for value in updated_order):
            messagebox.showerror("Lỗi", "Vui lòng không để trống các trường.")
            return

        sample_data[order_table.index(selected_item)] = updated_order
        order_table.item(selected_item, values=updated_order)
        edit_window.destroy()

    save_button = ttk.Button(edit_window, text="Lưu", bootstyle="superhero", command=submit_edit)
    save_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)

def delete_order():
    selected_items = order_table.selection()
    if selected_items:
        for selected_item in selected_items:
            index = order_table.index(selected_item)
            order_table.delete(selected_item)
            sample_data.pop(index)  # Xóa khỏi sample_data

        # Cập nhật lại bảng để đồng bộ màu sắc các hàng
        refresh_order_table()
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn hàng để xóa.")

sample_data.extend(read_csv('orders.csv'))
if __name__ == "__main__":
    pass  

