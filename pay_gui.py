import tkinter as tk
from tkinter import messagebox
import random

# 商品数据库（模拟）
PRODUCT_DB = {
    '1001': {'name': '矿泉水', 'price': 2.0},
    '1002': {'name': '泡面', 'price': 4.5},
    '1003': {'name': '牛奶', 'price': 6.0},
    '1004': {'name': '饼干', 'price': 3.5},
}

# 购物车模型
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product_id):
        if product_id in PRODUCT_DB:
            self.items.append(product_id)
        else:
            raise ValueError("无效的商品条码")

    def clear(self):
        self.items = []

    def total_price(self):
        return sum(PRODUCT_DB[pid]['price'] for pid in self.items)

    def get_summary(self):
        summary = {}
        for pid in self.items:
            summary[pid] = summary.get(pid, 0) + 1
        return summary

# GUI + 后端逻辑
class CashierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("收银系统模拟")
        self.cart = ShoppingCart()

        self.entry = tk.Entry(root, font=('Arial', 14))
        self.entry.pack(pady=5)

        self.add_btn = tk.Button(root, text="扫码录入", command=self.scan_product)
        self.add_btn.pack()

        self.cart_display = tk.Text(root, width=40, height=10)
        self.cart_display.pack()

        self.checkout_btn = tk.Button(root, text="结账并生成小票", command=self.checkout)
        self.checkout_btn.pack(pady=10)

    def scan_product(self):
        code = self.entry.get().strip()
        try:
            self.cart.add_item(code)
            self.entry.delete(0, tk.END)
            self.update_cart_display()
        except ValueError as e:
            messagebox.showerror("错误", str(e))

    def update_cart_display(self):
        self.cart_display.delete('1.0', tk.END)
        summary = self.cart.get_summary()
        lines = []
        for pid, count in summary.items():
            info = PRODUCT_DB[pid]
            lines.append(f"{info['name']} x{count} @ ￥{info['price']}")
        lines.append(f"\n总价：￥{self.cart.total_price():.2f}")
        self.cart_display.insert(tk.END, '\n'.join(lines))

    def checkout(self):
        if not self.cart.items:
            messagebox.showinfo("提示", "购物车为空")
            return

        total = self.cart.total_price()
        receipt_id = random.randint(100000, 999999)
        items = self.cart.get_summary()
        text = f"收据编号: #{receipt_id}\n"
        for pid, count in items.items():
            p = PRODUCT_DB[pid]
            text += f"{p['name']} x{count} = ￥{p['price']*count:.2f}\n"
        text += f"\n总计: ￥{total:.2f}\n支付方式: 微信/支付宝/现金\n感谢光临！"
        messagebox.showinfo("打印小票", text)
        self.cart.clear()
        self.update_cart_display()

if __name__ == '__main__':
    root = tk.Tk()
    app = CashierApp(root)
    root.mainloop()