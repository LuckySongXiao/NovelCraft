import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
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
  Progress,
  Tooltip,
  Row,
  Col,
  Statistic,
  Collapse,
  List,
  Divider,
  Tabs,
  Empty
} from 'antd';
import {
  PlusOutlined,
  FileTextOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  BookOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  FolderOutlined,
  OrderedListOutlined,
  BarChartOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { Panel } = Collapse;
const { TabPane } = Tabs;

const VolumeList = () => {
  const { id: projectId } = useParams();
  const navigate = useNavigate();
  const [volumes, setVolumes] = useState([]);
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(false);
  const [volumeModalVisible, setVolumeModalVisible] = useState(false);
  const [chapterModalVisible, setChapterModalVisible] = useState(false);
  const [assignModalVisible, setAssignModalVisible] = useState(false);
  const [editingVolume, setEditingVolume] = useState(null);
  const [editingChapter, setEditingChapter] = useState(null);
  const [assigningChapter, setAssigningChapter] = useState(null);
  const [selectedVolumeId, setSelectedVolumeId] = useState(null);
  const [activeTab, setActiveTab] = useState('volumes');
  const [volumeForm] = Form.useForm();
  const [chapterForm] = Form.useForm();
  const [assignForm] = Form.useForm();

  // 状态配置
  const volumeStatusConfig = {
    planning: { color: 'blue', text: '规划中' },
    writing: { color: 'orange', text: '写作中' },
    completed: { color: 'green', text: '已完成' },
    reviewing: { color: 'purple', text: '审阅中' },
    revised: { color: 'cyan', text: '已修订' },
    published: { color: 'success', text: '已发布' }
  };

  const chapterStatusConfig = {
    planning: { color: 'blue', text: '规划中' },
    draft: { color: 'orange', text: '草稿' },
    writing: { color: 'processing', text: '写作中' },
    completed: { color: 'green', text: '已完成' },
    published: { color: 'success', text: '已发布' }
  };

  // 模拟卷宗数据
  const mockVolumes = [
    {
      id: 1,
      title: '第一卷：初入修仙界',
      volumeNumber: 1,
      status: 'writing',
      summary: '主角初次踏入修仙世界，遇到师父，开始修炼之路',
      totalChapters: 10,
      completedChapters: 6,
      totalWords: 45000,
      targetWords: 80000,
      progress: 60,
      createdAt: '2024-01-15',
      updatedAt: '2024-01-20'
    },
    {
      id: 2,
      title: '第二卷：宗门试炼',
      volumeNumber: 2,
      status: 'planning',
      summary: '主角参加宗门入门试炼，展现天赋，结识同门',
      totalChapters: 8,
      completedChapters: 0,
      totalWords: 0,
      targetWords: 60000,
      progress: 0,
      createdAt: '2024-01-21',
      updatedAt: '2024-01-21'
    }
  ];

  // 模拟章节数据
  const mockChapters = [
    {
      id: 1,
      volumeId: 1,
      title: '第一章：觉醒',
      chapterNumber: 1,
      content: '在这个充满灵气的世界里，少年踏上了修仙之路...',
      wordCount: 3500,
      status: 'published',
      outline: '主角初次接触修仙世界，遇到第一位师父',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-16'
    },
    {
      id: 2,
      volumeId: 1,
      title: '第二章：师父',
      chapterNumber: 2,
      content: '经过数月的修炼，主角终于感受到了灵气的存在...',
      wordCount: 4200,
      status: 'completed',
      outline: '主角开始正式修炼，学习基础功法',
      createdAt: '2024-01-17',
      updatedAt: '2024-01-18'
    },
    {
      id: 3,
      volumeId: 1,
      title: '第三章：修炼',
      chapterNumber: 3,
      content: '',
      wordCount: 0,
      status: 'planning',
      outline: '主角参加宗门入门试炼，展现天赋',
      createdAt: '2024-01-19',
      updatedAt: '2024-01-19'
    },
    {
      id: 4,
      volumeId: 2,
      title: '第四章：试炼开始',
      chapterNumber: 1,
      content: '',
      wordCount: 0,
      status: 'planning',
      outline: '宗门试炼正式开始，各路天才汇聚',
      createdAt: '2024-01-20',
      updatedAt: '2024-01-20'
    },
    {
      id: 5,
      volumeId: null, // 独立章节，未分配到卷宗
      title: '番外：师父的过往',
      chapterNumber: null,
      content: '很久以前，师父也是一个普通的修炼者...',
      wordCount: 2800,
      status: 'draft',
      outline: '讲述师父的背景故事',
      createdAt: '2024-01-21',
      updatedAt: '2024-01-21'
    }
  ];

  useEffect(() => {
    setVolumes(mockVolumes);
    setChapters(mockChapters);
  }, []);

  // 统计数据
  const totalVolumes = volumes.length;
  const totalChapters = chapters.length;
  const completedChapters = chapters.filter(c => c.status === 'completed' || c.status === 'published').length;
  const totalWords = chapters.reduce((sum, chapter) => sum + (chapter.wordCount || 0), 0);
  const independentChapters = chapters.filter(c => !c.volumeId).length;

  // 卷宗表格列配置
  const volumeColumns = [
    {
      title: '卷宗标题',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) => (
        <Space>
          <FolderOutlined />
          <Text strong>{text}</Text>
          <Tag color="blue">第{record.volumeNumber}卷</Tag>
        </Space>
      )
    },
    {
      title: '进度',
      dataIndex: 'progress',
      key: 'progress',
      render: (progress, record) => (
        <div>
          <Progress percent={progress} size="small" />
          <Text type="secondary">
            {record.completedChapters}/{record.totalChapters} 章节
          </Text>
        </div>
      ),
      sorter: (a, b) => a.progress - b.progress
    },
    {
      title: '字数',
      dataIndex: 'totalWords',
      key: 'totalWords',
      render: (words, record) => (
        <div>
          <Text>{words.toLocaleString()} 字</Text>
          {record.targetWords && (
            <div>
              <Text type="secondary">目标: {record.targetWords.toLocaleString()}</Text>
            </div>
          )}
        </div>
      ),
      sorter: (a, b) => a.totalWords - b.totalWords
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={volumeStatusConfig[status].color}>
          {volumeStatusConfig[status].text}
        </Tag>
      ),
      filters: Object.entries(volumeStatusConfig).map(([key, config]) => ({
        text: config.text,
        value: key
      })),
      onFilter: (value, record) => record.status === value
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
          <Tooltip title="查看章节">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => handleViewVolumeChapters(record)}
            />
          </Tooltip>
          <Tooltip title="编辑卷宗">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEditVolume(record)}
            />
          </Tooltip>
          <Tooltip title="添加章节">
            <Button
              type="text"
              icon={<PlusOutlined />}
              onClick={() => handleAddChapter(record)}
            />
          </Tooltip>
          <Tooltip title="AI生成大纲">
            <Button
              type="text"
              icon={<RobotOutlined />}
              onClick={() => handleAIGenerateOutline(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个卷宗吗？这将同时删除其下所有章节。"
            onConfirm={() => handleDeleteVolume(record.id)}
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

  // 章节表格列配置
  const chapterColumns = [
    {
      title: '章节标题',
      dataIndex: 'title',
      key: 'title',
      render: (text, record) => (
        <Space>
          <FileTextOutlined />
          <Text strong>{text}</Text>
          {record.chapterNumber && (
            <Tag color="blue">第{record.chapterNumber}章</Tag>
          )}
        </Space>
      )
    },
    {
      title: '所属卷宗',
      dataIndex: 'volumeId',
      key: 'volumeId',
      render: (volumeId) => {
        if (!volumeId) {
          return <Tag color="orange">独立章节</Tag>;
        }
        const volume = volumes.find(v => v.id === volumeId);
        return volume ? (
          <Tag color="blue">{volume.title}</Tag>
        ) : (
          <Tag color="red">未知卷宗</Tag>
        );
      },
      filters: [
        { text: '独立章节', value: null },
        ...volumes.map(v => ({ text: v.title, value: v.id }))
      ],
      onFilter: (value, record) => record.volumeId === value
    },
    {
      title: '字数',
      dataIndex: 'wordCount',
      key: 'wordCount',
      render: (count) => (
        <Text type={count === 0 ? 'secondary' : 'default'}>
          {count.toLocaleString()} 字
        </Text>
      ),
      sorter: (a, b) => a.wordCount - b.wordCount
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={chapterStatusConfig[status].color}>
          {chapterStatusConfig[status].text}
        </Tag>
      ),
      filters: Object.entries(chapterStatusConfig).map(([key, config]) => ({
        text: config.text,
        value: key
      })),
      onFilter: (value, record) => record.status === value
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
          <Tooltip title="查看">
            <Button
              type="text"
              icon={<EyeOutlined />}
              onClick={() => handleViewChapter(record)}
            />
          </Tooltip>
          <Tooltip title="编辑">
            <Button
              type="text"
              icon={<EditOutlined />}
              onClick={() => handleEditChapter(record)}
            />
          </Tooltip>
          <Tooltip title="AI续写">
            <Button
              type="text"
              icon={<RobotOutlined />}
              onClick={() => handleAIContinueChapter(record)}
            />
          </Tooltip>
          <Tooltip title="分配到卷宗">
            <Button
              type="text"
              icon={<FolderOutlined />}
              onClick={() => handleAssignToVolume(record)}
            />
          </Tooltip>
          <Popconfirm
            title="确定删除这个章节吗？"
            onConfirm={() => handleDeleteChapter(record.id)}
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

  // 处理函数
  const handleCreateVolume = () => {
    setEditingVolume(null);
    volumeForm.resetFields();
    setVolumeModalVisible(true);
  };

  const handleEditVolume = (volume) => {
    setEditingVolume(volume);
    volumeForm.setFieldsValue(volume);
    setVolumeModalVisible(true);
  };

  const handleViewVolumeChapters = (volume) => {
    setSelectedVolumeId(volume.id);
    message.info(`查看卷宗《${volume.title}》的章节`);
  };

  const handleAddChapter = (volume) => {
    setSelectedVolumeId(volume.id);
    setEditingChapter(null);
    chapterForm.resetFields();
    chapterForm.setFieldsValue({ volumeId: volume.id });
    setChapterModalVisible(true);
  };

  const handleAIGenerateOutline = (volume) => {
    message.info(`AI生成卷宗《${volume.title}》大纲功能`);
  };

  const handleDeleteVolume = async (id) => {
    try {
      // 调用后端API删除卷宗
      await axios.delete(`/api/project-data/projects/${projectId}/data/volume/${id}`);

      // 删除成功后从列表中移除
      setVolumes(volumes.filter(v => v.id !== id));
      setChapters(chapters.filter(c => c.volumeId !== id));
      message.success('卷宗删除成功');
    } catch (error) {
      console.error('删除卷宗失败:', error);
      message.error('删除卷宗失败');
    }
  };

  const handleVolumeModalOk = async () => {
    try {
      const values = await volumeForm.validateFields();
      setLoading(true);

      if (editingVolume) {
        // 编辑卷宗
        setVolumes(volumes.map(v =>
          v.id === editingVolume.id
            ? { ...v, ...values, updatedAt: new Date().toISOString().split('T')[0] }
            : v
        ));
        message.success('卷宗更新成功');
      } else {
        // 新建卷宗
        const newVolume = {
          id: Date.now(),
          ...values,
          totalChapters: 0,
          completedChapters: 0,
          totalWords: 0,
          progress: 0,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setVolumes([...volumes, newVolume]);
        message.success('卷宗创建成功');
      }

      setVolumeModalVisible(false);
      volumeForm.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleChapterModalOk = async () => {
    try {
      const values = await chapterForm.validateFields();
      setLoading(true);

      if (editingChapter) {
        // 编辑章节
        setChapters(chapters.map(c =>
          c.id === editingChapter.id
            ? { ...c, ...values, updatedAt: new Date().toISOString().split('T')[0] }
            : c
        ));
        message.success('章节更新成功');
      } else {
        // 新建章节
        const newChapter = {
          id: Date.now(),
          ...values,
          wordCount: 0,
          createdAt: new Date().toISOString().split('T')[0],
          updatedAt: new Date().toISOString().split('T')[0]
        };
        setChapters([...chapters, newChapter]);
        message.success('章节创建成功');
      }

      setChapterModalVisible(false);
      chapterForm.resetFields();
    } catch (error) {
      console.error('表单验证失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 章节相关处理函数
  const handleCreateChapter = () => {
    setEditingChapter(null);
    chapterForm.resetFields();
    chapterForm.setFieldsValue({ volumeId: null }); // 默认为独立章节
    setChapterModalVisible(true);
  };

  const handleViewChapter = (chapter) => {
    const volumeId = chapter.volumeId || 'independent';
    navigate(`/projects/${projectId}/volumes/${volumeId}/chapters/${chapter.id}`);
  };

  const handleEditChapter = (chapter) => {
    setEditingChapter(chapter);
    chapterForm.setFieldsValue(chapter);
    setChapterModalVisible(true);
  };

  const handleAIContinueChapter = (chapter) => {
    message.info(`AI续写功能：${chapter.title}`);
  };

  const handleAssignToVolume = (chapter) => {
    setAssigningChapter(chapter);
    assignForm.setFieldsValue({ volumeId: chapter.volumeId });
    setAssignModalVisible(true);
  };

  const handleAssignModalOk = async () => {
    try {
      const values = await assignForm.validateFields();
      setLoading(true);

      setChapters(chapters.map(c =>
        c.id === assigningChapter.id
          ? { ...c, volumeId: values.volumeId, updatedAt: new Date().toISOString().split('T')[0] }
          : c
      ));

      message.success('章节分配成功');
      setAssignModalVisible(false);
      assignForm.resetFields();
    } catch (error) {
      console.error('分配失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteChapter = async (id) => {
    try {
      // 调用后端API删除章节
      await axios.delete(`/api/project-data/projects/${projectId}/data/chapter/${id}`);

      // 删除成功后从列表中移除
      setChapters(chapters.filter(c => c.id !== id));
      message.success('章节删除成功');
    } catch (error) {
      console.error('删除章节失败:', error);
      message.error('删除章节失败');
    }
  };

  // 获取指定卷宗的章节
  const getVolumeChapters = (volumeId) => {
    return chapters.filter(c => c.volumeId === volumeId);
  };

  // 获取独立章节
  const getIndependentChapters = () => {
    return chapters.filter(c => !c.volumeId);
  };

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">卷宗管理</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总卷宗数"
              value={totalVolumes}
              prefix={<FolderOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总章节数"
              value={totalChapters}
              prefix={<BookOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="独立章节"
              value={independentChapters}
              prefix={<FileTextOutlined style={{ color: '#fa8c16' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总字数"
              value={totalWords}
              suffix="字"
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
      </Row>

      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'volumes',
              label: (
                <span>
                  <FolderOutlined />
                  卷宗管理
                </span>
              ),
              children: (
                <div>
                  <div className="toolbar" style={{ marginBottom: 16 }}>
                    <div className="toolbar-left">
                      <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={handleCreateVolume}
                      >
                        新建卷宗
                      </Button>
                    </div>
                  </div>

                  <Table
                    columns={volumeColumns}
                    dataSource={volumes}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      showSizeChanger: true,
                      showQuickJumper: true,
                      showTotal: (total) => `共 ${total} 个卷宗`
                    }}
                    expandable={{
                      expandedRowRender: (volume) => {
                        const volumeChapters = getVolumeChapters(volume.id);
                        return (
                          <div style={{ margin: 0 }}>
                            <Divider orientation="left">章节列表</Divider>
                            <List
                              size="small"
                              dataSource={volumeChapters}
                              renderItem={(chapter) => (
                                <List.Item
                                  actions={[
                                    <Button
                                      type="link"
                                      size="small"
                                      onClick={() => navigate(`/projects/${projectId}/volumes/${volume.id}/chapters/${chapter.id}`)}
                                    >
                                      编辑
                                    </Button>,
                                    <Button
                                      type="link"
                                      size="small"
                                      onClick={() => navigate(`/projects/${projectId}/volumes/${volume.id}/chapters/${chapter.id}`)}
                                    >
                                      查看
                                    </Button>
                                  ]}
                                >
                                  <List.Item.Meta
                                    avatar={<FileTextOutlined />}
                                    title={
                                      <Space>
                                        {chapter.title}
                                        <Tag color={chapterStatusConfig[chapter.status].color}>
                                          {chapterStatusConfig[chapter.status].text}
                                        </Tag>
                                      </Space>
                                    }
                                    description={`字数: ${chapter.wordCount} | 更新: ${chapter.updatedAt}`}
                                  />
                                </List.Item>
                              )}
                            />
                            {volumeChapters.length === 0 && (
                              <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
                                暂无章节，点击上方"添加章节"按钮创建
                              </div>
                            )}
                          </div>
                        );
                      },
                      rowExpandable: () => true,
                    }}
                  />
                </div>
              )
            },
            {
              key: 'chapters',
              label: (
                <span>
                  <FileTextOutlined />
                  章节管理
                </span>
              ),
              children: (
                <div>
                  <div className="toolbar" style={{ marginBottom: 16 }}>
                    <div className="toolbar-left">
                      <Button
                        type="primary"
                        icon={<PlusOutlined />}
                        onClick={handleCreateChapter}
                      >
                        新建章节
                      </Button>
                    </div>
                  </div>

                  <Table
                    columns={chapterColumns}
                    dataSource={chapters}
                    rowKey="id"
                    loading={loading}
                    pagination={{
                      showSizeChanger: true,
                      showQuickJumper: true,
                      showTotal: (total) => `共 ${total} 个章节`
                    }}
                  />

                  {getIndependentChapters().length > 0 && (
                    <div style={{ marginTop: 24 }}>
                      <Divider orientation="left">独立章节</Divider>
                      <List
                        dataSource={getIndependentChapters()}
                        renderItem={(chapter) => (
                          <List.Item
                            actions={[
                              <Button
                                type="link"
                                onClick={() => handleViewChapter(chapter)}
                              >
                                查看
                              </Button>,
                              <Button
                                type="link"
                                onClick={() => handleEditChapter(chapter)}
                              >
                                编辑
                              </Button>,
                              <Button
                                type="link"
                                onClick={() => handleAssignToVolume(chapter)}
                              >
                                分配到卷宗
                              </Button>
                            ]}
                          >
                            <List.Item.Meta
                              avatar={<FileTextOutlined />}
                              title={
                                <Space>
                                  {chapter.title}
                                  <Tag color={chapterStatusConfig[chapter.status].color}>
                                    {chapterStatusConfig[chapter.status].text}
                                  </Tag>
                                  <Tag color="orange">独立章节</Tag>
                                </Space>
                              }
                              description={`字数: ${chapter.wordCount} | 更新: ${chapter.updatedAt}`}
                            />
                          </List.Item>
                        )}
                      />
                    </div>
                  )}
                </div>
              )
            }
          ]}
        />
      </Card>

      {/* 新建/编辑卷宗模态框 */}
      <Modal
        title={editingVolume ? '编辑卷宗' : '新建卷宗'}
        open={volumeModalVisible}
        onOk={handleVolumeModalOk}
        onCancel={() => {
          setVolumeModalVisible(false);
          volumeForm.resetFields();
        }}
        confirmLoading={loading}
        width={800}
      >
        <Form
          form={volumeForm}
          layout="vertical"
          initialValues={{ status: 'planning' }}
        >
          <Row gutter={16}>
            <Col span={16}>
              <Form.Item
                name="title"
                label="卷宗标题"
                rules={[{ required: true, message: '请输入卷宗标题' }]}
              >
                <Input placeholder="请输入卷宗标题" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="volumeNumber"
                label="卷序号"
                rules={[{ required: true, message: '请输入卷序号' }]}
              >
                <Input type="number" placeholder="1" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="summary"
            label="卷宗摘要"
            rules={[{ required: true, message: '请输入卷宗摘要' }]}
          >
            <TextArea
              rows={3}
              placeholder="请简要描述本卷的主要内容和剧情发展"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择卷宗状态' }]}
              >
                <Select>
                  {Object.entries(volumeStatusConfig).map(([key, config]) => (
                    <Option key={key} value={key}>{config.text}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="targetWords"
                label="目标字数"
              >
                <Input type="number" placeholder="80000" suffix="字" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="outline"
            label="卷宗大纲"
          >
            <TextArea
              rows={6}
              placeholder="详细描述本卷的章节安排和剧情发展..."
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 新建/编辑章节模态框 */}
      <Modal
        title={editingChapter ? '编辑章节' : '新建章节'}
        open={chapterModalVisible}
        onOk={handleChapterModalOk}
        onCancel={() => {
          setChapterModalVisible(false);
          chapterForm.resetFields();
        }}
        confirmLoading={loading}
        width={600}
      >
        <Form
          form={chapterForm}
          layout="vertical"
          initialValues={{ status: 'planning' }}
        >
          <Form.Item
            name="volumeId"
            label="所属卷宗"
            help="留空则创建为独立章节"
          >
            <Select placeholder="请选择卷宗（可留空创建独立章节）" allowClear>
              {volumes.map(volume => (
                <Option key={volume.id} value={volume.id}>
                  {volume.title}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Row gutter={16}>
            <Col span={16}>
              <Form.Item
                name="title"
                label="章节标题"
                rules={[{ required: true, message: '请输入章节标题' }]}
              >
                <Input placeholder="请输入章节标题" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="chapterNumber"
                label="章节序号"
                help="独立章节可留空"
              >
                <Input type="number" placeholder="1" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="status"
            label="状态"
            rules={[{ required: true, message: '请选择章节状态' }]}
          >
            <Select>
              {Object.entries(chapterStatusConfig).map(([key, config]) => (
                <Option key={key} value={key}>{config.text}</Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="outline"
            label="章节大纲"
          >
            <TextArea
              rows={4}
              placeholder="请简要描述本章节的主要内容和情节发展"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 分配章节到卷宗模态框 */}
      <Modal
        title="分配章节到卷宗"
        open={assignModalVisible}
        onOk={handleAssignModalOk}
        onCancel={() => {
          setAssignModalVisible(false);
          assignForm.resetFields();
        }}
        confirmLoading={loading}
        width={400}
      >
        <Form
          form={assignForm}
          layout="vertical"
        >
          <div style={{ marginBottom: 16 }}>
            <Text strong>章节：</Text>
            <Text>{assigningChapter?.title}</Text>
          </div>

          <Form.Item
            name="volumeId"
            label="目标卷宗"
            help="选择要分配到的卷宗，留空则设为独立章节"
          >
            <Select placeholder="请选择卷宗" allowClear>
              {volumes.map(volume => (
                <Option key={volume.id} value={volume.id}>
                  {volume.title}
                </Option>
              ))}
            </Select>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default VolumeList;
