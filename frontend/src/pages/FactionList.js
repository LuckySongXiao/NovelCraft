import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
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
  InputNumber,
  Rate
} from 'antd';
import {
  PlusOutlined,
  TeamOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  CrownOutlined,
  SafetyOutlined,
  ToolOutlined,
  HomeOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const FactionList = () => {
  const { id: projectId } = useParams();
  const [factions, setFactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingFaction, setEditingFaction] = useState(null);
  const [viewingFaction, setViewingFaction] = useState(null);
  const [form] = Form.useForm();

  // 模拟势力数据
  const mockFactions = [
    {
      id: 1,
      name: '青云宗',
      type: 'sect',
      level: 'major',
      territory: '青云山脉',
      leader: '云长老',
      memberCount: 3000,
      strength: 4,
      influence: 5,
      description: '修仙界的正道大宗，以剑法闻名天下',
      history: '创立于三千年前，历经数代传承',
      specialties: ['剑法', '炼丹', '阵法'],
      allies: ['天剑门', '玄天宗'],
      enemies: ['血煞门', '魔道联盟'],
      resources: ['灵石矿', '药园', '剑冢'],
      status: 'active',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      name: '血煞门',
      type: 'sect',
      level: 'major',
      territory: '血煞谷',
      leader: '血煞魔君',
      memberCount: 1500,
      strength: 4,
      influence: 3,
      description: '魔道势力，以血煞功法著称',
      history: '魔道崛起的代表势力',
      specialties: ['血煞功', '魔道秘术', '炼魂术'],
      allies: ['魔道联盟'],
      enemies: ['青云宗', '正道联盟'],
      resources: ['血池', '魔石矿'],
      status: 'active',
      createdAt: '2024-01-16'
    },
    {
      id: 3,
      name: '商盟',
      type: 'organization',
      level: 'medium',
      territory: '各大城市',
      leader: '商会会长',
      memberCount: 5000,
      strength: 2,
      influence: 4,
      description: '修仙界最大的商业组织',
      history: '由各大商家联合组成',
      specialties: ['贸易', '情报', '物流'],
      allies: ['中立势力'],
      enemies: [],
      resources: ['商路', '仓库', '金库'],
      status: 'active',
      createdAt: '2024-01-17'
    }
  ];

  useEffect(() => {
    setFactions(mockFactions);
  }, []);

  // 势力类型配置
  const typeConfig = {
    sect: { color: 'blue', text: '宗门', icon: <HomeOutlined /> },
    family: { color: 'green', text: '家族', icon: <TeamOutlined /> },
    organization: { color: 'orange', text: '组织', icon: <SafetyOutlined /> },
    empire: { color: 'purple', text: '帝国', icon: <CrownOutlined /> },
    alliance: { color: 'gold', text: '联盟', icon: <ToolOutlined /> }
  };

  // 势力等级配置
  const levelConfig = {
    minor: { color: 'default', text: '小型' },
    medium: { color: 'blue', text: '中型' },
    major: { color: 'orange', text: '大型' },
    super: { color: 'red', text: '超级' }
  };

  // 表格列配置
  const columns = [
    {
      title: '势力名称',
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
        { text: '宗门', value: 'sect' },
        { text: '家族', value: 'family' },
        { text: '组织', value: 'organization' },
        { text: '帝国', value: 'empire' },
        { text: '联盟', value: 'alliance' }
      ],
      onFilter: (value, record) => record.type === value
    },
    {
      title: '等级',
      dataIndex: 'level',
      key: 'level',
      render: (level) => (
        <Tag color={levelConfig[level].color}>
          {levelConfig[level].text}
        </Tag>
      )
    },
    {
      title: '领袖',
      dataIndex: 'leader',
      key: 'leader'
    },
    {
      title: '成员数量',
      dataIndex: 'memberCount',
      key: 'memberCount',
      render: (count) => count.toLocaleString(),
      sorter: (a, b) => a.memberCount - b.memberCount
    },
    {
      title: '实力',
      dataIndex: 'strength',
      key: 'strength',
      render: (strength) => (
        <Rate disabled value={strength} style={{ fontSize: 14 }} />
      ),
      sorter: (a, b) => a.strength - b.strength
    },
    {
      title: '影响力',
      dataIndex: 'influence',
      key: 'influence',
      render: (influence) => (
        <Rate disabled value={influence} style={{ fontSize: 14 }} />
      ),
      sorter: (a, b) => a.influence - b.influence
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
            title="确定删除这个势力吗？"
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

  // 处理新建/编辑势力
  const handleCreateOrEdit = () => {
    setEditingFaction(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (faction) => {
    setEditingFaction(faction);
    form.setFieldsValue({
      ...faction,
      specialties: faction.specialties.join('\n'),
      allies: faction.allies.join('\n'),
      enemies: faction.enemies.join('\n'),
      resources: faction.resources.join('\n')
    });
    setModalVisible(true);
  };

  const handleView = (faction) => {
    setViewingFaction(faction);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (faction) => {
    message.info(`AI生成势力详情：${faction.name}`);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/faction/${id}`);

      // 删除成功后从列表中移除
      setFactions(factions.filter(f => f.id !== id));
      message.success('势力删除成功');
    } catch (error) {
      console.error('删除势力失败:', error);
      message.error('删除势力失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段
      const processedValues = {
        ...values,
        specialties: values.specialties ? values.specialties.split('\n').filter(item => item.trim()) : [],
        allies: values.allies ? values.allies.split('\n').filter(item => item.trim()) : [],
        enemies: values.enemies ? values.enemies.split('\n').filter(item => item.trim()) : [],
        resources: values.resources ? values.resources.split('\n').filter(item => item.trim()) : []
      };

      if (editingFaction) {
        // 编辑势力
        setFactions(factions.map(f =>
          f.id === editingFaction.id
            ? { ...f, ...processedValues }
            : f
        ));
        message.success('势力更新成功');
      } else {
        // 新建势力
        const newFaction = {
          id: Date.now(),
          ...processedValues,
          status: 'active',
          createdAt: new Date().toISOString().split('T')[0]
        };
        setFactions([...factions, newFaction]);
        message.success('势力创建成功');
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
  const totalFactions = factions.length;
  const sects = factions.filter(f => f.type === 'sect').length;
  const organizations = factions.filter(f => f.type === 'organization').length;
  const families = factions.filter(f => f.type === 'family').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">势力管理</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总势力数"
              value={totalFactions}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="宗门"
              value={sects}
              prefix={<HomeOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="组织"
              value={organizations}
              prefix={<SafetyOutlined style={{ color: '#fa8c16' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="家族"
              value={families}
              prefix={<TeamOutlined style={{ color: '#52c41a' }} />}
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
              添加势力
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={factions}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个势力`
          }}
        />
      </Card>

      {/* 新建/编辑势力模态框 */}
      <Modal
        title={editingFaction ? '编辑势力' : '新建势力'}
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
            type: 'sect',
            level: 'medium',
            strength: 3,
            influence: 3,
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="势力名称"
                rules={[{ required: true, message: '请输入势力名称' }]}
              >
                <Input placeholder="请输入势力名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="势力类型"
                rules={[{ required: true, message: '请选择势力类型' }]}
              >
                <Select>
                  <Option value="sect">宗门</Option>
                  <Option value="family">家族</Option>
                  <Option value="organization">组织</Option>
                  <Option value="empire">帝国</Option>
                  <Option value="alliance">联盟</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="level"
                label="势力等级"
                rules={[{ required: true, message: '请选择势力等级' }]}
              >
                <Select>
                  <Option value="minor">小型</Option>
                  <Option value="medium">中型</Option>
                  <Option value="major">大型</Option>
                  <Option value="super">超级</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="leader"
                label="领袖"
                rules={[{ required: true, message: '请输入领袖名称' }]}
              >
                <Input placeholder="请输入领袖名称" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="memberCount"
                label="成员数量"
                rules={[{ required: true, message: '请输入成员数量' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="territory"
                label="势力范围"
                rules={[{ required: true, message: '请输入势力范围' }]}
              >
                <Input placeholder="如：青云山脉、血煞谷等" />
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                name="strength"
                label="实力等级"
                rules={[{ required: true, message: '请选择实力等级' }]}
              >
                <Rate />
              </Form.Item>
            </Col>
            <Col span={6}>
              <Form.Item
                name="influence"
                label="影响力"
                rules={[{ required: true, message: '请选择影响力' }]}
              >
                <Rate />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="势力描述"
            rules={[{ required: true, message: '请输入势力描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述势力的基本情况、特色等"
            />
          </Form.Item>

          <Form.Item
            name="history"
            label="势力历史"
          >
            <TextArea
              rows={2}
              placeholder="请描述势力的发展历史"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="specialties"
                label="特色能力"
                tooltip="每行一个能力"
              >
                <TextArea
                  rows={3}
                  placeholder="如：剑法&#10;炼丹&#10;阵法"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="resources"
                label="势力资源"
                tooltip="每行一个资源"
              >
                <TextArea
                  rows={3}
                  placeholder="如：灵石矿&#10;药园&#10;剑冢"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="allies"
                label="盟友势力"
                tooltip="每行一个盟友"
              >
                <TextArea
                  rows={2}
                  placeholder="如：天剑门&#10;玄天宗"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="enemies"
                label="敌对势力"
                tooltip="每行一个敌人"
              >
                <TextArea
                  rows={2}
                  placeholder="如：血煞门&#10;魔道联盟"
                />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>

      {/* 势力详情查看模态框 */}
      <Modal
        title="势力详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={800}
      >
        {viewingFaction && (
          <Descriptions bordered column={2}>
            <Descriptions.Item label="势力名称" span={2}>
              <Space>
                {typeConfig[viewingFaction.type].icon}
                <Text strong>{viewingFaction.name}</Text>
                <Tag color={typeConfig[viewingFaction.type].color}>
                  {typeConfig[viewingFaction.type].text}
                </Tag>
                <Tag color={levelConfig[viewingFaction.level].color}>
                  {levelConfig[viewingFaction.level].text}
                </Tag>
              </Space>
            </Descriptions.Item>

            <Descriptions.Item label="领袖">{viewingFaction.leader}</Descriptions.Item>
            <Descriptions.Item label="成员数量">{viewingFaction.memberCount?.toLocaleString()}</Descriptions.Item>

            <Descriptions.Item label="势力范围">{viewingFaction.territory}</Descriptions.Item>
            <Descriptions.Item label="创建时间">{viewingFaction.createdAt}</Descriptions.Item>

            <Descriptions.Item label="实力等级">
              <Rate disabled value={viewingFaction.strength} style={{ fontSize: 16 }} />
            </Descriptions.Item>
            <Descriptions.Item label="影响力">
              <Rate disabled value={viewingFaction.influence} style={{ fontSize: 16 }} />
            </Descriptions.Item>

            <Descriptions.Item label="势力描述" span={2}>
              <Paragraph>{viewingFaction.description}</Paragraph>
            </Descriptions.Item>

            {viewingFaction.history && (
              <Descriptions.Item label="势力历史" span={2}>
                <Paragraph>{viewingFaction.history}</Paragraph>
              </Descriptions.Item>
            )}

            {viewingFaction.specialties && viewingFaction.specialties.length > 0 && (
              <Descriptions.Item label="特色能力" span={2}>
                <Space wrap>
                  {viewingFaction.specialties.map((specialty, index) => (
                    <Tag key={index} color="blue">{specialty}</Tag>
                  ))}
                </Space>
              </Descriptions.Item>
            )}

            {viewingFaction.resources && viewingFaction.resources.length > 0 && (
              <Descriptions.Item label="势力资源" span={2}>
                <Space wrap>
                  {viewingFaction.resources.map((resource, index) => (
                    <Tag key={index} color="green">{resource}</Tag>
                  ))}
                </Space>
              </Descriptions.Item>
            )}

            {viewingFaction.allies && viewingFaction.allies.length > 0 && (
              <Descriptions.Item label="盟友势力" span={2}>
                <Space wrap>
                  {viewingFaction.allies.map((ally, index) => (
                    <Tag key={index} color="cyan">{ally}</Tag>
                  ))}
                </Space>
              </Descriptions.Item>
            )}

            {viewingFaction.enemies && viewingFaction.enemies.length > 0 && (
              <Descriptions.Item label="敌对势力" span={2}>
                <Space wrap>
                  {viewingFaction.enemies.map((enemy, index) => (
                    <Tag key={index} color="red">{enemy}</Tag>
                  ))}
                </Space>
              </Descriptions.Item>
            )}
          </Descriptions>
        )}
      </Modal>
    </div>
  );
};

export default FactionList;