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
  Rate,
  Statistic,
  Progress,
  Tabs
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  HeartOutlined,
  ThunderboltOutlined,
  ShieldOutlined,
  StarOutlined,
  FireOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const PetSystems = () => {
  const { id: projectId } = useParams();
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingPet, setEditingPet] = useState(null);
  const [activeTab, setActiveTab] = useState('all');
  const [form] = Form.useForm();

  // 模拟数据
  const mockPets = [
    {
      id: 1,
      name: '九尾灵狐',
      type: 'spirit',
      element: 'fire',
      rarity: 5,
      level: 50,
      attributes: {
        health: 2000,
        attack: 800,
        defense: 400,
        speed: 120,
        intelligence: 150
      },
      skills: ['火球术', '幻术', '治愈术'],
      evolution: {
        stage: 3,
        maxStage: 5,
        nextForm: '天狐'
      },
      habitat: '灵山秘境',
      tamingDifficulty: 4,
      loyalty: 85,
      description: '传说中的九尾狐，拥有强大的火系法术和幻术能力',
      specialAbilities: ['火焰免疫', '魅惑', '预知危险'],
      feedingRequirements: '灵果、火晶石',
      lifespan: 1000
    },
    {
      id: 2,
      name: '雷鸣巨鹰',
      type: 'beast',
      element: 'thunder',
      rarity: 4,
      level: 35,
      attributes: {
        health: 1500,
        attack: 1000,
        defense: 300,
        speed: 200,
        intelligence: 80
      },
      skills: ['雷击', '俯冲攻击', '风刃'],
      evolution: {
        stage: 2,
        maxStage: 4,
        nextForm: '雷神鹰'
      },
      habitat: '雷云峰',
      tamingDifficulty: 3,
      loyalty: 70,
      description: '翱翔于雷云之中的巨鹰，掌控雷电之力',
      specialAbilities: ['飞行', '雷电操控', '敏锐视觉'],
      feedingRequirements: '雷兽肉、雷石',
      lifespan: 500
    }
  ];

  useEffect(() => {
    loadPets();
  }, [projectId]);

  const loadPets = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setPets(mockPets);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载宠物体系失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingPet(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (pet) => {
    setEditingPet(pet);
    form.setFieldsValue({
      ...pet,
      skills: pet.skills?.join(', '),
      specialAbilities: pet.specialAbilities?.join(', '),
      health: pet.attributes?.health,
      attack: pet.attributes?.attack,
      defense: pet.attributes?.defense,
      speed: pet.attributes?.speed,
      intelligence: pet.attributes?.intelligence,
      evolutionStage: pet.evolution?.stage,
      maxStage: pet.evolution?.maxStage,
      nextForm: pet.evolution?.nextForm
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/pet_system/${id}`);

      // 删除成功后从列表中移除
      setPets(pets.filter(p => p.id !== id));
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
        element: values.element,
        rarity: values.rarity,
        level: values.level,
        attributes: {
          health: values.health || 0,
          attack: values.attack || 0,
          defense: values.defense || 0,
          speed: values.speed || 0,
          intelligence: values.intelligence || 0
        },
        skills: values.skills?.split(',').map(s => s.trim()).filter(s => s) || [],
        evolution: {
          stage: values.evolutionStage || 1,
          maxStage: values.maxStage || 1,
          nextForm: values.nextForm || ''
        },
        habitat: values.habitat,
        tamingDifficulty: values.tamingDifficulty,
        loyalty: values.loyalty,
        description: values.description,
        specialAbilities: values.specialAbilities?.split(',').map(s => s.trim()).filter(s => s) || [],
        feedingRequirements: values.feedingRequirements,
        lifespan: values.lifespan
      };

      if (editingPet) {
        // 更新
        setPets(pets.map(p =>
          p.id === editingPet.id ? { ...p, ...processedValues } : p
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newPet = {
          id: Date.now(),
          ...processedValues
        };
        setPets([...pets, newPet]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      spirit: 'purple',
      beast: 'orange',
      dragon: 'red',
      elemental: 'blue',
      undead: 'gray'
    };
    return colors[type] || 'default';
  };

  const getElementColor = (element) => {
    const colors = {
      fire: 'red',
      water: 'blue',
      earth: 'brown',
      air: 'cyan',
      thunder: 'purple',
      ice: 'blue',
      light: 'gold',
      dark: 'black'
    };
    return colors[element] || 'default';
  };

  const columns = [
    {
      title: '宠物名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'spirit' ? '灵兽' :
             record.type === 'beast' ? '野兽' :
             record.type === 'dragon' ? '龙族' :
             record.type === 'elemental' ? '元素' : '亡灵'}
          </Tag>
        </Space>
      )
    },
    {
      title: '属性',
      dataIndex: 'element',
      key: 'element',
      render: (element) => (
        <Tag color={getElementColor(element)}>
          {element === 'fire' ? '火' :
           element === 'water' ? '水' :
           element === 'earth' ? '土' :
           element === 'air' ? '风' :
           element === 'thunder' ? '雷' :
           element === 'ice' ? '冰' :
           element === 'light' ? '光' : '暗'}
        </Tag>
      )
    },
    {
      title: '稀有度',
      dataIndex: 'rarity',
      key: 'rarity',
      render: (rarity) => (
        <Rate disabled value={rarity} style={{ fontSize: 16 }} />
      ),
      sorter: (a, b) => a.rarity - b.rarity
    },
    {
      title: '等级',
      dataIndex: 'level',
      key: 'level',
      sorter: (a, b) => a.level - b.level
    },
    {
      title: '战力',
      key: 'power',
      render: (_, record) => {
        const power = (record.attributes?.attack || 0) + (record.attributes?.defense || 0);
        return (
          <Space>
            <ThunderboltOutlined style={{ color: '#faad14' }} />
            <Text>{power}</Text>
          </Space>
        );
      },
      sorter: (a, b) => {
        const powerA = (a.attributes?.attack || 0) + (a.attributes?.defense || 0);
        const powerB = (b.attributes?.attack || 0) + (b.attributes?.defense || 0);
        return powerA - powerB;
      }
    },
    {
      title: '忠诚度',
      dataIndex: 'loyalty',
      key: 'loyalty',
      render: (loyalty) => (
        <Progress
          percent={loyalty}
          size="small"
          strokeColor={loyalty >= 80 ? '#52c41a' : loyalty >= 60 ? '#faad14' : '#f5222d'}
        />
      ),
      sorter: (a, b) => a.loyalty - b.loyalty
    },
    {
      title: '进化阶段',
      key: 'evolution',
      render: (_, record) => (
        <Text>{record.evolution?.stage || 1}/{record.evolution?.maxStage || 1}</Text>
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
            title="确定删除这个宠物吗？"
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

  const filteredPets = pets.filter(pet => {
    if (activeTab === 'all') return true;
    return pet.type === activeTab;
  });

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">
          <HeartOutlined /> 宠物体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加宠物
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="宠物总数"
              value={pets.length}
              prefix={<HeartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="灵兽数量"
              value={pets.filter(p => p.type === 'spirit').length}
              prefix={<StarOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="平均忠诚度"
              value={pets.length > 0 ? Math.round(pets.reduce((sum, p) => sum + p.loyalty, 0) / pets.length) : 0}
              suffix="%"
              prefix={<HeartOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="传说宠物"
              value={pets.filter(p => p.rarity >= 4).length}
              prefix={<FireOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="全部" key="all" />
          <TabPane tab="灵兽" key="spirit" />
          <TabPane tab="野兽" key="beast" />
          <TabPane tab="龙族" key="dragon" />
          <TabPane tab="元素" key="elemental" />
          <TabPane tab="亡灵" key="undead" />
        </Tabs>

        <Table
          columns={columns}
          dataSource={filteredPets}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 只宠物`
          }}
        />
      </Card>

      <Modal
        title={editingPet ? '编辑宠物' : '添加宠物'}
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
            type: 'spirit',
            element: 'fire',
            rarity: 1,
            level: 1,
            loyalty: 50,
            tamingDifficulty: 1,
            evolutionStage: 1,
            maxStage: 1
          }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="name"
                label="宠物名称"
                rules={[{ required: true, message: '请输入宠物名称' }]}
              >
                <Input placeholder="请输入宠物名称" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="type"
                label="宠物类型"
                rules={[{ required: true, message: '请选择宠物类型' }]}
              >
                <Select>
                  <Option value="spirit">灵兽</Option>
                  <Option value="beast">野兽</Option>
                  <Option value="dragon">龙族</Option>
                  <Option value="elemental">元素</Option>
                  <Option value="undead">亡灵</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="element"
                label="属性"
                rules={[{ required: true, message: '请选择属性' }]}
              >
                <Select>
                  <Option value="fire">火</Option>
                  <Option value="water">水</Option>
                  <Option value="earth">土</Option>
                  <Option value="air">风</Option>
                  <Option value="thunder">雷</Option>
                  <Option value="ice">冰</Option>
                  <Option value="light">光</Option>
                  <Option value="dark">暗</Option>
                </Select>
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
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="level"
                label="等级"
                rules={[{ required: true, message: '请输入等级' }]}
              >
                <InputNumber min={1} max={100} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="loyalty"
                label="忠诚度"
                rules={[{ required: true, message: '请输入忠诚度' }]}
              >
                <InputNumber min={0} max={100} style={{ width: '100%' }} addonAfter="%" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={10}>
              <Form.Item name="health" label="生命值">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={7}>
              <Form.Item name="attack" label="攻击力">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={7}>
              <Form.Item name="defense" label="防御力">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="speed" label="速度">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="intelligence" label="智力">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="tamingDifficulty" label="驯服难度">
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="evolutionStage" label="进化阶段">
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="maxStage" label="最大阶段">
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="lifespan" label="寿命(年)">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="habitat" label="栖息地">
                <Input placeholder="请输入栖息地" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="nextForm" label="下一进化形态">
                <Input placeholder="请输入下一进化形态" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="skills" label="技能" extra="多个技能请用逗号分隔">
            <Input placeholder="如：火球术, 幻术, 治愈术" />
          </Form.Item>

          <Form.Item name="specialAbilities" label="特殊能力" extra="多个能力请用逗号分隔">
            <Input placeholder="如：火焰免疫, 魅惑, 预知危险" />
          </Form.Item>

          <Form.Item name="feedingRequirements" label="喂养需求">
            <Input placeholder="请输入喂养需求" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={3} placeholder="请描述宠物的外观、性格、能力等" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default PetSystems;
