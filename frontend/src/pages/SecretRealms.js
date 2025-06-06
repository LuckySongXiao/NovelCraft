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
  EyeOutlined,
  EnvironmentOutlined,
  TrophyOutlined,
  WarningOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const SecretRealms = () => {
  const { id: projectId } = useParams();
  const [realms, setRealms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRealm, setEditingRealm] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockRealms = [
    {
      id: 1,
      name: '九幽炼狱',
      type: 'dungeon',
      location: '死亡沼泽深处',
      coordinates: { x: 150, y: 200 },
      dangerLevel: 5,
      recommendedLevel: '元婴期以上',
      entryRequirements: '需要九幽令牌',
      rewards: ['九幽真火', '炼狱魔晶', '地狱花'],
      description: '传说中的炼狱秘境，充满了危险的魔物和珍贵的宝物',
      maxCapacity: 10,
      timeLimit: 24,
      status: 'active',
      discoveredBy: '血魔宗',
      lastExplored: '2024-01-15'
    },
    {
      id: 2,
      name: '天机阁遗迹',
      type: 'ruins',
      location: '云海之上',
      coordinates: { x: 300, y: 100 },
      dangerLevel: 3,
      recommendedLevel: '金丹期以上',
      entryRequirements: '解开天机锁',
      rewards: ['天机秘典', '星辰石', '灵识丹'],
      description: '古代天机阁的遗迹，蕴含着预知未来的秘密',
      maxCapacity: 5,
      timeLimit: 12,
      status: 'sealed',
      discoveredBy: '天机门',
      lastExplored: '2023-12-20'
    }
  ];

  useEffect(() => {
    loadRealms();
  }, [projectId]);

  const loadRealms = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/secret-realm-distributions/?project_id=${projectId}`);
      setRealms(response.data || []);
    } catch (error) {
      console.error('加载秘境分布失败:', error);
      // 如果API失败，使用模拟数据
      setRealms(mockRealms);
      message.warning('使用模拟数据，请检查后端连接');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingRealm(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (realm) => {
    setEditingRealm(realm);
    form.setFieldsValue({
      ...realm,
      rewards: realm.rewards?.join(', ')
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/secret-realm-distributions/${id}`);

      // 删除成功后从列表中移除
      setRealms(realms.filter(r => r.id !== id));
      message.success('删除成功');
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values) => {
    setLoading(true);
    try {
      const processedValues = {
        ...values,
        project_id: parseInt(projectId),
        treasure_types: values.rewards?.split(',').map(s => ({ name: s.trim() })).filter(s => s.name) || [],
        realm_type: values.type,
        danger_level: values.dangerLevel,
        geographic_region: values.location,
        entry_requirements: values.entryRequirements ? [{ requirement: values.entryRequirements }] : [],
        exploration_status: values.status === 'active' ? '已开放' :
                           values.status === 'sealed' ? '已封印' :
                           values.status === 'destroyed' ? '已毁坏' : '隐藏中'
      };

      if (editingRealm) {
        // 更新
        const response = await axios.put(`/api/secret-realm-distributions/${editingRealm.id}`, processedValues);
        setRealms(realms.map(r =>
          r.id === editingRealm.id ? response.data : r
        ));
        message.success('更新成功');
      } else {
        // 新增
        const response = await axios.post('/api/secret-realm-distributions/', processedValues);
        setRealms([...realms, response.data]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      dungeon: 'red',
      ruins: 'orange',
      trial: 'blue',
      treasure: 'gold',
      forbidden: 'purple'
    };
    return colors[type] || 'default';
  };

  const getStatusColor = (status) => {
    const colors = {
      active: 'green',
      sealed: 'orange',
      destroyed: 'red',
      hidden: 'purple'
    };
    return colors[status] || 'default';
  };

  const getDangerColor = (level) => {
    if (level >= 5) return '#f5222d';
    if (level >= 4) return '#fa8c16';
    if (level >= 3) return '#faad14';
    if (level >= 2) return '#52c41a';
    return '#1890ff';
  };

  const columns = [
    {
      title: '秘境名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'dungeon' ? '地下城' :
             record.type === 'ruins' ? '遗迹' :
             record.type === 'trial' ? '试炼' :
             record.type === 'treasure' ? '宝库' : '禁地'}
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
      title: '危险等级',
      dataIndex: 'dangerLevel',
      key: 'dangerLevel',
      render: (level) => (
        <Space>
          <WarningOutlined style={{ color: getDangerColor(level) }} />
          <Rate disabled value={level} style={{ fontSize: 16 }} />
        </Space>
      ),
      sorter: (a, b) => a.dangerLevel - b.dangerLevel
    },
    {
      title: '推荐修为',
      dataIndex: 'recommendedLevel',
      key: 'recommendedLevel'
    },
    {
      title: '容量限制',
      dataIndex: 'maxCapacity',
      key: 'maxCapacity',
      render: (capacity) => `${capacity}人`,
      sorter: (a, b) => a.maxCapacity - b.maxCapacity
    },
    {
      title: '时间限制',
      dataIndex: 'timeLimit',
      key: 'timeLimit',
      render: (time) => (
        <Space>
          <ClockCircleOutlined />
          <Text>{time}小时</Text>
        </Space>
      ),
      sorter: (a, b) => a.timeLimit - b.timeLimit
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status === 'active' ? '开放' :
           status === 'sealed' ? '封印' :
           status === 'destroyed' ? '毁坏' : '隐藏'}
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
            title="确定删除这个秘境吗？"
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
          <EyeOutlined /> 秘境分布管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加秘境
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="秘境总数"
              value={realms.length}
              prefix={<EyeOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="开放秘境"
              value={realms.filter(r => r.status === 'active').length}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="封印秘境"
              value={realms.filter(r => r.status === 'sealed').length}
              prefix={<WarningOutlined />}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="平均危险等级"
              value={realms.length > 0 ? (realms.reduce((sum, r) => sum + r.dangerLevel, 0) / realms.length).toFixed(1) : 0}
              prefix={<WarningOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={realms}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个秘境`
          }}
        />
      </Card>

      <Modal
        title={editingRealm ? '编辑秘境' : '添加秘境'}
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
            type: 'dungeon',
            dangerLevel: 3,
            maxCapacity: 10,
            timeLimit: 24,
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="秘境名称"
                rules={[{ required: true, message: '请输入秘境名称' }]}
              >
                <Input placeholder="请输入秘境名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="秘境类型"
                rules={[{ required: true, message: '请选择秘境类型' }]}
              >
                <Select>
                  <Option value="dungeon">地下城</Option>
                  <Option value="ruins">遗迹</Option>
                  <Option value="trial">试炼</Option>
                  <Option value="treasure">宝库</Option>
                  <Option value="forbidden">禁地</Option>
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
                name="discoveredBy"
                label="发现者"
              >
                <Input placeholder="请输入发现者" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="dangerLevel"
                label="危险等级"
                rules={[{ required: true, message: '请选择危险等级' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="maxCapacity"
                label="容量限制"
                rules={[{ required: true, message: '请输入容量限制' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} addonAfter="人" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="timeLimit"
                label="时间限制"
                rules={[{ required: true, message: '请输入时间限制' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} addonAfter="小时" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="recommendedLevel"
                label="推荐修为"
                rules={[{ required: true, message: '请输入推荐修为' }]}
              >
                <Input placeholder="例如：金丹期以上" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择状态' }]}
              >
                <Select>
                  <Option value="active">开放</Option>
                  <Option value="sealed">封印</Option>
                  <Option value="destroyed">毁坏</Option>
                  <Option value="hidden">隐藏</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="entryRequirements"
            label="进入条件"
          >
            <Input placeholder="请输入进入条件" />
          </Form.Item>

          <Form.Item
            name="rewards"
            label="奖励物品"
            extra="多个物品请用逗号分隔"
          >
            <Input placeholder="例如：九幽真火, 炼狱魔晶, 地狱花" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述秘境的特点、历史背景等"
            />
          </Form.Item>

          <Form.Item
            name="lastExplored"
            label="最后探索时间"
          >
            <Input placeholder="例如：2024-01-15" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default SecretRealms;
