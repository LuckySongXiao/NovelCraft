# NovelCraft UI改进功能说明

## 改进概述

本次更新主要解决了以下问题：
1. 启动时重复打开网页的问题
2. 侧边栏缺少可折叠功能
3. AI助手默认配置优化
4. 页面功能完善和API调用优化

## 详细改进内容

### 1. 启动脚本优化

**问题**：启动脚本会通过`start http://localhost:3000`打开浏览器，而Electron应用也会自动打开窗口，导致重复打开。

**解决方案**：
- 修改 `Start-System.bat` 第116-118行
- 移除 `start http://localhost:3000` 命令
- 添加说明文字："Browser will open automatically when frontend is ready..."

**文件位置**：`Start-System.bat`

### 2. 侧边栏可折叠功能

**问题**：内容管理和设定管理菜单项过多，需要可折叠的分组功能。

**解决方案**：
- 重构 `Layout.js` 组件的菜单结构
- 使用 Ant Design 的 `Collapse` 组件
- 添加内容管理和设定管理的可折叠分组
- 保持工具菜单独立显示

**主要变更**：
- 导入 `Collapse` 组件
- 添加折叠状态管理：`contentCollapsed`, `settingsCollapsed`
- 重构菜单项为分组结构：`baseMenuItems`, `contentMenuItems`, `settingsMenuItems`, `toolsMenuItems`
- 使用 `Collapse.Panel` 包装内容管理和设定管理菜单

**文件位置**：`frontend/src/components/Layout.js`

### 3. CSS样式优化

**新增样式**：
- 可折叠菜单样式优化
- 菜单项选中状态美化
- 侧边栏折叠状态适配
- 工具菜单分隔线和标题样式

**文件位置**：`frontend/src/App.css`

### 4. AI助手默认配置

**确认配置**：
- 默认AI提供商：Ollama
- 默认模型：`mollysama/rwkv-7-g1:0.4B`
- 服务地址：`http://localhost:11434`

**配置位置**：
- 后端配置：`backend/app/core/config.py`
- 前端配置：`frontend/src/components/AIConfigPanel.js`

### 5. API功能完善

**项目数据API**：
- 完善了AI助手读写项目数据的接口
- 支持项目级数据隔离
- 提供批量操作和搜索功能

**主要接口**：
- `/api/project-data/ai/set-project/{project_id}` - 设置当前项目
- `/api/project-data/ai/read-data` - 读取项目数据
- `/api/project-data/ai/write-data/{data_type}` - 写入项目数据
- `/api/project-data/ai/batch-write` - 批量写入数据
- `/api/project-data/ai/search` - 搜索项目数据

**文件位置**：`backend/app/api/endpoints/project_data.py`

## 功能特性

### 可折叠侧边栏

1. **内容管理分组**：
   - 人物管理
   - 势力管理
   - 剧情管理
   - 卷宗管理
   - 资源分布
   - 种族分布
   - 秘境分布

2. **设定管理分组**：
   - 世界设定
   - 修炼体系
   - 装备体系
   - 宠物体系
   - 地图结构
   - 维度结构
   - 灵宝体系
   - 生民体系
   - 司法体系
   - 职业体系
   - 时间线
   - 关系网络

3. **工具菜单**：
   - AI助手
   - AI测试
   - 系统设置

### AI助手功能

1. **智能对话**：
   - 支持多轮对话
   - 思维链处理
   - 上下文保持

2. **内容生成**：
   - 人物生成
   - 设定生成
   - 剧情生成
   - 批量生成模式

3. **项目数据操作**：
   - 读取项目全部数据
   - 写入和更新数据
   - 数据搜索和过滤
   - 操作日志记录

## 使用说明

### 启动系统

1. 运行 `Start-System.bat`
2. 系统会自动启动后端和前端服务
3. Electron应用会自动打开，无需手动打开浏览器

### 使用可折叠菜单

1. 在项目页面中，侧边栏会显示内容管理和设定管理分组
2. 点击分组标题可以展开/折叠菜单项
3. 侧边栏折叠时，分组会自动适配显示

### AI助手配置

1. 进入"系统设置"页面
2. 在AI配置面板中选择提供商
3. 默认使用Ollama本地模型
4. 可以切换到其他AI提供商（需要配置API Key）

### AI助手使用

1. 点击"AI助手"菜单进入对话页面
2. 可以进行智能对话和内容生成
3. AI助手会自动读取当前项目的数据
4. 生成的内容可以直接保存到项目中

## 测试验证

运行测试脚本验证功能：

```bash
python test_ui_improvements.py
```

测试内容包括：
- 启动脚本修改验证
- 后端服务状态
- AI提供商配置
- AI服务连接状态
- Ollama模型检测
- 项目数据API
- 前端可访问性

## 技术细节

### 前端技术栈
- React 18
- Ant Design 5
- React Router 6
- Axios
- Electron

### 后端技术栈
- FastAPI
- SQLAlchemy
- Pydantic
- Python 3.9+

### AI集成
- 支持多种AI提供商
- 统一的AI服务接口
- 思维链处理
- 本地模型支持

## 注意事项

1. **Ollama安装**：使用默认AI功能需要安装Ollama和对应模型
2. **端口占用**：确保3000和8000端口未被占用
3. **网络连接**：使用在线AI服务需要稳定的网络连接
4. **数据备份**：重要项目数据建议定期备份

## 后续优化建议

1. 添加更多AI模型支持
2. 优化大数据量项目的性能
3. 增加更多内容生成模板
4. 完善数据导入导出功能
5. 添加协作功能支持
