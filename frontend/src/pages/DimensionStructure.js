import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
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
  Statistic,
  Rate
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  GatewayOutlined,
  StarOutlined,
  ThunderboltOutlined,
  EyeOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const DimensionStructure = () => {
  const { id: projectId } = useParams();
  const [dimensions, setDimensions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingDimension, setEditingDimension] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockDimensions = [
    {
      id: 1,
      name: '主物质界',
      type: 'material',
      level: 1,
      stability: 5,
      timeFlow: 1.0,
      spaceSize: 'infinite',
      lawStrength: 5,
      energyDensity: 3,
      accessMethods: ['自然存在'],
      restrictions: ['无'],
      inhabitants: ['人族', '妖族', '魔族'],
      uniqueFeatures: ['完整的天地法则', '稳定的时空结构'],
      description: '修仙世界的主要维度，所有生灵的家园',
      connectedDimensions: ['灵界', '魔界'],
      dangerLevel: 2,
      discoveredBy: '天然存在',
      status: 'stable'
    },
    {
      id: 2,
      name: '灵界',
      type: 'spiritual',
      level: 2,
      stability: 4,
      timeFlow: 0.5,
      spaceSize: 'vast',
      lawStrength: 4,
      energyDensity: 5,
      accessMethods: ['渡劫飞升', '空间裂缝'],
      restrictions: ['需要元婴期以上修为'],
      inhabitants: ['仙人', '灵兽', '天使'],
      uniqueFeatures: ['灵气极度浓郁', '时间流速缓慢'],
      description: '修仙者向往的高等维度，灵气充沛',
      connectedDimensions: ['主物质界', '仙界'],
      dangerLevel: 3,
      discoveredBy: '古代仙人',
      status: 'stable'
    },
    {
      id: 3,
      name: '虚空乱流',
      type: 'chaotic',
      level: 0,
      stability: 1,
      timeFlow: 'variable',
      spaceSize: 'unknown',
      lawStrength: 1,
      energyDensity: 2,
      accessMethods: ['空间撕裂', '意外传送'],
      restrictions: ['极度危险'],
      inhabitants: ['虚空生物', '迷失者'],
      uniqueFeatures: ['时空混乱', '法则不稳定'],
      description: '危险的混沌维度，充满未知的威胁',
      connectedDimensions: ['所有维度'],
      dangerLevel: 5,
      discoveredBy: '意外发现',
      status: 'chaotic'
    }
  ];

  useEffect(() => {
    loadDimensions();
  }, [projectId]);

  const loadDimensions = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setDimensions(mockDimensions);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载维度结构失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingDimension(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (dimension) => {
    setEditingDimension(dimension);
    form.setFieldsValue({
      ...dimension,
      accessMethods: dimension.accessMethods?.join(', '),
      restrictions: dimension.restrictions?.join(', '),
      inhabitants: dimension.inhabitants?.join(', '),
      uniqueFeatures: dimension.uniqueFeatures?.join(', '),
      connectedDimensions: dimension.connectedDimensions?.join(', ')
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/dimension_structure/${id}`);

      // 删除成功后从列表中移除
      setDimensions(dimensions.filter(d => d.id !== id));
      message.success('删除成功');
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values) => {
    try {
      const processedValues = {
        name: values.name,
        type: values.type,
        level: values.level,
        stability: values.stability,
        timeFlow: values.timeFlow,
        spaceSize: values.spaceSize,
        lawStrength: values.lawStrength,
        energyDensity: values.energyDensity,
        accessMethods: values.accessMethods?.split(',').map(m => m.trim()).filter(m => m) || [],
        restrictions: values.restrictions?.split(',').map(r => r.trim()).filter(r => r) || [],
        inhabitants: values.inhabitants?.split(',').map(i => i.trim()).filter(i => i) || [],
        uniqueFeatures: values.uniqueFeatures?.split(',').map(f => f.trim()).filter(f => f) || [],
        description: values.description,
        connectedDimensions: values.connectedDimensions?.split(',').map(d => d.trim()).filter(d => d) || [],
        dangerLevel: values.dangerLevel,
        discoveredBy: values.discoveredBy,
        status: values.status
      };

      if (editingDimension) {
        // 更新
        setDimensions(dimensions.map(d =>
          d.id === editingDimension.id ? { ...d, ...processedValues } : d
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newDimension = {
          id: Date.now(),
          ...processedValues
        };
        setDimensions([...dimensions, newDimension]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      material: 'blue',
      spiritual: 'purple',
      elemental: 'orange',
      chaotic: 'red',
      divine: 'gold',
      shadow: 'black'
    };
    return colors[type] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      stable: 'green',
      unstable: 'orange',
      chaotic: 'red',
      sealed: 'gray'
    };
    return colors[status] || 'default';
  };

  const columns = [
    {
      title: '维度名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'material' ? '物质' :
             record.type === 'spiritual' ? '灵界' :
             record.type === 'elemental' ? '元素' :
             record.type === 'chaotic' ? '混沌' :
             record.type === 'divine' ? '神界' : '阴影'}
          </Tag>
        </Space>
      )
    },
    {
      title: '维度等级',
      dataIndex: 'level',
      key: 'level',
      render: (level) => (
        <Space>
          <StarOutlined style={{ color: '#faad14' }} />
          <Text>{level}</Text>
        </Space>
      ),
      sorter: (a, b) => a.level - b.level
    },
    {
      title: '稳定性',
      dataIndex: 'stability',
      key: 'stability',
      render: (stability) => (
        <Rate disabled value={stability} style={{ fontSize: 16 }} />
      ),
      sorter: (a, b) => a.stability - b.stability
    },
    {
      title: '时间流速',
      dataIndex: 'timeFlow',
      key: 'timeFlow',
      render: (flow) => (
        <Space>
          <ClockCircleOutlined />
          <Text>{typeof flow === 'number' ? `${flow}x` : flow}</Text>
        </Space>
      )
    },
    {
      title: '法则强度',
      dataIndex: 'lawStrength',
      key: 'lawStrength',
      render: (strength) => (
        <Space>
          <ThunderboltOutlined style={{ color: '#722ed1' }} />
          <Rate disabled value={strength} style={{ fontSize: 16 }} />
        </Space>
      ),
      sorter: (a, b) => a.lawStrength - b.lawStrength
    },
    {
      title: '危险等级',
      dataIndex: 'dangerLevel',
      key: 'dangerLevel',
      render: (level) => {
        const color = level >= 4 ? '#f5222d' : level >= 3 ? '#fa8c16' : level >= 2 ? '#faad14' : '#52c41a';
        return <Tag color={color}>{level}/5</Tag>;
      },
      sorter: (a, b) => a.dangerLevel - b.dangerLevel
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status === 'stable' ? '稳定' :
           status === 'unstable' ? '不稳定' :
           status === 'chaotic' ? '混沌' : '封印'}
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
            title="确定删除这个维度吗？"
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
          <GatewayOutlined /> 维度结构管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加维度
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="维度总数"
              value={dimensions.length}
              prefix={<GatewayOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="稳定维度"
              value={dimensions.filter(d => d.status === 'stable').length}
              prefix={<StarOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="混沌维度"
              value={dimensions.filter(d => d.status === 'chaotic').length}
              prefix={<ThunderboltOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="平均危险等级"
              value={dimensions.length > 0 ? (dimensions.reduce((sum, d) => sum + d.dangerLevel, 0) / dimensions.length).toFixed(1) : 0}
              prefix={<EyeOutlined />}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={dimensions}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个维度`
          }}
        />
      </Card>

      <Modal
        title={editingDimension ? '编辑维度' : '添加维度'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        confirmLoading={loading}
        width={900}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            type: 'material',
            level: 1,
            stability: 3,
            timeFlow: 1.0,
            spaceSize: 'large',
            lawStrength: 3,
            energyDensity: 3,
            dangerLevel: 1,
            status: 'stable'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="维度名称"
                rules={[{ required: true, message: '请输入维度名称' }]}
              >
                <Input placeholder="请输入维度名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="维度类型"
                rules={[{ required: true, message: '请选择维度类型' }]}
              >
                <Select>
                  <Option value="material">物质</Option>
                  <Option value="spiritual">灵界</Option>
                  <Option value="elemental">元素</Option>
                  <Option value="chaotic">混沌</Option>
                  <Option value="divine">神界</Option>
                  <Option value="shadow">阴影</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="level"
                label="维度等级"
                rules={[{ required: true, message: '请输入维度等级' }]}
              >
                <InputNumber min={0} max={10} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="stability"
                label="稳定性"
                rules={[{ required: true, message: '请选择稳定性' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="dangerLevel"
                label="危险等级"
                rules={[{ required: true, message: '请选择危险等级' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="timeFlow"
                label="时间流速"
                rules={[{ required: true, message: '请输入时间流速' }]}
              >
                <InputNumber min={0} step={0.1} style={{ width: '100%' }} addonAfter="x" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="lawStrength"
                label="法则强度"
                rules={[{ required: true, message: '请选择法则强度' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="energyDensity"
                label="能量密度"
                rules={[{ required: true, message: '请选择能量密度' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="spaceSize"
                label="空间大小"
                rules={[{ required: true, message: '请选择空间大小' }]}
              >
                <Select>
                  <Option value="tiny">微小</Option>
                  <Option value="small">小型</Option>
                  <Option value="medium">中型</Option>
                  <Option value="large">大型</Option>
                  <Option value="vast">广阔</Option>
                  <Option value="infinite">无限</Option>
                  <Option value="unknown">未知</Option>
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
                  <Option value="stable">稳定</Option>
                  <Option value="unstable">不稳定</Option>
                  <Option value="chaotic">混沌</Option>
                  <Option value="sealed">封印</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="discoveredBy" label="发现者">
            <Input placeholder="请输入发现者" />
          </Form.Item>

          <Form.Item name="accessMethods" label="进入方法" extra="多个方法请用逗号分隔">
            <Input placeholder="如：渡劫飞升, 空间裂缝" />
          </Form.Item>

          <Form.Item name="restrictions" label="进入限制" extra="多个限制请用逗号分隔">
            <Input placeholder="如：需要元婴期以上修为" />
          </Form.Item>

          <Form.Item name="inhabitants" label="居住者" extra="多个种族请用逗号分隔">
            <Input placeholder="如：仙人, 灵兽, 天使" />
          </Form.Item>

          <Form.Item name="uniqueFeatures" label="独特特征" extra="多个特征请用逗号分隔">
            <Input placeholder="如：灵气极度浓郁, 时间流速缓慢" />
          </Form.Item>

          <Form.Item name="connectedDimensions" label="连接维度" extra="多个维度请用逗号分隔">
            <Input placeholder="如：主物质界, 仙界" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={3} placeholder="请描述维度的特点、环境、历史等" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DimensionStructure;
