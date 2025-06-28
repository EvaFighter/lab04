from openai import OpenAI
from openai.types.chat import ChatCompletion

# 替换为你自己的 BASE_URL 和 API_KEY
BASE_URL = "https://api.chatfire.cn/v1"
API_KEY = "sk-"

# 初始化客户端
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# 调用模型进行需求建模
completion: ChatCompletion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "你是一个专业的需求建模专家，擅长从用户描述中提取系统用例。"
        },
        {
            "role": "user",
            "content": "我想开发一个自动驾驶系统，车辆可以自主驾驶、检测障碍物、识别交通信号灯、保持车道行驶，并在必要时自动刹车。请帮我提取该系统的核心用例，输出格式为 JSON。每个用例包含：用例名称、描述、参与者。"
        }
    ]
)

# 打印模型的输出
print(completion.choices[0].message.content)