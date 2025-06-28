#!/bin/bash

curl https://api.chatfire.cn/v1/chat/completions\
  -H "Content-Type: application/json" \
  -H "Authorization: sk-" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "system",
        "content": "你是一个需求分析专家，帮助提取系统需求。"
      },
      {
        "role": "user",
        "content": "我想开发一个自动驾驶系统，车辆可以自主驾驶、检测障碍物、识别交通信号灯、保持车道行驶，并在必要时自动刹车。请帮我提取该系统的核心用例，输出格式为 JSON。每个用例包含：用例名称、描述、参与者。"
      }
    ]
  }'