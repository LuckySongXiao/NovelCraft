import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  Space,
  Typography,
  Row,
  Col,
  Tag,
  Popconfirm,
  message,
  Tooltip,
  Rate,
  Progress
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EnvironmentOutlined,
  GoldOutlined,
  ThunderboltOutlined,
  FireOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const ResourceDistribution = () => {
  const { id: projectId } = useParams();
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingResource, setEditingResource] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockResources = [
    {
      id: 1,
      name: '灵石矿脉',
      type: 'mineral',
      location: '青云山脉',
      coordinates: { x: 120, y: 80 },
      rarity: 'rare',
      difficulty: 4,
      economicValue: 5,
      description: '蕴含丰富灵气的矿脉，是修炼者必需的资源',
      extractionMethod: '需要筑基期以上修为才能安全开采',
      renewalRate: 'slow',
      controllingFaction: '青云宗',
      status: 'active'
    },
    {
      id: 2,
      name: '千年雪莲',
      type: 'herb',
      location: '雪域高原',
      coordinates: { x: 200, y: 150 },
      rarity: 'legendary',
      difficulty: 5,
      economicValue: 5,
      description: '极其珍贵的炼丹材料，可延年益寿',
      extractionMethod: '需要在特定时间采摘，且需要抵御严寒',
      renewalRate: 'very_slow',
      controllingFaction: '无',
      status: 'protected'
    }
  ];

  useEffect(() => {
    loadResources();
  }, [projectId]);

  const loadResources = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setResources(mockResources);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载资源分布失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingResource(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (resource) => {
    setEditingResource(resource);
    form.setFieldsValue(resource);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 模拟API调用
      setResources(resources.filter(r => r.id !== id));
      message.success('删除成功');
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values) => {
    try {
      if (editingResource) {
        // 更新
        setResources(resources.map(r =>
          r.id === editingResource.id ? { ...r, ...values } : r
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newResource = {
          id: Date.now(),
          ...values
        };
        setResources([...resources, newResource]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      mineral: 'gold',
      herb: 'green',
      water: 'blue',
      energy: 'purple',
      artifact: 'red'
    };
    return colors[type] || 'default';
  };

  const getRarityColor = (rarity) => {
    const colors = {
      common: 'default',
      uncommon: 'blue',
      rare: 'purple',
      epic: 'orange',
      legendary: 'red'
    };
    return colors[rarity] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'green',
      depleted: 'red',
      protected: 'blue',
      contested: 'orange'
    };
    return colors[status] || 'default';
  };

  const columns = [
    {
      title: '资源名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'mineral' ? '矿物' :
             record.type === 'herb' ? '草药' :
             record.type === 'water' ? '水源' :
             record.type === 'energy' ? '能量' : '神器'}
          </Tag>
        </Space>
      )
    },
    {
      title: '位置',
      dataIndex: 'location',
      key: 'location',
      render: (text, record) => (
        <Space>
          <EnvironmentOutlined />
          <Text>{text}</Text>
          <Text type="secondary">
            ({record.coordinates?.x}, {record.coordinates?.y})
          </Text>
        </Space>
      )
    },
    {
      title: '稀有度',
      dataIndex: 'rarity',
      key: 'rarity',
      render: (rarity) => (
        <Tag color={getRarityColor(rarity)}>
          {rarity === 'common' ? '普通' :
           rarity === 'uncommon' ? '不常见' :
           rarity === 'rare' ? '稀有' :
           rarity === 'epic' ? '史诗' : '传说'}
        </Tag>
      )
    },
    {
      title: '开采难度',
      dataIndex: 'difficulty',
      key: 'difficulty',
      render: (difficulty) => (
        <Rate disabled value={difficulty} style={{ fontSize: 16 }} />
      )
    },
    {
      title: '经济价值',
      dataIndex: 'economicValue',
      key: 'economicValue',
      render: (value) => (
        <Space>
          <GoldOutlined style={{ color: '#faad14' }} />
          <Rate disabled value={value} style={{ fontSize: 16 }} />
        </Space>
      )
    },
    {
      title: '控制势力',
      dataIndex: 'controllingFaction',
      key: 'controllingFaction',
      render: (faction) => faction || <Text type="secondary">无</Text>
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status === 'active' ? '活跃' :
           status === 'depleted' ? '枯竭' :
           status === 'protected' ? '受保护' : '争夺中'}
        </Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个资源吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Tooltip title="删除">
              <Button
                type="text"
                danger
                icon={<DeleteOutlined />}
              />
            </Tooltip>
          </Popconfirm>
        </Space>
      )
    }
  ];

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">
          <EnvironmentOutlined /> 资源分布管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加资源
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <GoldOutlined style={{ fontSize: 24, color: '#faad14' }} />
              <div style={{ marginTop: 8 }}>
                <Text type="secondary">总资源数</Text>
                <div style={{ fontSize: 20, fontWeight: 'bold' }}>
                  {resources.length}
                </div>
              </div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <ThunderboltOutlined style={{ fontSize: 24, color: '#52c41a' }} />
              <div style={{ marginTop: 8 }}>
                <Text type="secondary">活跃资源</Text>
                <div style={{ fontSize: 20, fontWeight: 'bold' }}>
                  {resources.filter(r => r.status === 'active').length}
                </div>
              </div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <FireOutlined style={{ fontSize: 24, color: '#f5222d' }} />
              <div style={{ marginTop: 8 }}>
                <Text type="secondary">争夺资源</Text>
                <div style={{ fontSize: 20, fontWeight: 'bold' }}>
                  {resources.filter(r => r.status === 'contested').length}
                </div>
              </div>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <div style={{ textAlign: 'center' }}>
              <EnvironmentOutlined style={{ fontSize: 24, color: '#1890ff' }} />
              <div style={{ marginTop: 8 }}>
                <Text type="secondary">受保护资源</Text>
                <div style={{ fontSize: 20, fontWeight: 'bold' }}>
                  {resources.filter(r => r.status === 'protected').length}
                </div>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={resources}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个资源`
          }}
        />
      </Card>

      <Modal
        title={editingResource ? '编辑资源' : '添加资源'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        confirmLoading={loading}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            type: 'mineral',
            rarity: 'common',
            difficulty: 1,
            economicValue: 1,
            renewalRate: 'medium',
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="资源名称"
                rules={[{ required: true, message: '请输入资源名称' }]}
              >
                <Input placeholder="请输入资源名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="资源类型"
                rules={[{ required: true, message: '请选择资源类型' }]}
              >
                <Select>
                  <Option value="mineral">矿物</Option>
                  <Option value="herb">草药</Option>
                  <Option value="water">水源</Option>
                  <Option value="energy">能量</Option>
                  <Option value="artifact">神器</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="location"
                label="位置"
                rules={[{ required: true, message: '请输入位置' }]}
              >
                <Input placeholder="请输入位置" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="controllingFaction"
                label="控制势力"
              >
                <Input placeholder="请输入控制势力" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="rarity"
                label="稀有度"
                rules={[{ required: true, message: '请选择稀有度' }]}
              >
                <Select>
                  <Option value="common">普通</Option>
                  <Option value="uncommon">不常见</Option>
                  <Option value="rare">稀有</Option>
                  <Option value="epic">史诗</Option>
                  <Option value="legendary">传说</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="difficulty"
                label="开采难度"
                rules={[{ required: true, message: '请选择开采难度' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="economicValue"
                label="经济价值"
                rules={[{ required: true, message: '请选择经济价值' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="renewalRate"
                label="再生速度"
                rules={[{ required: true, message: '请选择再生速度' }]}
              >
                <Select>
                  <Option value="very_slow">极慢</Option>
                  <Option value="slow">缓慢</Option>
                  <Option value="medium">中等</Option>
                  <Option value="fast">快速</Option>
                  <Option value="very_fast">极快</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择状态' }]}
              >
                <Select>
                  <Option value="active">活跃</Option>
                  <Option value="depleted">枯竭</Option>
                  <Option value="protected">受保护</Option>
                  <Option value="contested">争夺中</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述资源的特点和用途"
            />
          </Form.Item>

          <Form.Item
            name="extractionMethod"
            label="开采方法"
          >
            <TextArea
              rows={2}
              placeholder="请描述开采方法和注意事项"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ResourceDistribution;
