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
  Avatar,
  Tooltip,
  Row,
  Col,
  Statistic,
  Descriptions,
  Upload,
  InputNumber
} from 'antd';
import {
  PlusOutlined,
  UserOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  TeamOutlined,
  CrownOutlined,
  HeartOutlined,
  UploadOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const CharacterList = () => {
  const { id: projectId } = useParams();
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingCharacter, setEditingCharacter] = useState(null);
  const [viewingCharacter, setViewingCharacter] = useState(null);
  const [form] = Form.useForm();

  // 模拟人物数据
  const mockCharacters = [
    {
      id: 1,
      name: '林天',
      role: 'protagonist',
      gender: 'male',
      age: 18,
      cultivation: '筑基期',
      faction: '青云宗',
      appearance: '身材修长，剑眉星目，气质出尘',
      personality: '坚毅果敢，重情重义，天赋异禀',
      background: '出身平凡，因缘际会踏入修仙之路',
      abilities: ['剑法精通', '灵力感知', '快速修炼'],
      relationships: ['师父：云长老', '师兄：王峰'],
      avatar: null,
      importance: 'high',
      status: 'active'
    },
    {
      id: 2,
      name: '苏雪儿',
      role: 'supporting',
      gender: 'female',
      age: 17,
      cultivation: '练气期',
      faction: '青云宗',
      appearance: '容貌绝美，肌肤如雪，气质清冷',
      personality: '冰雪聪明，外冷内热，心地善良',
      background: '宗门长老之女，从小修炼',
      abilities: ['冰系法术', '炼丹术', '阵法'],
      relationships: ['父亲：苏长老', '青梅竹马：林天'],
      avatar: null,
      importance: 'high',
      status: 'active'
    },
    {
      id: 3,
      name: '魔君血煞',
      role: 'antagonist',
      gender: 'male',
      age: 500,
      cultivation: '元婴期',
      faction: '血煞门',
      appearance: '身材魁梧，面容狰狞，煞气逼人',
      personality: '残忍嗜血，野心勃勃，实力强大',
      background: '魔道巨擘，称霸一方',
      abilities: ['血煞神功', '魔道秘术', '精神攻击'],
      relationships: ['手下：血煞四将'],
      avatar: null,
      importance: 'medium',
      status: 'active'
    }
  ];

  useEffect(() => {
    setCharacters(mockCharacters);
  }, []);

  // 角色类型配置
  const roleConfig = {
    protagonist: { color: 'gold', text: '主角', icon: <CrownOutlined /> },
    supporting: { color: 'blue', text: '配角', icon: <UserOutlined /> },
    antagonist: { color: 'red', text: '反派', icon: <UserOutlined /> },
    minor: { color: 'default', text: '次要', icon: <UserOutlined /> }
  };

  // 重要性配置
  const importanceConfig = {
    high: { color: 'red', text: '重要' },
    medium: { color: 'orange', text: '一般' },
    low: { color: 'default', text: '次要' }
  };

  // 表格列配置
  const columns = [
    {
      title: '头像',
      dataIndex: 'avatar',
      key: 'avatar',
      render: (avatar, record) => (
        <Avatar
          size={40}
          src={avatar}
          icon={<UserOutlined />}
          style={{ backgroundColor: record.role === 'protagonist' ? '#f56a00' : '#87d068' }}
        >
          {!avatar && record.name.charAt(0)}
        </Avatar>
      )
    },
    {
      title: '姓名',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          {roleConfig[record.role].icon}
          <Text strong>{text}</Text>
        </Space>
      )
    },
    {
      title: '角色类型',
      dataIndex: 'role',
      key: 'role',
      render: (role) => (
        <Tag color={roleConfig[role].color}>
          {roleConfig[role].text}
        </Tag>
      ),
      filters: [
        { text: '主角', value: 'protagonist' },
        { text: '配角', value: 'supporting' },
        { text: '反派', value: 'antagonist' },
        { text: '次要', value: 'minor' }
      ],
      onFilter: (value, record) => record.role === value
    },
    {
      title: '性别',
      dataIndex: 'gender',
      key: 'gender',
      render: (gender) => gender === 'male' ? '男' : '女'
    },
    {
      title: '年龄',
      dataIndex: 'age',
      key: 'age',
      sorter: (a, b) => a.age - b.age
    },
    {
      title: '修为',
      dataIndex: 'cultivation',
      key: 'cultivation'
    },
    {
      title: '势力',
      dataIndex: 'faction',
      key: 'faction'
    },
    {
      title: '重要性',
      dataIndex: 'importance',
      key: 'importance',
      render: (importance) => (
        <Tag color={importanceConfig[importance].color}>
          {importanceConfig[importance].text}
        </Tag>
      )
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
            title="确定删除这个人物吗？"
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

  // 处理新建/编辑人物
  const handleCreateOrEdit = () => {
    setEditingCharacter(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (character) => {
    setEditingCharacter(character);
    form.setFieldsValue({
      ...character,
      abilities: character.abilities.join('\n'),
      relationships: character.relationships.join('\n')
    });
    setModalVisible(true);
  };

  const handleView = (character) => {
    setViewingCharacter(character);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (character) => {
    message.info(`AI生成人物详情：${character.name}`);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/character/${id}`);

      // 删除成功后从列表中移除
      setCharacters(characters.filter(c => c.id !== id));
      message.success('人物删除成功');
    } catch (error) {
      console.error('删除人物失败:', error);
      message.error('删除人物失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段
      const processedValues = {
        ...values,
        abilities: values.abilities ? values.abilities.split('\n').filter(item => item.trim()) : [],
        relationships: values.relationships ? values.relationships.split('\n').filter(item => item.trim()) : []
      };

      if (editingCharacter) {
        // 编辑人物
        setCharacters(characters.map(c =>
          c.id === editingCharacter.id
            ? { ...c, ...processedValues }
            : c
        ));
        message.success('人物更新成功');
      } else {
        // 新建人物
        const newCharacter = {
          id: Date.now(),
          ...processedValues,
          status: 'active'
        };
        setCharacters([...characters, newCharacter]);
        message.success('人物创建成功');
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
  const totalCharacters = characters.length;
  const protagonists = characters.filter(c => c.role === 'protagonist').length;
  const antagonists = characters.filter(c => c.role === 'antagonist').length;
  const supporting = characters.filter(c => c.role === 'supporting').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">人物管理</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总人物数"
              value={totalCharacters}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="主角"
              value={protagonists}
              prefix={<CrownOutlined style={{ color: '#faad14' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="配角"
              value={supporting}
              prefix={<UserOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="反派"
              value={antagonists}
              prefix={<UserOutlined style={{ color: '#f5222d' }} />}
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
              添加人物
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={characters}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个人物`
          }}
        />
      </Card>

      {/* 新建/编辑人物模态框 */}
      <Modal
        title={editingCharacter ? '编辑人物' : '新建人物'}
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
            role: 'supporting',
            gender: 'male',
            importance: 'medium',
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="姓名"
                rules={[{ required: true, message: '请输入人物姓名' }]}
              >
                <Input placeholder="请输入人物姓名" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="role"
                label="角色类型"
                rules={[{ required: true, message: '请选择角色类型' }]}
              >
                <Select>
                  <Option value="protagonist">主角</Option>
                  <Option value="supporting">配角</Option>
                  <Option value="antagonist">反派</Option>
                  <Option value="minor">次要</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="gender"
                label="性别"
                rules={[{ required: true, message: '请选择性别' }]}
              >
                <Select>
                  <Option value="male">男</Option>
                  <Option value="female">女</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="age"
                label="年龄"
                rules={[{ required: true, message: '请输入年龄' }]}
              >
                <InputNumber min={1} max={10000} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="importance"
                label="重要性"
                rules={[{ required: true, message: '请选择重要性' }]}
              >
                <Select>
                  <Option value="high">重要</Option>
                  <Option value="medium">一般</Option>
                  <Option value="low">次要</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="cultivation"
                label="修为境界"
              >
                <Input placeholder="如：筑基期、金丹期等" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="faction"
                label="所属势力"
              >
                <Input placeholder="如：青云宗、魔道门派等" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="appearance"
            label="外貌描述"
          >
            <TextArea
              rows={3}
              placeholder="描述人物的外貌特征..."
            />
          </Form.Item>

          <Form.Item
            name="personality"
            label="性格特点"
          >
            <TextArea
              rows={3}
              placeholder="描述人物的性格特征..."
            />
          </Form.Item>

          <Form.Item
            name="background"
            label="背景故事"
          >
            <TextArea
              rows={3}
              placeholder="描述人物的背景经历..."
            />
          </Form.Item>

          <Form.Item
            name="abilities"
            label="能力技能"
            extra="每行一个技能"
          >
            <TextArea
              rows={3}
              placeholder="如：剑法精通&#10;灵力感知&#10;快速修炼"
            />
          </Form.Item>

          <Form.Item
            name="relationships"
            label="人际关系"
            extra="每行一个关系"
          >
            <TextArea
              rows={3}
              placeholder="如：师父：云长老&#10;师兄：王峰&#10;青梅竹马：苏雪儿"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 人物详情模态框 */}
      <Modal
        title="人物详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={800}
      >
        {viewingCharacter && (
          <div>
            <Row gutter={16} style={{ marginBottom: 16 }}>
              <Col span={4}>
                <Avatar
                  size={80}
                  src={viewingCharacter.avatar}
                  icon={<UserOutlined />}
                  style={{ backgroundColor: viewingCharacter.role === 'protagonist' ? '#f56a00' : '#87d068' }}
                >
                  {!viewingCharacter.avatar && viewingCharacter.name.charAt(0)}
                </Avatar>
              </Col>
              <Col span={20}>
                <Title level={3}>{viewingCharacter.name}</Title>
                <Space>
                  <Tag color={roleConfig[viewingCharacter.role].color}>
                    {roleConfig[viewingCharacter.role].text}
                  </Tag>
                  <Tag color={importanceConfig[viewingCharacter.importance].color}>
                    {importanceConfig[viewingCharacter.importance].text}
                  </Tag>
                </Space>
              </Col>
            </Row>

            <Descriptions bordered column={2}>
              <Descriptions.Item label="性别">
                {viewingCharacter.gender === 'male' ? '男' : '女'}
              </Descriptions.Item>
              <Descriptions.Item label="年龄">
                {viewingCharacter.age}岁
              </Descriptions.Item>
              <Descriptions.Item label="修为境界">
                {viewingCharacter.cultivation || '未知'}
              </Descriptions.Item>
              <Descriptions.Item label="所属势力">
                {viewingCharacter.faction || '无'}
              </Descriptions.Item>
              <Descriptions.Item label="外貌描述" span={2}>
                {viewingCharacter.appearance || '暂无描述'}
              </Descriptions.Item>
              <Descriptions.Item label="性格特点" span={2}>
                {viewingCharacter.personality || '暂无描述'}
              </Descriptions.Item>
              <Descriptions.Item label="背景故事" span={2}>
                {viewingCharacter.background || '暂无描述'}
              </Descriptions.Item>
              <Descriptions.Item label="能力技能" span={2}>
                {viewingCharacter.abilities && viewingCharacter.abilities.length > 0 ? (
                  <Space wrap>
                    {viewingCharacter.abilities.map((ability, index) => (
                      <Tag key={index} color="blue">{ability}</Tag>
                    ))}
                  </Space>
                ) : '暂无'}
              </Descriptions.Item>
              <Descriptions.Item label="人际关系" span={2}>
                {viewingCharacter.relationships && viewingCharacter.relationships.length > 0 ? (
                  <div>
                    {viewingCharacter.relationships.map((relation, index) => (
                      <div key={index} style={{ marginBottom: 4 }}>
                        <HeartOutlined style={{ marginRight: 8, color: '#f5222d' }} />
                        {relation}
                      </div>
                    ))}
                  </div>
                ) : '暂无'}
              </Descriptions.Item>
            </Descriptions>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default CharacterList;
