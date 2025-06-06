import React, { useState } from 'react';
import {
  Card,
  Typography,
  Button,
  Form,
  Select,
  Switch,
  Tabs,
  Row,
  Col,
  message,
  Space
} from 'antd';
import {
  SettingOutlined,
  SaveOutlined,
  RobotOutlined,
  DatabaseOutlined
} from '@ant-design/icons';
import AIConfigPanel from '../components/AIConfigPanel';

const { Title, Text } = Typography;
const { Option } = Select;
const { TabPane } = Tabs;

const Settings = () => {
  const [loading, setLoading] = useState(false);
  const [generalForm] = Form.useForm();
  const [activeTab, setActiveTab] = useState('ai');



  // 保存通用设置
  const saveGeneralSettings = async (values) => {
    try {
      setLoading(true);
      // 这里应该调用保存通用配置的API
      message.success('通用设置保存成功');
    } catch (error) {
      message.error('通用设置保存失败');
    } finally {
      setLoading(false);
    }
  };



  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">系统设置</Title>
      </div>

      <Tabs activeKey={activeTab} onChange={setActiveTab}>
        <TabPane tab={<span><RobotOutlined />AI配置</span>} key="ai">
          <AIConfigPanel />
        </TabPane>

          <TabPane tab={<span><SettingOutlined />通用设置</span>} key="general">
            <Form
              form={generalForm}
              layout="vertical"
              onFinish={saveGeneralSettings}
              initialValues={{
                autoSave: true,
                autoBackup: true,
                theme: 'default',
                language: 'zh-CN'
              }}
            >
              <Row gutter={[24, 24]}>
                <Col span={12}>
                  <Card title="界面设置" size="small">
                    <Form.Item name="theme" label="主题">
                      <Select>
                        <Option value="default">默认主题</Option>
                        <Option value="dark">暗黑主题</Option>
                        <Option value="light">明亮主题</Option>
                      </Select>
                    </Form.Item>

                    <Form.Item name="language" label="语言">
                      <Select>
                        <Option value="zh-CN">简体中文</Option>
                        <Option value="en-US">English</Option>
                      </Select>
                    </Form.Item>
                  </Card>
                </Col>

                <Col span={12}>
                  <Card title="功能设置" size="small">
                    <Form.Item name="autoSave" label="自动保存" valuePropName="checked">
                      <Switch />
                    </Form.Item>

                    <Form.Item name="autoBackup" label="自动备份" valuePropName="checked">
                      <Switch />
                    </Form.Item>

                    <Form.Item name="consistencyCheck" label="一致性检查" valuePropName="checked">
                      <Switch />
                    </Form.Item>
                  </Card>
                </Col>
              </Row>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} icon={<SaveOutlined />}>
                  保存通用设置
                </Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane tab={<span><DatabaseOutlined />数据管理</span>} key="data">
            <Row gutter={[24, 24]}>
              <Col span={12}>
                <Card title="数据备份" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <Button block>创建备份</Button>
                    <Button block>恢复备份</Button>
                    <Button block>导出数据</Button>
                    <Button block>导入数据</Button>
                  </Space>
                </Card>
              </Col>

              <Col span={12}>
                <Card title="数据清理" size="small">
                  <Space direction="vertical" style={{ width: '100%' }}>
                    <Button block>清理缓存</Button>
                    <Button block>清理日志</Button>
                    <Button block danger>重置设置</Button>
                  </Space>
                </Card>
              </Col>
            </Row>
          </TabPane>
        </Tabs>
    </div>
  );
};

export default Settings;
