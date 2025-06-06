import React, { useState, useEffect, useRef } from 'react';
import {
  Card,
  Typography,
  Button,
  Input,
  Select,
  Row,
  Col,
  Tabs,
  Form,
  message,
  Spin,
  Space,
  Tag,
  Divider,
  Alert,
  Modal,
  List,

  Slider,
  Switch,
  InputNumber,

  Badge,
  Popconfirm,

  Drawer
} from 'antd';
import {
  RobotOutlined,
  MessageOutlined,
  SendOutlined,
  BulbOutlined,
  UserOutlined,
  ReloadOutlined,
  BookOutlined,
  EditOutlined,
  CheckCircleOutlined,

  HistoryOutlined,

  DownloadOutlined,

  CopyOutlined,
  DeleteOutlined,
  SettingOutlined,

  FileTextOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;


const AIAssistant = () => {
  const [loading, setLoading] = useState(false);
  const [providers, setProviders] = useState([]);
  const [currentProvider, setCurrentProvider] = useState('');
  const [aiStatus, setAiStatus] = useState({ connected: false, status: 'offline' });
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [generateForm] = Form.useForm();
  const [plotForm] = Form.useForm();
  const [continueForm] = Form.useForm();
  const [checkForm] = Form.useForm();
  const [activeTab, setActiveTab] = useState('chat');
  const messagesEndRef = useRef(null);

  // 新增状态
  const [generatedContent, setGeneratedContent] = useState('');
  const [contentHistory, setContentHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [templates, setTemplates] = useState([]);
  const [aiParams, setAiParams] = useState({
    temperature: 0.7,
    max_tokens: 2000,
    top_p: 1.0,
    frequency_penalty: 0.0,
    presence_penalty: 0.0
  });
  const [batchMode, setBatchMode] = useState(false);
  const [batchCount, setBatchCount] = useState(3);

  // 思维链相关状态
  const [currentThinking, setCurrentThinking] = useState('');
  const [showThinking, setShowThinking] = useState(false);
  const [thinkingHistory, setThinkingHistory] = useState([]);

  // 获取AI提供商列表
  const fetchProviders = async () => {
    try {
      const response = await axios.get('/api/ai/providers');
      setProviders(response.data.providers);
      setCurrentProvider(response.data.current);
    } catch (error) {
      message.error('获取AI提供商列表失败');
    }
  };

  // 获取AI状态
  const fetchAIStatus = async () => {
    try {
      const response = await axios.get('/api/ai/status');
      setAiStatus(response.data);
    } catch (error) {
      setAiStatus({ connected: false, status: 'error' });
    }
  };

  // 切换AI提供商
  const switchProvider = async (provider) => {
    try {
      setLoading(true);
      await axios.post('/api/v1/ai/switch-provider', { provider });
      setCurrentProvider(provider);
      message.success(`已切换到 ${provider}`);
      await fetchAIStatus();
    } catch (error) {
      message.error('切换AI提供商失败');
    } finally {
      setLoading(false);
    }
  };

  // 发送聊天消息
  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { role: 'user', content: inputMessage };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputMessage('');
    setLoading(true);

    try {
      const response = await axios.post('/api/ai/chat', {
        messages: newMessages,
        ...aiParams
      });

      const aiMessage = {
        role: 'assistant',
        content: response.data.response,
        thinking: response.data.thinking,
        timestamp: new Date().toISOString()
      };

      setMessages([...newMessages, aiMessage]);

      // 如果有思维过程，保存到历史记录
      if (response.data.thinking) {
        setThinkingHistory(prev => [{
          id: Date.now(),
          content: response.data.response,
          thinking: response.data.thinking,
          timestamp: new Date().toLocaleString(),
          type: 'chat'
        }, ...prev]);
      }

    } catch (error) {
      if (error.response?.status === 503) {
        message.error('AI服务连接失败，请检查配置和网络连接');
      } else {
        message.error(error.response?.data?.detail || 'AI对话失败');
      }
    } finally {
      setLoading(false);
    }
  };

  // 生成内容
  const generateContent = async (type, values, isBatch = false) => {
    try {
      setLoading(true);
      const params = {
        prompt: values.prompt,
        max_tokens: values.maxTokens || aiParams.max_tokens,
        temperature: values.temperature || aiParams.temperature,
        ...aiParams
      };

      if (isBatch && batchMode) {
        // 批量生成
        const results = [];
        for (let i = 0; i < batchCount; i++) {
          const response = await axios.post(`/api/v1/ai/generate-${type}`, params);
          results.push({
            id: Date.now() + i,
            content: response.data.content,
            thinking: response.data.thinking,
            type: type,
            timestamp: new Date().toLocaleString(),
            provider: currentProvider
          });

          // 保存思维过程
          if (response.data.thinking) {
            setThinkingHistory(prev => [{
              id: Date.now() + i + 1000,
              content: response.data.content,
              thinking: response.data.thinking,
              timestamp: new Date().toLocaleString(),
              type: type
            }, ...prev]);
          }
        }

        // 保存到历史记录
        setContentHistory(prev => [...results, ...prev]);
        setGeneratedContent(results[0].content);
        setCurrentThinking(results[0].thinking || '');
        message.success(`批量生成${batchCount}个${type}成功`);
        return results[0].content;
      } else {
        // 单个生成
        const response = await axios.post(`/api/v1/ai/generate-${type}`, params);
        const result = {
          id: Date.now(),
          content: response.data.content,
          thinking: response.data.thinking,
          type: type,
          timestamp: new Date().toLocaleString(),
          provider: currentProvider
        };

        // 保存到历史记录
        setContentHistory(prev => [result, ...prev]);
        setGeneratedContent(response.data.content);
        setCurrentThinking(response.data.thinking || '');

        // 保存思维过程
        if (response.data.thinking) {
          setThinkingHistory(prev => [{
            id: Date.now() + 1000,
            content: response.data.content,
            thinking: response.data.thinking,
            timestamp: new Date().toLocaleString(),
            type: type
          }, ...prev]);
        }

        message.success('内容生成成功');
        return response.data.content;
      }
    } catch (error) {
      if (error.response?.status === 503) {
        message.error('AI服务连接失败，请检查配置和网络连接');
      } else {
        message.error(error.response?.data?.detail || `生成${type}失败`);
      }
      return null;
    } finally {
      setLoading(false);
    }
  };

  // 保存内容到本地
  const saveContent = (content, filename) => {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename || `ai_content_${Date.now()}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    message.success('内容已保存到本地');
  };

  // 复制内容到剪贴板
  const copyToClipboard = (content) => {
    navigator.clipboard.writeText(content).then(() => {
      message.success('内容已复制到剪贴板');
    }).catch(() => {
      message.error('复制失败');
    });
  };

  // 加载模板
  const loadTemplates = () => {
    const defaultTemplates = [
      {
        id: 1,
        name: '玄幻世界设定',
        type: 'setting',
        content: '创建一个修仙世界，包含多个门派，有完整的修炼体系和等级划分...'
      },
      {
        id: 2,
        name: '现代都市背景',
        type: 'setting',
        content: '设定一个现代都市背景，包含商业、科技、社会结构...'
      },
      {
        id: 3,
        name: '主角人物模板',
        type: 'character',
        content: '创建一个年轻的主角，有特殊能力，性格坚韧不拔...'
      },
      {
        id: 4,
        name: '反派角色模板',
        type: 'character',
        content: '设计一个有深度的反派角色，有合理的动机和背景...'
      }
    ];
    setTemplates(defaultTemplates);
  };

  // 应用模板
  const applyTemplate = (template) => {
    if (template.type === 'setting') {
      generateForm.setFieldsValue({ prompt: template.content });
      setActiveTab('setting');
    } else if (template.type === 'character') {
      generateForm.setFieldsValue({ prompt: template.content });
      setActiveTab('character');
    }
    setShowTemplates(false);
    message.success(`已应用模板：${template.name}`);
  };

  // 滚动到消息底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    fetchProviders();
    fetchAIStatus();
    loadTemplates();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 状态指示器
  const StatusIndicator = () => (
    <Space>
      <Tag color={aiStatus.connected ? 'green' : 'red'}>
        {aiStatus.connected ? '在线' : '离线'}
      </Tag>
      <Text type="secondary">当前提供商: {currentProvider}</Text>
      <Button
        size="small"
        icon={<ReloadOutlined />}
        onClick={fetchAIStatus}
        loading={loading}
      >
        刷新状态
      </Button>
      <Button
        size="small"
        icon={<HistoryOutlined />}
        onClick={() => setShowHistory(true)}
      >
        历史记录 <Badge count={contentHistory.length} />
      </Button>
      <Button
        size="small"
        icon={<FileTextOutlined />}
        onClick={() => setShowTemplates(true)}
      >
        模板库
      </Button>
      <Button
        size="small"
        icon={<SettingOutlined />}
        onClick={() => setShowSettings(true)}
      >
        高级设置
      </Button>
      <Button
        size="small"
        icon={<BulbOutlined />}
        onClick={() => setShowThinking(true)}
        type={thinkingHistory.length > 0 ? 'primary' : 'default'}
      >
        思维过程 <Badge count={thinkingHistory.length} />
      </Button>
    </Space>
  );

  // AI参数设置面板
  const AISettingsPanel = () => (
    <Drawer
      title="AI高级参数设置"
      placement="right"
      onClose={() => setShowSettings(false)}
      open={showSettings}
      width={400}
    >
      <Form layout="vertical">
        <Form.Item label="温度参数 (Temperature)">
          <Slider
            min={0}
            max={2}
            step={0.1}
            value={aiParams.temperature}
            onChange={(value) => setAiParams(prev => ({ ...prev, temperature: value }))}
            marks={{
              0: '保守',
              0.7: '平衡',
              1.4: '创新',
              2: '随机'
            }}
          />
          <Text type="secondary">控制输出的随机性和创造性</Text>
        </Form.Item>

        <Form.Item label="最大Token数">
          <InputNumber
            min={100}
            max={8000}
            value={aiParams.max_tokens}
            onChange={(value) => setAiParams(prev => ({ ...prev, max_tokens: value }))}
            style={{ width: '100%' }}
          />
          <Text type="secondary">控制生成内容的长度</Text>
        </Form.Item>

        <Form.Item label="Top P">
          <Slider
            min={0}
            max={1}
            step={0.1}
            value={aiParams.top_p}
            onChange={(value) => setAiParams(prev => ({ ...prev, top_p: value }))}
            marks={{
              0: '0',
              0.5: '0.5',
              1: '1'
            }}
          />
          <Text type="secondary">控制词汇选择的多样性</Text>
        </Form.Item>

        <Form.Item label="频率惩罚 (Frequency Penalty)">
          <Slider
            min={-2}
            max={2}
            step={0.1}
            value={aiParams.frequency_penalty}
            onChange={(value) => setAiParams(prev => ({ ...prev, frequency_penalty: value }))}
            marks={{
              '-2': '-2',
              '0': '0',
              '2': '2'
            }}
          />
          <Text type="secondary">减少重复内容的出现</Text>
        </Form.Item>

        <Form.Item label="存在惩罚 (Presence Penalty)">
          <Slider
            min={-2}
            max={2}
            step={0.1}
            value={aiParams.presence_penalty}
            onChange={(value) => setAiParams(prev => ({ ...prev, presence_penalty: value }))}
            marks={{
              '-2': '-2',
              '0': '0',
              '2': '2'
            }}
          />
          <Text type="secondary">鼓励讨论新话题</Text>
        </Form.Item>

        <Divider />

        <Form.Item label="批量生成模式">
          <Space direction="vertical" style={{ width: '100%' }}>
            <Switch
              checked={batchMode}
              onChange={setBatchMode}
              checkedChildren="开启"
              unCheckedChildren="关闭"
            />
            {batchMode && (
              <InputNumber
                min={2}
                max={10}
                value={batchCount}
                onChange={setBatchCount}
                addonBefore="生成数量"
                style={{ width: '100%' }}
              />
            )}
          </Space>
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            block
            onClick={() => {
              message.success('参数设置已保存');
              setShowSettings(false);
            }}
          >
            保存设置
          </Button>
        </Form.Item>
      </Form>
    </Drawer>
  );

  // 历史记录面板
  const HistoryPanel = () => (
    <Modal
      title="生成历史记录"
      open={showHistory}
      onCancel={() => setShowHistory(false)}
      width={800}
      footer={[
        <Button key="clear" danger onClick={() => {
          setContentHistory([]);
          message.success('历史记录已清空');
        }}>
          清空记录
        </Button>,
        <Button key="close" onClick={() => setShowHistory(false)}>
          关闭
        </Button>
      ]}
    >
      <List
        dataSource={contentHistory}
        renderItem={(item) => (
          <List.Item
            actions={[
              <Button
                size="small"
                icon={<CopyOutlined />}
                onClick={() => copyToClipboard(item.content)}
              >
                复制
              </Button>,
              <Button
                size="small"
                icon={<DownloadOutlined />}
                onClick={() => saveContent(item.content, `${item.type}_${item.id}.txt`)}
              >
                下载
              </Button>,
              <Popconfirm
                title="确定删除这条记录吗？"
                onConfirm={() => {
                  setContentHistory(prev => prev.filter(h => h.id !== item.id));
                  message.success('记录已删除');
                }}
              >
                <Button size="small" danger icon={<DeleteOutlined />}>
                  删除
                </Button>
              </Popconfirm>
            ]}
          >
            <List.Item.Meta
              title={
                <Space>
                  <Tag color="blue">{item.type}</Tag>
                  <Text>{item.timestamp}</Text>
                  <Tag color="green">{item.provider}</Tag>
                </Space>
              }
              description={
                <Paragraph
                  ellipsis={{ rows: 3, expandable: true }}
                  style={{ marginBottom: 0 }}
                >
                  {item.content}
                </Paragraph>
              }
            />
          </List.Item>
        )}
        locale={{ emptyText: '暂无生成记录' }}
      />
    </Modal>
  );

  // 模板库面板
  const TemplatePanel = () => (
    <Modal
      title="模板库"
      open={showTemplates}
      onCancel={() => setShowTemplates(false)}
      width={600}
      footer={[
        <Button key="close" onClick={() => setShowTemplates(false)}>
          关闭
        </Button>
      ]}
    >
      <List
        dataSource={templates}
        renderItem={(template) => (
          <List.Item
            actions={[
              <Button
                type="primary"
                size="small"
                onClick={() => applyTemplate(template)}
              >
                应用模板
              </Button>
            ]}
          >
            <List.Item.Meta
              title={
                <Space>
                  <Text strong>{template.name}</Text>
                  <Tag color="blue">{template.type}</Tag>
                </Space>
              }
              description={
                <Paragraph
                  ellipsis={{ rows: 2, expandable: true }}
                  style={{ marginBottom: 0 }}
                >
                  {template.content}
                </Paragraph>
              }
            />
          </List.Item>
        )}
      />
    </Modal>
  );

  // 思维链面板
  const ThinkingPanel = () => (
    <Modal
      title="AI思维过程"
      open={showThinking}
      onCancel={() => setShowThinking(false)}
      width={900}
      footer={[
        <Button key="clear" danger onClick={() => {
          setThinkingHistory([]);
          setCurrentThinking('');
          message.success('思维记录已清空');
        }}>
          清空记录
        </Button>,
        <Button key="close" onClick={() => setShowThinking(false)}>
          关闭
        </Button>
      ]}
    >
      {currentThinking && (
        <Card
          title="当前思维过程"
          size="small"
          style={{ marginBottom: 16 }}
          extra={
            <Button
              size="small"
              icon={<CopyOutlined />}
              onClick={() => copyToClipboard(currentThinking)}
            >
              复制
            </Button>
          }
        >
          <Paragraph style={{
            backgroundColor: '#f0f8ff',
            padding: '12px',
            borderRadius: '6px',
            fontFamily: 'monospace',
            fontSize: '13px',
            whiteSpace: 'pre-wrap'
          }}>
            {currentThinking}
          </Paragraph>
        </Card>
      )}

      <List
        dataSource={thinkingHistory}
        renderItem={(item) => (
          <List.Item
            actions={[
              <Button
                size="small"
                icon={<CopyOutlined />}
                onClick={() => copyToClipboard(item.thinking)}
              >
                复制思维
              </Button>,
              <Button
                size="small"
                icon={<CopyOutlined />}
                onClick={() => copyToClipboard(item.content)}
              >
                复制结果
              </Button>,
              <Button
                size="small"
                icon={<DownloadOutlined />}
                onClick={() => saveContent(
                  `思维过程：\n${item.thinking}\n\n生成结果：\n${item.content}`,
                  `thinking_${item.id}.txt`
                )}
              >
                下载
              </Button>
            ]}
          >
            <List.Item.Meta
              title={
                <Space>
                  <Tag color="purple">思维链</Tag>
                  <Tag color="blue">{item.type}</Tag>
                  <Text type="secondary">{item.timestamp}</Text>
                </Space>
              }
              description={
                <div>
                  <div style={{ marginBottom: 8 }}>
                    <Text strong>思维过程：</Text>
                    <Paragraph
                      ellipsis={{ rows: 3, expandable: true }}
                      style={{
                        backgroundColor: '#f0f8ff',
                        padding: '8px',
                        borderRadius: '4px',
                        marginTop: 4,
                        fontFamily: 'monospace',
                        fontSize: '12px'
                      }}
                    >
                      {item.thinking}
                    </Paragraph>
                  </div>
                  <div>
                    <Text strong>生成结果：</Text>
                    <Paragraph
                      ellipsis={{ rows: 2, expandable: true }}
                      style={{ marginTop: 4 }}
                    >
                      {item.content}
                    </Paragraph>
                  </div>
                </div>
              }
            />
          </List.Item>
        )}
        locale={{ emptyText: '暂无思维记录' }}
      />
    </Modal>
  );

  // 聊天界面
  const ChatInterface = () => (
    <div style={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', border: '1px solid #d9d9d9', borderRadius: '6px' }}>
        {messages.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#999', marginTop: '100px' }}>
            <RobotOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
            <div>开始与AI助手对话吧！</div>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: '16px' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start' }}>
                {msg.role === 'user' ? (
                  <UserOutlined style={{ marginRight: '8px', marginTop: '4px' }} />
                ) : (
                  <RobotOutlined style={{ marginRight: '8px', marginTop: '4px', color: '#1890ff' }} />
                )}
                <div style={{ flex: 1 }}>
                  <Text strong>{msg.role === 'user' ? '用户' : 'AI助手'}</Text>
                  <Paragraph style={{ marginTop: '4px', marginBottom: 0 }}>
                    {msg.content}
                  </Paragraph>
                  {msg.thinking && (
                    <div style={{ marginTop: '8px' }}>
                      <Button
                        size="small"
                        type="link"
                        icon={<BulbOutlined />}
                        onClick={() => {
                          setCurrentThinking(msg.thinking);
                          setShowThinking(true);
                        }}
                      >
                        查看思维过程
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div style={{ textAlign: 'center', padding: '16px' }}>
            <Spin /> <Text type="secondary">AI正在思考中...</Text>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div style={{ marginTop: '16px' }}>
        <Input.Group compact>
          <Input
            style={{ width: 'calc(100% - 80px)' }}
            placeholder="输入您的问题..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onPressEnter={sendMessage}
            disabled={loading || !aiStatus.connected}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={sendMessage}
            loading={loading}
            disabled={!aiStatus.connected}
          >
            发送
          </Button>
        </Input.Group>
      </div>
    </div>
  );

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">AI助手</Title>
        <StatusIndicator />
      </div>

      <Row gutter={[16, 16]}>
        <Col span={18}>
          <Card>
            <Tabs activeKey={activeTab} onChange={setActiveTab}>
              <TabPane tab={<span><MessageOutlined />智能对话</span>} key="chat">
                <ChatInterface />
              </TabPane>

              <TabPane tab={<span><BulbOutlined />设定生成</span>} key="setting">
                <Form
                  form={generateForm}
                  layout="vertical"
                  onFinish={(values) => generateContent('setting', values, batchMode)}
                >
                  <Form.Item
                    name="prompt"
                    label="生成要求"
                    rules={[{ required: true, message: '请输入生成要求' }]}
                  >
                    <TextArea
                      rows={4}
                      placeholder="请描述您想要生成的世界设定，例如：一个修仙世界，有多个门派..."
                    />
                  </Form.Item>

                  <Row gutter={16}>
                    <Col span={12}>
                      <Form.Item name="maxTokens" label="最大字数" initialValue={2000}>
                        <Select>
                          <Option value={1000}>1000字</Option>
                          <Option value={2000}>2000字</Option>
                          <Option value={3000}>3000字</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col span={12}>
                      <Form.Item name="temperature" label="创意度" initialValue={0.7}>
                        <Select>
                          <Option value={0.3}>保守</Option>
                          <Option value={0.7}>平衡</Option>
                          <Option value={0.9}>创新</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                  </Row>

                  <Form.Item>
                    <Space>
                      <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={!aiStatus.connected}
                        icon={batchMode ? <ThunderboltOutlined /> : <BulbOutlined />}
                      >
                        {batchMode ? `批量生成(${batchCount}个)` : '生成世界设定'}
                      </Button>
                      {generatedContent && (
                        <>
                          <Button
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(generatedContent)}
                          >
                            复制
                          </Button>
                          <Button
                            icon={<DownloadOutlined />}
                            onClick={() => saveContent(generatedContent, 'setting.txt')}
                          >
                            下载
                          </Button>
                          {currentThinking && (
                            <Button
                              icon={<BulbOutlined />}
                              onClick={() => setShowThinking(true)}
                            >
                              思维过程
                            </Button>
                          )}
                        </>
                      )}
                    </Space>
                  </Form.Item>

                  {generatedContent && (
                    <Form.Item label="生成结果">
                      <TextArea
                        value={generatedContent}
                        rows={8}
                        readOnly
                        style={{ backgroundColor: '#f5f5f5' }}
                      />
                    </Form.Item>
                  )}
                </Form>
              </TabPane>

              <TabPane tab={<span><UserOutlined />人物生成</span>} key="character">
                <Form
                  layout="vertical"
                  onFinish={(values) => generateContent('character', values, batchMode)}
                >
                  <Form.Item
                    name="prompt"
                    label="人物要求"
                    rules={[{ required: true, message: '请输入人物要求' }]}
                  >
                    <TextArea
                      rows={4}
                      placeholder="请描述您想要生成的人物，例如：一个年轻的剑修，性格冷傲..."
                    />
                  </Form.Item>

                  <Row gutter={16}>
                    <Col span={12}>
                      <Form.Item name="maxTokens" label="最大字数" initialValue={2000}>
                        <Select>
                          <Option value={1000}>1000字</Option>
                          <Option value={2000}>2000字</Option>
                          <Option value={3000}>3000字</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col span={12}>
                      <Form.Item name="temperature" label="创意度" initialValue={0.7}>
                        <Select>
                          <Option value={0.3}>保守</Option>
                          <Option value={0.7}>平衡</Option>
                          <Option value={0.9}>创新</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                  </Row>

                  <Form.Item>
                    <Space>
                      <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={!aiStatus.connected}
                        icon={batchMode ? <ThunderboltOutlined /> : <UserOutlined />}
                      >
                        {batchMode ? `批量生成(${batchCount}个)` : '生成人物设定'}
                      </Button>
                      {generatedContent && (
                        <>
                          <Button
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(generatedContent)}
                          >
                            复制
                          </Button>
                          <Button
                            icon={<DownloadOutlined />}
                            onClick={() => saveContent(generatedContent, 'character.txt')}
                          >
                            下载
                          </Button>
                        </>
                      )}
                    </Space>
                  </Form.Item>

                  {generatedContent && (
                    <Form.Item label="生成结果">
                      <TextArea
                        value={generatedContent}
                        rows={8}
                        readOnly
                        style={{ backgroundColor: '#f5f5f5' }}
                      />
                    </Form.Item>
                  )}
                </Form>
              </TabPane>

              <TabPane tab={<span><BookOutlined />剧情生成</span>} key="plot">
                <Form
                  form={plotForm}
                  layout="vertical"
                  onFinish={(values) => generateContent('plot', values, batchMode)}
                >
                  <Form.Item
                    name="prompt"
                    label="剧情要求"
                    rules={[{ required: true, message: '请输入剧情要求' }]}
                  >
                    <TextArea
                      rows={4}
                      placeholder="请描述您想要生成的剧情，例如：主角在修仙门派中遇到的第一个挑战..."
                    />
                  </Form.Item>

                  <Row gutter={16}>
                    <Col span={8}>
                      <Form.Item name="maxTokens" label="最大字数" initialValue={3000}>
                        <Select>
                          <Option value={2000}>2000字</Option>
                          <Option value={3000}>3000字</Option>
                          <Option value={5000}>5000字</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col span={8}>
                      <Form.Item name="temperature" label="创意度" initialValue={0.8}>
                        <Select>
                          <Option value={0.5}>保守</Option>
                          <Option value={0.8}>平衡</Option>
                          <Option value={1.0}>创新</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col span={8}>
                      <Form.Item name="plotType" label="剧情类型" initialValue="adventure">
                        <Select>
                          <Option value="adventure">冒险</Option>
                          <Option value="romance">爱情</Option>
                          <Option value="conflict">冲突</Option>
                          <Option value="mystery">悬疑</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                  </Row>

                  <Form.Item>
                    <Space>
                      <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={!aiStatus.connected}
                        icon={batchMode ? <ThunderboltOutlined /> : <BookOutlined />}
                      >
                        {batchMode ? `批量生成(${batchCount}个)` : '生成剧情大纲'}
                      </Button>
                      {generatedContent && (
                        <>
                          <Button
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(generatedContent)}
                          >
                            复制
                          </Button>
                          <Button
                            icon={<DownloadOutlined />}
                            onClick={() => saveContent(generatedContent, 'plot.txt')}
                          >
                            下载
                          </Button>
                        </>
                      )}
                    </Space>
                  </Form.Item>

                  {generatedContent && (
                    <Form.Item label="生成结果">
                      <TextArea
                        value={generatedContent}
                        rows={8}
                        readOnly
                        style={{ backgroundColor: '#f5f5f5' }}
                      />
                    </Form.Item>
                  )}
                </Form>
              </TabPane>

              <TabPane tab={<span><EditOutlined />续写功能</span>} key="continue">
                <Form
                  form={continueForm}
                  layout="vertical"
                  onFinish={(values) => {
                    const prompt = values.continueHint
                      ? `${values.prompt}\n\n续写提示：${values.continueHint}`
                      : values.prompt;
                    generateContent('continue-writing', { ...values, prompt });
                  }}
                >
                  <Form.Item
                    name="prompt"
                    label="原文内容"
                    rules={[{ required: true, message: '请输入需要续写的原文内容' }]}
                  >
                    <TextArea
                      rows={6}
                      placeholder="请粘贴需要续写的原文内容..."
                    />
                  </Form.Item>

                  <Form.Item
                    name="continueHint"
                    label="续写提示（可选）"
                  >
                    <TextArea
                      rows={2}
                      placeholder="可以提供续写的方向提示，例如：接下来主角遇到了..."
                    />
                  </Form.Item>

                  <Row gutter={16}>
                    <Col span={12}>
                      <Form.Item name="maxTokens" label="续写长度" initialValue={2000}>
                        <Select>
                          <Option value={1000}>短篇(1000字)</Option>
                          <Option value={2000}>中篇(2000字)</Option>
                          <Option value={3000}>长篇(3000字)</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                    <Col span={12}>
                      <Form.Item name="temperature" label="创意度" initialValue={0.7}>
                        <Select>
                          <Option value={0.5}>保守</Option>
                          <Option value={0.7}>平衡</Option>
                          <Option value={0.9}>创新</Option>
                        </Select>
                      </Form.Item>
                    </Col>
                  </Row>

                  <Form.Item>
                    <Space>
                      <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={!aiStatus.connected}
                        icon={<EditOutlined />}
                      >
                        AI续写
                      </Button>
                      {generatedContent && (
                        <>
                          <Button
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(generatedContent)}
                          >
                            复制
                          </Button>
                          <Button
                            icon={<DownloadOutlined />}
                            onClick={() => saveContent(generatedContent, 'continue.txt')}
                          >
                            下载
                          </Button>
                        </>
                      )}
                    </Space>
                  </Form.Item>

                  {generatedContent && (
                    <Form.Item label="续写结果">
                      <TextArea
                        value={generatedContent}
                        rows={8}
                        readOnly
                        style={{ backgroundColor: '#f5f5f5' }}
                      />
                    </Form.Item>
                  )}
                </Form>
              </TabPane>

              <TabPane tab={<span><CheckCircleOutlined />一致性检查</span>} key="check">
                <Form
                  form={checkForm}
                  layout="vertical"
                  onFinish={(values) => {
                    const prompt = `检查类型：${values.checkType}\n\n内容：\n${values.prompt}`;
                    generateContent('check-consistency', { ...values, prompt });
                  }}
                >
                  <Form.Item
                    name="prompt"
                    label="检查内容"
                    rules={[{ required: true, message: '请输入需要检查的内容' }]}
                  >
                    <TextArea
                      rows={8}
                      placeholder="请粘贴需要进行一致性检查的小说内容..."
                    />
                  </Form.Item>

                  <Form.Item
                    name="checkType"
                    label="检查类型"
                    initialValue="all"
                  >
                    <Select>
                      <Option value="all">全面检查</Option>
                      <Option value="character">人物一致性</Option>
                      <Option value="plot">情节逻辑</Option>
                      <Option value="setting">设定一致性</Option>
                      <Option value="timeline">时间线</Option>
                    </Select>
                  </Form.Item>

                  <Form.Item>
                    <Space>
                      <Button
                        type="primary"
                        htmlType="submit"
                        loading={loading}
                        disabled={!aiStatus.connected}
                        icon={<CheckCircleOutlined />}
                      >
                        开始检查
                      </Button>
                      {generatedContent && (
                        <>
                          <Button
                            icon={<CopyOutlined />}
                            onClick={() => copyToClipboard(generatedContent)}
                          >
                            复制
                          </Button>
                          <Button
                            icon={<DownloadOutlined />}
                            onClick={() => saveContent(generatedContent, 'check_report.txt')}
                          >
                            下载报告
                          </Button>
                        </>
                      )}
                    </Space>
                  </Form.Item>

                  {generatedContent && (
                    <Form.Item label="检查报告">
                      <TextArea
                        value={generatedContent}
                        rows={8}
                        readOnly
                        style={{ backgroundColor: '#f5f5f5' }}
                      />
                    </Form.Item>
                  )}
                </Form>
              </TabPane>
            </Tabs>
          </Card>
        </Col>

        <Col span={6}>
          <Card title="AI设置" size="small">
            <div style={{ marginBottom: '16px' }}>
              <Text strong>AI提供商</Text>
              <Select
                style={{ width: '100%', marginTop: '8px' }}
                value={currentProvider}
                onChange={switchProvider}
                loading={loading}
              >
                {providers.map(provider => (
                  <Option key={provider} value={provider}>
                    {provider.toUpperCase()}
                  </Option>
                ))}
              </Select>
            </div>

            <Divider />

            <div>
              <Text strong>快速操作</Text>
              <div style={{ marginTop: '8px' }}>
                <Button
                  block
                  style={{ marginBottom: '8px' }}
                  onClick={() => setMessages([])}
                >
                  清空对话
                </Button>
                <Button
                  block
                  onClick={fetchAIStatus}
                  loading={loading}
                >
                  检查连接
                </Button>
              </div>
            </div>
          </Card>

          {!aiStatus.connected && (
            <Alert
              style={{ marginTop: '16px' }}
              message="AI服务离线"
              description="请检查AI服务配置或网络连接"
              type="warning"
              showIcon
            />
          )}
        </Col>
      </Row>

      {/* 新增的组件 */}
      <AISettingsPanel />
      <HistoryPanel />
      <TemplatePanel />
      <ThinkingPanel />
    </div>
  );
};

export default AIAssistant;
