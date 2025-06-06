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
  BankOutlined,
  SafetyOutlined,
  GlobalOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const JudicialSystems = () => {
  const { id: projectId } = useParams();
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSystem, setEditingSystem] = useState(null);
  const [form] = Form.useForm();

  // 法律体系类型选项
  const legalSystemOptions = [
    { value: 'civil_law', label: '成文法系' },
    { value: 'common_law', label: '普通法系' },
    { value: 'religious_law', label: '宗教法系' },
    { value: 'customary_law', label: '习惯法系' },
    { value: 'mixed_system', label: '混合法系' }
  ];

  // 审判程序类型选项
  const procedureOptions = [
    { value: 'inquisitorial', label: '纠问式' },
    { value: 'adversarial', label: '对抗式' },
    { value: 'mixed', label: '混合式' }
  ];

  useEffect(() => {
    fetchSystems();
  }, [projectId]);

  const fetchSystems = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/judicial-systems/?project_id=${projectId}`);
      setSystems(response.data);
    } catch (error) {
      console.error('获取司法体系失败:', error);
      message.error('获取司法体系失败');
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
      await axios.delete(`/api/judicial-systems/${systemId}`);
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
        await axios.put(`/api/judicial-systems/${editingSystem.id}`, systemData);
        message.success('更新成功');
      } else {
        await axios.post('/api/judicial-systems/', systemData);
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

  const getLegalSystemLabel = (value) => {
    const option = legalSystemOptions.find(opt => opt.value === value);
    return option ? option.label : value;
  };

  const getProcedureLabel = (value) => {
    const option = procedureOptions.find(opt => opt.value === value);
    return option ? option.label : value;
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div>
          <Text strong>{text}</Text>
          {record.jurisdiction_name && (
            <div>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                <GlobalOutlined /> {record.jurisdiction_name}
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
      title: '法律体系',
      dataIndex: 'legal_system_type',
      key: 'legal_system_type',
      render: (type) => (
        <Tag color="green">{getLegalSystemLabel(type)}</Tag>
      )
    },
    {
      title: '审判程序',
      dataIndex: 'procedure_type',
      key: 'procedure_type',
      render: (type) => (
        <Tag color="orange">{getProcedureLabel(type)}</Tag>
      )
    },
    {
      title: '司法效率',
      key: 'judicial_efficiency',
      render: (_, record) => {
        const efficiency = record.judicial_efficiency || {};
        return (
          <Space direction="vertical" size="small">
            <Text style={{ fontSize: '12px' }}>
              处理速度: {(efficiency.case_processing_speed || 0).toFixed(1)}%
            </Text>
            <Text style={{ fontSize: '12px' }}>
              定罪准确率: {(efficiency.conviction_accuracy || 0).toFixed(1)}%
            </Text>
          </Space>
        );
      }
    },
    {
      title: '公众信任度',
      key: 'public_trust',
      render: (_, record) => {
        const efficiency = record.judicial_efficiency || {};
        const trust = efficiency.public_trust || 0;
        return (
          <Progress 
            percent={trust} 
            size="small" 
            format={percent => `${percent}%`}
            strokeColor={trust >= 70 ? '#52c41a' : trust >= 40 ? '#faad14' : '#ff4d4f'}
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
            title="确定删除这个司法体系吗？"
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
          <BankOutlined /> 司法体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加司法体系
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
            showTotal: (total) => `共 ${total} 个司法体系`
          }}
        />
      </Card>

      <Modal
        title={editingSystem ? '编辑司法体系' : '添加司法体系'}
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
          initialValues={{
            legal_system_type: 'civil_law',
            procedure_type: 'mixed'
          }}
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
                name="jurisdiction_name"
                label="司法管辖区"
              >
                <Input placeholder="请输入司法管辖区名称" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
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
            <Col span={8}>
              <Form.Item
                name="legal_system_type"
                label="法律体系类型"
                rules={[{ required: true, message: '请选择法律体系类型' }]}
              >
                <Select placeholder="请选择法律体系类型">
                  {legalSystemOptions.map(option => (
                    <Option key={option.value} value={option.value}>
                      {option.label}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="procedure_type"
                label="审判程序类型"
                rules={[{ required: true, message: '请选择审判程序类型' }]}
              >
                <Select placeholder="请选择审判程序类型">
                  {procedureOptions.map(option => (
                    <Option key={option.value} value={option.value}>
                      {option.label}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="描述"
          >
            <TextArea 
              rows={3} 
              placeholder="请输入司法体系描述"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default JudicialSystems;
