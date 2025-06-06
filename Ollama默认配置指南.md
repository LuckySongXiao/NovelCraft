# Ollama默认配置指南

## 概述

NovelCraft系统已将Ollama设置为默认AI提供商，使用mollysama/rwkv-7-g1:0.4B作为默认模型。这样配置的优势：

- ✅ **本地运行**: 无需网络连接，数据隐私安全
- ✅ **免费使用**: 无需API Key，无使用限制
- ✅ **快速响应**: 本地推理，响应速度快
- ✅ **轻量模型**: 0.4B参数，资源占用小

## 快速开始

### 1. 安装Ollama

#### Windows系统
1. 访问 [Ollama官网](https://ollama.ai/)
2. 下载Windows安装包
3. 运行安装程序，按提示完成安装
4. 安装完成后，Ollama会自动启动服务

#### 验证安装
```powershell
# 检查Ollama版本
ollama --version

# 检查服务状态
ollama list
```

### 2. 下载默认模型

```powershell
# 下载默认模型 mollysama/rwkv-7-g1:0.4B
ollama pull mollysama/rwkv-7-g1:0.4B

# 验证模型下载
ollama list
```

### 3. 测试模型

```powershell
# 测试模型对话
ollama run mollysama/rwkv-7-g1:0.4B

# 输入测试问题
# 例如: "你好，请介绍一下自己"
# 按 Ctrl+D 退出对话
```

## 模型特性

### mollysama/rwkv-7-g1:0.4B 模型介绍

- **模型类型**: RWKV (Receptance Weighted Key Value)
- **参数规模**: 0.4B (4亿参数)
- **模型大小**: 约 800MB
- **语言支持**: 中英文双语
- **适用场景**: 
  - 小说创作辅助
  - 对话交互
  - 文本生成
  - 内容续写

### 性能特点

- **内存占用**: 约 1-2GB RAM
- **推理速度**: 快速响应（本地CPU/GPU）
- **质量表现**: 适合创作辅助和日常对话
- **兼容性**: 支持Windows/Linux/macOS

## 系统配置

### 默认配置参数

NovelCraft系统的默认Ollama配置：

```json
{
  "provider": "ollama",
  "base_url": "http://localhost:11434",
  "model": "mollysama/rwkv-7-g1:0.4B",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

### 配置验证

1. 启动NovelCraft系统
2. 进入 **系统设置** → **AI配置**
3. 确认当前提供商为"Ollama"
4. 确认模型为"mollysama/rwkv-7-g1:0.4B"
5. 点击"测试连接"验证配置

## 故障排除

### 常见问题

#### 1. 模型下载失败
**问题**: `ollama pull` 命令失败
**解决方案**:
```powershell
# 检查网络连接
ping ollama.ai

# 重试下载
ollama pull mollysama/rwkv-7-g1:0.4B

# 如果仍然失败，尝试其他模型
ollama pull llama2:7b-chat-q4_0
```

#### 2. 服务连接失败
**问题**: NovelCraft无法连接到Ollama服务
**解决方案**:
```powershell
# 检查服务状态
ollama list

# 手动启动服务
ollama serve

# 检查端口占用
netstat -an | findstr 11434
```

#### 3. 内存不足
**问题**: 模型加载时内存不足
**解决方案**:
- 关闭其他占用内存的程序
- 使用更小的量化模型
- 增加系统虚拟内存

#### 4. 模型响应慢
**问题**: AI响应速度较慢
**解决方案**:
- 确保Ollama使用GPU加速（如果有独立显卡）
- 调整模型参数（降低max_tokens）
- 考虑使用更小的模型

### 替代模型推荐

如果默认模型不适合，可以尝试以下替代方案：

#### 轻量级模型
```powershell
# 更小的模型，更快的响应
ollama pull qwen:0.5b
ollama pull phi:2.7b
```

#### 中文优化模型
```powershell
# 中文表现更好的模型
ollama pull qwen:7b-chat
ollama pull chatglm3:6b
```

#### 代码生成模型
```powershell
# 适合代码生成的模型
ollama pull codellama:7b-code
ollama pull deepseek-coder:6.7b
```

## 高级配置

### 自定义模型参数

在NovelCraft的AI配置中，可以调整以下参数：

- **Temperature**: 控制输出随机性（0.1-1.0）
- **Max Tokens**: 最大输出长度（100-4000）
- **Top P**: 核采样参数（0.1-1.0）
- **Repeat Penalty**: 重复惩罚（1.0-1.2）

### 环境变量配置

```powershell
# 设置Ollama环境变量（可选）
set OLLAMA_HOST=0.0.0.0:11434  # 允许外部访问
set OLLAMA_MODELS=D:\ollama\models  # 自定义模型存储路径
set OLLAMA_NUM_PARALLEL=2  # 并行处理数量
```

## 使用建议

### 最佳实践

1. **首次使用**:
   - 先测试默认模型是否正常工作
   - 熟悉基本对话功能
   - 了解模型的能力和限制

2. **创作辅助**:
   - 使用简洁明确的提示词
   - 分段生成长文本
   - 结合人工编辑优化内容

3. **性能优化**:
   - 定期清理不用的模型
   - 监控系统资源使用
   - 根据需要调整参数

### 注意事项

- 🔸 首次运行模型时需要加载时间
- 🔸 模型输出质量取决于输入提示的质量
- 🔸 本地模型的能力可能不如云端大模型
- 🔸 定期更新Ollama和模型版本

## 技术支持

如遇到问题，请按以下顺序排查：

1. 检查Ollama服务是否正常运行
2. 验证模型是否正确下载
3. 确认网络和防火墙设置
4. 查看NovelCraft的错误日志
5. 联系技术支持团队

---

**祝您使用愉快！享受本地AI带来的便利和安全。**
