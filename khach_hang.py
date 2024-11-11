import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.messagebox as messagebox  # Import messagebox từ tkinter
import pandas as pd 
from PIL import Image, ImageTk
from tkinter import StringVar
import csv
from setting import load_settings  # Import thêm load_settings
import tkinter as tk

sample_customers = []
def read_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.values.tolist()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
        return []
def save_to_csv(filename):
    # Mở file ở chế độ ghi (write mode)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Ghi tiêu đề cột nếu cần
        header = ["ID Khách Hàng", "Tên Khách Hàng", "Địa Chỉ", "Số Điện Thoại", "Email", "Lịch Sử Mua Hàng"]  # Thay đổi theo các cột của bạn
        writer.writerow(header)
        
        # Ghi từng dòng dữ liệu từ sample_products
        for customer in sample_customers:
            writer.writerow(customer)

def button_click(button_name, app):
    if button_name == "Tìm kiếm":
        search_customer(app)
    elif button_name == "Thêm khách hàng":
        add_customer(app)
    elif button_name == "Mới nhất":
        latest_customers()
    elif button_name == "Sửa":
        edit_customer(app)

def latest_customers():
    for row in customer_table.get_children():
        customer_table.delete(row)

    for row in sample_customers:
        customer_table.insert("", "end", values=row)
    update_row_colors()
def search_customer(app):
    search_value = search_entry.get().lower()
    for row in customer_table.get_children():
        customer_table.delete(row)

    for row in sample_customers:
        if search_value in row[1].lower():
            customer_table.insert("", "end", values=row)

        update_row_colors()
def add_customer(app):
    add_window = ttk.Toplevel(app)
    add_window.title("Thêm Khách Hàng")

    fields = ["ID Khách Hàng", "Tên Khách Hàng", "Địa Chỉ", "Số Điện Thoại", "Email", "Lịch Sử Mua Hàng"]
    entries = {}

    for i, field in enumerate(fields):
        label = ttk.Label(add_window, text=field)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(add_window, bootstyle="superhero", width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[field] = entry
        

    def submit_customer():
        new_customer = tuple(entries[field].get().strip() for field in fields)
        try:
            if any(not value for value in new_customer):
                raise ValueError("Vui lòng không để trống các trường.")

            customer_table.insert("", "end", values=new_customer)
            sample_customers.append(new_customer)
            refresh_customers_table()
            save_to_csv('customers.csv')
            add_window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    add_button = ttk.Button(add_window, text="Thêm", bootstyle="superhero", command=submit_customer)
    add_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)

def refresh_customers_table():
    for row in customer_table.get_children():
        customer_table.delete(row)
    for product in sample_customers:
        customer_table.insert("", "end", values=product)
    update_row_colors()

def update_row_colors():
    # Tải cài đặt từ file
    current_settings = load_settings()
    theme = current_settings.get('theme', 'minty')  # Mặc định là 'minty' nếu không có theme nào

    # Cấu hình màu sắc dựa trên theme
    theme_colors = {
        "minty": {"foreground": "#000000", "background_even": "#e8f5e9", "background_odd": "#ffffff"},
        "flatly": {"foreground": "#2c3e50", "background_even": "#f8f9fa", "background_odd": "#ffffff"},
        "darkly": {"foreground": "#ffffff", "background_even": "#343a40", "background_odd": "#23272b"},
        "pulse": {"foreground": "#495057", "background_even": "#e1e8f0", "background_odd": "#ffffff"},
        "solar": {"foreground": "#657b83", "background_even": "#fdf6e3", "background_odd": "#ffffff"},
    }

    # Lấy màu chữ và nền theo theme
    colors = theme_colors.get(theme, theme_colors["minty"])
    font_color = colors["foreground"]
    background_even = colors["background_even"]
    background_odd = colors["background_odd"]

    # Tạo tag cho font với font cố định là 'superhero' và màu chữ thay đổi theo theme
    customer_table.tag_configure("custom_font1", font=('superhero', 10), background=background_even, foreground=font_color)
    customer_table.tag_configure("custom_font2", font=('superhero', 10), background=background_odd, foreground=font_color)

    # Áp dụng các tag xen kẽ để tạo màu nền cho các dòng
    for index, item in enumerate(customer_table.get_children()):
        if index % 2 == 0:
            customer_table.item(item, tags=('custom_font1',))
        else:
            customer_table.item(item, tags=('custom_font2',))

def edit_customer(app):
    selected_item = customer_table.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một khách hàng để sửa.")
        return

    customer_data = customer_table.item(selected_item)["values"]
    edit_window = ttk.Toplevel(app)
    edit_window.title("Sửa Thông Tin Khách Hàng")

    fields = ["ID Khách Hàng", "Tên Khách Hàng", "Địa Chỉ", "Số Điện Thoại", "Email", "Lịch Sử Mua Hàng"]
    entries = {}

    for i, field in enumerate(fields):
        label = ttk.Label(edit_window, text=field)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(edit_window, bootstyle="superhero", width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, customer_data[i])
        entries[field] = entry

    def submit_edit():
        # Làm mới bảng và lưu thay đổi vào CSV
         # Lấy dữ liệu mới từ các trường nhập liệu
        updated_customer = tuple(entries[field].get().strip() for field in fields)
        
        # Kiểm tra dữ liệu có trống không
        if any(not value for value in updated_customer):
            messagebox.showerror("Lỗi", "Vui lòng không để trống các trường.")
            return

        sample_customers[customer_table.index(selected_item)] = updated_customer
        customer_table.item(selected_item, values=updated_customer)
        
        # Cập nhật dữ liệu trong `sample_products` để đồng bộ với CSV
        product_id = updated_customer[0]
        for index, existing_product in enumerate(sample_customers):
            if existing_product[0] == product_id:
                sample_customers[index] = updated_customer
                break
        
       
        save_to_csv('customers.csv')
        refresh_customers_table() 
        edit_window.destroy()
    # Nút cập nhật để lưu thay đổi
    update_button = ttk.Button(edit_window, text="Xác nhận", bootstyle="superhero", command=submit_edit)
    update_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10)

