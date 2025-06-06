#!/usr/bin/env python3
"""
测试思维链处理功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai_service import process_thinking_chain

def test_thinking_chain():
    """测试思维链处理功能"""
    
    # 测试用例1：包含思维链的文本
    test_text_1 = """
<think>
我需要创建一个修仙世界的设定。首先考虑世界观：
1. 这是一个以修仙为主的世界
2. 有不同的修炼境界
3. 存在各种门派
4. 有灵气和法宝系统
</think>

## 修仙世界设定

### 世界观背景
这是一个灵气充沛的修仙世界，名为"九州大陆"。在这个世界中，修炼者通过吸收天地灵气来提升自身实力。

### 修炼境界
1. 练气期（1-12层）
2. 筑基期（初期、中期、后期、大圆满）
3. 金丹期（初期、中期、后期、大圆满）
4. 元婴期（初期、中期、后期、大圆满）
5. 化神期（初期、中期、后期、大圆满）

### 主要门派
- 天剑宗：以剑修闻名
- 丹霞门：炼丹大宗
- 万兽山：御兽门派
- 玄机阁：阵法机关
"""

    # 测试用例2：不包含思维链的文本
    test_text_2 = """
## 现代都市背景设定

### 城市概况
这是一个现代化的大都市，名为"星海市"。

### 主要区域
1. 商业中心区
2. 科技园区
3. 居住区
4. 工业区
"""

    # 测试用例3：多个思维链
    test_text_3 = """
<think>
用户想要一个反派角色，我需要考虑：
1. 反派的动机要合理
2. 不能是纯粹的邪恶
3. 要有深度和复杂性
</think>

## 反派角色设定

### 基本信息
姓名：林暗影
年龄：45岁

<think>
现在添加背景故事，让这个角色更有说服力：
- 曾经是正派人物
- 因为某种悲剧转变
- 有自己的正义观念
</think>

### 背景故事
林暗影原本是天剑宗的天才弟子，因为师门被灭而走上复仇之路。
"""

    print("=== 思维链处理功能测试 ===\n")
    
    # 测试用例1
    print("测试用例1：包含单个思维链")
    content1, thinking1 = process_thinking_chain(test_text_1)
    print(f"原始文本长度: {len(test_text_1)}")
    print(f"处理后内容长度: {len(content1)}")
    print(f"思维过程长度: {len(thinking1) if thinking1 else 0}")
    print(f"是否检测到思维链: {'是' if thinking1 else '否'}")
    if thinking1:
        print(f"思维过程预览: {thinking1[:100]}...")
    print(f"内容预览: {content1[:100]}...")
    print("-" * 50)
    
    # 测试用例2
    print("测试用例2：不包含思维链")
    content2, thinking2 = process_thinking_chain(test_text_2)
    print(f"原始文本长度: {len(test_text_2)}")
    print(f"处理后内容长度: {len(content2)}")
    print(f"思维过程长度: {len(thinking2) if thinking2 else 0}")
    print(f"是否检测到思维链: {'是' if thinking2 else '否'}")
    print(f"内容预览: {content2[:100]}...")
    print("-" * 50)
    
    # 测试用例3
    print("测试用例3：包含多个思维链")
    content3, thinking3 = process_thinking_chain(test_text_3)
    print(f"原始文本长度: {len(test_text_3)}")
    print(f"处理后内容长度: {len(content3)}")
    print(f"思维过程长度: {len(thinking3) if thinking3 else 0}")
    print(f"是否检测到思维链: {'是' if thinking3 else '否'}")
    if thinking3:
        print(f"思维过程预览: {thinking3[:100]}...")
    print(f"内容预览: {content3[:100]}...")
    print("-" * 50)
    
    print("=== 测试完成 ===")

if __name__ == "__main__":
    test_thinking_chain()
