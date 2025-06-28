import tkinter as tk
import threading
import time

# === DSL 内容 ===
dsl = {
    "system": "AutoDrivingSystem",
    "modules": ["Perception", "Planning", "Control"],
    "usecases": [
        {
            "name": "车辆自主驾驶",
            "description": "系统实现车辆的自主驾驶，在不需要人为干预的情况下沿预定路径行驶。",
            "actors": ["用户", "系统"],
            "module": "Planning",
            "includes": [],
            "extends": [],
            "triggers": ["车辆启动后设定目的地", "用户未干预驾驶"],
            "results": ["车辆按照预定路径行驶并到达目的地"]
        },
        {
            "name": "检测障碍物",
            "description": "系统识别车辆周围的障碍物并做出相应决策以避免碰撞。",
            "actors": ["传感器", "系统"],
            "module": "Perception",
            "includes": [],
            "extends": [],
            "triggers": ["前方出现障碍物", "系统收到传感器警报"],
            "results": ["系统调整行驶路径或执行刹车以避免碰撞"]
        },
        {
            "name": "识别交通信号灯",
            "description": "系统识别道路上的交通信号灯状态，并根据灯色变化调整行驶策略。",
            "actors": ["摄像头", "系统"],
            "module": "Perception",
            "includes": [],
            "extends": [],
            "triggers": ["接近交通信号灯", "摄像头捕捉到信号灯颜色变化"],
            "results": ["系统调整车辆速度或停下以遵循交通信号规定"]
        },
        {
            "name": "保持车道行驶",
            "description": "系统确保车辆始终在车道内行驶，避免偏离或跨越车道。",
            "actors": ["传感器", "系统"],
            "module": "Control",
            "includes": [],
            "extends": [],
            "triggers": ["传感器实时监测到车辆偏离车道边界"],
            "results": ["系统调整方向盘以使车辆保持在车道中间行驶"]
        },
        {
            "name": "自动刹车",
            "description": "系统在遇到紧急情况时自动刹车以保护车辆和乘客安全。",
            "actors": ["传感器", "系统"],
            "module": "Control",
            "includes": [],
            "extends": [],
            "triggers": ["前方突然出现障碍物", "传感器检测到紧急情况"],
            "results": ["车辆立即执行刹车动作以尽快停止并避免碰撞"]
        }
    ]
}

# === GUI 仿真系统 ===
class DSLDrivenAutoDriveGUI:
    def __init__(self, root, dsl):
        self.dsl = dsl
        self.root = root
        root.title("DSL 驱动自动驾驶系统演示")
        root.geometry("800x500")

        self.canvas = tk.Canvas(root, width=780, height=250, bg="white")
        self.canvas.pack(pady=10)

        self.text_log = tk.Text(root, height=12, wrap=tk.WORD, font=("Arial", 10))
        self.text_log.pack(fill=tk.BOTH, padx=10)

        self.button = tk.Button(root, text="🚗 启动自动驾驶", command=self.start_simulation)
        self.button.pack(pady=10)

        self.vehicle = self.canvas.create_rectangle(50, 110, 100, 160, fill="blue")
        self.running = False

    def log(self, msg):
        self.text_log.insert(tk.END, msg + "\n")
        self.text_log.see(tk.END)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.text_log.delete(1.0, tk.END)
            threading.Thread(target=self.run_simulation).start()

    def move_vehicle(self, dx=10, times=10, delay=0.05):
        for _ in range(times):
            self.canvas.move(self.vehicle, dx, 0)
            self.root.update()
            time.sleep(delay)

    def run_simulation(self):
        self.log("🚗 正在启动自动驾驶系统...")
        time.sleep(1)
        for usecase in self.dsl["usecases"]:
            if not self.running:
                break
            self.log(f"\n📋 用例：{usecase['name']}")
            self.log("📡 模块：" + usecase.get("module", "未定义"))
            self.log("🔔 触发条件：" + "；".join(usecase.get("triggers", [])))
            self.move_vehicle()
            self.log("✅ 执行结果：" + "；".join(usecase.get("results", [])))
            time.sleep(1.5)
        self.log("\n🏁 到达目的地，驾驶结束。")
        self.running = False

# === 启动主程序 ===
if __name__ == "__main__":
    root = tk.Tk()
    app = DSLDrivenAutoDriveGUI(root, dsl)
    root.mainloop()