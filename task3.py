import re
from openai import OpenAI
import json
from typing import Dict

# ✅ 替换为你的真实 API KEY
client = OpenAI(
    api_key="sk-IRIZnFyJ1lBZsW13TDxUzL0crNsVDBJ2OgvCqU34iycS97c3",
    base_url="https://api.chatfire.cn/v1"  # 修改为你实际使用的服务地址
)

def build_agent4_prompt(usecase: Dict) -> str:
    return (
        "你是一个系统分析专家，请根据以下 usecase 信息，生成该用例的系统顺序图（System Sequence Diagram）。\n"
        "请只输出标准 Mermaid 顺序图代码，不需要多余解释。\n\n"
        f"usecase 信息如下：\n```json\n{json.dumps(usecase, ensure_ascii=False, indent=2)}\n```"
    )

def run_multi_agent_workflow(user_input: str):
    ### === Agent 1: 需求提取 === ###
    agent1_prompt = (
        "你是一个专业的软件需求分析专家，擅长从自然语言中识别系统的核心用例。\n"
        "请根据以下系统描述，提取所有核心用例，并为每个用例提供以下信息：\n"
        "- 用例名称（中文）\n"
        "- 用例功能描述（中文）\n"
        "- 参与者（如：用户、系统、传感器等）\n"
        "- 所属模块（从：Perception 感知、Planning 决策、Control 控制中选择其一）\n"
        "- 触发条件（可列举一到两个触发场景）\n"
        "- 执行结果（该用例成功执行后的效果）\n"
        "请按如下格式输出：\n"
        "用例名称：xxx\n功能描述：xxx\n参与者：[xxx]\n模块：xxx\n触发条件：[xxx]\n执行结果：[xxx]\n\n"
        f"系统需求描述如下：\n\"\"\"{user_input}\"\"\""
    )

    response1 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent1_prompt}]
    )
    agent1_output = response1.choices[0].message.content.strip()
    print("\n✅ Agent 1 输出：\n", agent1_output)

    ### === Agent 2: DSL 格式建模 === ###
    agent2_prompt = (
        "你是一个系统建模专家，擅长将软件用例信息转换为结构化 DSL。\n"
        "请根据以下用例清单，生成符合下面 JSON 模板的 DSL 模型：\n"
        "{\n"
        "  \"system\": \"AutoDrivingSystem\",\n"
        "  \"modules\": [\"Perception\", \"Planning\", \"Control\"],\n"
        "  \"usecases\": [\n"
        "    {\n"
        "      \"name\": \"useCaseName\",\n"
        "      \"description\": \"中文描述\",\n"
        "      \"actors\": [\"系统\"],\n"
        "      \"module\": \"模块名\",\n"
        "      \"includes\": [],\n"
        "      \"extends\": [],\n"
        "      \"triggers\": [\"触发条件1\", \"触发条件2\"],\n"
        "      \"results\": [\"执行结果\"]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        f"用例清单如下：\n\"\"\"{agent1_output}\"\"\""
    )

    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent2_prompt}]
    )
    agent2_output = response2.choices[0].message.content.strip()
    print("\n✅ Agent 2 输出（DSL JSON）：\n", agent2_output)

    # try:
    #     dsl_model = json.loads(agent2_output)
    #     print("\n✅ Agent 2 输出已成功解析为 JSON")
    # except json.JSONDecodeError:
    #     print("\n⚠️ Agent 2 输出不是合法 JSON，建议在 Agent 3 自动修复")
    #     dsl_model = None
        
        
    # 提取被 ```json ... ``` 包裹的内容
    match = re.search(r"```json\n(.*?)\n```", agent2_output, re.DOTALL)
    if match:
        json_str = match.group(1)
        dsl_model = json.loads(json_str)
        print("✅ 已成功提取并解析 JSON")
    else:
        print("⚠️ 未找到合法 JSON 代码块")
        dsl_model = None

    ### === Agent 3: 格式校验 === ###
    agent3_prompt = (
        "你是一名建模语言的格式校验专家，擅长检查 JSON 型 DSL 模型的结构规范性与完整性。\n"
        "请对以下 DSL 模型进行全面校验，包括字段完整性、语法合规性、模块引用一致性等。\n\n"
        "如果发现问题，请修复；若一切正常，请回复：“DSL 合规”。\n\n"
        "以下模型：\n```json\n"
        f"{agent2_output}\n```"
    )

    response3 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent3_prompt}]
    )
    agent3_output = response3.choices[0].message.content.strip()
    print("\n✅ Agent 3 输出（校验结果）：\n", agent3_output)

    # === Agent 4: 顺序图生成 ===
    usecase = dsl_model["usecases"][0]  # 可遍历 usecases 批量生成
    agent4_prompt = (
        "你是一个系统分析专家，请根据以下 usecase 信息，生成该用例的系统顺序图（System Sequence Diagram）。\n"
        "请只输出标准 Mermaid 顺序图代码，不需要多余解释。\n\n"
        f"usecase 信息如下：\n```json\n{json.dumps(usecase, ensure_ascii=False, indent=2)}\n```"
    )

    response4 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent4_prompt}]
    )

    # 输出 Mermaid 图代码
    agent4_output = response4.choices[0].message.content.strip()
    print("\n✅ Agent 4 输出（系统顺序图 Mermaid）：\n")
    print(agent4_output)

    agent5_prompt = (
    "你是一位软件建模专家，请根据以下 DSL 模型，生成一个系统的概念类图。\n"
    "请输出标准 Mermaid 类图代码（classDiagram），包含代表系统中关键概念的类、它们的属性，以及关系（如：依赖、关联、聚合等）。\n"
    "不需要多余解释，只返回 Mermaid 代码。\n\n"
    f"以下为 DSL 模型：\n```json\n{json.dumps(dsl_model, ensure_ascii=False, indent=2)}\n```"
)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent5_prompt}]
    )

    print("\n✅ Agent 5 输出（概念类图 Mermaid）：\n")
    print(response.choices[0].message.content.strip())

    # === Agent6: OCL 生成 ===
    agent6_prompt = (
        "你是一位 OCL（Object Constraint Language）建模专家，擅长根据系统类模型自动生成精确的 OCL 约束语句。\n"
        "请根据以下 DSL 模型，为每个类生成合理的 OCL 表达式，包含：\n"
        "1. 不变式（inv）：类属性约束、状态约束、数据范围约束；\n"
        "2. 前置条件（pre）：操作调用的前提条件；\n"
        "3. 后置条件（post）：操作后的状态变化（如 balance@pre）；\n\n"
        "要求：\n"
        "- 使用标准 OCL 语法\n"
        "- 每条表达式前添加简要注释（以 -- 开头）\n"
        "- 不要输出解释说明，只返回 OCL 代码块\n\n"
        f"以下为 DSL 模型：\n```json\n{json.dumps(dsl_model, ensure_ascii=False, indent=2)}\n```"
    )

    response6 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": agent6_prompt}]
    )

    agent6_output = response6.choices[0].message.content.strip()
    print("\n✅ Agent 6 输出（OCL 约束）：\n")
    print(agent6_output)

    return {
        "usecase_text": agent1_output,
        "dsl_raw": agent2_output,
        "dsl_parsed": dsl_model,
        "validation": agent3_output
    }

    
def generate_usecase_mermaid(dsl):
    header = "graph TB\n"
    actor_lines = set()
    system_lines = []

    for usecase in dsl["usecases"]:
        name = usecase["name"]
        actors = usecase.get("actors", [])
        system_lines.append(f'    系统 --> {name}')
        for actor in actors:
            actor_id = f"actor_{actor}"
            actor_lines.add(f'    {actor_id}({actor})')
            system_lines.append(f'    {actor_id} --> {name}')
    return "%% 系统用例图\n" + header + "\n".join(sorted(actor_lines)) + "\n    系统(自动驾驶系统)\n" + "\n".join(system_lines)





# ✅ 示例调用
if __name__ == "__main__":
    user_input = (
        "我希望开发一款用于小型商店的收银软件系统。系统需要具备商品扫码、购物车管理、打折促销、结账支付和生成小票等功能。操作员可以使用扫码枪录入商品，系统应自动识别商品信息、计算总价，并支持折扣规则（例如买一送一或满减）。顾客可选择现金、刷卡或移动支付进行付款，系统需在支付成功后打印小票并清空购物车。"
    )
    result = run_multi_agent_workflow(user_input)
    print(generate_usecase_mermaid(result["dsl_parsed"]))