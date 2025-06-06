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
  TeamOutlined,
  BarChartOutlined,
  GlobalOutlined
} from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const CivilianSystems = () => {
  const { id: projectId } = useParams();
  const [systems, setSystems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingSystem, setEditingSystem] = useState(null);
  const [form] = Form.useForm();

  // 社会阶层选项
  const socialClassOptions = [
    { value: 'nobility', label: '贵族' },
    { value: 'merchant', label: '商人' },
    { value: 'artisan', label: '工匠' },
    { value: 'farmer', label: '农民' },
    { value: 'laborer', label: '劳工' },
    { value: 'slave', label: '奴隶' },
    { value: 'clergy', label: '神职人员' },
    { value: 'scholar', label: '学者' },
    { value: 'warrior', label: '武士' },
    { value: 'other', label: '其他' }
  ];

  // 生活方式选项
  const lifestyleOptions = [
    { value: 'urban', label: '城市生活' },
    { value: 'rural', label: '乡村生活' },
    { value: 'nomadic', label: '游牧生活' },
    { value: 'tribal', label: '部落生活' },
    { value: 'monastic', label: '修道生活' },
    { value: 'military', label: '军事生活' },
    { value: 'merchant', label: '商旅生活' },
    { value: 'scholarly', label: '学者生活' }
  ];

  useEffect(() => {
    fetchSystems();
  }, [projectId]);

  const fetchSystems = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`/api/civilian-systems/?project_id=${projectId}`);
      setSystems(response.data);
    } catch (error) {
      console.error('获取生民体系失败:', error);
      message.error('获取生民体系失败');
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
      ...record,
      total_population: record.total_population || 0,
      population_density: record.population_density || 0,
      population_growth_rate: record.population_growth_rate || 0,
      literacy_rate: record.literacy_rate || 0
    });
    setModalVisible(true);
  };

  const handleDelete = async (systemId) => {
    try {
      await axios.delete(`/api/civilian-systems/${systemId}`);
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
        await axios.put(`/api/civilian-systems/${editingSystem.id}`, systemData);
        message.success('更新成功');
      } else {
        await axios.post('/api/civilian-systems/', systemData);
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
          {record.region_name && (
            <div>
              <Text type="secondary" style={{ fontSize: '12px' }}>
                <GlobalOutlined /> {record.region_name}
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
      title: '总人口',
      dataIndex: 'total_population',
      key: 'total_population',
      render: (population) => (
        <Statistic 
          value={population || 0} 
          suffix="人"
          valueStyle={{ fontSize: '14px' }}
        />
      )
    },
    {
      title: '人口密度',
      dataIndex: 'population_density',
      key: 'population_density',
      render: (density) => (
        <Text>{density || 0} 人/km²</Text>
      )
    },
    {
      title: '识字率',
      dataIndex: 'literacy_rate',
      key: 'literacy_rate',
      render: (rate) => (
        <Progress 
          percent={rate || 0} 
          size="small" 
          format={percent => `${percent}%`}
        />
      )
    },
    {
      title: '社会指标',
      key: 'social_metrics',
      render: (_, record) => {
        const metrics = record.social_metrics || {};
        return (
          <Space direction="vertical" size="small">
            <Text style={{ fontSize: '12px' }}>
              稳定性: {(metrics.social_stability || 0).toFixed(1)}%
            </Text>
            <Text style={{ fontSize: '12px' }}>
              多样性: {(metrics.cultural_diversity || 0).toFixed(1)}%
            </Text>
          </Space>
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
            title="确定删除这个生民体系吗？"
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
          <TeamOutlined /> 生民体系管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加生民体系
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
            showTotal: (total) => `共 ${total} 个生民体系`
          }}
        />
      </Card>

      <Modal
        title={editingSystem ? '编辑生民体系' : '添加生民体系'}
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
            total_population: 0,
            population_density: 0,
            population_growth_rate: 0,
            literacy_rate: 0
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
                name="region_name"
                label="区域名称"
              >
                <Input placeholder="请输入区域名称" />
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
            <Col span={12}>
              <Form.Item
                name="total_population"
                label="总人口"
              >
                <InputNumber 
                  placeholder="请输入总人口" 
                  style={{ width: '100%' }}
                  min={0}
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="population_density"
                label="人口密度 (人/km²)"
              >
                <InputNumber 
                  placeholder="人口密度" 
                  style={{ width: '100%' }}
                  min={0}
                  step={0.1}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="population_growth_rate"
                label="人口增长率 (%)"
              >
                <InputNumber 
                  placeholder="增长率" 
                  style={{ width: '100%' }}
                  step={0.1}
                />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="literacy_rate"
                label="识字率 (%)"
              >
                <InputNumber 
                  placeholder="识字率" 
                  style={{ width: '100%' }}
                  min={0}
                  max={100}
                  step={0.1}
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
              placeholder="请输入生民体系描述"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default CivilianSystems;
