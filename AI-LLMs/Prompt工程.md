让我为您详细总结LLM应用优化中的Prompt工程关键点：

1. Prompt工程最佳实践：

```python
# 基础Prompt结构
prompt = f"""
系统：你是一个专业的{domain}专家
任务：{task_description}
输入：{user_input}
输出格式：
1. {format_item1}
2. {format_item2}
注意事项：
- {note1}
- {note2}
"""

# 链式思维（Chain-of-Thought）
prompt = f"""
问题：{question}
让我们一步步思考：
1. 首先分析问题的关键点
2. 确定需要的知识领域
3. 逐步推理得出答案
最终答案：
"""

# Zero-shot vs Few-shot
# Zero-shot
prompt = "请解释什么是人工智能"

# Few-shot
prompt = """
示例1：
问题：什么是机器学习？
回答：机器学习是人工智能的一个分支，它使计算机能够从数据中学习并改进其性能。

示例2：
问题：什么是深度学习？
回答：深度学习是机器学习的一个子领域，使用深层神经网络来学习数据的复杂模式。

问题：什么是强化学习？
"""

# Context Window管理
# 使用滑动窗口
context_size = 4096  # 根据模型限制
current_context = []
def add_to_context(text):
    global current_context
    current_context.append(text)
    while len(" ".join(current_context)) > context_size:
        current_context.pop(0)

# Token优化
def optimize_prompt(prompt):
    # 移除不必要的空格
    prompt = " ".join(prompt.split())
    # 使用更短的指令词
    prompt = prompt.replace("请详细解释", "解释")
    return prompt
```

3. Prompt工程技巧：

```python
# 角色设定
prompt = """
你是一位专业的{domain}顾问
你的特点：
- 专业且准确
- 语言简洁
- 逻辑清晰
- 注重细节
"""

# 输出控制
prompt = """
输出格式：
- 使用Markdown格式
- 每个要点单独一行
- 重要信息加粗
- 使用列表展示步骤
"""

# 思维链
prompt = """
思考过程：
1. 理解问题核心
2. 分析相关知识
3. 考虑可能的解决方案
4. 选择最佳方案
5. 给出详细解释
"""

# 多轮对话
prompt = """
对话历史：
{previous_conversations}

当前问题：
{current_question}
"""

# 代码生成
prompt = """
任务：生成{language}代码
要求：
- 代码可运行
- 添加注释
- 包含错误处理
- 优化性能
"""

# 数据分析
prompt = """
数据：
{data}

分析要求：
1. 描述性统计
2. 趋势分析
3. 异常检测
4. 关联分析
"""

# 创意生成
prompt = """
创意类型：{type}
风格：{style}
要求：
- 独特且创新
- 符合主题
- 逻辑连贯
- 表达清晰
"""

# 问题解决
prompt = """
问题描述：
{problem}

已知信息：
{known_info}

解决方案：
1. 分析问题原因
2. 提出解决方案
3. 实施步骤
4. 预期结果
"""

# 代码审查
prompt = """
代码：
{code}

审查要点：
1. 代码规范
2. 逻辑正确性
3. 性能优化
4. 安全性
5. 可维护性
"""

# 文档生成
prompt = """
文档类型：{type}
内容要求：
- 清晰的目录结构
- 详细的说明
- 示例代码
- 注意事项
- 最佳实践
"""

# 多语言处理
prompt = """
语言：{target_language}
原文：
{source_text}

翻译要求：
- 保持原意
- 语言流畅
- 专业术语准确
"""

