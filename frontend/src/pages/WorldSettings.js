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
  Tabs,
  Collapse
} from 'antd';
import {
  PlusOutlined,
  GlobalOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  EnvironmentOutlined,
  HistoryOutlined,
  BankOutlined,
  TeamOutlined,
  BookOutlined,
  DollarOutlined,
  ShopOutlined,
  UsergroupAddOutlined,
  ThunderboltOutlined,
  ToolOutlined,
  HeartOutlined,
  CompassOutlined,
  GatewayOutlined,
  StarOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { Panel } = Collapse;

const WorldSettings = () => {
  const [settings, setSettings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingSetting, setEditingSetting] = useState(null);
  const [viewingSetting, setViewingSetting] = useState(null);
  const [form] = Form.useForm();

  // 模拟世界设定数据
  const mockSettings = [
    {
      id: 1,
      name: '修仙世界基础设定',
      category: 'world_basic',
      description: '修仙世界的基本世界观和规则',
      content: {
        worldName: '九州大陆',
        geography: '九州大陆分为九个州，每州都有不同的地理环境和修炼资源',
        history: '上古时期，仙魔大战，仙界封印，修仙者只能在凡间修炼',
        politics: '各大宗门割据一方，皇朝统治凡人，修仙者超然物外',
        economy: '以灵石为主要货币，凡人使用金银铜钱',
        culture: '尊师重道，强者为尊，追求长生不老'
      },
      status: 'active',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-16'
    },
    {
      id: 2,
      name: '修炼体系',
      category: 'cultivation',
      description: '详细的修炼境界和体系',
      content: {
        realms: ['练气期', '筑基期', '金丹期', '元婴期', '化神期', '合体期', '大乘期', '渡劫期'],
        methods: '吸收天地灵气，炼化为真元，淬炼肉身和神魂',
        resources: '灵石、丹药、法器、功法、灵草',
        bottlenecks: '每个大境界都有天劫考验',
        lifespan: '每提升一个大境界，寿命大幅增加'
      },
      status: 'active',
      createdAt: '2024-01-17',
      updatedAt: '2024-01-18'
    },
    {
      id: 3,
      name: '宗门势力',
      category: 'factions',
      description: '各大宗门和势力的详细设定',
      content: {
        majorSects: ['青云宗', '天剑门', '万花谷', '血煞门'],
        relationships: '正邪对立，内部也有竞争',
        territories: '各占一方，互不侵犯',
        resources: '控制灵脉和修炼资源',
        hierarchy: '宗主、长老、内门弟子、外门弟子'
      },
      status: 'draft',
      createdAt: '2024-01-19',
      updatedAt: '2024-01-19'
    }
  ];

  useEffect(() => {
    setSettings(mockSettings);
  }, []);

  // 设定类型配置
  const categoryConfig = {
    world_basic: { color: 'blue', text: '世界基础', icon: <GlobalOutlined /> },
    geography: { color: 'green', text: '地理环境', icon: <EnvironmentOutlined /> },
    history: { color: 'orange', text: '历史文化', icon: <HistoryOutlined /> },
    politics: { color: 'red', text: '政治体系', icon: <BankOutlined /> },
    currency: { color: 'gold', text: '货币体系', icon: <DollarOutlined /> },
    commerce: { color: 'lime', text: '商业体系', icon: <ShopOutlined /> },
    races: { color: 'magenta', text: '种族类别', icon: <UsergroupAddOutlined /> },
    martial_arts: { color: 'volcano', text: '功法体系', icon: <ThunderboltOutlined /> },
    equipment: { color: 'orange', text: '装备体系', icon: <ToolOutlined /> },
    pets: { color: 'pink', text: '宠物体系', icon: <HeartOutlined /> },
    maps: { color: 'cyan', text: '地图结构', icon: <CompassOutlined /> },
    dimensions: { color: 'purple', text: '维度结构', icon: <GatewayOutlined /> },
    spiritual_treasures: { color: 'gold', text: '灵宝体系', icon: <StarOutlined /> },
    cultivation: { color: 'geekblue', text: '修炼体系', icon: <BookOutlined /> },
    factions: { color: 'lime', text: '势力组织', icon: <TeamOutlined /> },
    economy: { color: 'green', text: '经济制度', icon: <BankOutlined /> },
    other: { color: 'default', text: '其他', icon: <GlobalOutlined /> }
  };

  // 表格列配置
  const columns = [
    {
      title: '设定名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          {categoryConfig[record.category].icon}
          <Text strong>{text}</Text>
        </Space>
      )
    },
    {
      title: '类型',
      dataIndex: 'category',
      key: 'category',
      render: (category) => (
        <Tag color={categoryConfig[category].color}>
          {categoryConfig[category].text}
        </Tag>
      ),
      filters: Object.keys(categoryConfig).map(key => ({
        text: categoryConfig[key].text,
        value: key
      })),
      onFilter: (value, record) => record.category === value
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'active' ? 'green' : 'orange'}>
          {status === 'active' ? '已完成' : '草稿'}
        </Tag>
      )
    },
    {
      title: '更新时间',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
      sorter: (a, b) => new Date(a.updatedAt) - new Date(b.updatedAt)
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
            title="确定删除这个设定吗？"
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

  // 处理新建/编辑设定
  const handleCreateOrEdit = () => {
    setEditingSetting(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (setting) => {
    setEditingSetting(setting);
    form.setFieldsValue({
      ...setting,
      ...setting.content
    });
    setModalVisible(true);
  };

  const handleView = (setting) => {
    setViewingSetting(setting);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (setting) => {
    message.info(`AI生成世界设定：${setting.name}`);
  };

  const handleDelete = (id) => {
    setSettings(settings.filter(s => s.id !== id));
    message.success('设定删除成功');
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 分离基本信息和内容
      const { name, category, description, status, ...content } = values;
      const processedValues = {
        name,
        category,
        description,
        status,
        content
      };

      if (editingSetting) {
        // 编辑设定
        setSettings(settings.map(s =>
          s.id === editingSetting.id
            ? { ...s, ...processedValues, updatedAt: new Date().toISOString().split('T')[0] }
            : s
        ));
        message.success('设定更新成功');
      } else {
        // 新建设定
        const newSetting = {
          id: Date.now(),
          ...processedValues,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setSettings([...settings, newSetting]);
        message.success('设定创建成功');
      }

      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 统计数据
  const totalSettings = settings.length;
  const activeSettings = settings.filter(s => s.status === 'active').length;
  const draftSettings = settings.filter(s => s.status === 'draft').length;
  const categoryStats = Object.keys(categoryConfig).reduce((acc, key) => {
    acc[key] = settings.filter(s => s.category === key).length;
    return acc;
  }, {});

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">世界设定</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总设定数"
              value={totalSettings}
              prefix={<GlobalOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已完成"
              value={activeSettings}
              prefix={<BookOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="草稿"
              value={draftSettings}
              prefix={<EditOutlined style={{ color: '#faad14' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="修炼体系"
              value={categoryStats.cultivation || 0}
              prefix={<BookOutlined style={{ color: '#722ed1' }} />}
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
              添加设定
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={settings}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个设定`
          }}
        />
      </Card>

      {/* 新建/编辑设定模态框 */}
      <Modal
        title={editingSetting ? '编辑世界设定' : '新建世界设定'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={loading}
        width={1000}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            category: 'world_basic',
            status: 'draft'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="设定名称"
                rules={[{ required: true, message: '请输入设定名称' }]}
              >
                <Input placeholder="请输入设定名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="category"
                label="设定类型"
                rules={[{ required: true, message: '请选择设定类型' }]}
              >
                <Select>
                  {Object.keys(categoryConfig).map(key => (
                    <Option key={key} value={key}>
                      {categoryConfig[key].text}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="设定描述"
            rules={[{ required: true, message: '请输入设定描述' }]}
          >
            <TextArea
              rows={2}
              placeholder="简要描述这个设定的内容和作用"
            />
          </Form.Item>

          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择状态' }]}
          >
            <Select>
              <Option value="draft">草稿</Option>
              <Option value="active">已完成</Option>
            </Select>
          </Form.Item>

          <Tabs defaultActiveKey="basic">
            <TabPane tab="基础信息" key="basic">
              <Form.Item name="worldName" label="世界名称">
                <Input placeholder="如：九州大陆、修仙界等" />
              </Form.Item>

              <Form.Item name="overview" label="世界概述">
                <TextArea
                  rows={4}
                  placeholder="描述世界的整体情况和特色..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="地理环境" key="geography">
              <Form.Item name="geography" label="地理描述">
                <TextArea
                  rows={4}
                  placeholder="描述世界的地理环境、地形地貌..."
                />
              </Form.Item>

              <Form.Item name="climate" label="气候环境">
                <TextArea
                  rows={3}
                  placeholder="描述气候特点、季节变化..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="历史文化" key="history">
              <Form.Item name="history" label="历史背景">
                <TextArea
                  rows={4}
                  placeholder="描述世界的历史发展、重大事件..."
                />
              </Form.Item>

              <Form.Item name="culture" label="文化特色">
                <TextArea
                  rows={3}
                  placeholder="描述文化传统、价值观念..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="政治经济" key="politics">
              <Form.Item name="politics" label="政治体系">
                <TextArea
                  rows={3}
                  placeholder="描述政治制度、权力结构..."
                />
              </Form.Item>

              <Form.Item name="economy" label="经济制度">
                <TextArea
                  rows={3}
                  placeholder="描述经济体系、货币制度..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="货币体系" key="currency">
              <Form.Item name="currencyName" label="主要货币">
                <Input placeholder="如：灵石、金币等" />
              </Form.Item>

              <Form.Item name="currencySystem" label="货币制度">
                <TextArea
                  rows={3}
                  placeholder="描述货币制度、汇率体系..."
                />
              </Form.Item>

              <Form.Item name="monetaryPolicy" label="货币政策">
                <TextArea
                  rows={3}
                  placeholder="描述发行机构、监管制度..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="商业体系" key="commerce">
              <Form.Item name="tradeRoutes" label="贸易路线">
                <TextArea
                  rows={3}
                  placeholder="描述主要贸易路线、商业网络..."
                />
              </Form.Item>

              <Form.Item name="guilds" label="商会组织">
                <TextArea
                  rows={3}
                  placeholder="描述商会、公会等商业组织..."
                />
              </Form.Item>

              <Form.Item name="marketRules" label="市场规则">
                <TextArea
                  rows={3}
                  placeholder="描述市场机制、商业法规..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="种族类别" key="races">
              <Form.Item name="majorRaces" label="主要种族">
                <TextArea
                  rows={3}
                  placeholder="描述世界中的主要种族..."
                />
              </Form.Item>

              <Form.Item name="raceRelations" label="种族关系">
                <TextArea
                  rows={3}
                  placeholder="描述种族间的关系、冲突..."
                />
              </Form.Item>

              <Form.Item name="raceTraits" label="种族特征">
                <TextArea
                  rows={3}
                  placeholder="描述各种族的特殊能力、文化..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="功法体系" key="martial_arts">
              <Form.Item name="techniqueTypes" label="功法分类">
                <TextArea
                  rows={3}
                  placeholder="描述功法的分类、等级..."
                />
              </Form.Item>

              <Form.Item name="cultivationMethods" label="修炼方法">
                <TextArea
                  rows={3}
                  placeholder="描述修炼方式、资源需求..."
                />
              </Form.Item>

              <Form.Item name="martialArtsRules" label="功法规则">
                <TextArea
                  rows={3}
                  placeholder="描述功法的限制、禁忌..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="装备体系" key="equipment">
              <Form.Item name="equipmentTypes" label="装备分类">
                <TextArea
                  rows={3}
                  placeholder="描述装备的类型、品级..."
                />
              </Form.Item>

              <Form.Item name="enhancementSystem" label="强化系统">
                <TextArea
                  rows={3}
                  placeholder="描述装备强化、升级机制..."
                />
              </Form.Item>

              <Form.Item name="craftingSystem" label="制作系统">
                <TextArea
                  rows={3}
                  placeholder="描述装备制作、材料需求..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="宠物体系" key="pets">
              <Form.Item name="petTypes" label="宠物分类">
                <TextArea
                  rows={3}
                  placeholder="描述宠物的种类、稀有度..."
                />
              </Form.Item>

              <Form.Item name="petEvolution" label="进化系统">
                <TextArea
                  rows={3}
                  placeholder="描述宠物进化、成长机制..."
                />
              </Form.Item>

              <Form.Item name="petSkills" label="技能系统">
                <TextArea
                  rows={3}
                  placeholder="描述宠物技能、培养方式..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="地图结构" key="maps">
              <Form.Item name="mapHierarchy" label="地图层级">
                <TextArea
                  rows={3}
                  placeholder="描述地图的层级结构..."
                />
              </Form.Item>

              <Form.Item name="terrainTypes" label="地形类型">
                <TextArea
                  rows={3}
                  placeholder="描述各种地形特征..."
                />
              </Form.Item>

              <Form.Item name="specialAreas" label="特殊区域">
                <TextArea
                  rows={3}
                  placeholder="描述特殊地点、秘境..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="维度结构" key="dimensions">
              <Form.Item name="dimensionTypes" label="维度类型">
                <TextArea
                  rows={3}
                  placeholder="描述不同维度的特征..."
                />
              </Form.Item>

              <Form.Item name="dimensionLaws" label="维度法则">
                <TextArea
                  rows={3}
                  placeholder="描述各维度的物理法则..."
                />
              </Form.Item>

              <Form.Item name="dimensionTravel" label="维度穿越">
                <TextArea
                  rows={3}
                  placeholder="描述维度间的旅行方式..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="灵宝体系" key="spiritual_treasures">
              <Form.Item name="treasureGrades" label="灵宝品级">
                <TextArea
                  rows={3}
                  placeholder="描述灵宝的品级划分..."
                />
              </Form.Item>

              <Form.Item name="spiritSystem" label="器灵系统">
                <TextArea
                  rows={3}
                  placeholder="描述器灵的觉醒、能力..."
                />
              </Form.Item>

              <Form.Item name="refiningMethods" label="炼制方法">
                <TextArea
                  rows={3}
                  placeholder="描述灵宝的炼制、升级..."
                />
              </Form.Item>
            </TabPane>

            <TabPane tab="特殊规则" key="rules">
              <Form.Item name="rules" label="世界规则">
                <TextArea
                  rows={4}
                  placeholder="描述世界的特殊规则、法则..."
                />
              </Form.Item>

              <Form.Item name="magic" label="力量体系">
                <TextArea
                  rows={3}
                  placeholder="描述修炼、魔法等力量体系..."
                />
              </Form.Item>
            </TabPane>
          </Tabs>
        </Form>
      </Modal>

      {/* 设定详情模态框 */}
      <Modal
        title="世界设定详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={1000}
      >
        {viewingSetting && (
          <div>
            <Row gutter={16} style={{ marginBottom: 16 }}>
              <Col span={24}>
                <Title level={3}>{viewingSetting.name}</Title>
                <Space>
                  <Tag color={categoryConfig[viewingSetting.category].color}>
                    {categoryConfig[viewingSetting.category].text}
                  </Tag>
                  <Tag color={viewingSetting.status === 'active' ? 'green' : 'orange'}>
                    {viewingSetting.status === 'active' ? '已完成' : '草稿'}
                  </Tag>
                </Space>
                <Paragraph style={{ marginTop: 16 }}>
                  {viewingSetting.description}
                </Paragraph>
              </Col>
            </Row>

            <Collapse defaultActiveKey={['1']}>
              {viewingSetting.content.worldName && (
                <Panel header="世界名称" key="1">
                  <Text>{viewingSetting.content.worldName}</Text>
                </Panel>
              )}

              {viewingSetting.content.geography && (
                <Panel header="地理环境" key="2">
                  <Paragraph>{viewingSetting.content.geography}</Paragraph>
                </Panel>
              )}

              {viewingSetting.content.history && (
                <Panel header="历史背景" key="3">
                  <Paragraph>{viewingSetting.content.history}</Paragraph>
                </Panel>
              )}

              {viewingSetting.content.politics && (
                <Panel header="政治体系" key="4">
                  <Paragraph>{viewingSetting.content.politics}</Paragraph>
                </Panel>
              )}

              {viewingSetting.content.economy && (
                <Panel header="经济制度" key="5">
                  <Paragraph>{viewingSetting.content.economy}</Paragraph>
                </Panel>
              )}

              {viewingSetting.content.culture && (
                <Panel header="文化特色" key="6">
                  <Paragraph>{viewingSetting.content.culture}</Paragraph>
                </Panel>
              )}

              {viewingSetting.content.currencySystem && (
                <Panel header="货币体系" key="7">
                  <Paragraph>{viewingSetting.content.currencySystem}</Paragraph>
                  {viewingSetting.content.currencyName && (
                    <Text strong>主要货币：{viewingSetting.content.currencyName}</Text>
                  )}
                </Panel>
              )}

              {viewingSetting.content.tradeRoutes && (
                <Panel header="商业体系" key="8">
                  <Paragraph>{viewingSetting.content.tradeRoutes}</Paragraph>
                  {viewingSetting.content.guilds && (
                    <Paragraph><Text strong>商会组织：</Text>{viewingSetting.content.guilds}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.majorRaces && (
                <Panel header="种族类别" key="9">
                  <Paragraph>{viewingSetting.content.majorRaces}</Paragraph>
                  {viewingSetting.content.raceRelations && (
                    <Paragraph><Text strong>种族关系：</Text>{viewingSetting.content.raceRelations}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.techniqueTypes && (
                <Panel header="功法体系" key="10">
                  <Paragraph>{viewingSetting.content.techniqueTypes}</Paragraph>
                  {viewingSetting.content.cultivationMethods && (
                    <Paragraph><Text strong>修炼方法：</Text>{viewingSetting.content.cultivationMethods}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.equipmentTypes && (
                <Panel header="装备体系" key="11">
                  <Paragraph>{viewingSetting.content.equipmentTypes}</Paragraph>
                  {viewingSetting.content.enhancementSystem && (
                    <Paragraph><Text strong>强化系统：</Text>{viewingSetting.content.enhancementSystem}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.petTypes && (
                <Panel header="宠物体系" key="12">
                  <Paragraph>{viewingSetting.content.petTypes}</Paragraph>
                  {viewingSetting.content.petEvolution && (
                    <Paragraph><Text strong>进化系统：</Text>{viewingSetting.content.petEvolution}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.mapHierarchy && (
                <Panel header="地图结构" key="13">
                  <Paragraph>{viewingSetting.content.mapHierarchy}</Paragraph>
                  {viewingSetting.content.terrainTypes && (
                    <Paragraph><Text strong>地形类型：</Text>{viewingSetting.content.terrainTypes}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.dimensionTypes && (
                <Panel header="维度结构" key="14">
                  <Paragraph>{viewingSetting.content.dimensionTypes}</Paragraph>
                  {viewingSetting.content.dimensionLaws && (
                    <Paragraph><Text strong>维度法则：</Text>{viewingSetting.content.dimensionLaws}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.treasureGrades && (
                <Panel header="灵宝体系" key="15">
                  <Paragraph>{viewingSetting.content.treasureGrades}</Paragraph>
                  {viewingSetting.content.spiritSystem && (
                    <Paragraph><Text strong>器灵系统：</Text>{viewingSetting.content.spiritSystem}</Paragraph>
                  )}
                </Panel>
              )}

              {viewingSetting.content.rules && (
                <Panel header="世界规则" key="16">
                  <Paragraph>{viewingSetting.content.rules}</Paragraph>
                </Panel>
              )}
            </Collapse>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default WorldSettings;
