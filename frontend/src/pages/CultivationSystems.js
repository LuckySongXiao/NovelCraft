import React, { useState, useEffect } from 'react';
import {
  Card,
  Typography,
  Button,
  Table,
  Space,
  Tag,
  Modal,
  Form,
  Input,
  Select,
  message,
  Popconfirm,
  Tooltip,
  Row,
  Col,
  Statistic,
  Descriptions,
  Steps,
  InputNumber,
  Collapse,
  Divider,
  List
} from 'antd';
import {
  PlusOutlined,
  ThunderboltOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  FireOutlined,
  StarOutlined,
  CrownOutlined,
  TrophyOutlined,
  MinusCircleOutlined,
  PlusCircleOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { Step } = Steps;
const { Panel } = Collapse;

const CultivationSystems = () => {
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [levelEditModalVisible, setLevelEditModalVisible] = useState(false);
  const [editingSystem, setEditingSystem] = useState(null);
  const [viewingSystem, setViewingSystem] = useState(null);
  const [editingLevels, setEditingLevels] = useState([]);
  const [form] = Form.useForm();
  const [levelForm] = Form.useForm();

  // 模拟修炼体系数据
  const mockSystems = [
    {
      id: 1,
      name: '仙道修炼体系',
      type: 'immortal',
      category: 'traditional',
      description: '传统的仙侠修炼体系，以灵气修炼为主',
      totalLevels: 9,
      levels: [
        {
          name: '练气期',
          description: '初入修仙，感知灵气，开始修炼基础',
          requirements: '天赋觉醒，拜师入门',
          power: 1,
          abilities: ['感知灵气', '基础吐纳'],
          resources: ['聚气丹', '灵石'],
          duration: '1-3年',
          risks: ['走火入魔', '经脉受损']
        },
        {
          name: '筑基期',
          description: '筑建修炼根基，打通经脉',
          requirements: '练气九层圆满，筑基丹',
          power: 3,
          abilities: ['御器飞行', '简单法术'],
          resources: ['筑基丹', '中品灵石'],
          duration: '5-10年',
          risks: ['筑基失败', '根基不稳']
        },
        {
          name: '金丹期',
          description: '凝结金丹，寿命大增',
          requirements: '筑基圆满，结丹机缘',
          power: 8,
          abilities: ['金丹神通', '炼制法器'],
          resources: ['结丹灵药', '上品灵石'],
          duration: '10-30年',
          risks: ['结丹失败', '丹毒侵体']
        },
        {
          name: '元婴期',
          description: '元婴出窍，神识大增',
          requirements: '金丹破碎重组',
          power: 20,
          abilities: ['元婴出窍', '神识攻击'],
          resources: ['化婴丹', '极品灵石'],
          duration: '30-100年',
          risks: ['元婴夭折', '神识受创']
        },
        {
          name: '化神期',
          description: '神识化形，法则初窥',
          requirements: '元婴成熟，感悟法则',
          power: 50,
          abilities: ['法则运用', '空间挪移'],
          resources: ['化神果', '仙灵石'],
          duration: '100-300年',
          risks: ['法则反噬', '心魔入侵']
        },
        {
          name: '炼虚期',
          description: '炼化虚空，掌控空间',
          requirements: '化神圆满，空间感悟',
          power: 100,
          abilities: ['空间撕裂', '虚空遁术'],
          resources: ['虚空石', '混沌气'],
          duration: '300-500年',
          risks: ['空间风暴', '虚空迷失']
        },
        {
          name: '合体期',
          description: '天人合一，与道相合',
          requirements: '炼虚巅峰，道心圆满',
          power: 200,
          abilities: ['天地法相', '道法自然'],
          resources: ['合体丹', '天地灵气'],
          duration: '500-1000年',
          risks: ['天劫降临', '道心崩坏']
        },
        {
          name: '大乘期',
          description: '大道有成，接近仙道',
          requirements: '合体圆满，功德圆满',
          power: 500,
          abilities: ['移山填海', '呼风唤雨'],
          resources: ['大乘丹', '功德之力'],
          duration: '1000-3000年',
          risks: ['心魔劫', '因果劫']
        },
        {
          name: '渡劫期',
          description: '渡天劫成仙，超脱凡俗',
          requirements: '大乘巅峰，天劫降临',
          power: 1000,
          abilities: ['仙术神通', '不死不灭'],
          resources: ['渡劫丹', '天劫之力'],
          duration: '不定',
          risks: ['天劫灭杀', '飞升失败']
        }
      ],
      attributes: ['灵力', '神识', '体魄'],
      techniques: ['吐纳术', '御剑术', '炼丹术'],
      resources: ['灵石', '丹药', '法器'],
      advantages: ['寿命悠长', '神通广大', '超脱凡俗'],
      disadvantages: ['修炼缓慢', '资源消耗大', '天劫危险'],
      status: 'active',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      name: '武道修炼体系',
      type: 'martial',
      category: 'physical',
      description: '以武功修炼为主的体系，注重身体锻炼',
      totalLevels: 7,
      levels: [
        { name: '后天境', description: '初学武功', requirements: '基础体质', power: 1 },
        { name: '先天境', description: '打通经脉', requirements: '后天圆满', power: 3 },
        { name: '宗师境', description: '武道宗师', requirements: '先天巅峰', power: 8 },
        { name: '大宗师', description: '武道大成', requirements: '宗师圆满', power: 15 },
        { name: '武圣境', description: '武道圣者', requirements: '大宗师巅峰', power: 30 },
        { name: '武神境', description: '武道之神', requirements: '武圣圆满', power: 60 },
        { name: '武帝境', description: '武道帝者', requirements: '武神巅峰', power: 120 }
      ],
      attributes: ['力量', '速度', '防御'],
      techniques: ['内功心法', '外功招式', '轻功身法'],
      resources: ['秘籍', '丹药', '兵器'],
      advantages: ['战斗力强', '修炼直接', '适应性强'],
      disadvantages: ['寿命有限', '突破困难', '依赖天赋'],
      status: 'active',
      createdAt: '2024-01-16'
    },
    {
      id: 3,
      name: '魔道修炼体系',
      type: 'demonic',
      category: 'dark',
      description: '魔道修炼体系，以吞噬他人修为为主',
      totalLevels: 6,
      levels: [
        { name: '魔徒', description: '初入魔道', requirements: '堕入魔道', power: 2 },
        { name: '魔士', description: '魔道小成', requirements: '魔徒圆满', power: 5 },
        { name: '魔将', description: '魔道有成', requirements: '魔士巅峰', power: 15 },
        { name: '魔王', description: '魔道王者', requirements: '魔将圆满', power: 40 },
        { name: '魔皇', description: '魔道皇者', requirements: '魔王巅峰', power: 100 },
        { name: '魔帝', description: '魔道至尊', requirements: '魔皇圆满', power: 300 }
      ],
      attributes: ['魔力', '杀意', '血气'],
      techniques: ['吞噬术', '魔功', '血祭'],
      resources: ['魔石', '血丹', '魔器'],
      advantages: ['修炼快速', '战力强大', '恢复力强'],
      disadvantages: ['心魔缠身', '众人敌视', '容易走火入魔'],
      status: 'active',
      createdAt: '2024-01-17'
    }
  ];

  useEffect(() => {
    setSystems(mockSystems);
  }, []);

  // 体系类型配置
  const typeConfig = {
    immortal: { color: 'blue', text: '仙道', icon: <StarOutlined /> },
    martial: { color: 'orange', text: '武道', icon: <FireOutlined /> },
    demonic: { color: 'red', text: '魔道', icon: <ThunderboltOutlined /> },
    divine: { color: 'gold', text: '神道', icon: <CrownOutlined /> },
    beast: { color: 'green', text: '妖道', icon: <TrophyOutlined /> }
  };

  // 分类配置
  const categoryConfig = {
    traditional: { color: 'blue', text: '传统' },
    physical: { color: 'orange', text: '体修' },
    mental: { color: 'purple', text: '神修' },
    dark: { color: 'red', text: '邪道' },
    special: { color: 'gold', text: '特殊' }
  };

  // 表格列配置
  const columns = [
    {
      title: '体系名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          {typeConfig[record.type].icon}
          <Text strong>{text}</Text>
        </Space>
      )
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type) => (
        <Tag color={typeConfig[type].color}>
          {typeConfig[type].text}
        </Tag>
      ),
      filters: [
        { text: '仙道', value: 'immortal' },
        { text: '武道', value: 'martial' },
        { text: '魔道', value: 'demonic' },
        { text: '神道', value: 'divine' },
        { text: '妖道', value: 'beast' }
      ],
      onFilter: (value, record) => record.type === value
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      render: (category) => (
        <Tag color={categoryConfig[category].color}>
          {categoryConfig[category].text}
        </Tag>
      )
    },
    {
      title: '境界数量',
      dataIndex: 'totalLevels',
      key: 'totalLevels',
      render: (levels) => `${levels} 个境界`,
      sorter: (a, b) => a.totalLevels - b.totalLevels
    },
    {
      title: '主要属性',
      dataIndex: 'attributes',
      key: 'attributes',
      render: (attributes) => (
        <Space wrap>
          {attributes.slice(0, 2).map((attr, index) => (
            <Tag key={index} size="small">{attr}</Tag>
          ))}
          {attributes.length > 2 && <Text type="secondary">...</Text>}
        </Space>
      )
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt',
      sorter: (a, b) => new Date(a.createdAt) - new Date(b.createdAt)
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Tooltip title="查看详情">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => handleView(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Tooltip title="AI生成">
            <Button
              type="text"
              icon={<RobotOutlined />}
              onClick={() => handleAIGenerate(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个修炼体系吗？"
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

  // 处理新建/编辑修炼体系
  const handleCreateOrEdit = () => {
    setEditingSystem(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (system) => {
    setEditingSystem(system);
    form.setFieldsValue({
      ...system,
      attributes: system.attributes.join('\n'),
      techniques: system.techniques.join('\n'),
      resources: system.resources.join('\n'),
      advantages: system.advantages.join('\n'),
      disadvantages: system.disadvantages.join('\n')
    });
    setModalVisible(true);
  };

  const handleView = (system) => {
    setViewingSystem(system);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (system) => {
    message.info(`AI生成修炼体系：${system.name}`);
  };

  const handleDelete = (id) => {
    setSystems(systems.filter(s => s.id !== id));
    message.success('修炼体系删除成功');
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段
      const processedValues = {
        ...values,
        attributes: values.attributes ? values.attributes.split('\n').filter(item => item.trim()) : [],
        techniques: values.techniques ? values.techniques.split('\n').filter(item => item.trim()) : [],
        resources: values.resources ? values.resources.split('\n').filter(item => item.trim()) : [],
        advantages: values.advantages ? values.advantages.split('\n').filter(item => item.trim()) : [],
        disadvantages: values.disadvantages ? values.disadvantages.split('\n').filter(item => item.trim()) : [],
        levels: editingSystem ? editingSystem.levels : [] // 保留原有境界信息
      };

      if (editingSystem) {
        // 编辑体系
        setSystems(systems.map(s =>
          s.id === editingSystem.id
            ? { ...s, ...processedValues }
            : s
        ));
        message.success('修炼体系更新成功');
      } else {
        // 新建体系
        const newSystem = {
          id: Date.now(),
          ...processedValues,
          totalLevels: 0,
          status: 'active',
          createdAt: new Date().toISOString().split('T')[0]
        };
        setSystems([...systems, newSystem]);
        message.success('修炼体系创建成功');
      }

      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 处理境界编辑
  const handleLevelEdit = () => {
    if (viewingSystem && viewingSystem.levels) {
      setEditingLevels([...viewingSystem.levels]);
      levelForm.setFieldsValue({
        levels: viewingSystem.levels
      });
    } else {
      setEditingLevels([]);
      levelForm.resetFields();
    }
    setLevelEditModalVisible(true);
  };

  const handleLevelModalOk = async () => {
    try {
      const values = await levelForm.validateFields();
      setLoading(true);

      // 更新体系的境界信息
      const updatedSystem = {
        ...viewingSystem,
        levels: editingLevels,
        totalLevels: editingLevels.length
      };

      setSystems(systems.map(s =>
        s.id === viewingSystem.id ? updatedSystem : s
      ));

      setViewingSystem(updatedSystem);
      setLevelEditModalVisible(false);
      message.success('境界信息更新成功');
    } catch (error) {
      console.error('境界编辑失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 添加新境界
  const addLevel = () => {
    const newLevel = {
      name: '',
      description: '',
      requirements: '',
      power: 1,
      abilities: [],
      resources: [],
      duration: '',
      risks: []
    };
    setEditingLevels([...editingLevels, newLevel]);
  };

  // 删除境界
  const removeLevel = (index) => {
    const newLevels = editingLevels.filter((_, i) => i !== index);
    setEditingLevels(newLevels);
  };

  // 更新境界信息
  const updateLevel = (index, field, value) => {
    const newLevels = [...editingLevels];
    if (field === 'abilities' || field === 'resources' || field === 'risks') {
      newLevels[index][field] = value.split(',').map(item => item.trim()).filter(item => item);
    } else {
      newLevels[index][field] = value;
    }
    setEditingLevels(newLevels);
  };

  // 统计数据
  const totalSystems = systems.length;
  const immortalSystems = systems.filter(s => s.type === 'immortal').length;
  const martialSystems = systems.filter(s => s.type === 'martial').length;
  const demonicSystems = systems.filter(s => s.type === 'demonic').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">修炼体系</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总体系数"
              value={totalSystems}
              prefix={<ThunderboltOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="仙道体系"
              value={immortalSystems}
              prefix={<StarOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="武道体系"
              value={martialSystems}
              prefix={<FireOutlined style={{ color: '#fa8c16' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="魔道体系"
              value={demonicSystems}
              prefix={<ThunderboltOutlined style={{ color: '#f5222d' }} />}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <div className="toolbar">
          <div className="toolbar-left">
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleCreateOrEdit}
            >
              创建体系
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={systems}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个修炼体系`
          }}
        />
      </Card>

      {/* 新建/编辑修炼体系模态框 */}
      <Modal
        title={editingSystem ? '编辑修炼体系' : '新建修炼体系'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={loading}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            type: 'immortal',
            category: 'traditional'
          }}
        >
          <Row gutter={16}>
            <Col span={16}>
              <Form.Item
                name="name"
                label="体系名称"
                rules={[{ required: true, message: '请输入体系名称' }]}
              >
                <Input placeholder="请输入修炼体系名称" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="type"
                label="体系类型"
                rules={[{ required: true, message: '请选择体系类型' }]}
              >
                <Select>
                  <Option value="immortal">仙道</Option>
                  <Option value="martial">武道</Option>
                  <Option value="demonic">魔道</Option>
                  <Option value="divine">神道</Option>
                  <Option value="beast">妖道</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="category"
                label="修炼分类"
                rules={[{ required: true, message: '请选择修炼分类' }]}
              >
                <Select>
                  <Option value="traditional">传统</Option>
                  <Option value="physical">体修</Option>
                  <Option value="mental">神修</Option>
                  <Option value="dark">邪道</Option>
                  <Option value="special">特殊</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="totalLevels"
                label="境界数量"
              >
                <InputNumber min={1} max={20} style={{ width: '100%' }} placeholder="境界总数" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="体系描述"
            rules={[{ required: true, message: '请输入体系描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述这个修炼体系的特点和原理"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="attributes"
                label="主要属性"
                tooltip="每行一个属性"
              >
                <TextArea
                  rows={3}
                  placeholder="如：灵力&#10;神识&#10;体魄"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="techniques"
                label="修炼技法"
                tooltip="每行一个技法"
              >
                <TextArea
                  rows={3}
                  placeholder="如：吐纳术&#10;御剑术&#10;炼丹术"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="resources"
                label="修炼资源"
                tooltip="每行一个资源"
              >
                <TextArea
                  rows={2}
                  placeholder="如：灵石&#10;丹药&#10;法器"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="advantages"
                label="体系优势"
                tooltip="每行一个优势"
              >
                <TextArea
                  rows={2}
                  placeholder="如：寿命悠长&#10;神通广大"
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="disadvantages"
            label="体系劣势"
            tooltip="每行一个劣势"
          >
            <TextArea
              rows={2}
              placeholder="如：修炼缓慢&#10;资源消耗大"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 修炼体系详情查看模态框 */}
      <Modal
        title="修炼体系详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={1000}
      >
        {viewingSystem && (
          <div>
            <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
              <Descriptions.Item label="体系名称" span={2}>
                <Space>
                  {typeConfig[viewingSystem.type].icon}
                  <Text strong>{viewingSystem.name}</Text>
                  <Tag color={typeConfig[viewingSystem.type].color}>
                    {typeConfig[viewingSystem.type].text}
                  </Tag>
                  <Tag color={categoryConfig[viewingSystem.category].color}>
                    {categoryConfig[viewingSystem.category].text}
                  </Tag>
                </Space>
              </Descriptions.Item>

              <Descriptions.Item label="境界数量">{viewingSystem.totalLevels} 个境界</Descriptions.Item>
              <Descriptions.Item label="创建时间">{viewingSystem.createdAt}</Descriptions.Item>

              <Descriptions.Item label="体系描述" span={2}>
                <Paragraph>{viewingSystem.description}</Paragraph>
              </Descriptions.Item>
            </Descriptions>

            {/* 境界等级展示 */}
            {viewingSystem.levels && viewingSystem.levels.length > 0 && (
              <Card
                title="境界等级"
                style={{ marginBottom: 16 }}
                extra={
                  <Button
                    type="primary"
                    size="small"
                    icon={<EditOutlined />}
                    onClick={handleLevelEdit}
                  >
                    编辑境界
                  </Button>
                }
              >
                <Steps
                  direction="vertical"
                  size="small"
                  current={viewingSystem.levels.length}
                >
                  {viewingSystem.levels.map((level, index) => (
                    <Step
                      key={index}
                      title={
                        <Space>
                          <Text strong>{level.name}</Text>
                          <Tag color="blue">第{index + 1}境</Tag>
                          {level.power && (
                            <Tag color="red">战力: {level.power}</Tag>
                          )}
                        </Space>
                      }
                      description={
                        <div style={{ marginTop: 8 }}>
                          <Paragraph style={{ marginBottom: 8 }}>
                            <Text>{level.description}</Text>
                          </Paragraph>
                          <Row gutter={[8, 4]}>
                            <Col span={24}>
                              <Text type="secondary" strong>突破条件：</Text>
                              <Text type="secondary">{level.requirements}</Text>
                            </Col>
                            {level.abilities && level.abilities.length > 0 && (
                              <Col span={24}>
                                <Text type="secondary" strong>获得能力：</Text>
                                <Space wrap style={{ marginTop: 4 }}>
                                  {level.abilities.map((ability, idx) => (
                                    <Tag key={idx} color="green" size="small">{ability}</Tag>
                                  ))}
                                </Space>
                              </Col>
                            )}
                            {level.resources && level.resources.length > 0 && (
                              <Col span={24}>
                                <Text type="secondary" strong>所需资源：</Text>
                                <Space wrap style={{ marginTop: 4 }}>
                                  {level.resources.map((resource, idx) => (
                                    <Tag key={idx} color="orange" size="small">{resource}</Tag>
                                  ))}
                                </Space>
                              </Col>
                            )}
                            {level.duration && (
                              <Col span={24}>
                                <Text type="secondary" strong>修炼周期：</Text>
                                <Text type="secondary">{level.duration}</Text>
                              </Col>
                            )}
                            {level.risks && level.risks.length > 0 && (
                              <Col span={24}>
                                <Text type="secondary" strong>修炼风险：</Text>
                                <Space wrap style={{ marginTop: 4 }}>
                                  {level.risks.map((risk, idx) => (
                                    <Tag key={idx} color="volcano" size="small">{risk}</Tag>
                                  ))}
                                </Space>
                              </Col>
                            )}
                          </Row>
                        </div>
                      }
                    />
                  ))}
                </Steps>
              </Card>
            )}

            <Row gutter={16}>
              <Col span={12}>
                <Card title="主要属性" size="small">
                  {viewingSystem.attributes && viewingSystem.attributes.length > 0 ? (
                    <Space wrap>
                      {viewingSystem.attributes.map((attr, index) => (
                        <Tag key={index} color="blue">{attr}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无属性信息</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card title="修炼技法" size="small">
                  {viewingSystem.techniques && viewingSystem.techniques.length > 0 ? (
                    <Space wrap>
                      {viewingSystem.techniques.map((technique, index) => (
                        <Tag key={index} color="green">{technique}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无技法信息</Text>
                  )}
                </Card>
              </Col>
            </Row>

            <Row gutter={16} style={{ marginTop: 16 }}>
              <Col span={12}>
                <Card title="修炼资源" size="small">
                  {viewingSystem.resources && viewingSystem.resources.length > 0 ? (
                    <Space wrap>
                      {viewingSystem.resources.map((resource, index) => (
                        <Tag key={index} color="orange">{resource}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无资源信息</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Collapse size="small">
                  <Panel header="体系优劣势分析" key="1">
                    <Row gutter={16}>
                      <Col span={12}>
                        <Text strong style={{ color: '#52c41a' }}>优势：</Text>
                        <br />
                        {viewingSystem.advantages && viewingSystem.advantages.length > 0 ? (
                          viewingSystem.advantages.map((advantage, index) => (
                            <div key={index}>
                              <Text>• {advantage}</Text>
                            </div>
                          ))
                        ) : (
                          <Text type="secondary">暂无优势信息</Text>
                        )}
                      </Col>
                      <Col span={12}>
                        <Text strong style={{ color: '#f5222d' }}>劣势：</Text>
                        <br />
                        {viewingSystem.disadvantages && viewingSystem.disadvantages.length > 0 ? (
                          viewingSystem.disadvantages.map((disadvantage, index) => (
                            <div key={index}>
                              <Text>• {disadvantage}</Text>
                            </div>
                          ))
                        ) : (
                          <Text type="secondary">暂无劣势信息</Text>
                        )}
                      </Col>
                    </Row>
                  </Panel>
                </Collapse>
              </Col>
            </Row>
          </div>
        )}
      </Modal>

      {/* 境界编辑模态框 */}
      <Modal
        title="编辑修炼境界"
        open={levelEditModalVisible}
        onOk={handleLevelModalOk}
        onCancel={() => {
          setLevelEditModalVisible(false);
          setEditingLevels([]);
          levelForm.resetFields();
        }}
        confirmLoading={loading}
        width={1200}
        style={{ top: 20 }}
      >
        <div style={{ marginBottom: 16 }}>
          <Button
            type="dashed"
            icon={<PlusCircleOutlined />}
            onClick={addLevel}
            style={{ width: '100%' }}
          >
            添加新境界
          </Button>
        </div>

        <div style={{ maxHeight: '60vh', overflowY: 'auto' }}>
          {editingLevels.map((level, index) => (
            <Card
              key={index}
              size="small"
              title={
                <Space>
                  <Text strong>第 {index + 1} 境界</Text>
                  <Tag color="blue">{level.name || '未命名'}</Tag>
                </Space>
              }
              extra={
                <Popconfirm
                  title="确定删除这个境界吗？"
                  onConfirm={() => removeLevel(index)}
                  okText="确定"
                  cancelText="取消"
                >
                  <Button
                    type="text"
                    danger
                    icon={<MinusCircleOutlined />}
                    size="small"
                  >
                    删除
                  </Button>
                </Popconfirm>
              }
              style={{ marginBottom: 16 }}
            >
              <Row gutter={16}>
                <Col span={8}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>境界名称</Text>
                    <Input
                      value={level.name}
                      onChange={(e) => updateLevel(index, 'name', e.target.value)}
                      placeholder="如：练气期"
                      style={{ marginTop: 4 }}
                    />
                  </div>
                </Col>
                <Col span={8}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>战力指数</Text>
                    <InputNumber
                      value={level.power}
                      onChange={(value) => updateLevel(index, 'power', value)}
                      min={1}
                      style={{ width: '100%', marginTop: 4 }}
                      placeholder="战力数值"
                    />
                  </div>
                </Col>
                <Col span={8}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>修炼周期</Text>
                    <Input
                      value={level.duration}
                      onChange={(e) => updateLevel(index, 'duration', e.target.value)}
                      placeholder="如：1-3年"
                      style={{ marginTop: 4 }}
                    />
                  </div>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={24}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>境界描述</Text>
                    <TextArea
                      value={level.description}
                      onChange={(e) => updateLevel(index, 'description', e.target.value)}
                      placeholder="描述这个境界的特点和修炼状态"
                      rows={2}
                      style={{ marginTop: 4 }}
                    />
                  </div>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={24}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>突破条件</Text>
                    <TextArea
                      value={level.requirements}
                      onChange={(e) => updateLevel(index, 'requirements', e.target.value)}
                      placeholder="描述突破到这个境界需要的条件"
                      rows={2}
                      style={{ marginTop: 4 }}
                    />
                  </div>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={12}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>获得能力</Text>
                    <Tooltip title="多个能力用逗号分隔">
                      <Input
                        value={level.abilities ? level.abilities.join(', ') : ''}
                        onChange={(e) => updateLevel(index, 'abilities', e.target.value)}
                        placeholder="如：感知灵气, 基础吐纳"
                        style={{ marginTop: 4 }}
                      />
                    </Tooltip>
                  </div>
                </Col>
                <Col span={12}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>所需资源</Text>
                    <Tooltip title="多个资源用逗号分隔">
                      <Input
                        value={level.resources ? level.resources.join(', ') : ''}
                        onChange={(e) => updateLevel(index, 'resources', e.target.value)}
                        placeholder="如：聚气丹, 灵石"
                        style={{ marginTop: 4 }}
                      />
                    </Tooltip>
                  </div>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col span={24}>
                  <div style={{ marginBottom: 12 }}>
                    <Text strong>修炼风险</Text>
                    <Tooltip title="多个风险用逗号分隔">
                      <Input
                        value={level.risks ? level.risks.join(', ') : ''}
                        onChange={(e) => updateLevel(index, 'risks', e.target.value)}
                        placeholder="如：走火入魔, 经脉受损"
                        style={{ marginTop: 4 }}
                      />
                    </Tooltip>
                  </div>
                </Col>
              </Row>

              {/* 境界预览 */}
              <Divider style={{ margin: '12px 0' }} />
              <div>
                <Text type="secondary" strong>预览效果：</Text>
                <div style={{ marginTop: 8, padding: 12, backgroundColor: '#fafafa', borderRadius: 6 }}>
                  <Space>
                    <Text strong>{level.name || '未命名境界'}</Text>
                    <Tag color="blue">第{index + 1}境</Tag>
                    {level.power && <Tag color="red">战力: {level.power}</Tag>}
                  </Space>
                  <div style={{ marginTop: 8 }}>
                    <Text>{level.description || '暂无描述'}</Text>
                  </div>
                  <div style={{ marginTop: 4 }}>
                    <Text type="secondary">突破条件：{level.requirements || '暂无'}</Text>
                  </div>
                  {level.abilities && level.abilities.length > 0 && (
                    <div style={{ marginTop: 4 }}>
                      <Text type="secondary">获得能力：</Text>
                      <Space wrap style={{ marginLeft: 8 }}>
                        {level.abilities.map((ability, idx) => (
                          <Tag key={idx} color="green" size="small">{ability}</Tag>
                        ))}
                      </Space>
                    </div>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>

        {editingLevels.length === 0 && (
          <div style={{ textAlign: 'center', padding: '40px 0', color: '#999' }}>
            <Text type="secondary">暂无境界信息，点击上方按钮添加新境界</Text>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default CultivationSystems;