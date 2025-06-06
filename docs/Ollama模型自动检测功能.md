# Ollama模型自动检测功能

## 功能概述

本系统已实现Ollama本地模型的自动检测功能，可以实时获取本地已安装的Ollama模型列表，并在AI配置界面中动态显示可用模型。

## 主要特性

### 1. 自动模型检测
- 🔍 **实时检测**: 自动检测本地Ollama服务中已安装的模型
- 📊 **模型信息**: 显示模型名称、大小、修改时间等详细信息
- 🔄 **动态刷新**: 支持手动刷新模型列表，实时更新可用模型

### 2. 智能配置界面
- 🎯 **动态选择**: 模型选择框根据实际安装的模型动态生成
- 📏 **大小显示**: 在模型选择时显示每个模型的存储大小
- ⚡ **快速操作**: 一键刷新模型列表，无需重启应用

### 3. 状态监控
- 🟢 **连接状态**: 实时显示Ollama服务连接状态
- 📈 **统计信息**: 显示本地模型数量和总存储大小
- ⚠️ **错误提示**: 当Ollama服务未运行时提供友好的错误提示

## API端点

### 获取模型列表
```
GET /api/v1/ai/ollama/models
```

**响应示例:**
```json
{
  "models": [
    {
      "name": "llama2:latest",
      "size": 3825819519,
      "modified_at": "2024-01-15T10:30:00Z",
      "digest": "sha256:abc123...",
      "details": {}
    }
  ],
  "count": 1,
  "status": "success"
}
```

### 获取模型详细信息
```
GET /api/v1/ai/ollama/models/{model_name}
```

**响应示例:**
```json
{
  "model": {
    "modelfile": "FROM llama2\n...",
    "parameters": "...",
    "template": "...",
    "details": {
      "format": "gguf",
      "family": "llama",
      "families": ["llama"],
      "parameter_size": "7B",
      "quantization_level": "Q4_0"
    }
  },
  "status": "success"
}
```

## 前端功能

### AI配置面板增强
- **动态模型选择**: 当选择Ollama提供商时，模型选择框自动加载本地可用模型
- **模型信息显示**: 在选择框中显示模型名称和大小
- **刷新按钮**: 模型选择框旁边的刷新按钮，可手动更新模型列表
- **状态指示**: 显示模型加载状态和错误信息

### 专用测试页面
访问 `/ollama-test` 可以查看专门的Ollama测试页面，包含：
- Ollama服务状态检查
- 本地模型列表展示
- 模型详细信息查看
- 统计信息显示

## 使用指南

### 1. 安装Ollama
```bash
# 下载并安装Ollama
# 访问 https://ollama.ai/ 下载对应平台的安装包
```

### 2. 下载模型
```bash
# 下载常用模型
ollama pull llama2
ollama pull mistral
ollama pull qwen
ollama pull codellama

# 查看已安装模型
ollama list
```

### 3. 启动Ollama服务
```bash
# Ollama通常会自动启动服务
# 如果需要手动启动：
ollama serve
```

### 4. 在系统中使用
1. 打开AI配置面板
2. 选择"Ollama"提供商
3. 系统会自动检测并显示可用模型
4. 选择要使用的模型
5. 保存配置

## 技术实现

### 后端实现
- **OllamaService类**: 扩展了获取模型列表和模型信息的方法
- **API端点**: 新增了专门的Ollama模型相关API
- **错误处理**: 优雅处理Ollama服务不可用的情况

### 前端实现
- **动态组件**: AI配置面板根据提供商类型动态渲染
- **状态管理**: 使用React Hooks管理模型列表和加载状态
- **用户体验**: 提供加载指示器和错误提示

## 故障排除

### 常见问题

1. **无法检测到模型**
   - 确保Ollama服务正在运行
   - 检查Ollama API地址配置（默认: http://localhost:11434）
   - 使用 `ollama list` 命令确认模型已安装

2. **连接失败**
   - 检查Ollama服务状态
   - 确认防火墙设置
   - 验证API地址配置

3. **模型列表为空**
   - 使用 `ollama pull <model>` 下载模型
   - 刷新模型列表
   - 检查Ollama服务日志

### 调试命令
```bash
# 检查Ollama服务状态
curl http://localhost:11434/api/tags

# 查看已安装模型
ollama list

# 检查特定模型信息
ollama show <model_name>
```

## 未来改进

- [ ] 支持模型下载进度显示
- [ ] 模型性能基准测试
- [ ] 模型使用统计
- [ ] 自动模型推荐
- [ ] 模型版本管理

## 相关文档

- [Ollama官方文档](https://ollama.ai/docs)
- [AI配置指南](./AI功能更新说明.md)
- [系统架构文档](../README.md)
