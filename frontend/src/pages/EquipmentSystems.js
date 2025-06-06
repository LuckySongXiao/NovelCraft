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
  ShoppingOutlined,
  ThunderboltOutlined,
  SafetyOutlined,
  CrownOutlined,
  StarOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const EquipmentSystems = () => {
  const { id: projectId } = useParams();
  const [equipment, setEquipment] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingEquipment, setEditingEquipment] = useState(null);
  const [activeTab, setActiveTab] = useState('weapon');
  const [form] = Form.useForm();

  // 模拟数据
  const mockEquipment = [
    {
      id: 1,
      name: '龙鳞剑',
      type: 'weapon',
      category: 'sword',
      grade: 'legendary',
      level: 50,
      attributes: {
        attack: 1200,
        durability: 800,
        criticalRate: 15
      },
      requirements: {
        level: 45,
        strength: 200,
        cultivation: '元婴期'
      },
      effects: ['龙威：攻击时有10%几率震慑敌人', '破甲：无视30%防御'],
      materials: ['龙鳞', '玄铁', '灵石'],
      description: '传说中的神兵，蕴含真龙之力',
      rarity: 5,
      value: 100000
    },
    {
      id: 2,
      name: '凤羽护甲',
      type: 'armor',
      category: 'chest',
      grade: 'epic',
      level: 40,
      attributes: {
        defense: 800,
        durability: 600,
        magicResist: 25
      },
      requirements: {
        level: 35,
        constitution: 150,
        cultivation: '金丹期'
      },
      effects: ['凤凰庇护：受到致命伤害时有20%几率免疫', '火焰抗性：减少50%火焰伤害'],
      materials: ['凤羽', '秘银', '火晶石'],
      description: '凤凰羽毛编织而成的护甲，轻盈而坚固',
      rarity: 4,
      value: 50000
    }
  ];

  useEffect(() => {
    loadEquipment();
  }, [projectId]);

  const loadEquipment = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setEquipment(mockEquipment);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载装备体系失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingEquipment(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (item) => {
    setEditingEquipment(item);
    form.setFieldsValue({
      ...item,
      effects: item.effects?.join('\n'),
      materials: item.materials?.join(', '),
      attack: item.attributes?.attack,
      defense: item.attributes?.defense,
      durability: item.attributes?.durability,
      criticalRate: item.attributes?.criticalRate,
      magicResist: item.attributes?.magicResist,
      reqLevel: item.requirements?.level,
      reqStrength: item.requirements?.strength,
      reqConstitution: item.requirements?.constitution,
      reqCultivation: item.requirements?.cultivation
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/equipment_system/${id}`);

      // 删除成功后从列表中移除
      setEquipment(equipment.filter(e => e.id !== id));
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
        category: values.category,
        grade: values.grade,
        level: values.level,
        attributes: {
          attack: values.attack || 0,
          defense: values.defense || 0,
          durability: values.durability || 0,
          criticalRate: values.criticalRate || 0,
          magicResist: values.magicResist || 0
        },
        requirements: {
          level: values.reqLevel || 0,
          strength: values.reqStrength || 0,
          constitution: values.reqConstitution || 0,
          cultivation: values.reqCultivation || ''
        },
        effects: values.effects?.split('\n').filter(e => e.trim()) || [],
        materials: values.materials?.split(',').map(m => m.trim()).filter(m => m) || [],
        description: values.description,
        rarity: values.rarity,
        value: values.value
      };

      if (editingEquipment) {
        // 更新
        setEquipment(equipment.map(e =>
          e.id === editingEquipment.id ? { ...e, ...processedValues } : e
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newEquipment = {
          id: Date.now(),
          ...processedValues
        };
        setEquipment([...equipment, newEquipment]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      weapon: 'red',
      armor: 'blue',
      accessory: 'purple',
      consumable: 'green'
    };
    return colors[type] || 'default';
  };

  const getGradeColor = (grade) => {
    const colors = {
      common: 'default',
      uncommon: 'blue',
      rare: 'purple',
      epic: 'orange',
      legendary: 'red',
      mythic: 'gold'
    };
    return colors[grade] || 'default';
  };

  const columns = [
    {
      title: '装备名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'weapon' ? '武器' :
             record.type === 'armor' ? '防具' :
             record.type === 'accessory' ? '饰品' : '消耗品'}
          </Tag>
        </Space>
      )
    },
    {
      title: '品级',
      dataIndex: 'grade',
      key: 'grade',
      render: (grade) => (
        <Tag color={getGradeColor(grade)}>
          {grade === 'common' ? '普通' :
           grade === 'uncommon' ? '优秀' :
           grade === 'rare' ? '稀有' :
           grade === 'epic' ? '史诗' :
           grade === 'legendary' ? '传说' : '神话'}
        </Tag>
      )
    },
    {
      title: '等级',
      dataIndex: 'level',
      key: 'level',
      sorter: (a, b) => a.level - b.level
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
      title: '主属性',
      key: 'mainAttribute',
      render: (_, record) => {
        if (record.type === 'weapon') {
          return (
            <Space>
              <ThunderboltOutlined style={{ color: '#f5222d' }} />
              <Text>{record.attributes?.attack || 0}</Text>
            </Space>
          );
        } else if (record.type === 'armor') {
          return (
            <Space>
              <SafetyOutlined style={{ color: '#1890ff' }} />
              <Text>{record.attributes?.defense || 0}</Text>
            </Space>
          );
        }
        return '-';
      }
    },
    {
      title: '价值',
      dataIndex: 'value',
      key: 'value',
      render: (value) => `${value?.toLocaleString() || 0} 金币`,
      sorter: (a, b) => a.value - b.value
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
            title="确定删除这个装备吗？"
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

  const filteredEquipment = equipment.filter(item => {
    if (activeTab === 'all') return true;
    return item.type === activeTab;
  });

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">
          <ShoppingOutlined /> 装备体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加装备
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="装备总数"
              value={equipment.length}
              prefix={<ShoppingOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="武器数量"
              value={equipment.filter(e => e.type === 'weapon').length}
              prefix={<ThunderboltOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="防具数量"
              value={equipment.filter(e => e.type === 'armor').length}
              prefix={<SafetyOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="传说装备"
              value={equipment.filter(e => e.grade === 'legendary').length}
              prefix={<CrownOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Tabs activeKey={activeTab} onChange={setActiveTab}>
          <TabPane tab="全部" key="all" />
          <TabPane tab="武器" key="weapon" />
          <TabPane tab="防具" key="armor" />
          <TabPane tab="饰品" key="accessory" />
          <TabPane tab="消耗品" key="consumable" />
        </Tabs>

        <Table
          columns={columns}
          dataSource={filteredEquipment}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 件装备`
          }}
        />
      </Card>

      <Modal
        title={editingEquipment ? '编辑装备' : '添加装备'}
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
            type: 'weapon',
            category: 'sword',
            grade: 'common',
            level: 1,
            rarity: 1,
            value: 100
          }}
        >
          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="name"
                label="装备名称"
                rules={[{ required: true, message: '请输入装备名称' }]}
              >
                <Input placeholder="请输入装备名称" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="type"
                label="装备类型"
                rules={[{ required: true, message: '请选择装备类型' }]}
              >
                <Select>
                  <Option value="weapon">武器</Option>
                  <Option value="armor">防具</Option>
                  <Option value="accessory">饰品</Option>
                  <Option value="consumable">消耗品</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="category"
                label="装备分类"
                rules={[{ required: true, message: '请输入装备分类' }]}
              >
                <Input placeholder="如：剑、盾、戒指等" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="grade"
                label="品级"
                rules={[{ required: true, message: '请选择品级' }]}
              >
                <Select>
                  <Option value="common">普通</Option>
                  <Option value="uncommon">优秀</Option>
                  <Option value="rare">稀有</Option>
                  <Option value="epic">史诗</Option>
                  <Option value="legendary">传说</Option>
                  <Option value="mythic">神话</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="level"
                label="装备等级"
                rules={[{ required: true, message: '请输入装备等级' }]}
              >
                <InputNumber min={1} max={100} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="rarity"
                label="稀有度"
                rules={[{ required: true, message: '请选择稀有度' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="attack" label="攻击力">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="defense" label="防御力">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="durability" label="耐久度">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="criticalRate" label="暴击率(%)">
                <InputNumber min={0} max={100} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="magicResist" label="魔抗(%)">
                <InputNumber min={0} max={100} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="value" label="价值(金币)">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="reqLevel" label="需求等级">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="reqStrength" label="需求力量">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="reqConstitution" label="需求体质">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="reqCultivation" label="需求修为">
            <Input placeholder="如：金丹期、元婴期等" />
          </Form.Item>

          <Form.Item name="materials" label="制作材料" extra="多个材料请用逗号分隔">
            <Input placeholder="如：龙鳞, 玄铁, 灵石" />
          </Form.Item>

          <Form.Item name="effects" label="特殊效果" extra="每行一个效果">
            <TextArea rows={3} placeholder="如：龙威：攻击时有10%几率震慑敌人" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={3} placeholder="请描述装备的外观、历史背景等" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default EquipmentSystems;
