import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  InputNumber,
  Select,
  message,
  Popconfirm,
  Tooltip,
  Typography,
  Row,
  Col,
  Statistic,
  Progress,
  Tag
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  UserOutlined,
  ToolOutlined,
  GlobalOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const ProfessionSystems = () => {
  const { id: projectId } = useParams();
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSystem, setEditingSystem] = useState(null);
  const [form] = Form.useForm();

  // 职业类别选项
  const professionCategoryOptions = [
    { value: 'combat', label: '战斗类' },
    { value: 'crafting', label: '制作类' },
    { value: 'scholarly', label: '学术类' },
    { value: 'mercantile', label: '商业类' },
    { value: 'agricultural', label: '农业类' },
    { value: 'artistic', label: '艺术类' },
    { value: 'religious', label: '宗教类' },
    { value: 'administrative', label: '行政类' },
    { value: 'medical', label: '医疗类' },
    { value: 'magical', label: '魔法类' },
    { value: 'technical', label: '技术类' },
    { value: 'service', label: '服务类' }
  ];

  useEffect(() => {
    fetchSystems();
  }, [projectId]);

  const fetchSystems = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/profession-systems/?project_id=${projectId}`);
      setSystems(response.data);
    } catch (error) {
      console.error('获取职业体系失败:', error);
      message.error('获取职业体系失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingSystem(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingSystem(record);
    form.setFieldsValue({
      ...record
    });
    setModalVisible(true);
  };

  const handleDelete = async (systemId) => {
    try {
      await axios.delete(`/api/profession-systems/${systemId}`);
      message.success('删除成功');
      fetchSystems();
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      const systemData = {
        ...values,
        project_id: parseInt(projectId)
      };

      if (editingSystem) {
        await axios.put(`/api/profession-systems/${editingSystem.id}`, systemData);
        message.success('更新成功');
      } else {
        await axios.post('/api/profession-systems/', systemData);
        message.success('创建成功');
      }

      setModalVisible(false);
      form.resetFields();
      fetchSystems();
    } catch (error) {
      console.error('操作失败:', error);
      message.error('操作失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div>
          <Text strong>{text}</Text>
          {record.economic_context && (
            <div>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                <GlobalOutlined /> {record.economic_context}
              </Text>
            </div>
          )}
        </div>
      )
    },
    {
      title: '维度',
      dataIndex: 'dimension_id',
      key: 'dimension_id',
      render: (dimensionId) => (
        dimensionId ? <Tag color="blue">维度 {dimensionId}</Tag> : <Tag>主维度</Tag>
      )
    },
    {
      title: '职业多样性',
      key: 'profession_diversity',
      render: (_, record) => {
        const metrics = record.profession_metrics || {};
        const diversity = metrics.profession_diversity || 0;
        return (
          <Progress 
            percent={diversity} 
            size="small" 
            format={percent => `${percent}%`}
            strokeColor={diversity >= 70 ? '#52c41a' : diversity >= 40 ? '#faad14' : '#ff4d4f'}
          />
        );
      }
    },
    {
      title: '技能复杂性',
      key: 'skill_complexity',
      render: (_, record) => {
        const metrics = record.profession_metrics || {};
        const complexity = metrics.skill_complexity || 0;
        return (
          <Progress 
            percent={complexity} 
            size="small" 
            format={percent => `${percent}%`}
            strokeColor="#1890ff"
          />
        );
      }
    },
    {
      title: '职业流动性',
      key: 'career_mobility',
      render: (_, record) => {
        const metrics = record.profession_metrics || {};
        const mobility = metrics.career_mobility || 0;
        return (
          <Progress 
            percent={mobility} 
            size="small" 
            format={percent => `${percent}%`}
            strokeColor="#722ed1"
          />
        );
      }
    },
    {
      title: '组织覆盖率',
      key: 'organization_coverage',
      render: (_, record) => {
        const metrics = record.profession_metrics || {};
        const coverage = metrics.organization_coverage || 0;
        return (
          <Progress 
            percent={coverage} 
            size="small" 
            format={percent => `${percent}%`}
            strokeColor="#fa8c16"
          />
        );
      }
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Space>
          <Tooltip title="查看详情">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEdit(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个职业体系吗？"
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
          <UserOutlined /> 职业体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加职业体系
        </Button>
      </div>

      <Card>
        <Table
          columns={columns}
          dataSource={systems}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个职业体系`
          }}
        />
      </Card>

      <Modal
        title={editingSystem ? '编辑职业体系' : '添加职业体系'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        width={800}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="体系名称"
                rules={[{ required: true, message: '请输入体系名称' }]}
              >
                <Input placeholder="请输入体系名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="economic_context"
                label="经济背景"
              >
                <Input placeholder="请输入经济背景" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="dimension_id"
                label="维度ID"
              >
                <InputNumber 
                  placeholder="请输入维度ID" 
                  style={{ width: '100%' }}
                  min={0}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="描述"
          >
            <TextArea 
              rows={3} 
              placeholder="请输入职业体系描述"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ProfessionSystems;
