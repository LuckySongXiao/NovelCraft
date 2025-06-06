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
  Divider
} from 'antd';
import {
  PlusOutlined,
  ShareAltOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  HeartOutlined,
  TeamOutlined,
  UserOutlined,
  DislikeOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const Relations = () => {
  const [relations, setRelations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingRelation, setEditingRelation] = useState(null);
  const [viewingRelation, setViewingRelation] = useState(null);
  const [form] = Form.useForm();

  // 模拟关系数据
  const mockRelations = [
    {
      id: 1,
      fromCharacter: '林天',
      toCharacter: '苏雪儿',
      relationType: 'love',
      relationName: '恋人',
      strength: 'strong',
      status: 'active',
      description: '青梅竹马，两情相悦',
      development: '从小一起长大，感情深厚，后来发展为恋人关系',
      keyEvents: ['初次相遇', '共同修炼', '表白成功'],
      influence: '相互扶持，共同成长',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20'
    },
    {
      id: 2,
      fromCharacter: '林天',
      toCharacter: '云长老',
      relationType: 'mentor',
      relationName: '师徒',
      strength: 'strong',
      status: 'active',
      description: '师父与弟子的关系',
      development: '云长老发现林天的天赋，收其为徒',
      keyEvents: ['拜师仪式', '传授功法', '指导修炼'],
      influence: '师父的指导对林天的成长至关重要',
      createdAt: '2024-01-16',
      updatedAt: '2024-01-18'
    },
    {
      id: 3,
      fromCharacter: '林天',
      toCharacter: '血煞魔君',
      relationType: 'enemy',
      relationName: '宿敌',
      strength: 'strong',
      status: 'active',
      description: '正邪对立的宿敌关系',
      development: '因理念不合而成为敌人',
      keyEvents: ['初次交锋', '生死决斗', '势不两立'],
      influence: '推动剧情发展的重要对立关系',
      createdAt: '2024-01-17',
      updatedAt: '2024-01-19'
    },
    {
      id: 4,
      fromCharacter: '苏雪儿',
      toCharacter: '苏长老',
      relationType: 'family',
      relationName: '父女',
      strength: 'strong',
      status: 'active',
      description: '血缘亲情关系',
      development: '天生的父女关系，感情深厚',
      keyEvents: ['出生', '成长陪伴', '修炼指导'],
      influence: '家庭背景对苏雪儿性格形成的影响',
      createdAt: '2024-01-18',
      updatedAt: '2024-01-20'
    }
  ];

  useEffect(() => {
    setRelations(mockRelations);
  }, []);

  // 关系类型配置
  const relationTypeConfig = {
    love: { color: 'red', text: '恋人', icon: <HeartOutlined /> },
    family: { color: 'blue', text: '亲情', icon: <TeamOutlined /> },
    friend: { color: 'green', text: '友情', icon: <UserOutlined /> },
    mentor: { color: 'orange', text: '师徒', icon: <UserOutlined /> },
    enemy: { color: 'red', text: '敌对', icon: <DislikeOutlined /> },
    rival: { color: 'purple', text: '竞争', icon: <ThunderboltOutlined /> },
    ally: { color: 'cyan', text: '盟友', icon: <TeamOutlined /> },
    neutral: { color: 'default', text: '中性', icon: <UserOutlined /> }
  };

  // 关系强度配置
  const strengthConfig = {
    weak: { color: 'default', text: '微弱' },
    medium: { color: 'blue', text: '一般' },
    strong: { color: 'orange', text: '强烈' },
    extreme: { color: 'red', text: '极强' }
  };

  // 状态配置
  const statusConfig = {
    active: { color: 'green', text: '活跃' },
    inactive: { color: 'default', text: '冷淡' },
    broken: { color: 'red', text: '破裂' },
    developing: { color: 'blue', text: '发展中' }
  };

  // 表格列配置
  const columns = [
    {
      title: '关系双方',
      key: 'characters',
      render: (_, record) => (
        <Space direction="vertical" size="small">
          <Text strong>{record.fromCharacter}</Text>
          <ShareAltOutlined style={{ color: '#1890ff' }} />
          <Text strong>{record.toCharacter}</Text>
        </Space>
      )
    },
    {
      title: '关系类型',
      dataIndex: 'relationType',
      key: 'relationType',
      render: (type) => (
        <Tag color={relationTypeConfig[type].color} icon={relationTypeConfig[type].icon}>
          {relationTypeConfig[type].text}
        </Tag>
      ),
      filters: [
        { text: '恋人', value: 'love' },
        { text: '亲情', value: 'family' },
        { text: '友情', value: 'friend' },
        { text: '师徒', value: 'mentor' },
        { text: '敌对', value: 'enemy' },
        { text: '竞争', value: 'rival' },
        { text: '盟友', value: 'ally' }
      ],
      onFilter: (value, record) => record.relationType === value
    },
    {
      title: '关系名称',
      dataIndex: 'relationName',
      key: 'relationName'
    },
    {
      title: '关系强度',
      dataIndex: 'strength',
      key: 'strength',
      render: (strength) => (
        <Tag color={strengthConfig[strength].color}>
          {strengthConfig[strength].text}
        </Tag>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={statusConfig[status].color}>
          {statusConfig[status].text}
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
          <Tooltip title="AI分析">
            <Button
              type="text"
              icon={<RobotOutlined />}
              onClick={() => handleAIAnalyze(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个关系吗？"
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

  // 处理新建/编辑关系
  const handleCreateOrEdit = () => {
    setEditingRelation(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (relation) => {
    setEditingRelation(relation);
    form.setFieldsValue({
      ...relation,
      keyEvents: relation.keyEvents.join('\n')
    });
    setModalVisible(true);
  };

  const handleView = (relation) => {
    setViewingRelation(relation);
    setDetailModalVisible(true);
  };

  const handleAIAnalyze = (relation) => {
    message.info(`AI分析关系：${relation.fromCharacter} - ${relation.toCharacter}`);
  };

  const handleDelete = (id) => {
    setRelations(relations.filter(r => r.id !== id));
    message.success('关系删除成功');
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段
      const processedValues = {
        ...values,
        keyEvents: values.keyEvents ? values.keyEvents.split('\n').filter(item => item.trim()) : []
      };

      if (editingRelation) {
        // 编辑关系
        setRelations(relations.map(r =>
          r.id === editingRelation.id
            ? { ...r, ...processedValues, updatedAt: new Date().toISOString().split('T')[0] }
            : r
        ));
        message.success('关系更新成功');
      } else {
        // 新建关系
        const newRelation = {
          id: Date.now(),
          ...processedValues,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setRelations([...relations, newRelation]);
        message.success('关系创建成功');
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
  const totalRelations = relations.length;
  const loveRelations = relations.filter(r => r.relationType === 'love').length;
  const familyRelations = relations.filter(r => r.relationType === 'family').length;
  const enemyRelations = relations.filter(r => r.relationType === 'enemy').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">关系网络</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总关系数"
              value={totalRelations}
              prefix={<ShareAltOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="恋爱关系"
              value={loveRelations}
              prefix={<HeartOutlined style={{ color: '#f5222d' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="亲情关系"
              value={familyRelations}
              prefix={<TeamOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="敌对关系"
              value={enemyRelations}
              prefix={<DislikeOutlined style={{ color: '#fa8c16' }} />}
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
              添加关系
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={relations}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个关系`
          }}
        />
      </Card>

      {/* 新建/编辑关系模态框 */}
      <Modal
        title={editingRelation ? '编辑关系' : '新建关系'}
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
            relationType: 'friend',
            strength: 'medium',
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="fromCharacter"
                label="人物A"
                rules={[{ required: true, message: '请输入人物A' }]}
              >
                <Input placeholder="请输入人物名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="toCharacter"
                label="人物B"
                rules={[{ required: true, message: '请输入人物B' }]}
              >
                <Input placeholder="请输入人物名称" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="relationType"
                label="关系类型"
                rules={[{ required: true, message: '请选择关系类型' }]}
              >
                <Select>
                  <Option value="love">恋人</Option>
                  <Option value="family">亲情</Option>
                  <Option value="friend">友情</Option>
                  <Option value="mentor">师徒</Option>
                  <Option value="enemy">敌对</Option>
                  <Option value="rival">竞争</Option>
                  <Option value="ally">盟友</Option>
                  <Option value="neutral">中性</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="strength"
                label="关系强度"
                rules={[{ required: true, message: '请选择关系强度' }]}
              >
                <Select>
                  <Option value="weak">微弱</Option>
                  <Option value="medium">一般</Option>
                  <Option value="strong">强烈</Option>
                  <Option value="extreme">极强</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="status"
                label="关系状态"
                rules={[{ required: true, message: '请选择关系状态' }]}
              >
                <Select>
                  <Option value="active">活跃</Option>
                  <Option value="inactive">冷淡</Option>
                  <Option value="broken">破裂</Option>
                  <Option value="developing">发展中</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="relationName"
            label="关系名称"
            rules={[{ required: true, message: '请输入关系名称' }]}
          >
            <Input placeholder="如：恋人、师徒、宿敌等" />
          </Form.Item>

          <Form.Item
            name="description"
            label="关系描述"
            rules={[{ required: true, message: '请输入关系描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请简要描述这个关系的特点"
            />
          </Form.Item>

          <Form.Item
            name="development"
            label="关系发展"
          >
            <TextArea
              rows={3}
              placeholder="请描述这个关系是如何发展形成的"
            />
          </Form.Item>

          <Form.Item
            name="keyEvents"
            label="关键事件"
            tooltip="每行一个事件"
          >
            <TextArea
              rows={3}
              placeholder="如：初次相遇&#10;共同经历&#10;关系转折"
            />
          </Form.Item>

          <Form.Item
            name="influence"
            label="关系影响"
          >
            <TextArea
              rows={2}
              placeholder="这个关系对双方或剧情产生的影响"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 关系详情查看模态框 */}
      <Modal
        title="关系详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={800}
      >
        {viewingRelation && (
          <div>
            <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
              <Descriptions.Item label="关系双方" span={2}>
                <Space size="large">
                  <Text strong>{viewingRelation.fromCharacter}</Text>
                  <ShareAltOutlined style={{ color: '#1890ff', fontSize: '16px' }} />
                  <Text strong>{viewingRelation.toCharacter}</Text>
                </Space>
              </Descriptions.Item>

              <Descriptions.Item label="关系类型">
                <Tag color={relationTypeConfig[viewingRelation.relationType].color}
                     icon={relationTypeConfig[viewingRelation.relationType].icon}>
                  {relationTypeConfig[viewingRelation.relationType].text}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="关系名称">{viewingRelation.relationName}</Descriptions.Item>

              <Descriptions.Item label="关系强度">
                <Tag color={strengthConfig[viewingRelation.strength].color}>
                  {strengthConfig[viewingRelation.strength].text}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="关系状态">
                <Tag color={statusConfig[viewingRelation.status].color}>
                  {statusConfig[viewingRelation.status].text}
                </Tag>
              </Descriptions.Item>

              <Descriptions.Item label="创建时间">{viewingRelation.createdAt}</Descriptions.Item>
              <Descriptions.Item label="更新时间">{viewingRelation.updatedAt}</Descriptions.Item>

              <Descriptions.Item label="关系描述" span={2}>
                <Paragraph>{viewingRelation.description}</Paragraph>
              </Descriptions.Item>

              {viewingRelation.development && (
                <Descriptions.Item label="关系发展" span={2}>
                  <Paragraph>{viewingRelation.development}</Paragraph>
                </Descriptions.Item>
              )}

              {viewingRelation.influence && (
                <Descriptions.Item label="关系影响" span={2}>
                  <Paragraph>{viewingRelation.influence}</Paragraph>
                </Descriptions.Item>
              )}
            </Descriptions>

            {viewingRelation.keyEvents && viewingRelation.keyEvents.length > 0 && (
              <Card title="关键事件" size="small" style={{ marginTop: 16 }}>
                <Space direction="vertical" style={{ width: '100%' }}>
                  {viewingRelation.keyEvents.map((event, index) => (
                    <div key={index} style={{ padding: '8px 0', borderBottom: index < viewingRelation.keyEvents.length - 1 ? '1px solid #f0f0f0' : 'none' }}>
                      <Text>• {event}</Text>
                    </div>
                  ))}
                </Space>
              </Card>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Relations;