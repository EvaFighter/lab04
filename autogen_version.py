import json
import re
from autogen import AssistantAgent, GroupChat, GroupChatManager, UserProxyAgent

# Chat model config
config = {
    "config_list": [
        {
            "model": "gpt-4o",  # 或 gpt-35-turbo 等
            "api_key": "sk-IRIZnFyJ1lBZsW13TDxUzL0crNsVDBJ2OgvCqU34iycS97c3",
            "base_url": "https://api.chatfire.cn/v1"  # ✅ 自定义 base URL
        }
    ],
    "cache_seed": 42
}

# Step 1: 用户代理（发起任务）
user_proxy = UserProxyAgent(name="user", system_message="发起系统建模任务", code_execution_config=False)

# Step 2: Agent1：需求提取专家
agent1 = AssistantAgent(
    name="RequirementExtractor",
    system_message=(
        "你是一个专业的软件需求分析专家，擅长从自然语言中识别系统的核心用例。\n"
        "请根据提供的系统描述，提取所有核心用例，并为每个用例提供：用例名称、功能描述、参与者、模块、触发条件、执行结果。\n"
        "按以下格式输出：\n"
        "用例名称：xxx\n功能描述：xxx\n参与者：[xxx]\n模块：xxx\n触发条件：[xxx]\n执行结果：[xxx]\n\n"
    ),
    llm_config=config
)

# Step 3: Agent2：DSL建模专家
agent2 = AssistantAgent(
    name="DSLModeler",
    system_message=(
        "你是一个系统建模专家，擅长将软件用例信息转换为结构化 DSL。\n"
        "请根据以下用例清单，生成如下 JSON 模型：\n"
        "{\n"
        "  \"system\": \"AutoDrivingSystem\",\n"
        "  \"modules\": [\"Perception\", \"Planning\", \"Control\"],\n"
        "  \"usecases\": [...]\n"
        "}\n"
        "注意格式正确，字段齐全。"
    ),
    llm_config=config
)

# Step 4: Agent3：格式校验专家
agent3 = AssistantAgent(
    name="DSLValidator",
    system_message=(
        "你是一名建模语言的格式校验专家，擅长检查 JSON 型 DSL 模型的结构规范性与完整性。\n"
        "请检查结构、语法、模块引用等是否规范，并修复错误；若一切正常，请回复：“DSL 合规”。"
    ),
    llm_config=config
)

# Step 5: Agent4：顺序图生成
agent4 = AssistantAgent(
    name="SequenceDiagramGenerator",
    system_message=(
        "你是一个系统分析专家，请根据 usecase 信息生成 Mermaid 格式的系统顺序图代码（sequenceDiagram），不需要解释。"
    ),
    llm_config=config
)

# Step 6: Agent5：类图生成
agent5 = AssistantAgent(
    name="ClassDiagramGenerator",
    system_message=(
        "你是一位软件建模专家，请根据 DSL 模型生成 Mermaid classDiagram 代码，包含类、属性、关系。只输出 Mermaid 图。"
    ),
    llm_config=config
)

# Step 7: Agent6：OCL生成
agent6 = AssistantAgent(
    name="OCLGenerator",
    system_message=(
        "你是一位 OCL 建模专家，请根据 DSL 模型为每个类生成合理的 OCL 表达式（包含 inv、pre、post），"
        "使用标准语法，每条表达式前加 -- 注释。只输出 OCL 代码。"
    ),
    llm_config=config
)

agent7 = AssistantAgent(
    name="PrototypeGenerator",
    system_message=(
        "你是一位资深全栈开发工程师，请根据以下 DSL 模型生成系统的前后端原型：\n\n"
        "输出要求：\n"
        "1. 前端：HTML + TailwindCSS 或 React（任选），展示主要交互界面（如商品扫码、购物车、结账按钮等）；\n"
        "2. 后端：使用 Flask，按 usecase 生成接口，每个接口单独一个 Python 文件（例如 checkout.py）；\n"
        "3. 数据库：用 SQLAlchemy 定义商品、购物车、订单等数据模型；\n"
        "4. 按文件形式输出：每段代码前注明文件名，例如：\n"
        "文件：backend/main.py\n```python\n# 内容\n```\n"
        "5. 所有代码写入本地目录 `./output/`，不需要任何多余解释。"
    ),
    code_execution_config={"work_dir": "./output", "use_docker": False},
    llm_config=config
)

# 建立 GroupChat
groupchat = GroupChat(
    agents=[
        user_proxy,
        agent1, agent2, agent3,
        agent4, agent5, agent6,
        agent7  # ✅ 新增
    ],
    messages=[],
    max_round=15
)

manager = GroupChatManager(groupchat=groupchat, llm_config=config)


# 执行任务
def run_autogen_workflow(user_input: str):
    user_proxy.initiate_chat(
        manager,
        message=f"请根据以下需求描述启动系统建模流程：\n\"\"\"{user_input}\"\"\""
    )


# 示例调用
if __name__ == "__main__":
    input_text = (
        "我希望开发一款用于小型商店的收银软件系统。系统需要具备商品扫码、购物车管理、打折促销、结账支付和生成小票等功能。"
        "操作员可以使用扫码枪录入商品，系统应自动识别商品信息、计算总价，并支持折扣规则。顾客可选择现金、刷卡或移动支付进行付款，"
        "系统需在支付成功后打印小票并清空购物车。"
    )
    run_autogen_workflow(input_text)