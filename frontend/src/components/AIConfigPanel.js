import React, { useState, useEffect } from 'react';
import {
  Card,
  Form,
  Input,
  Select,
  Button,
  Space,
  Tag,
  Alert,
  Row,
  Col,
  Divider,
  Typography,
  Switch,
  InputNumber,
  message,
  Tooltip
} from 'antd';
import {
  RobotOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  ReloadOutlined,
  SaveOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone,
  InfoCircleOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;

// AI提供商配置信息
const AI_PROVIDERS = {
  openai: {
    name: 'OpenAI',
    icon: '🤖',
    color: '#10a37f',
    description: '最先进的GPT模型',
    models: ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'gpt-4o'],
    fields: ['api_key', 'base_url', 'model']
  },
  claude: {
    name: 'Claude',
    icon: '🧠',
    color: '#ff6b35',
    description: 'Anthropic的Claude模型',
    models: ['claude-3-haiku-20240307', 'claude-3-sonnet-20240229', 'claude-3-opus-20240229'],
    fields: ['api_key', 'base_url', 'model']
  },
  zhipu: {
    name: '智谱AI',
    icon: '🇨🇳',
    color: '#1890ff',
    description: '国产优秀大语言模型',
    models: ['glm-4', 'glm-3-turbo', 'chatglm3-6b'],
    fields: ['api_key', 'base_url', 'model']
  },
  siliconflow: {
    name: '硅基流动',
    icon: '⚡',
    color: '#722ed1',
    description: '高性能AI推理平台',
    models: ['deepseek-chat', 'qwen-turbo', 'yi-large'],
    fields: ['api_key', 'base_url', 'model']
  },
  google: {
    name: 'Google AI',
    icon: '🔍',
    color: '#4285f4',
    description: 'Google的Gemini模型',
    models: ['gemini-pro', 'gemini-pro-vision', 'gemini-ultra'],
    fields: ['api_key', 'base_url', 'model']
  },
  grok: {
    name: 'Grok',
    icon: '🚀',
    color: '#1da1f2',
    description: 'xAI的Grok模型',
    models: ['grok-beta', 'grok-1'],
    fields: ['api_key', 'base_url', 'model']
  },
  ollama: {
    name: 'Ollama',
    icon: '🏠',
    color: '#52c41a',
    description: '本地部署开源模型',
    models: ['mollysama/rwkv-7-g1:0.4B', 'llama2', 'mistral', 'codellama', 'qwen'],
    fields: ['base_url', 'model']
  },
  custom: {
    name: '自定义',
    icon: '⚙️',
    color: '#8c8c8c',
    description: 'OpenAI兼容接口',
    models: [],
    fields: ['api_key', 'base_url', 'model']
  }
};

