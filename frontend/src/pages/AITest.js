import React, { useState, useEffect } from 'react';
import { Card, Button, Space, Alert, Typography, Divider, Tag } from 'antd';
import axios from 'axios';

const { Title, Text, Paragraph } = Typography;

const AITest = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({});
  const [error, setError] = useState(null);

  const testAPI = async (endpoint, description) => {
    try {
      setLoading(true);
      setError(null);

      console.log(`Testing ${endpoint}...`);
      const response = await axios.get(endpoint);

      setResults(prev => ({
        ...prev,
        [endpoint]: {
          success: true,
          data: response.data,
          description
        }
      }));

      return response.data;
    } catch (error) {
      console.error(`Error testing ${endpoint}:`, error);
      setResults(prev => ({
        ...prev,
        [endpoint]: {
          success: false,
          error: error.response?.data || error.message,
          description
        }
      }));
      setError(`${description} 测试失败: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const testAllAPIs = async () => {
    setResults({});
    setError(null);

    const tests = [
      { endpoint: '/api/ai/providers', description: 'AI提供商列表' },
      { endpoint: '/api/ai/status', description: 'AI服务状态' },
    ];

    for (const test of tests) {
      await testAPI(test.endpoint, test.description);
      // 添加延迟避免请求过快
      await new Promise(resolve => setTimeout(resolve, 500));
    }
  };

  const testProviderSwitch = async (provider) => {
    try {
      setLoading(true);
      setError(null);

      console.log(`Testing provider switch to ${provider}...`);
      const response = await axios.post('/api/v1/ai/switch-provider', { provider });

      setResults(prev => ({
        ...prev,
        [`switch-${provider}`]: {
          success: true,
          data: response.data,
          description: `切换到 ${provider}`
        }
      }));

      // 测试获取配置
      await testAPI(`/api/v1/ai/config/${provider}`, `获取 ${provider} 配置`);

    } catch (error) {
      console.error(`Error switching to ${provider}:`, error);
      setResults(prev => ({
        ...prev,
        [`switch-${provider}`]: {
          success: false,
          error: error.response?.data || error.message,
          description: `切换到 ${provider}`
        }
      }));
      setError(`切换到 ${provider} 失败: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderResult = (key, result) => {
    return (
      <Card
        key={key}
        size="small"
        style={{ marginBottom: '8px' }}
        title={
          <Space>
            <Tag color={result.success ? 'green' : 'red'}>
              {result.success ? '成功' : '失败'}
            </Tag>
            {result.description}
          </Space>
        }
      >
        {result.success ? (
          <div>
            <Text type="success">✅ 测试通过</Text>
            <Divider type="vertical" />
            <Text code>{JSON.stringify(result.data, null, 2).substring(0, 200)}...</Text>
          </div>
        ) : (
          <div>
            <Text type="danger">❌ 测试失败</Text>
            <Divider type="vertical" />
            <Text code>{JSON.stringify(result.error, null, 2)}</Text>
          </div>
        )}
      </Card>
    );
  };

  useEffect(() => {
    // 页面加载时自动测试基础API
    testAllAPIs();
  }, []);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px' }}>
      <Title level={2}>AI功能测试页面</Title>
      <Paragraph>
        这个页面用于测试AI配置功能是否正常工作。
      </Paragraph>

      {error && (
        <Alert
          message="测试错误"
          description={error}
          type="error"
          closable
          style={{ marginBottom: '24px' }}
          onClose={() => setError(null)}
        />
      )}

      <Card title="基础API测试" style={{ marginBottom: '24px' }}>
        <Space wrap>
          <Button
            type="primary"
            onClick={testAllAPIs}
            loading={loading}
          >
            测试所有API
          </Button>
          <Button
            onClick={() => testAPI('/api/ai/providers', 'AI提供商列表')}
            loading={loading}
          >
            测试提供商列表
          </Button>
          <Button
            onClick={() => testAPI('/api/ai/status', 'AI服务状态')}
            loading={loading}
          >
            测试服务状态
          </Button>
        </Space>
      </Card>

      <Card title="提供商切换测试" style={{ marginBottom: '24px' }}>
        <Space wrap>
          {['openai', 'claude', 'zhipu', 'siliconflow', 'google', 'grok', 'ollama', 'custom'].map(provider => (
            <Button
              key={provider}
              onClick={() => testProviderSwitch(provider)}
              loading={loading}
              size="small"
            >
              切换到 {provider}
            </Button>
          ))}
        </Space>
      </Card>

      <Card title="测试结果" style={{ marginBottom: '24px' }}>
        {Object.keys(results).length === 0 ? (
          <Text type="secondary">暂无测试结果</Text>
        ) : (
          <div>
            {Object.entries(results).map(([key, result]) =>
              renderResult(key, result)
            )}
          </div>
        )}
      </Card>

      <Card title="调试信息" size="small">
        <Text code>
          打开浏览器开发者工具的Console标签页查看详细的调试信息
        </Text>
      </Card>
    </div>
  );
};

export default AITest;
