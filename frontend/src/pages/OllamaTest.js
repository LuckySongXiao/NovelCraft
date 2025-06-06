import React, { useState, useEffect } from 'react';
import {
  Card,
  Button,
  Space,
  Alert,
  List,
  Tag,
  Typography,
  Spin,
  message,
  Row,
  Col,
  Statistic
} from 'antd';
import {
  ReloadOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;

const OllamaTest = () => {
  const [loading, setLoading] = useState(false);
  const [models, setModels] = useState([]);
  const [ollamaStatus, setOllamaStatus] = useState(null);
  const [error, setError] = useState(null);

  // 获取Ollama模型列表
  const fetchOllamaModels = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await axios.get('/api/ai/ollama/models');
      console.log('Ollama models response:', response.data);

      setModels(response.data.models);
      message.success(`成功获取 ${response.data.count} 个模型`);
    } catch (error) {
      console.error('获取Ollama模型失败:', error);
      setError(error.response?.data?.detail || error.message);
      message.error('获取Ollama模型失败');
      setModels([]);
    } finally {
      setLoading(false);
    }
  };

  // 检查Ollama状态
  const checkOllamaStatus = async () => {
    try {
      // 先切换到ollama提供商
      await axios.post('/api/ai/switch-provider', { provider: 'ollama' });

      // 然后检查状态
      const response = await axios.get('/api/ai/status');
      setOllamaStatus(response.data);
    } catch (error) {
      console.error('检查Ollama状态失败:', error);
      setOllamaStatus({ connected: false, status: 'error', error: error.message });
    }
  };

  // 获取模型详细信息
  const getModelInfo = async (modelName) => {
    try {
      const response = await axios.get(`/api/ai/ollama/models/${modelName}`);
      console.log(`Model ${modelName} info:`, response.data);
      message.success(`获取模型 ${modelName} 信息成功`);
    } catch (error) {
      console.error(`获取模型 ${modelName} 信息失败:`, error);
      message.error(`获取模型 ${modelName} 信息失败`);
    }
  };

  // 格式化文件大小
  const formatSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  useEffect(() => {
    checkOllamaStatus();
    fetchOllamaModels();
  }, []);

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2}>
        <RobotOutlined /> Ollama模型检测测试
      </Title>

      {/* 状态概览 */}
      <Row gutter={24} style={{ marginBottom: '24px' }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="Ollama状态"
              value={ollamaStatus?.connected ? '在线' : '离线'}
              prefix={ollamaStatus?.connected ? <CheckCircleOutlined style={{ color: '#52c41a' }} /> : <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />}
              valueStyle={{ color: ollamaStatus?.connected ? '#52c41a' : '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="本地模型数量"
              value={models.length}
              prefix={<RobotOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="总大小"
              value={formatSize(models.reduce((total, model) => total + (model.size || 0), 0))}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 操作按钮 */}
      <Card style={{ marginBottom: '24px' }}>
        <Space>
          <Button
            type="primary"
            icon={<ReloadOutlined />}
            onClick={fetchOllamaModels}
            loading={loading}
          >
            刷新模型列表
          </Button>
          <Button
            icon={<CheckCircleOutlined />}
            onClick={checkOllamaStatus}
          >
            检查状态
          </Button>
        </Space>
      </Card>

      {/* 错误信息 */}
      {error && (
        <Alert
          message="错误"
          description={error}
          type="error"
          showIcon
          style={{ marginBottom: '24px' }}
        />
      )}

      {/* Ollama状态信息 */}
      {ollamaStatus && (
        <Card title="Ollama服务状态" style={{ marginBottom: '24px' }}>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div>
              <Text strong>提供商: </Text>
              <Tag color="blue">{ollamaStatus.provider}</Tag>
            </div>
            <div>
              <Text strong>连接状态: </Text>
              <Tag color={ollamaStatus.connected ? 'green' : 'red'}>
                {ollamaStatus.connected ? '已连接' : '未连接'}
              </Tag>
            </div>
            <div>
              <Text strong>服务状态: </Text>
              <Tag color={ollamaStatus.status === 'online' ? 'green' : 'orange'}>
                {ollamaStatus.status}
              </Tag>
            </div>
            {ollamaStatus.error && (
              <div>
                <Text strong>错误信息: </Text>
                <Text type="danger">{ollamaStatus.error}</Text>
              </div>
            )}
          </Space>
        </Card>
      )}

      {/* 模型列表 */}
      <Card title={`本地模型列表 (${models.length})`}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <Spin size="large" />
            <div style={{ marginTop: '16px' }}>正在获取模型列表...</div>
          </div>
        ) : models.length > 0 ? (
          <List
            dataSource={models}
            renderItem={(model) => (
              <List.Item
                actions={[
                  <Button
                    type="link"
                    onClick={() => getModelInfo(model.name)}
                  >
                    查看详情
                  </Button>
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Text strong>{model.name}</Text>
                      <Tag color="blue">{formatSize(model.size)}</Tag>
                    </Space>
                  }
                  description={
                    <Space direction="vertical" size="small">
                      <div>
                        <Text type="secondary">修改时间: </Text>
                        <Text>{new Date(model.modified_at).toLocaleString()}</Text>
                      </div>
                      {model.digest && (
                        <div>
                          <Text type="secondary">摘要: </Text>
                          <Text code style={{ fontSize: '12px' }}>
                            {model.digest.substring(0, 16)}...
                          </Text>
                        </div>
                      )}
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        ) : (
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <ExclamationCircleOutlined style={{ fontSize: '48px', color: '#faad14', marginBottom: '16px' }} />
            <div style={{ marginBottom: '16px' }}>
              <Text>未检测到本地Ollama模型</Text>
            </div>
            <div>
              <Text type="secondary">
                请确保Ollama服务正在运行，并使用以下命令下载模型：
              </Text>
            </div>
            <div style={{ marginTop: '8px' }}>
              <Text code>ollama pull llama2</Text>
              <br />
              <Text code>ollama pull mistral</Text>
              <br />
              <Text code>ollama pull qwen</Text>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default OllamaTest;
