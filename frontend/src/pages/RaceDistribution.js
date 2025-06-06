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
  Progress,
  Statistic
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  TeamOutlined,
  UserOutlined,
  EnvironmentOutlined,
  CrownOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const RaceDistribution = () => {
  const { id: projectId } = useParams();
  const [races, setRaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRace, setEditingRace] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockRaces = [
    {
      id: 1,
      name: '人族',
      type: 'humanoid',
      population: 1000000,
      territory: '中原大陆',
      dominantRegions: ['天元城', '青云山脉', '东海之滨'],
      characteristics: '适应性强，修炼天赋中等，善于团结协作',
      culture: '重视血缘关系，崇尚修仙成道',
      powerLevel: 3,
      influence: 4,
      relations: {
        allies: ['精灵族'],
        enemies: ['魔族'],
        neutral: ['妖族', '龙族']
      },
      status: 'thriving'
    },
    {
      id: 2,
      name: '精灵族',
      type: 'magical',
      population: 500000,
      territory: '翡翠森林',
      dominantRegions: ['生命之树', '月光湖', '星辰谷'],
      characteristics: '寿命悠长，魔法天赋极高，与自然和谐共处',
      culture: '崇尚自然，追求魔法的极致',
      powerLevel: 4,
      influence: 3,
      relations: {
        allies: ['人族'],
        enemies: ['魔族'],
        neutral: ['龙族']
      },
      status: 'stable'
    }
  ];

  useEffect(() => {
    loadRaces();
  }, [projectId]);

  const loadRaces = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setRaces(mockRaces);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载种族分布失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingRace(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (race) => {
    setEditingRace(race);
    form.setFieldsValue({
      ...race,
      dominantRegions: race.dominantRegions?.join(', '),
      allies: race.relations?.allies?.join(', '),
      enemies: race.relations?.enemies?.join(', '),
      neutral: race.relations?.neutral?.join(', ')
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 模拟API调用
      setRaces(races.filter(r => r.id !== id));
      message.success('删除成功');
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values) => {
    try {
      const processedValues = {
        ...values,
        dominantRegions: values.dominantRegions?.split(',').map(s => s.trim()).filter(s => s),
        relations: {
          allies: values.allies?.split(',').map(s => s.trim()).filter(s => s) || [],
          enemies: values.enemies?.split(',').map(s => s.trim()).filter(s => s) || [],
          neutral: values.neutral?.split(',').map(s => s.trim()).filter(s => s) || []
        }
      };

      if (editingRace) {
        // 更新
        setRaces(races.map(r =>
          r.id === editingRace.id ? { ...r, ...processedValues } : r
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newRace = {
          id: Date.now(),
          ...processedValues
        };
        setRaces([...races, newRace]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      humanoid: 'blue',
      magical: 'purple',
      beast: 'orange',
      elemental: 'cyan',
      undead: 'red',
      divine: 'gold'
    };
    return colors[type] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      thriving: 'green',
      stable: 'blue',
      declining: 'orange',
      endangered: 'red',
      extinct: 'gray'
    };
    return colors[status] || 'default';
  };

  const formatPopulation = (population) => {
    if (population >= 1000000) {
      return `${(population / 1000000).toFixed(1)}M`;
    } else if (population >= 1000) {
      return `${(population / 1000).toFixed(1)}K`;
    }
    return population.toString();
  };

  const columns = [
    {
      title: '种族名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'humanoid' ? '类人' :
             record.type === 'magical' ? '魔法' :
             record.type === 'beast' ? '兽族' :
             record.type === 'elemental' ? '元素' :
             record.type === 'undead' ? '不死' : '神族'}
          </Tag>
        </Space>
      )
    },
    {
      title: '人口',
      dataIndex: 'population',
      key: 'population',
      render: (population) => (
        <Space>
          <UserOutlined />
          <Text>{formatPopulation(population)}</Text>
        </Space>
      ),
      sorter: (a, b) => a.population - b.population
    },
    {
      title: '主要领土',
      dataIndex: 'territory',
      key: 'territory',
      render: (text) => (
        <Space>
          <EnvironmentOutlined />
          <Text>{text}</Text>
        </Space>
      )
    },
    {
      title: '实力等级',
      dataIndex: 'powerLevel',
      key: 'powerLevel',
      render: (level) => (
        <Progress
          percent={level * 20}
          size="small"
          format={() => `${level}/5`}
          strokeColor={level >= 4 ? '#f5222d' : level >= 3 ? '#fa8c16' : '#52c41a'}
        />
      ),
      sorter: (a, b) => a.powerLevel - b.powerLevel
    },
    {
      title: '影响力',
      dataIndex: 'influence',
      key: 'influence',
      render: (influence) => (
        <Progress
          percent={influence * 20}
          size="small"
          format={() => `${influence}/5`}
          strokeColor={influence >= 4 ? '#722ed1' : influence >= 3 ? '#1890ff' : '#52c41a'}
        />
      ),
      sorter: (a, b) => a.influence - b.influence
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status === 'thriving' ? '繁荣' :
           status === 'stable' ? '稳定' :
           status === 'declining' ? '衰落' :
           status === 'endangered' ? '濒危' : '灭绝'}
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
            title="确定删除这个种族吗？"
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

  const totalPopulation = races.reduce((sum, race) => sum + race.population, 0);

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">
          <TeamOutlined /> 种族分布管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加种族
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="种族总数"
              value={races.length}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="总人口"
              value={totalPopulation}
              formatter={(value) => formatPopulation(value)}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="繁荣种族"
              value={races.filter(r => r.status === 'thriving').length}
              prefix={<CrownOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="濒危种族"
              value={races.filter(r => r.status === 'endangered').length}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={races}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个种族`
          }}
        />
      </Card>

      <Modal
        title={editingRace ? '编辑种族' : '添加种族'}
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
            type: 'humanoid',
            powerLevel: 3,
            influence: 3,
            status: 'stable'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="种族名称"
                rules={[{ required: true, message: '请输入种族名称' }]}
              >
                <Input placeholder="请输入种族名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="种族类型"
                rules={[{ required: true, message: '请选择种族类型' }]}
              >
                <Select>
                  <Option value="humanoid">类人</Option>
                  <Option value="magical">魔法</Option>
                  <Option value="beast">兽族</Option>
                  <Option value="elemental">元素</Option>
                  <Option value="undead">不死</Option>
                  <Option value="divine">神族</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="population"
                label="人口数量"
                rules={[{ required: true, message: '请输入人口数量' }]}
              >
                <InputNumber
                  min={0}
                  style={{ width: '100%' }}
                  placeholder="请输入人口数量"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="territory"
                label="主要领土"
                rules={[{ required: true, message: '请输入主要领土' }]}
              >
                <Input placeholder="请输入主要领土" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="dominantRegions"
            label="统治区域"
            extra="多个区域请用逗号分隔"
          >
            <Input placeholder="例如：天元城, 青云山脉, 东海之滨" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="powerLevel"
                label="实力等级"
                rules={[{ required: true, message: '请选择实力等级' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="influence"
                label="影响力"
                rules={[{ required: true, message: '请选择影响力' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="status"
                label="种族状态"
                rules={[{ required: true, message: '请选择种族状态' }]}
              >
                <Select>
                  <Option value="thriving">繁荣</Option>
                  <Option value="stable">稳定</Option>
                  <Option value="declining">衰落</Option>
                  <Option value="endangered">濒危</Option>
                  <Option value="extinct">灭绝</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="characteristics"
            label="种族特征"
            rules={[{ required: true, message: '请输入种族特征' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述种族的生理特征、能力特点等"
            />
          </Form.Item>

          <Form.Item
            name="culture"
            label="文化背景"
          >
            <TextArea
              rows={2}
              placeholder="请描述种族的文化、信仰、传统等"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="allies"
                label="盟友种族"
                extra="多个种族请用逗号分隔"
              >
                <Input placeholder="例如：精灵族, 矮人族" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="enemies"
                label="敌对种族"
                extra="多个种族请用逗号分隔"
              >
                <Input placeholder="例如：魔族, 兽人族" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="neutral"
                label="中立种族"
                extra="多个种族请用逗号分隔"
              >
                <Input placeholder="例如：龙族, 妖族" />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default RaceDistribution;
