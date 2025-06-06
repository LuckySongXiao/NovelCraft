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
  Progress,
  Timeline
} from 'antd';
import {
  PlusOutlined,
  BookOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  BranchesOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const PlotList = () => {
  const { id: projectId } = useParams();
  const [plots, setPlots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingPlot, setEditingPlot] = useState(null);
  const [viewingPlot, setViewingPlot] = useState(null);
  const [form] = Form.useForm();

  // 模拟剧情数据
  const mockPlots = [
    {
      id: 1,
      title: '主线：修仙之路',
      type: 'main',
      status: 'active',
      priority: 'high',
      progress: 65,
      description: '主角从凡人踏上修仙之路的主要故事线',
      outline: '凡人觉醒 -> 入门修炼 -> 宗门试炼 -> 历练成长 -> 面临挑战',
      characters: ['林天', '云长老', '苏雪儿'],
      chapters: ['第一章', '第二章', '第三章'],
      conflicts: ['内心挣扎', '外部阻力'],
      themes: ['成长', '坚持', '友情'],
      startChapter: 1,
      endChapter: 10,
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20'
    },
    {
      id: 2,
      title: '支线：师门恩怨',
      type: 'subplot',
      status: 'planning',
      priority: 'medium',
      progress: 20,
      description: '青云宗内部的恩怨情仇',
      outline: '历史恩怨 -> 矛盾激化 -> 真相揭露 -> 和解或决裂',
      characters: ['云长老', '苏长老', '王峰'],
      chapters: ['第五章', '第八章'],
      conflicts: ['师门内斗', '利益冲突'],
      themes: ['恩怨', '正义', '选择'],
      startChapter: 5,
      endChapter: 12,
      createdAt: '2024-01-16',
      updatedAt: '2024-01-18'
    },
    {
      id: 3,
      title: '支线：情感线索',
      type: 'subplot',
      status: 'completed',
      priority: 'low',
      progress: 100,
      description: '主角与苏雪儿的感情发展',
      outline: '初遇 -> 相识 -> 相知 -> 相恋',
      characters: ['林天', '苏雪儿'],
      chapters: ['第二章', '第四章', '第六章'],
      conflicts: ['身份差距', '外界阻力'],
      themes: ['爱情', '成长', '坚持'],
      startChapter: 2,
      endChapter: 8,
      createdAt: '2024-01-10',
      updatedAt: '2024-01-19'
    }
  ];

  useEffect(() => {
    setPlots(mockPlots);
  }, []);

  // 剧情类型配置
  const typeConfig = {
    main: { color: 'red', text: '主线', icon: <BookOutlined /> },
    subplot: { color: 'blue', text: '支线', icon: <BranchesOutlined /> },
    side: { color: 'green', text: '番外', icon: <BookOutlined /> }
  };

  // 状态配置
  const statusConfig = {
    planning: { color: 'blue', text: '规划中', icon: <ClockCircleOutlined /> },
    active: { color: 'orange', text: '进行中', icon: <ExclamationCircleOutlined /> },
    completed: { color: 'green', text: '已完成', icon: <CheckCircleOutlined /> },
    paused: { color: 'default', text: '暂停', icon: <ClockCircleOutlined /> }
  };

  // 优先级配置
  const priorityConfig = {
    high: { color: 'red', text: '高' },
    medium: { color: 'orange', text: '中' },
    low: { color: 'default', text: '低' }
  };

  // 表格列配置
  const columns = [
    {
      title: '剧情标题',
      dataIndex: 'title',
      key: 'title',
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
        { text: '主线', value: 'main' },
        { text: '支线', value: 'subplot' },
        { text: '番外', value: 'side' }
      ],
      onFilter: (value, record) => record.type === value
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={statusConfig[status].color} icon={statusConfig[status].icon}>
          {statusConfig[status].text}
        </Tag>
      ),
      filters: [
        { text: '规划中', value: 'planning' },
        { text: '进行中', value: 'active' },
        { text: '已完成', value: 'completed' },
        { text: '暂停', value: 'paused' }
      ],
      onFilter: (value, record) => record.status === value
    },
    {
      title: '优先级',
      dataIndex: 'priority',
      key: 'priority',
      render: (priority) => (
        <Tag color={priorityConfig[priority].color}>
          {priorityConfig[priority].text}
        </Tag>
      )
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress) => (
        <Progress
          percent={progress}
          size="small"
          status={progress === 100 ? 'success' : 'active'}
        />
      ),
      sorter: (a, b) => a.progress - b.progress
    },
    {
      title: '章节范围',
      key: 'chapterRange',
      render: (_, record) => (
        <Text type="secondary">
          第{record.startChapter}章 - 第{record.endChapter}章
        </Text>
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
            title="确定删除这个剧情吗？"
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

  // 处理新建/编辑剧情
  const handleCreateOrEdit = () => {
    setEditingPlot(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (plot) => {
    setEditingPlot(plot);
    form.setFieldsValue({
      ...plot,
      characters: plot.characters.join('\n'),
      chapters: plot.chapters.join('\n'),
      conflicts: plot.conflicts.join('\n'),
      themes: plot.themes.join('\n')
    });
    setModalVisible(true);
  };

  const handleView = (plot) => {
    setViewingPlot(plot);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (plot) => {
    message.info(`AI生成剧情详情：${plot.title}`);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/plot/${id}`);

      // 删除成功后从列表中移除
      setPlots(plots.filter(p => p.id !== id));
      message.success('剧情删除成功');
    } catch (error) {
      console.error('删除剧情失败:', error);
      message.error('删除剧情失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段
      const processedValues = {
        ...values,
        characters: values.characters ? values.characters.split('\n').filter(item => item.trim()) : [],
        chapters: values.chapters ? values.chapters.split('\n').filter(item => item.trim()) : [],
        conflicts: values.conflicts ? values.conflicts.split('\n').filter(item => item.trim()) : [],
        themes: values.themes ? values.themes.split('\n').filter(item => item.trim()) : []
      };

      if (editingPlot) {
        // 编辑剧情
        setPlots(plots.map(p =>
          p.id === editingPlot.id
            ? { ...p, ...processedValues, updatedAt: new Date().toISOString().split('T')[0] }
            : p
        ));
        message.success('剧情更新成功');
      } else {
        // 新建剧情
        const newPlot = {
          id: Date.now(),
          ...processedValues,
          progress: 0,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setPlots([...plots, newPlot]);
        message.success('剧情创建成功');
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
  const totalPlots = plots.length;
  const mainPlots = plots.filter(p => p.type === 'main').length;
  const subPlots = plots.filter(p => p.type === 'subplot').length;
  const activePlots = plots.filter(p => p.status === 'active').length;
  const completedPlots = plots.filter(p => p.status === 'completed').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">剧情管理</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总剧情数"
              value={totalPlots}
              prefix={<BookOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="主线剧情"
              value={mainPlots}
              prefix={<BookOutlined style={{ color: '#f5222d' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="支线剧情"
              value={subPlots}
              prefix={<BranchesOutlined style={{ color: '#1890ff' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="进行中"
              value={activePlots}
              prefix={<ExclamationCircleOutlined style={{ color: '#fa8c16' }} />}
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
              添加剧情
            </Button>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={plots}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个剧情`
          }}
        />
      </Card>

      {/* 新建/编辑剧情模态框 */}
      <Modal
        title={editingPlot ? '编辑剧情' : '新建剧情'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        confirmLoading={loading}
        width={900}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            type: 'subplot',
            status: 'planning',
            priority: 'medium'
          }}
        >
          <Row gutter={16}>
            <Col span={16}>
              <Form.Item
                name="title"
                label="剧情标题"
                rules={[{ required: true, message: '请输入剧情标题' }]}
              >
                <Input placeholder="请输入剧情标题" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="type"
                label="剧情类型"
                rules={[{ required: true, message: '请选择剧情类型' }]}
              >
                <Select>
                  <Option value="main">主线</Option>
                  <Option value="subplot">支线</Option>
                  <Option value="side">番外</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择状态' }]}
              >
                <Select>
                  <Option value="planning">规划中</Option>
                  <Option value="active">进行中</Option>
                  <Option value="completed">已完成</Option>
                  <Option value="paused">暂停</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="priority"
                label="优先级"
                rules={[{ required: true, message: '请选择优先级' }]}
              >
                <Select>
                  <Option value="high">高</Option>
                  <Option value="medium">中</Option>
                  <Option value="low">低</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="progress"
                label="进度 (%)"
              >
                <Input type="number" min={0} max={100} placeholder="0-100" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="startChapter"
                label="起始章节"
                rules={[{ required: true, message: '请输入起始章节' }]}
              >
                <Input type="number" min={1} placeholder="如：1" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="endChapter"
                label="结束章节"
                rules={[{ required: true, message: '请输入结束章节' }]}
              >
                <Input type="number" min={1} placeholder="如：10" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="剧情描述"
            rules={[{ required: true, message: '请输入剧情描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请简要描述这个剧情的主要内容"
            />
          </Form.Item>

          <Form.Item
            name="outline"
            label="剧情大纲"
            rules={[{ required: true, message: '请输入剧情大纲' }]}
          >
            <TextArea
              rows={3}
              placeholder="请描述剧情的发展脉络，如：开端 -> 发展 -> 高潮 -> 结局"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="characters"
                label="相关人物"
                tooltip="每行一个人物名称"
              >
                <TextArea
                  rows={3}
                  placeholder="如：林天&#10;苏雪儿&#10;云长老"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="chapters"
                label="涉及章节"
                tooltip="每行一个章节"
              >
                <TextArea
                  rows={3}
                  placeholder="如：第一章&#10;第二章&#10;第三章"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="conflicts"
                label="冲突要素"
                tooltip="每行一个冲突"
              >
                <TextArea
                  rows={2}
                  placeholder="如：内心挣扎&#10;外部阻力"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="themes"
                label="主题元素"
                tooltip="每行一个主题"
              >
                <TextArea
                  rows={2}
                  placeholder="如：成长&#10;友情&#10;坚持"
                />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>

      {/* 剧情详情查看模态框 */}
      <Modal
        title="剧情详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={900}
      >
        {viewingPlot && (
          <div>
            <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
              <Descriptions.Item label="剧情标题" span={2}>
                <Space>
                  {typeConfig[viewingPlot.type].icon}
                  <Text strong>{viewingPlot.title}</Text>
                  <Tag color={typeConfig[viewingPlot.type].color}>
                    {typeConfig[viewingPlot.type].text}
                  </Tag>
                  <Tag color={statusConfig[viewingPlot.status].color}>
                    {statusConfig[viewingPlot.status].text}
                  </Tag>
                  <Tag color={priorityConfig[viewingPlot.priority].color}>
                    优先级：{priorityConfig[viewingPlot.priority].text}
                  </Tag>
                </Space>
              </Descriptions.Item>

              <Descriptions.Item label="章节范围">
                第{viewingPlot.startChapter}章 - 第{viewingPlot.endChapter}章
              </Descriptions.Item>
              <Descriptions.Item label="进度">
                <Progress
                  percent={viewingPlot.progress}
                  size="small"
                  status={viewingPlot.progress === 100 ? 'success' : 'active'}
                />
              </Descriptions.Item>

              <Descriptions.Item label="创建时间">{viewingPlot.createdAt}</Descriptions.Item>
              <Descriptions.Item label="更新时间">{viewingPlot.updatedAt}</Descriptions.Item>

              <Descriptions.Item label="剧情描述" span={2}>
                <Paragraph>{viewingPlot.description}</Paragraph>
              </Descriptions.Item>

              <Descriptions.Item label="剧情大纲" span={2}>
                <Paragraph>{viewingPlot.outline}</Paragraph>
              </Descriptions.Item>
            </Descriptions>

            <Row gutter={16}>
              <Col span={12}>
                <Card title="相关人物" size="small">
                  {viewingPlot.characters && viewingPlot.characters.length > 0 ? (
                    <Space wrap>
                      {viewingPlot.characters.map((character, index) => (
                        <Tag key={index} color="blue">{character}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无相关人物</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card title="涉及章节" size="small">
                  {viewingPlot.chapters && viewingPlot.chapters.length > 0 ? (
                    <Space wrap>
                      {viewingPlot.chapters.map((chapter, index) => (
                        <Tag key={index} color="green">{chapter}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无涉及章节</Text>
                  )}
                </Card>
              </Col>
            </Row>

            <Row gutter={16} style={{ marginTop: 16 }}>
              <Col span={12}>
                <Card title="冲突要素" size="small">
                  {viewingPlot.conflicts && viewingPlot.conflicts.length > 0 ? (
                    <Space wrap>
                      {viewingPlot.conflicts.map((conflict, index) => (
                        <Tag key={index} color="orange">{conflict}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无冲突要素</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card title="主题元素" size="small">
                  {viewingPlot.themes && viewingPlot.themes.length > 0 ? (
                    <Space wrap>
                      {viewingPlot.themes.map((theme, index) => (
                        <Tag key={index} color="purple">{theme}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无主题元素</Text>
                  )}
                </Card>
              </Col>
            </Row>

            {/* 剧情发展时间线 */}
            <Card title="剧情发展时间线" size="small" style={{ marginTop: 16 }}>
              <Timeline>
                <Timeline.Item color="blue">
                  <Text strong>剧情创建</Text>
                  <br />
                  <Text type="secondary">{viewingPlot.createdAt}</Text>
                </Timeline.Item>
                {viewingPlot.status === 'active' && (
                  <Timeline.Item color="orange">
                    <Text strong>剧情进行中</Text>
                    <br />
                    <Text type="secondary">进度：{viewingPlot.progress}%</Text>
                  </Timeline.Item>
                )}
                {viewingPlot.status === 'completed' && (
                  <Timeline.Item color="green">
                    <Text strong>剧情完成</Text>
                    <br />
                    <Text type="secondary">{viewingPlot.updatedAt}</Text>
                  </Timeline.Item>
                )}
                {viewingPlot.status === 'planning' && (
                  <Timeline.Item color="gray">
                    <Text strong>规划阶段</Text>
                    <br />
                    <Text type="secondary">等待开始</Text>
                  </Timeline.Item>
                )}
              </Timeline>
            </Card>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default PlotList;