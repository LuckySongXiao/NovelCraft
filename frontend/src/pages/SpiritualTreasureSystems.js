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
  Progress
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  StarOutlined,
  ThunderboltOutlined,
  FireOutlined,
  CrownOutlined,
  GiftOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const SpiritualTreasureSystems = () => {
  const { id: projectId } = useParams();
  const [treasures, setTreasures] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingTreasure, setEditingTreasure] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockTreasures = [
    {
      id: 1,
      name: '混沌钟',
      type: 'artifact',
      grade: 'chaos',
      rank: 10,
      spirituality: 5,
      powerLevel: 10000,
      attributes: {
        attack: 5000,
        defense: 8000,
        special: 3000
      },
      abilities: ['时间静止', '空间封锁', '混沌之力'],
      origin: '开天辟地时诞生',
      currentOwner: '东皇太一',
      recognitionMethod: '血脉认主',
      restrictions: ['需要混沌体质', '需要至尊修为'],
      materials: ['混沌石', '时间碎片', '空间本源'],
      refinementLevel: 49,
      maxRefinement: 49,
      description: '传说中的混沌至宝，拥有镇压一切的威能',
      specialEffects: ['免疫一切攻击', '时空掌控', '因果逆转'],
      awakening: {
        stage: 'complete',
        consciousness: 'supreme'
      },
      status: 'active'
    },
    {
      id: 2,
      name: '太极图',
      type: 'formation',
      grade: 'innate',
      rank: 9,
      spirituality: 5,
      powerLevel: 8000,
      attributes: {
        attack: 3000,
        defense: 6000,
        special: 5000
      },
      abilities: ['阴阳转换', '太极领域', '万法归一'],
      origin: '太上老君炼制',
      currentOwner: '太上老君',
      recognitionMethod: '道心认主',
      restrictions: ['需要太清道法', '需要大罗金仙修为'],
      materials: ['先天阴阳气', '太极本源', '道则碎片'],
      refinementLevel: 36,
      maxRefinement: 49,
      description: '先天灵宝，蕴含阴阳大道的至高奥义',
      specialEffects: ['阴阳调和', '道法加持', '因果护体'],
      awakening: {
        stage: 'partial',
        consciousness: 'high'
      },
      status: 'active'
    },
    {
      id: 3,
      name: '诛仙剑阵',
      type: 'array',
      grade: 'innate',
      rank: 8,
      spirituality: 4,
      powerLevel: 7000,
      attributes: {
        attack: 8000,
        defense: 2000,
        special: 4000
      },
      abilities: ['诛仙剑气', '四象杀阵', '剑意通天'],
      origin: '通天教主炼制',
      currentOwner: '通天教主',
      recognitionMethod: '剑心认主',
      restrictions: ['需要剑道天赋', '需要准圣修为'],
      materials: ['诛仙剑', '戮仙剑', '陷仙剑', '绝仙剑'],
      refinementLevel: 33,
      maxRefinement: 49,
      description: '杀伐第一的剑阵，非四圣不可破',
      specialEffects: ['无视防御', '剑气纵横', '杀意滔天'],
      awakening: {
        stage: 'partial',
        consciousness: 'medium'
      },
      status: 'active'
    }
  ];

  useEffect(() => {
    loadTreasures();
  }, [projectId]);

  const loadTreasures = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setTreasures(mockTreasures);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载灵宝体系失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingTreasure(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (treasure) => {
    setEditingTreasure(treasure);
    form.setFieldsValue({
      ...treasure,
      abilities: treasure.abilities?.join(', '),
      restrictions: treasure.restrictions?.join(', '),
      materials: treasure.materials?.join(', '),
      specialEffects: treasure.specialEffects?.join(', '),
      attack: treasure.attributes?.attack,
      defense: treasure.attributes?.defense,
      special: treasure.attributes?.special,
      awakeningStage: treasure.awakening?.stage,
      consciousness: treasure.awakening?.consciousness
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/spiritual_treasure_system/${id}`);

      // 删除成功后从列表中移除
      setTreasures(treasures.filter(t => t.id !== id));
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
        grade: values.grade,
        rank: values.rank,
        spirituality: values.spirituality,
        powerLevel: values.powerLevel,
        attributes: {
          attack: values.attack || 0,
          defense: values.defense || 0,
          special: values.special || 0
        },
        abilities: values.abilities?.split(',').map(a => a.trim()).filter(a => a) || [],
        origin: values.origin,
        currentOwner: values.currentOwner,
        recognitionMethod: values.recognitionMethod,
        restrictions: values.restrictions?.split(',').map(r => r.trim()).filter(r => r) || [],
        materials: values.materials?.split(',').map(m => m.trim()).filter(m => m) || [],
        refinementLevel: values.refinementLevel,
        maxRefinement: values.maxRefinement,
        description: values.description,
        specialEffects: values.specialEffects?.split(',').map(e => e.trim()).filter(e => e) || [],
        awakening: {
          stage: values.awakeningStage || 'none',
          consciousness: values.consciousness || 'none'
        },
        status: values.status
      };

      if (editingTreasure) {
        // 更新
        setTreasures(treasures.map(t =>
          t.id === editingTreasure.id ? { ...t, ...processedValues } : t
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newTreasure = {
          id: Date.now(),
          ...processedValues
        };
        setTreasures([...treasures, newTreasure]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getGradeColor = (grade) => {
    const colors = {
      mortal: 'default',
      spiritual: 'blue',
      treasure: 'purple',
      innate: 'orange',
      chaos: 'red',
      merit: 'gold'
    };
    return colors[grade] || 'default';
  };

  const getTypeColor = (type) => {
    const colors = {
      weapon: 'red',
      armor: 'blue',
      artifact: 'purple',
      formation: 'orange',
      pill: 'green',
      talisman: 'cyan'
    };
    return colors[type] || 'default';
  };

  const columns = [
    {
      title: '灵宝名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getGradeColor(record.grade)}>
            {record.grade === 'mortal' ? '凡品' :
             record.grade === 'spiritual' ? '灵器' :
             record.grade === 'treasure' ? '法宝' :
             record.grade === 'innate' ? '先天' :
             record.grade === 'chaos' ? '混沌' : '功德'}
          </Tag>
        </Space>
      )
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type) => (
        <Tag color={getTypeColor(type)}>
          {type === 'weapon' ? '武器' :
           type === 'armor' ? '防具' :
           type === 'artifact' ? '神器' :
           type === 'formation' ? '阵法' :
           type === 'pill' ? '丹药' : '符箓'}
        </Tag>
      )
    },
    {
      title: '品阶',
      dataIndex: 'rank',
      key: 'rank',
      render: (rank) => (
        <Space>
          <StarOutlined style={{ color: '#faad14' }} />
          <Text>{rank}阶</Text>
        </Space>
      ),
      sorter: (a, b) => a.rank - b.rank
    },
    {
      title: '灵性',
      dataIndex: 'spirituality',
      key: 'spirituality',
      render: (spirituality) => (
        <Rate disabled value={spirituality} style={{ fontSize: 16 }} />
      ),
      sorter: (a, b) => a.spirituality - b.spirituality
    },
    {
      title: '威能',
      dataIndex: 'powerLevel',
      key: 'powerLevel',
      render: (power) => (
        <Space>
          <ThunderboltOutlined style={{ color: '#722ed1' }} />
          <Text>{power?.toLocaleString()}</Text>
        </Space>
      ),
      sorter: (a, b) => a.powerLevel - b.powerLevel
    },
    {
      title: '炼化程度',
      key: 'refinement',
      render: (_, record) => (
        <Progress
          percent={Math.round((record.refinementLevel / record.maxRefinement) * 100)}
          size="small"
          format={() => `${record.refinementLevel}/${record.maxRefinement}`}
        />
      ),
      sorter: (a, b) => (a.refinementLevel / a.maxRefinement) - (b.refinementLevel / b.maxRefinement)
    },
    {
      title: '当前主人',
      dataIndex: 'currentOwner',
      key: 'currentOwner',
      render: (owner) => owner || <Text type="secondary">无主</Text>
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'active' ? 'green' : status === 'sealed' ? 'orange' : 'red'}>
          {status === 'active' ? '活跃' : status === 'sealed' ? '封印' : '损坏'}
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
            title="确定删除这个灵宝吗？"
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
          <GiftOutlined /> 灵宝体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加灵宝
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="灵宝总数"
              value={treasures.length}
              prefix={<GiftOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="先天灵宝"
              value={treasures.filter(t => t.grade === 'innate').length}
              prefix={<StarOutlined />}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="混沌至宝"
              value={treasures.filter(t => t.grade === 'chaos').length}
              prefix={<CrownOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="平均品阶"
              value={treasures.length > 0 ? (treasures.reduce((sum, t) => sum + t.rank, 0) / treasures.length).toFixed(1) : 0}
              prefix={<FireOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={treasures}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 件灵宝`
          }}
        />
      </Card>

      <Modal
        title={editingTreasure ? '编辑灵宝' : '添加灵宝'}
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
            grade: 'spiritual',
            rank: 1,
            spirituality: 1,
            powerLevel: 100,
            refinementLevel: 1,
            maxRefinement: 49,
            awakeningStage: 'none',
            consciousness: 'none',
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="灵宝名称"
                rules={[{ required: true, message: '请输入灵宝名称' }]}
              >
                <Input placeholder="请输入灵宝名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="灵宝类型"
                rules={[{ required: true, message: '请选择灵宝类型' }]}
              >
                <Select>
                  <Option value="weapon">武器</Option>
                  <Option value="armor">防具</Option>
                  <Option value="artifact">神器</Option>
                  <Option value="formation">阵法</Option>
                  <Option value="pill">丹药</Option>
                  <Option value="talisman">符箓</Option>
                </Select>
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
                  <Option value="mortal">凡品</Option>
                  <Option value="spiritual">灵器</Option>
                  <Option value="treasure">法宝</Option>
                  <Option value="innate">先天</Option>
                  <Option value="chaos">混沌</Option>
                  <Option value="merit">功德</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="rank"
                label="品阶"
                rules={[{ required: true, message: '请输入品阶' }]}
              >
                <InputNumber min={1} max={10} style={{ width: '100%' }} addonAfter="阶" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="spirituality"
                label="灵性"
                rules={[{ required: true, message: '请选择灵性' }]}
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
              <Form.Item name="special" label="特殊属性">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="powerLevel"
                label="威能等级"
                rules={[{ required: true, message: '请输入威能等级' }]}
              >
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="refinementLevel"
                label="炼化层数"
                rules={[{ required: true, message: '请输入炼化层数' }]}
              >
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="maxRefinement"
                label="最大炼化"
                rules={[{ required: true, message: '请输入最大炼化层数' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="awakeningStage"
                label="觉醒阶段"
                rules={[{ required: true, message: '请选择觉醒阶段' }]}
              >
                <Select>
                  <Option value="none">未觉醒</Option>
                  <Option value="initial">初步觉醒</Option>
                  <Option value="partial">部分觉醒</Option>
                  <Option value="complete">完全觉醒</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="consciousness"
                label="器灵意识"
                rules={[{ required: true, message: '请选择器灵意识' }]}
              >
                <Select>
                  <Option value="none">无意识</Option>
                  <Option value="low">低级</Option>
                  <Option value="medium">中级</Option>
                  <Option value="high">高级</Option>
                  <Option value="supreme">至高</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择状态' }]}
              >
                <Select>
                  <Option value="active">活跃</Option>
                  <Option value="sealed">封印</Option>
                  <Option value="damaged">损坏</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="currentOwner" label="当前主人">
                <Input placeholder="请输入当前主人" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="recognitionMethod" label="认主方式">
                <Input placeholder="如：血脉认主、道心认主等" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="origin" label="来历">
            <Input placeholder="请输入灵宝的来历" />
          </Form.Item>

          <Form.Item name="abilities" label="能力" extra="多个能力请用逗号分隔">
            <Input placeholder="如：时间静止, 空间封锁, 混沌之力" />
          </Form.Item>

          <Form.Item name="restrictions" label="使用限制" extra="多个限制请用逗号分隔">
            <Input placeholder="如：需要混沌体质, 需要至尊修为" />
          </Form.Item>

          <Form.Item name="materials" label="炼制材料" extra="多个材料请用逗号分隔">
            <Input placeholder="如：混沌石, 时间碎片, 空间本源" />
          </Form.Item>

          <Form.Item name="specialEffects" label="特殊效果" extra="多个效果请用逗号分隔">
            <Input placeholder="如：免疫一切攻击, 时空掌控, 因果逆转" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={3} placeholder="请描述灵宝的外观、历史、传说等" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default SpiritualTreasureSystems;
