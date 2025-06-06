# Ollama安装配置指南

## 问题诊断

如果您遇到"ollama 本地模型检测拉取失败"的问题，通常是以下原因之一：

### 常见错误类型
- ❌ `502 Bad Gateway` - Ollama服务未启动
- ❌ `Connection refused` - Ollama未安装或端口错误
- ❌ `Timeout` - 网络连接问题
- ❌ `Empty model list` - 没有下载任何模型

## 完整安装步骤

### 1. 下载安装Ollama

#### Windows系统
1. 访问 [Ollama官网](https://ollama.ai/)
2. 点击"Download for Windows"
3. 下载并运行安装程序
4. 安装完成后，Ollama会自动启动

#### 验证安装
```powershell
# 检查Ollama版本
ollama --version

# 检查服务状态
ollama list
```

### 2. 启动Ollama服务

#### 自动启动（推荐）
Ollama安装后通常会自动启动服务，监听端口 `11434`

#### 手动启动
```powershell
# 启动Ollama服务
ollama serve
```

#### 检查服务状态
```powershell
# 检查端口是否监听
netstat -an | findstr :11434

# 测试API连接
curl http://localhost:11434/api/tags
```

### 3. 下载模型

#### 推荐模型
```powershell
# 下载Llama2 (7B参数，约4GB)
ollama pull llama2

# 下载Mistral (7B参数，约4GB)
ollama pull mistral

# 下载Qwen (7B参数，约4GB)
ollama pull qwen

# 下载CodeLlama (代码生成，7B参数)
ollama pull codellama
```

#### 查看已安装模型
```powershell
# 列出所有本地模型
ollama list

# 查看模型详细信息
ollama show llama2
```

### 4. 测试模型
```powershell
# 测试模型对话
ollama run llama2
# 输入: Hello, how are you?
# 按 Ctrl+D 退出
```

## 系统配置

### 1. 检查配置文件
系统默认配置：
- **服务地址**: `http://localhost:11434`
- **超时时间**: 10秒
- **自动检测**: 启用

### 2. 修改配置（如需要）
如果Ollama运行在不同端口，请在AI配置面板中修改：
1. 打开AI配置面板
2. 选择Ollama提供商
3. 修改"服务地址"字段
4. 保存配置

## 故障排除

### 问题1: 502 Bad Gateway
**原因**: Ollama服务未启动
**解决方案**:
```powershell
# 启动服务
ollama serve

# 或重启Ollama应用
# 在任务管理器中结束ollama进程，然后重新启动
```

### 问题2: Connection refused
**原因**: Ollama未安装或端口错误
**解决方案**:
```powershell
# 检查安装
ollama --version

# 检查端口
netstat -an | findstr :11434

# 如果端口不同，修改系统配置
```

### 问题3: 模型列表为空
**原因**: 没有下载任何模型
**解决方案**:
```powershell
# 下载推荐模型
ollama pull llama2

# 验证下载
ollama list
```

### 问题4: 下载速度慢
**原因**: 网络连接问题
**解决方案**:
```powershell
# 使用代理（如果需要）
set HTTP_PROXY=http://proxy:port
set HTTPS_PROXY=http://proxy:port
ollama pull llama2

# 或选择较小的模型
ollama pull llama2:7b-chat-q4_0  # 量化版本，更小
```

## 性能优化

### 1. 硬件要求
- **最低内存**: 8GB RAM
- **推荐内存**: 16GB+ RAM
- **存储空间**: 每个7B模型约4-8GB
- **GPU**: 可选，支持NVIDIA GPU加速

### 2. 模型选择建议
| 模型 | 大小 | 用途 | 推荐场景 |
|------|------|------|----------|
| llama2:7b | ~4GB | 通用对话 | 日常使用 |
| mistral:7b | ~4GB | 高质量对话 | 创作辅助 |
| codellama:7b | ~4GB | 代码生成 | 编程辅助 |
| qwen:7b | ~4GB | 中文优化 | 中文创作 |

### 3. 系统优化
```powershell
# 设置环境变量（可选）
set OLLAMA_HOST=0.0.0.0:11434  # 允许外部访问
set OLLAMA_MODELS=D:\ollama\models  # 自定义模型存储路径
```

## 验证安装

### 1. 使用系统测试页面
1. 启动系统前后端服务
2. 访问 `http://localhost:3000/ollama-test`
3. 点击"刷新模型列表"
4. 查看检测结果

### 2. 使用API测试
```powershell
# 运行测试脚本
python test_ollama_models.py
```

### 3. 手动验证
```powershell
# 测试API连接
curl http://localhost:11434/api/tags

# 测试模型对话
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Hello, world!",
  "stream": false
}'
```

## 常见问题FAQ

**Q: Ollama占用内存太大怎么办？**
A: 可以使用量化模型，如 `ollama pull llama2:7b-chat-q4_0`

**Q: 如何卸载Ollama？**
A: 在控制面板中卸载，然后删除模型文件夹

**Q: 支持哪些模型格式？**
A: Ollama支持GGUF格式的模型，可以从Hugging Face导入

**Q: 如何更新模型？**
A: 使用 `ollama pull model:latest` 更新到最新版本

**Q: 可以同时运行多个模型吗？**
A: 可以，但会占用更多内存，建议根据硬件配置选择

## 技术支持

如果仍然遇到问题，请：
1. 查看系统日志
2. 检查防火墙设置
3. 确认网络连接
4. 联系技术支持并提供错误日志

---

**提示**: 首次下载模型可能需要较长时间，请耐心等待。建议在网络状况良好时进行下载。
