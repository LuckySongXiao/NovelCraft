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
  Statistic,
  Tree
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EnvironmentOutlined,
  GlobalOutlined,
  HomeOutlined,
  BankOutlined,
  ShopOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const MapStructure = () => {
  const { id: projectId } = useParams();
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingLocation, setEditingLocation] = useState(null);
  const [form] = Form.useForm();

  // 模拟数据
  const mockLocations = [
    {
      id: 1,
      name: '天元大陆',
      type: 'continent',
      parentId: null,
      coordinates: { x: 0, y: 0 },
      size: 'massive',
      climate: 'temperate',
      terrain: 'mixed',
      population: 10000000,
      dangerLevel: 2,
      resources: ['灵石', '药材', '矿物'],
      controllingFaction: '修仙联盟',
      description: '修仙世界的主大陆，包含多个国家和宗门',
      specialFeatures: ['灵气浓郁', '天地法则完整'],
      accessRequirements: '无',
      status: 'active'
    },
    {
      id: 2,
      name: '青云山脉',
      type: 'mountain',
      parentId: 1,
      coordinates: { x: 100, y: 200 },
      size: 'large',
      climate: 'cold',
      terrain: 'mountain',
      population: 50000,
      dangerLevel: 3,
      resources: ['灵石矿', '雪莲', '寒冰晶'],
      controllingFaction: '青云宗',
      description: '连绵不绝的山脉，青云宗的总部所在地',
      specialFeatures: ['常年云雾缭绕', '灵气充沛'],
      accessRequirements: '青云宗弟子或邀请函',
      status: 'active'
    },
    {
      id: 3,
      name: '青云宗',
      type: 'sect',
      parentId: 2,
      coordinates: { x: 120, y: 220 },
      size: 'medium',
      climate: 'cold',
      terrain: 'mountain',
      population: 5000,
      dangerLevel: 1,
      resources: ['功法秘籍', '丹药', '法器'],
      controllingFaction: '青云宗',
      description: '正道第一大宗门，传承千年',
      specialFeatures: ['护山大阵', '藏经阁', '炼丹房'],
      accessRequirements: '宗门弟子或长老许可',
      status: 'active'
    }
  ];

  useEffect(() => {
    loadLocations();
  }, [projectId]);

  const loadLocations = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setLocations(mockLocations);
        setLoading(false);
      }, 500);
    } catch (error) {
      message.error('加载地图结构失败');
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingLocation(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (location) => {
    setEditingLocation(location);
    form.setFieldsValue({
      ...location,
      resources: location.resources?.join(', '),
      specialFeatures: location.specialFeatures?.join(', '),
      x: location.coordinates?.x,
      y: location.coordinates?.y
    });
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 检查是否有子位置
      const hasChildren = locations.some(loc => loc.parentId === id);
      if (hasChildren) {
        message.error('请先删除子位置');
        return;
      }

      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/map_structure/${id}`);

      // 删除成功后从列表中移除
      setLocations(locations.filter(l => l.id !== id));
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
        parentId: values.parentId || null,
        coordinates: {
          x: values.x || 0,
          y: values.y || 0
        },
        size: values.size,
        climate: values.climate,
        terrain: values.terrain,
        population: values.population,
        dangerLevel: values.dangerLevel,
        resources: values.resources?.split(',').map(r => r.trim()).filter(r => r) || [],
        controllingFaction: values.controllingFaction,
        description: values.description,
        specialFeatures: values.specialFeatures?.split(',').map(f => f.trim()).filter(f => f) || [],
        accessRequirements: values.accessRequirements,
        status: values.status
      };

      if (editingLocation) {
        // 更新
        setLocations(locations.map(l =>
          l.id === editingLocation.id ? { ...l, ...processedValues } : l
        ));
        message.success('更新成功');
      } else {
        // 新增
        const newLocation = {
          id: Date.now(),
          ...processedValues
        };
        setLocations([...locations, newLocation]);
        message.success('添加成功');
      }
      setModalVisible(false);
    } catch (error) {
      message.error('保存失败');
    }
  };

  const getTypeColor = (type) => {
    const colors = {
      continent: 'purple',
      country: 'blue',
      city: 'green',
      town: 'cyan',
      village: 'orange',
      sect: 'red',
      mountain: 'volcano',
      forest: 'lime',
      desert: 'gold',
      ocean: 'geekblue'
    };
    return colors[type] || 'default';
  };

  const getSizeColor = (size) => {
    const colors = {
      tiny: 'default',
      small: 'blue',
      medium: 'green',
      large: 'orange',
      huge: 'red',
      massive: 'purple'
    };
    return colors[size] || 'default';
  };

  const columns = [
    {
      title: '位置名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <Space>
          <Text strong>{text}</Text>
          <Tag color={getTypeColor(record.type)}>
            {record.type === 'continent' ? '大陆' :
             record.type === 'country' ? '国家' :
             record.type === 'city' ? '城市' :
             record.type === 'town' ? '城镇' :
             record.type === 'village' ? '村庄' :
             record.type === 'sect' ? '宗门' :
             record.type === 'mountain' ? '山脉' :
             record.type === 'forest' ? '森林' :
             record.type === 'desert' ? '沙漠' : '海洋'}
          </Tag>
        </Space>
      )
    },
    {
      title: '规模',
      dataIndex: 'size',
      key: 'size',
      render: (size) => (
        <Tag color={getSizeColor(size)}>
          {size === 'tiny' ? '微小' :
           size === 'small' ? '小型' :
           size === 'medium' ? '中型' :
           size === 'large' ? '大型' :
           size === 'huge' ? '巨大' : '超大'}
        </Tag>
      )
    },
    {
      title: '坐标',
      key: 'coordinates',
      render: (_, record) => (
        <Text>({record.coordinates?.x || 0}, {record.coordinates?.y || 0})</Text>
      )
    },
    {
      title: '人口',
      dataIndex: 'population',
      key: 'population',
      render: (population) => {
        if (population >= 1000000) {
          return `${(population / 1000000).toFixed(1)}M`;
        } else if (population >= 1000) {
          return `${(population / 1000).toFixed(1)}K`;
        }
        return population?.toString() || '0';
      },
      sorter: (a, b) => a.population - b.population
    },
    {
      title: '危险等级',
      dataIndex: 'dangerLevel',
      key: 'dangerLevel',
      render: (level) => {
        const color = level >= 4 ? '#f5222d' : level >= 3 ? '#fa8c16' : level >= 2 ? '#faad14' : '#52c41a';
        return <Tag color={color}>{level}/5</Tag>;
      },
      sorter: (a, b) => a.dangerLevel - b.dangerLevel
    },
    {
      title: '控制势力',
      dataIndex: 'controllingFaction',
      key: 'controllingFaction',
      render: (faction) => faction || <Text type="secondary">无</Text>
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'active' ? 'green' : status === 'sealed' ? 'orange' : 'red'}>
          {status === 'active' ? '开放' : status === 'sealed' ? '封印' : '毁坏'}
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
            title="确定删除这个位置吗？"
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

  // 构建树形结构数据
  const buildTreeData = (locations) => {
    const locationMap = {};
    const roots = [];

    // 创建位置映射
    locations.forEach(location => {
      locationMap[location.id] = {
        key: location.id,
        title: location.name,
        children: [],
        ...location
      };
    });

    // 构建树形结构
    locations.forEach(location => {
      if (location.parentId && locationMap[location.parentId]) {
        locationMap[location.parentId].children.push(locationMap[location.id]);
      } else {
        roots.push(locationMap[location.id]);
      }
    });

    return roots;
  };

  const treeData = buildTreeData(locations);

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">
          <GlobalOutlined /> 地图结构管理
        </Title>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加位置
        </Button>
      </div>

      <Row gutter={[16, 16]} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="位置总数"
              value={locations.length}
              prefix={<EnvironmentOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="大陆数量"
              value={locations.filter(l => l.type === 'continent').length}
              prefix={<GlobalOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="城市数量"
              value={locations.filter(l => l.type === 'city').length}
              prefix={<BankOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card size="small">
            <Statistic
              title="宗门数量"
              value={locations.filter(l => l.type === 'sect').length}
              prefix={<HomeOutlined />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={8}>
          <Card title="地图层级结构" size="small">
            <Tree
              treeData={treeData}
              defaultExpandAll
              showLine
              showIcon={false}
            />
          </Card>
        </Col>
        <Col span={16}>
          <Card title="位置列表">
            <Table
              columns={columns}
              dataSource={locations}
              rowKey="id"
              loading={loading}
              pagination={{
                pageSize: 8,
                showSizeChanger: true,
                showQuickJumper: true,
                showTotal: (total) => `共 ${total} 个位置`
              }}
            />
          </Card>
        </Col>
      </Row>

      <Modal
        title={editingLocation ? '编辑位置' : '添加位置'}
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
            type: 'city',
            size: 'medium',
            climate: 'temperate',
            terrain: 'plain',
            dangerLevel: 1,
            status: 'active'
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="位置名称"
                rules={[{ required: true, message: '请输入位置名称' }]}
              >
                <Input placeholder="请输入位置名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="type"
                label="位置类型"
                rules={[{ required: true, message: '请选择位置类型' }]}
              >
                <Select>
                  <Option value="continent">大陆</Option>
                  <Option value="country">国家</Option>
                  <Option value="city">城市</Option>
                  <Option value="town">城镇</Option>
                  <Option value="village">村庄</Option>
                  <Option value="sect">宗门</Option>
                  <Option value="mountain">山脉</Option>
                  <Option value="forest">森林</Option>
                  <Option value="desert">沙漠</Option>
                  <Option value="ocean">海洋</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="parentId"
                label="上级位置"
              >
                <Select placeholder="请选择上级位置" allowClear>
                  {locations.map(loc => (
                    <Option key={loc.id} value={loc.id}>{loc.name}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="size"
                label="规模"
                rules={[{ required: true, message: '请选择规模' }]}
              >
                <Select>
                  <Option value="tiny">微小</Option>
                  <Option value="small">小型</Option>
                  <Option value="medium">中型</Option>
                  <Option value="large">大型</Option>
                  <Option value="huge">巨大</Option>
                  <Option value="massive">超大</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item name="x" label="X坐标">
                <InputNumber style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item name="y" label="Y坐标">
                <InputNumber style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="dangerLevel"
                label="危险等级"
                rules={[{ required: true, message: '请选择危险等级' }]}
              >
                <InputNumber min={1} max={5} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="climate"
                label="气候"
                rules={[{ required: true, message: '请选择气候' }]}
              >
                <Select>
                  <Option value="tropical">热带</Option>
                  <Option value="temperate">温带</Option>
                  <Option value="cold">寒带</Option>
                  <Option value="desert">沙漠</Option>
                  <Option value="arctic">极地</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="terrain"
                label="地形"
                rules={[{ required: true, message: '请选择地形' }]}
              >
                <Select>
                  <Option value="plain">平原</Option>
                  <Option value="mountain">山地</Option>
                  <Option value="forest">森林</Option>
                  <Option value="desert">沙漠</Option>
                  <Option value="swamp">沼泽</Option>
                  <Option value="coast">海岸</Option>
                  <Option value="mixed">混合</Option>
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
                  <Option value="active">开放</Option>
                  <Option value="sealed">封印</Option>
                  <Option value="destroyed">毁坏</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="population" label="人口数量">
                <InputNumber min={0} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="controllingFaction" label="控制势力">
                <Input placeholder="请输入控制势力" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="resources" label="资源" extra="多个资源请用逗号分隔">
            <Input placeholder="如：灵石, 药材, 矿物" />
          </Form.Item>

          <Form.Item name="specialFeatures" label="特殊特征" extra="多个特征请用逗号分隔">
            <Input placeholder="如：灵气浓郁, 天地法则完整" />
          </Form.Item>

          <Form.Item name="accessRequirements" label="进入条件">
            <Input placeholder="请输入进入条件" />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={3} placeholder="请描述位置的特点、历史背景等" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default MapStructure;