const AIConfigPanel = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [currentProvider, setCurrentProvider] = useState('ollama');
  const [aiStatus, setAiStatus] = useState({ connected: false, status: 'offline' });
  const [providers, setProviders] = useState([]);
  const [ollamaModels, setOllamaModels] = useState([]);
  const [loadingOllamaModels, setLoadingOllamaModels] = useState(false);

  // 获取Ollama模型列表
  const fetchOllamaModels = async () => {
    try {
      setLoadingOllamaModels(true);
      const response = await axios.get('/api/ai/ollama/models');
      console.log('Ollama models response:', response.data);

      const data = response.data;

      if (data.status === 'error') {
        // 显示详细的错误信息和建议
        message.error({
          content: (
            <div>
              <div>Ollama连接失败</div>
              <div style={{ fontSize: '12px', marginTop: '4px' }}>
                {data.suggestions?.slice(0, 2).map((suggestion, index) => (
                  <div key={index}>• {suggestion}</div>
                ))}
              </div>
            </div>
          ),
          duration: 8
        });
        setOllamaModels([]);
        AI_PROVIDERS.ollama.models = [];
        return [];
      }

      const models = data.models.map(model => ({
        name: model.name,
        size: model.size,
        modified_at: model.modified_at
      }));

      setOllamaModels(models);

      // 更新AI_PROVIDERS中的ollama模型列表
      AI_PROVIDERS.ollama.models = models.map(model => model.name);

      if (models.length === 0) {
        message.info({
          content: (
            <div>
              <div>未检测到本地Ollama模型</div>
              <div style={{ fontSize: '12px', marginTop: '4px' }}>
                使用 ollama pull llama2 下载模型
              </div>
            </div>
          ),
          duration: 6
        });
      } else {
        message.success(`检测到 ${models.length} 个本地模型`);
      }

      return models;
    } catch (error) {
      console.error('获取Ollama模型失败:', error);
      message.error({
        content: (
          <div>
            <div>无法连接Ollama服务</div>
            <div style={{ fontSize: '12px', marginTop: '4px' }}>
              请确保Ollama已安装并正在运行
            </div>
          </div>
        ),
        duration: 8
      });
      setOllamaModels([]);
      AI_PROVIDERS.ollama.models = [];
      return [];
    } finally {
      setLoadingOllamaModels(false);
    }
  };

  // 测试Ollama连接
  const testOllamaConnection = async () => {
    try {
      setLoadingOllamaModels(true);
      const response = await axios.get('/api/ai/ollama/test-connection');
      const data = response.data;

      if (data.connected) {
        message.success({
          content: (
            <div>
              <div>Ollama连接成功</div>
              <div style={{ fontSize: '12px', marginTop: '4px' }}>
                检测到 {data.models_count} 个模型
              </div>
            </div>
          ),
          duration: 5
        });

        // 连接成功后自动刷新模型列表
        await fetchOllamaModels();
      } else {
        message.error({
          content: (
            <div>
              <div>Ollama连接失败</div>
              <div style={{ fontSize: '12px', marginTop: '4px' }}>
                {data.suggestions?.slice(0, 2).map((suggestion, index) => (
                  <div key={index}>• {suggestion}</div>
                ))}
              </div>
            </div>
          ),
          duration: 8
        });
      }
    } catch (error) {
      console.error('测试Ollama连接失败:', error);
      message.error({
        content: (
          <div>
            <div>连接测试失败</div>
            <div style={{ fontSize: '12px', marginTop: '4px' }}>
              请检查Ollama服务是否正在运行
            </div>
          </div>
        ),
        duration: 8
      });
    } finally {
      setLoadingOllamaModels(false);
    }
  };

  // 获取AI信息
  const fetchAIInfo = async () => {
    console.log('Fetching AI info...');
    try {
      const [providersRes, statusRes] = await Promise.all([
        axios.get('/api/ai/providers'),
        axios.get('/api/ai/status')
      ]);

      console.log('Providers response:', providersRes.data);
      console.log('Status response:', statusRes.data);

      setProviders(providersRes.data.providers);
      setCurrentProvider(providersRes.data.current);
      setAiStatus(statusRes.data);

      // 如果当前提供商是ollama，获取模型列表
      if (providersRes.data.current === 'ollama') {
        await fetchOllamaModels();
      }

      // 获取当前提供商的配置
      if (providersRes.data.current) {
        try {
          const configRes = await axios.get(`/api/ai/config/${providersRes.data.current}`);
          console.log('Current provider config:', configRes.data);
          form.setFieldsValue(configRes.data.config);
        } catch (error) {
          console.warn('获取配置失败:', error);
        }
      }
    } catch (error) {
      console.error('获取AI信息失败:', error);
      message.error('获取AI信息失败');
    }
  };

  // 测试连接
  const testConnection = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/ai/status');
      setAiStatus(response.data);

      if (response.data.connected) {
        message.success('连接测试成功');
      } else {
        message.warning('连接测试失败');
      }
    } catch (error) {
      message.error('连接测试失败');
    } finally {
      setLoading(false);
    }
  };

  // 切换提供商
  const switchProvider = async (provider) => {
    console.log('Switching to provider:', provider);
    try {
      setLoading(true);

      const response = await axios.post('/api/ai/switch-provider', { provider });
      console.log('Switch provider response:', response.data);

      setCurrentProvider(provider);
      message.success(`已切换到 ${AI_PROVIDERS[provider]?.name || provider}`);

      // 如果切换到ollama，先获取模型列表
      if (provider === 'ollama') {
        await fetchOllamaModels();
      }

      // 加载新提供商的配置
      try {
        const configRes = await axios.get(`/api/ai/config/${provider}`);
        console.log('Config loaded:', configRes.data);
        form.setFieldsValue(configRes.data.config);
      } catch (error) {
        console.warn('获取配置失败:', error);
        // 重置表单为默认值
        const defaultValues = {
          max_tokens: 2000,
          temperature: 0.7,
          enabled: true
        };

        // 为Ollama设置默认值
        if (provider === 'ollama') {
          defaultValues.model = 'mollysama/rwkv-7-g1:0.4B';
          defaultValues.base_url = 'http://localhost:11434';
        }

        console.log('Setting default values:', defaultValues);
        form.setFieldsValue(defaultValues);
      }

      await fetchAIInfo();
    } catch (error) {
      console.error('切换提供商失败:', error);
      message.error(`切换提供商失败: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // 保存配置
  const saveConfig = async (values) => {
    try {
      setLoading(true);
      await axios.post('/api/ai/config', {
        provider: currentProvider,
        config: values
      });
      message.success('配置保存成功');
      await fetchAIInfo();
    } catch (error) {
      console.error('配置保存失败:', error);
      message.error('配置保存失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAIInfo();
  }, []);

  // 提供商选择卡片
  const ProviderCard = ({ provider, isActive, onClick, disabled = false }) => {
    const config = AI_PROVIDERS[provider];

    const handleClick = () => {
      if (disabled) return;
      console.log('Provider card clicked:', provider);
      onClick(provider);
    };

    return (
      <Card
        size="small"
        hoverable={!disabled}
        className={`provider-card ${isActive ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
        onClick={handleClick}
        style={{
          borderColor: isActive ? config.color : '#d9d9d9',
          backgroundColor: isActive ? `${config.color}10` : disabled ? '#f5f5f5' : '#fff',
          cursor: disabled ? 'not-allowed' : 'pointer',
          transition: 'all 0.3s',
          minHeight: '120px',
          border: isActive ? `2px solid ${config.color}` : '1px solid #d9d9d9',
          opacity: disabled ? 0.6 : 1
        }}
      >
        <div style={{ textAlign: 'center', padding: '8px' }}>
          <div style={{ fontSize: '24px', marginBottom: '8px' }}>
            {config.icon}
          </div>
          <div style={{
            fontWeight: 'bold',
            color: disabled ? '#999' : config.color,
            marginBottom: '4px'
          }}>
            {config.name}
          </div>
          <div style={{
            fontSize: '12px',
            color: disabled ? '#999' : '#666',
            lineHeight: '1.4'
          }}>
            {config.description}
          </div>
          {isActive && !disabled && (
            <div style={{ marginTop: '8px' }}>
              <Tag color={config.color} size="small">当前选择</Tag>
            </div>
          )}
          {disabled && (
            <div style={{ marginTop: '8px' }}>
              <Tag color="default" size="small">加载中...</Tag>
            </div>
          )}
        </div>
      </Card>
    );
  };

  // 状态指示器
  const StatusIndicator = () => (
    <div style={{ textAlign: 'center', padding: '16px' }}>
      <div style={{ marginBottom: '12px' }}>
        <Tag
          color={aiStatus.connected ? 'green' : 'red'}
          icon={aiStatus.connected ? <CheckCircleOutlined /> : <ExclamationCircleOutlined />}
          style={{ fontSize: '14px', padding: '4px 12px' }}
        >
          {aiStatus.connected ? '在线' : '离线'}
        </Tag>
      </div>
      <div style={{ marginBottom: '12px' }}>
        <Text type="secondary">当前提供商</Text>
        <br />
        <Text strong style={{ color: AI_PROVIDERS[currentProvider]?.color }}>
          {AI_PROVIDERS[currentProvider]?.icon} {AI_PROVIDERS[currentProvider]?.name}
        </Text>
      </div>
      <Button
        type="primary"
        icon={<ReloadOutlined />}
        onClick={testConnection}
        loading={loading}
        size="small"
      >
        测试连接
      </Button>
    </div>
  );

  const currentConfig = AI_PROVIDERS[currentProvider];

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* 状态概览 */}
      <Card style={{ marginBottom: '24px' }}>
        <Row gutter={24} align="middle">
          <Col span={18}>
            <Space size="large">
              <div>
                <RobotOutlined style={{ fontSize: '32px', color: currentConfig?.color }} />
              </div>
              <div>
                <Title level={4} style={{ margin: 0 }}>AI配置管理</Title>
                <Text type="secondary">配置和管理多种AI提供商</Text>
              </div>
            </Space>
          </Col>
          <Col span={6}>
            <StatusIndicator />
          </Col>
        </Row>
      </Card>

      <Row gutter={24}>
        {/* 提供商选择 */}
        <Col span={16}>
          <Card
            title={
              <Space>
                选择AI提供商
                <Tag color="blue">{Object.keys(AI_PROVIDERS).length} 个可用</Tag>
              </Space>
            }
            style={{ marginBottom: '24px' }}
            extra={
              <Button
                size="small"
                onClick={fetchAIInfo}
                loading={loading}
                icon={<ReloadOutlined />}
              >
                刷新
              </Button>
            }
          >
            {loading ? (
              <div style={{ textAlign: 'center', padding: '40px' }}>
                <Space direction="vertical">
                  <div>正在加载AI提供商...</div>
                </Space>
              </div>
            ) : (
              <Row gutter={[16, 16]}>
                {Object.keys(AI_PROVIDERS).map(provider => (
                  <Col span={6} key={provider}>
                    <ProviderCard
                      provider={provider}
                      isActive={currentProvider === provider}
                      onClick={switchProvider}
                      disabled={loading}
                    />
                  </Col>
                ))}
              </Row>
            )}
          </Card>

          {/* 配置表单 */}
          <Card title={`${currentConfig?.name} 配置`}>
            <Form
              form={form}
              layout="vertical"
              onFinish={saveConfig}
              initialValues={{
                max_tokens: 2000,
                temperature: 0.7,
                enabled: true,
                model: currentProvider === 'ollama' ? 'mollysama/rwkv-7-g1:0.4B' : undefined,
                base_url: currentProvider === 'ollama' ? 'http://localhost:11434' : undefined
              }}
            >
              {/* API Key */}
              {currentConfig?.fields.includes('api_key') && (
                <Form.Item
                  name="api_key"
                  label={
                    <Space>
                      API Key
                      <Tooltip title="从对应平台获取的API密钥">
                        <InfoCircleOutlined />
                      </Tooltip>
                    </Space>
                  }
                >
                  <Input.Password
                    placeholder={`请输入${currentConfig.name} API Key`}
                    iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                  />
                </Form.Item>
              )}

              {/* Base URL */}
              {currentConfig?.fields.includes('base_url') && (
                <Form.Item
                  name="base_url"
                  label="API地址"
                >
                  <Input placeholder="API服务地址" />
                </Form.Item>
              )}

              {/* 模型选择 */}
              {currentConfig?.fields.includes('model') && (
                <Form.Item
                  name="model"
                  label={
                    <Space>
                      模型
                      {currentProvider === 'ollama' && (
                        <Space>
                          <Button
                            type="link"
                            size="small"
                            icon={<ReloadOutlined />}
                            onClick={fetchOllamaModels}
                            loading={loadingOllamaModels}
                            style={{ padding: 0 }}
                          >
                            刷新
                          </Button>
                          <Button
                            type="link"
                            size="small"
                            onClick={testOllamaConnection}
                            style={{ padding: 0 }}
                          >
                            测试连接
                          </Button>
                        </Space>
                      )}
                    </Space>
                  }
                >
                  <Select
                    placeholder={currentProvider === 'ollama' ? "选择本地模型" : "选择模型"}
                    loading={currentProvider === 'ollama' && loadingOllamaModels}
                    notFoundContent={
                      currentProvider === 'ollama'
                        ? (loadingOllamaModels ? "加载中..." : "未找到本地模型，请先下载模型")
                        : "未找到模型"
                    }
                  >
                    {currentProvider === 'ollama' ? (
                      ollamaModels.map(model => (
                        <Option key={model.name} value={model.name}>
                          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span>{model.name}</span>
                            <Text type="secondary" style={{ fontSize: '12px' }}>
                              {(model.size / (1024 * 1024 * 1024)).toFixed(1)}GB
                            </Text>
                          </div>
                        </Option>
                      ))
                    ) : (
                      currentConfig.models.map(model => (
                        <Option key={model} value={model}>{model}</Option>
                      ))
                    )}
                  </Select>
                </Form.Item>
              )}

              <Divider />

              {/* 通用参数 */}
              <Row gutter={16}>
                <Col span={8}>
                  <Form.Item name="max_tokens" label="最大Token数">
                    <InputNumber
                      min={100}
                      max={8000}
                      style={{ width: '100%' }}
                      placeholder="2000"
                    />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="temperature" label="温度参数">
                    <InputNumber
                      min={0}
                      max={2}
                      step={0.1}
                      style={{ width: '100%' }}
                      placeholder="0.7"
                    />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="enabled" label="启用" valuePropName="checked">
                    <Switch />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item>
                <Button
                  type="primary"
                  htmlType="submit"
                  icon={<SaveOutlined />}
                  loading={loading}
                  size="large"
                >
                  保存配置
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        {/* 侧边栏信息 */}
        <Col span={8}>
          <Card title="使用说明" size="small" style={{ marginBottom: '16px' }}>
            <div style={{ fontSize: '12px', lineHeight: '1.8' }}>
              <p><strong>{currentConfig?.icon} {currentConfig?.name}</strong></p>
              <p>{currentConfig?.description}</p>

              {currentProvider === 'openai' && (
                <div>
                  <p>• 访问 <a href="https://platform.openai.com/" target="_blank" rel="noopener noreferrer">OpenAI官网</a> 获取API Key</p>
                  <p>• 支持GPT-3.5和GPT-4系列模型</p>
                </div>
              )}

              {currentProvider === 'claude' && (
                <div>
                  <p>• 访问 <a href="https://console.anthropic.com/" target="_blank" rel="noopener noreferrer">Anthropic官网</a> 获取API Key</p>
                  <p>• 支持Claude 3系列模型</p>
                </div>
              )}

              {currentProvider === 'zhipu' && (
                <div>
                  <p>• 访问 <a href="https://open.bigmodel.cn/" target="_blank" rel="noopener noreferrer">智谱AI官网</a> 获取API Key</p>
                  <p>• 国产优秀大语言模型</p>
                </div>
              )}

              {currentProvider === 'siliconflow' && (
                <div>
                  <p>• 访问 <a href="https://siliconflow.cn/" target="_blank" rel="noopener noreferrer">硅基流动官网</a> 获取API Key</p>
                  <p>• 高性能AI推理平台</p>
                  <p>• 支持多种开源模型</p>
                </div>
              )}

              {currentProvider === 'google' && (
                <div>
                  <p>• 访问 <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer">Google AI Studio</a> 获取API Key</p>
                  <p>• 支持Gemini系列模型</p>
                  <p>• 多模态能力强大</p>
                </div>
              )}

              {currentProvider === 'grok' && (
                <div>
                  <p>• 访问 <a href="https://x.ai/" target="_blank" rel="noopener noreferrer">xAI官网</a> 获取API Key</p>
                  <p>• 支持Grok系列模型</p>
                  <p>• 实时信息获取能力</p>
                </div>
              )}

              {currentProvider === 'ollama' && (
                <div>
                  <p>• 需要本地安装Ollama服务</p>
                  <p>• 支持多种开源模型</p>
                  <p>• 数据完全本地化</p>
                  <p>• 下载地址: <a href="https://ollama.ai/" target="_blank" rel="noopener noreferrer">ollama.ai</a></p>
                  <Divider style={{ margin: '8px 0' }} />
                  <p><strong>本地模型状态:</strong></p>
                  {loadingOllamaModels ? (
                    <p>• 正在检测模型...</p>
                  ) : ollamaModels.length > 0 ? (
                    <div>
                      <p>• 已安装 {ollamaModels.length} 个模型</p>
                      {ollamaModels.slice(0, 3).map(model => (
                        <p key={model.name} style={{ fontSize: '11px', margin: '2px 0' }}>
                          - {model.name} ({(model.size / (1024 * 1024 * 1024)).toFixed(1)}GB)
                        </p>
                      ))}
                      {ollamaModels.length > 3 && (
                        <p style={{ fontSize: '11px', margin: '2px 0' }}>
                          ... 还有 {ollamaModels.length - 3} 个模型
                        </p>
                      )}
                    </div>
                  ) : (
                    <div>
                      <p>• 未检测到本地模型</p>
                      <p style={{ fontSize: '11px' }}>使用 ollama pull &lt;model&gt; 下载模型</p>
                    </div>
                  )}
                </div>
              )}

              {currentProvider === 'custom' && (
                <div>
                  <p>• 支持OpenAI兼容的API接口</p>
                  <p>• 可配置自定义服务地址</p>
                  <p>• 适用于私有部署的模型</p>
                </div>
              )}
            </div>
          </Card>

          {aiStatus.error && (
            <Alert
              message="连接错误"
              description={aiStatus.error}
              type="error"
              size="small"
              style={{ marginBottom: '16px' }}
            />
          )}

          <Card title="快速操作" size="small">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button block onClick={fetchAIInfo} loading={loading}>
                刷新状态
              </Button>
              <Button block onClick={testConnection} loading={loading}>
                测试连接
              </Button>
              {currentProvider === 'ollama' && (
                <Button
                  block
                  onClick={fetchOllamaModels}
                  loading={loadingOllamaModels}
                  icon={<ReloadOutlined />}
                >
                  刷新模型列表
                </Button>
              )}
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default AIConfigPanel;
