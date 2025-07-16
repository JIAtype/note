[Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

大型语言模型首次出现时，用户必须将代码复制粘贴到文本界面才能与其交互。这很快被证明是不够的，因此需要自定义集成以实现更好的上下文加载。然而，这些集成非常分散，需要单独开发。模型上下文协议 (MCP) 解决了这个问题，它提供了一个通用协议，可与本地和远程资源高效地进行 AI 交互。

MCP 是一种开放协议，它使 AI 模型能够通过标准化的服务器实现与本地和远程资源安全地交互。本列表重点介绍已投入生产和处于实验阶段的 MCP 服务器，这些服务器通过文件访问、数据库连接、API 集成和其他上下文服务来扩展 AI 功能。

平台：[Glama](https://glama.ai/mcp/servers)
搜索、比较并连接数千台 MCP 服务器。Glama 根据安全性、兼容性和易用性对服务器进行索引、扫描和排名。

例子：
使用 PostgreSQL 的 Zed 扩展的示例，它可以立即向模型告知我们的整个数据库模式，因此当我们要求它为我们编写查询时，它确切地知道存在哪些表和列，以及它们的类型是什么。

使用智能搜索扩展，可以让模型以更简介或聪明的方式给出回答。

再比如使用代码理解扩展，可以让模型立马明白代码结构给出建议。

---

Ah, the Model Context Protocol (MCP). It's related to the LambdaMOO programming environment used in multi-user environments like MUDs (multi-user dungeons). MCP is a protocol designed to facilitate extended communications between a server (like a MUD server) and a client by encapsulating messages and sending structured data.

**Usage of MCP:**

1. **Understanding MCP Structure**:
   - MCP messages start with `#$#` followed by the package name and message type. For example: `#$#mcp package-name`.

2. **MCP Packages**:
   - MCP defines various packages, each with a specific purpose, like `mcp.gmcp`, `mcp.cookie`, and more. Each package contains specific messages that clients may support.

3. **Client Support**:
   - To use MCP, make sure the client application in use supports the MCP protocol. Some MUD clients have built-in support for MCP.

4. **Implementation**:
   - You would usually implement MCP handling in the server or use an MCP-supporting library in your client application so they can understand and respond to MCP messages accordingly.
   - MCP messages make use of tags that separate multiple arguments. Clients need to parse these messages appropriately to extract data or invoke behavior.

5. **Python Implementation**:
   - If you're writing a client or server in Python, you'd handle MCP protocols in the socket communication part of your code. 
   - Libraries or frameworks specific to MUD/MOO may already have MCP handling functions available.

6. **Example Skeleton for MCP Client in Python**:
   ```python
   import socket

   def send_mcp_message(sock, package, message):
       mcp_message = f"#$#{package} {message}\n"
       sock.sendall(mcp_message.encode())

   def receive_mcp_message(sock):
       data = sock.recv(1024).decode()
       if data.startswith("#$#"):
           # Parse the MCP message and handle it
           print(f"MCP Message Received: {data.strip()}")  # Simplistic display

   def main():
       # Connect to a server that supports MCP
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.connect(('example.server', 12345))  # Replace with actual server details

       # Example of sending a message
       send_mcp_message(sock, 'mcp.package', 'some-message')

       # Example of receiving a message
       receive_mcp_message(sock)

       sock.close()

   if __name__ == '__main__':
       main()
   ```

This is a simplified structure and you'd need to expand this to properly handle MCP message types, packages, and the interactions defined by the MCP protocol. Reading precise MCP documentation related to the specific environment is critical for developing full support.

---

智能文档助手：实时文档助手，确保代码无误，提升开发效率。

适用于快速更新的框架（如 Next.js、React Query），它提供最新的API和代码示例，避免因文档过时而导致的错误，确保开发环境与当前框架版本一致。

```
{
  "mcpServers":{
    "context7":{
      "command":"npx",
      "args":[
        "-y",
        "@upstash/context7-mcp@latest"
      ]
    }
  }
}
```

sequential-thinking：顺序推理能手

适合处理复杂逻辑（如 if 嵌套、for 循环等），一步一步帮助你理清思路，轻松应对复杂代码。

```
{
  "mcpServers":{
    "context7":{
      "command":"npx",
      "args":[
        "-y",
        "@modelcontextprotocol/server-sequential-thinking"
      ]
    }
  }
}
```

mcp-feedback-enhanced：AI代码审查官

在代码完成后，它提供实时优化建议，帮助识别性能问题、重复变量和潜在 bug，提升代码质量。

```
{
  "mcpServers":{
    "context7":{
      "command":"uvx",
      "args":[
        "mcp-feedback-enhanced@latest"
      ]
    }
  }
}
```


---

让我为您详细总结Model Context Protocol (MCP) 的基础操作和核心概念：

1. MCP基本概念：

```python
# MCP基础类
class ModelContextProtocol:
    def __init__(self):
        self.context = {}
        self.operations = []
        self.version = "1.0"
        
    def initialize(self, model_config):
        # 初始化模型上下文
        self.context = self.create_initial_context(model_config)
        self.setup_operations()
        
    def create_initial_context(self, config):
        # 创建初始上下文
        return {
            'model_state': 'initialized',
            'parameters': config.parameters,
            'metadata': config.metadata
        }
```

2. 上下文管理：

```python
# 上下文管理
class ContextManager:
    def __init__(self):
        self.current_context = None
        self.history = []
        
    def update_context(self, new_data):
        # 更新上下文
        self.current_context = self.merge_contexts(self.current_context, new_data)
        self.history.append(self.current_context)
        
    def merge_contexts(self, old, new):
        # 合并上下文
        return {**old, **new}
        
    def get_context_snapshot(self):
        # 获取上下文快照
        return self.current_context.copy()
```

3. 基本操作：

```python
# MCP基本操作
class MCPOperations:
    def __init__(self):
        self.supported_operations = [
            'query',
            'update',
            'validate',
            'transform'
        ]
        
    def query(self, parameters):
        # 查询操作
        return self.execute_operation('query', parameters)
        
    def update(self, data):
        # 更新操作
        return self.execute_operation('update', data)
        
    def validate(self, context):
        # 验证操作
        return self.execute_operation('validate', context)
        
    def transform(self, input_data):
        # 转换操作
        return self.execute_operation('transform', input_data)
        
    def execute_operation(self, op_type, data):
        # 执行操作
        if op_type in self.supported_operations:
            return self.perform_operation(op_type, data)
        raise MCPError(f"Unsupported operation: {op_type}")
```

4. 错误处理：

```python
# 错误处理
class MCPError(Exception):
    def __init__(self, message, code=None):
        self.message = message
        self.code = code or "MCP_ERROR"
        
    def __str__(self):
        return f"[{self.code}] {self.message}"
        
class ErrorManager:
    def __init__(self):
        self.error_handlers = {}
        
    def register_error_handler(self, error_type, handler):
        # 注册错误处理器
        self.error_handlers[error_type] = handler
        
    def handle_error(self, error):
        # 处理错误
        handler = self.error_handlers.get(type(error))
        if handler:
            return handler(error)
        return self.default_error_handler(error)
```

5. 会话管理：

```python
# 会话管理
class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.session_timeout = 300  # 5 minutes
        
    def create_session(self, context):
        # 创建会话
        session_id = self.generate_session_id()
        self.sessions[session_id] = {
            'context': context,
            'last_activity': time.time()
        }
        return session_id
        
    def get_session(self, session_id):
        # 获取会话
        session = self.sessions.get(session_id)
        if session:
            self.update_session_activity(session_id)
        return session
        
    def update_session_activity(self, session_id):
        # 更新会话活动时间
        self.sessions[session_id]['last_activity'] = time.time()
```

6. 上下文转换：

```python
# 上下文转换
class ContextTransformer:
    def __init__(self):
        self.transformations = {}
        
    def register_transformation(self, name, func):
        # 注册转换函数
        self.transformations[name] = func
        
    def transform(self, context, transformation_name):
        # 执行转换
        transformer = self.transformations.get(transformation_name)
        if transformer:
            return transformer(context)
        raise MCPError(f"Unknown transformation: {transformation_name}")
```

7. 版本控制：

```python
# 版本控制
class VersionManager:
    def __init__(self):
        self.current_version = "1.0"
        self.versions = {}
        
    def set_version(self, version):
        # 设置版本
        self.current_version = version
        self.versions[version] = self.get_current_context()
        
    def get_version(self):
        # 获取版本
        return self.current_version
        
    def rollback_to_version(self, version):
        # 回滚到特定版本
        if version in self.versions:
            self.current_version = version
            return self.versions[version]
        raise MCPError(f"Version not found: {version}")
```

8. 安全性：

```python
# 安全性
class SecurityManager:
    def __init__(self):
        self.access_control = {}
        self.audit_logs = []
        
    def validate_access(self, operation, user):
        # 验证访问权限
        if not self.check_permissions(operation, user):
            raise MCPError("Access denied")
            
    def log_operation(self, operation, user, result):
        # 记录操作日志
        self.audit_logs.append({
            'timestamp': time.time(),
            'operation': operation,
            'user': user,
            'result': result
        })
```

9. 性能优化：

```python
# 性能优化
class PerformanceOptimizer:
    def __init__(self):
        self.caches = {}
        self.metrics = {}
        
    def cache_operation(self, operation, result):
        # 缓存操作结果