def delete_customer():
    selected_item = customer_table.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm cần xóa.")
        return

    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?")
    if confirm:
        selected_index = customer_table.index(selected_item)
        del sample_customers[selected_index]

        refresh_customers_table()
        save_to_csv('customers.csv')
def create_khach_hang_tab(notebook, app):
    global search_entry, customer_table

    frame_khach_hang = ttk.Frame(notebook)
    notebook.add(frame_khach_hang, text="KHÁCH HÀNG", padding=(20,20))
    
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
    
    image5 = Image.open("icon/arrowup.png")
    image5 = image5.resize((20,20), Image.LANCZOS)
    arrowup_icon = ImageTk.PhotoImage(image5)
    
    search_value = StringVar()

    search_entry = ttk.Entry(frame_khach_hang, bootstyle="superhero", width=30, textvariable=search_value)
    search_entry.insert(0, "Tìm kiếm theo tên khách hàng")
    search_entry.config(foreground="grey")
    search_entry.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    
    def on_focus_in(event):
        if  search_entry.get() == "Tìm kiếm theo tên khách hàng":
            search_entry.delete(0, "end")  # Clear the placeholder text
            search_entry.config(foreground="black")

    def on_focus_out(event):
        if search_entry.get() == "":  # If empty, reset placeholder
            search_entry.insert(0, "Tìm kiếm theo tên khách hàng")
            search_entry.config(foreground="grey")

    # Bind focus events to the entry widget
    search_entry.bind("<FocusIn>", on_focus_in)
    search_entry.bind("<FocusOut>", on_focus_out)

    notebook.after(100, lambda: search_entry.focus_set())  # Set focus after window is initialized
    # Bind Enter key to perform the search

    search_button = ttk.Button(frame_khach_hang, text="Tìm kiếm", bootstyle="superhero", image=search_icon, compound=LEFT, cursor="hand2", command=lambda: button_click("Tìm kiếm", app))
    search_button.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    frame_khach_hang.search_icon = search_icon  # Keep reference to avoid garbage collection

    add_customer_button = ttk.Button(frame_khach_hang, text="Thêm khách hàng", bootstyle="superhero",image=multiple_icon,compound=LEFT,cursor="hand2",command=lambda: button_click("Thêm khách hàng", app))
    add_customer_button.grid(row=0, column=2, padx=5, pady=5, sticky=W)
    frame_khach_hang.multiple_icon = multiple_icon
 
    edit_button = ttk.Button(frame_khach_hang, text="Sửa", bootstyle="superhero",image= wrenchalt_icon,compound=LEFT,cursor="hand2",command=lambda: button_click("Sửa", app))
    edit_button.grid(row=0, column=3, padx=5, pady=5, sticky=W)
    frame_khach_hang.wrenchalt_icon = wrenchalt_icon

    delete_button = ttk.Button(frame_khach_hang, text="Xóa", bootstyle="superhero",image=trash_icon ,compound=LEFT,cursor="hand2", command=delete_customer)
    delete_button.grid(row=0, column=4, padx=5, pady=5, sticky=W)
    frame_khach_hang.trash_icon = trash_icon
    
    # latest_button = ttk.Button(frame_khach_hang, text="Mới nhất", bootstyle="superhero",image=arrowup_icon ,compound=LEFT,cursor ="hand2",command=lambda: button_click("Mới nhất", app))
    # latest_button.grid(row=0, column=5, padx=5, pady=5, sticky=W)
    # frame_khach_hang.arrowup_icon = arrowup_icon
    
    columns = ["ID Khách Hàng", "Tên Khách Hàng", "Địa Chỉ", "Số Điện Thoại", "Email", "Lịch Sử Mua Hàng"]

    customer_table = ttk.Treeview(frame_khach_hang, columns=columns, show="headings", bootstyle="superhero")
    customer_table.grid(row=2, column=0, columnspan=len(columns), padx=5, pady=5, sticky="nsew")

    for col in columns:
        customer_table.heading(col, text=col)
        customer_table.column(col, width=100)
        if col == "ID Khách Hàng":
            customer_table.column(col,anchor='center') 
        else:
            customer_table.column(col, anchor='w')
    for row in sample_customers:
        customer_table.insert("", "end", values=row)

    frame_khach_hang.grid_rowconfigure(2, weight=1)
    frame_khach_hang.grid_columnconfigure(0, weight=1)

    refresh_customers_table()
sample_customers.extend(read_csv('customers.csv'))

