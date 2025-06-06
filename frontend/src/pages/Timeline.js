import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import {
  Card,
  Typography,
  Button,
  Timeline as AntTimeline,
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
  DatePicker,
  InputNumber,
  Divider
} from 'antd';
import {
  PlusOutlined,
  ClockCircleOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  RobotOutlined,
  CalendarOutlined,
  HistoryOutlined,
  StarOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';

const { Title, Text, Paragraph } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const Timeline = () => {
  const { id: projectId } = useParams();
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [detailModalVisible, setDetailModalVisible] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);
  const [viewingEvent, setViewingEvent] = useState(null);
  const [form] = Form.useForm();

  // 模拟时间线事件数据
  const mockEvents = [
    {
      id: 1,
      title: '林天觉醒修仙天赋',
      type: 'major',
      category: 'character',
      timeType: 'story',
      storyTime: '第1年春',
      realTime: '2024-01-15',
      chapter: 1,
      description: '主角林天在一次意外中觉醒了修仙天赋，从此踏上修仙之路',
      participants: ['林天'],
      location: '青云村',
      consequences: '开启修仙之路，改变人生轨迹',
      relatedPlots: ['主线：修仙之路'],
      importance: 5,
      status: 'completed',
      createdAt: '2024-01-15'
    },
    {
      id: 2,
      title: '拜入青云宗',
      type: 'major',
      category: 'plot',
      timeType: 'story',
      storyTime: '第1年夏',
      realTime: '2024-01-16',
      chapter: 3,
      description: '林天通过考核，正式拜入青云宗，成为云长老的弟子',
      participants: ['林天', '云长老'],
      location: '青云宗',
      consequences: '获得正式修炼资格，开始系统学习',
      relatedPlots: ['主线：修仙之路'],
      importance: 4,
      status: 'completed',
      createdAt: '2024-01-16'
    },
    {
      id: 3,
      title: '初遇苏雪儿',
      type: 'minor',
      category: 'relationship',
      timeType: 'story',
      storyTime: '第1年秋',
      realTime: '2024-01-17',
      chapter: 5,
      description: '林天在宗门内初次遇见苏雪儿，两人产生好感',
      participants: ['林天', '苏雪儿'],
      location: '青云宗藏书阁',
      consequences: '开启感情线，为后续发展埋下伏笔',
      relatedPlots: ['支线：情感线索'],
      importance: 3,
      status: 'completed',
      createdAt: '2024-01-17'
    },
    {
      id: 4,
      title: '首次与血煞魔君交锋',
      type: 'major',
      category: 'conflict',
      timeType: 'story',
      storyTime: '第2年春',
      realTime: '2024-01-18',
      chapter: 8,
      description: '林天在历练中遭遇血煞魔君，双方首次交手',
      participants: ['林天', '血煞魔君'],
      location: '血煞谷',
      consequences: '确立宿敌关系，推动主线剧情发展',
      relatedPlots: ['主线：修仙之路'],
      importance: 5,
      status: 'completed',
      createdAt: '2024-01-18'
    },
    {
      id: 5,
      title: '突破筑基期',
      type: 'minor',
      category: 'cultivation',
      timeType: 'story',
      storyTime: '第2年夏',
      realTime: '2024-01-19',
      chapter: 10,
      description: '林天经过刻苦修炼，成功突破到筑基期',
      participants: ['林天'],
      location: '青云宗修炼室',
      consequences: '实力大幅提升，为后续挑战做准备',
      relatedPlots: ['主线：修仙之路'],
      importance: 3,
      status: 'completed',
      createdAt: '2024-01-19'
    }
  ];

  useEffect(() => {
    setEvents(mockEvents.sort((a, b) => a.chapter - b.chapter));
  }, []);

  // 事件类型配置
  const typeConfig = {
    major: { color: 'red', text: '重大事件', icon: <StarOutlined /> },
    minor: { color: 'blue', text: '一般事件', icon: <ClockCircleOutlined /> },
    milestone: { color: 'gold', text: '里程碑', icon: <CheckCircleOutlined /> }
  };

  // 事件分类配置
  const categoryConfig = {
    character: { color: 'blue', text: '人物' },
    plot: { color: 'green', text: '剧情' },
    relationship: { color: 'pink', text: '关系' },
    conflict: { color: 'red', text: '冲突' },
    cultivation: { color: 'orange', text: '修炼' },
    world: { color: 'purple', text: '世界' }
  };

  // 状态配置
  const statusConfig = {
    planned: { color: 'blue', text: '计划中' },
    ongoing: { color: 'orange', text: '进行中' },
    completed: { color: 'green', text: '已完成' },
    cancelled: { color: 'default', text: '已取消' }
  };

  // 处理新建/编辑事件
  const handleCreateOrEdit = () => {
    setEditingEvent(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (event) => {
    setEditingEvent(event);
    form.setFieldsValue({
      ...event,
      participants: event.participants.join('\n'),
      relatedPlots: event.relatedPlots.join('\n'),
      realTime: event.realTime ? dayjs(event.realTime) : null
    });
    setModalVisible(true);
  };

  const handleView = (event) => {
    setViewingEvent(event);
    setDetailModalVisible(true);
  };

  const handleAIGenerate = (event) => {
    message.info(`AI分析事件：${event.title}`);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除数据
      await axios.delete(`/api/project-data/projects/${projectId}/data/timeline/${id}`);

      // 删除成功后从列表中移除
      setEvents(events.filter(e => e.id !== id));
      message.success('事件删除成功');
    } catch (error) {
      console.error('删除事件失败:', error);
      message.error('删除事件失败');
    }
  };

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 处理数组字段和日期
      const processedValues = {
        ...values,
        participants: values.participants ? values.participants.split('\n').filter(item => item.trim()) : [],
        relatedPlots: values.relatedPlots ? values.relatedPlots.split('\n').filter(item => item.trim()) : [],
        realTime: values.realTime ? values.realTime.format('YYYY-MM-DD') : null
      };

      if (editingEvent) {
        // 编辑事件
        setEvents(events.map(e =>
          e.id === editingEvent.id
            ? { ...e, ...processedValues }
            : e
        ).sort((a, b) => a.chapter - b.chapter));
        message.success('事件更新成功');
      } else {
        // 新建事件
        const newEvent = {
          id: Date.now(),
          ...processedValues,
          createdAt: new Date().toISOString().split('T')[0]
        };
        setEvents([...events, newEvent].sort((a, b) => a.chapter - b.chapter));
        message.success('事件创建成功');
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
  const totalEvents = events.length;
  const majorEvents = events.filter(e => e.type === 'major').length;
  const completedEvents = events.filter(e => e.status === 'completed').length;
  const plannedEvents = events.filter(e => e.status === 'planned').length;

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">时间线</Title>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总事件数"
              value={totalEvents}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="重大事件"
              value={majorEvents}
              prefix={<StarOutlined style={{ color: '#f5222d' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="已完成"
              value={completedEvents}
              prefix={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="计划中"
              value={plannedEvents}
              prefix={<ExclamationCircleOutlined style={{ color: '#1890ff' }} />}
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
              添加事件
            </Button>
          </div>
        </div>

        {/* 时间线展示 */}
        <AntTimeline mode="left" style={{ marginTop: 24 }}>
          {events.map((event) => (
            <AntTimeline.Item
              key={event.id}
              color={typeConfig[event.type].color}
              dot={typeConfig[event.type].icon}
            >
              <Card size="small" style={{ marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ flex: 1 }}>
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <div>
                        <Text strong style={{ fontSize: '16px' }}>{event.title}</Text>
                        <Space style={{ marginLeft: 16 }}>
                          <Tag color={typeConfig[event.type].color}>
                            {typeConfig[event.type].text}
                          </Tag>
                          <Tag color={categoryConfig[event.category].color}>
                            {categoryConfig[event.category].text}
                          </Tag>
                          <Tag color={statusConfig[event.status].color}>
                            {statusConfig[event.status].text}
                          </Tag>
                        </Space>
                      </div>

                      <Space>
                        <Text type="secondary">
                          <CalendarOutlined /> {event.storyTime}
                        </Text>
                        <Text type="secondary">
                          第{event.chapter}章
                        </Text>
                        {event.location && (
                          <Text type="secondary">
                            📍 {event.location}
                          </Text>
                        )}
                      </Space>

                      <Paragraph style={{ margin: 0, color: '#666' }}>
                        {event.description}
                      </Paragraph>

                      {event.participants && event.participants.length > 0 && (
                        <div>
                          <Text type="secondary">参与人物：</Text>
                          <Space wrap>
                            {event.participants.map((participant, index) => (
                              <Tag key={index} size="small">{participant}</Tag>
                            ))}
                          </Space>
                        </div>
                      )}
                    </Space>
                  </div>

                  <Space>
                    <Tooltip title="查看详情">
                      <Button
                        type="text"
                        icon={<EyeOutlined />}
                        onClick={() => handleView(event)}
                      />
                    </Tooltip>
                    <Tooltip title="编辑">
                      <Button
                        type="text"
                        icon={<EditOutlined />}
                        onClick={() => handleEdit(event)}
                      />
                    </Tooltip>
                    <Tooltip title="AI分析">
                      <Button
                        type="text"
                        icon={<RobotOutlined />}
                        onClick={() => handleAIGenerate(event)}
                      />
                    </Tooltip>
                    <Popconfirm
                      title="确定删除这个事件吗？"
                      onConfirm={() => handleDelete(event.id)}
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
                </div>
              </Card>
            </AntTimeline.Item>
          ))}
        </AntTimeline>
      </Card>

      {/* 新建/编辑事件模态框 */}
      <Modal
        title={editingEvent ? '编辑事件' : '新建事件'}
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
            type: 'minor',
            category: 'plot',
            timeType: 'story',
            status: 'planned',
            importance: 3
          }}
        >
          <Row gutter={16}>
            <Col span={16}>
              <Form.Item
                name="title"
                label="事件标题"
                rules={[{ required: true, message: '请输入事件标题' }]}
              >
                <Input placeholder="请输入事件标题" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="type"
                label="事件类型"
                rules={[{ required: true, message: '请选择事件类型' }]}
              >
                <Select>
                  <Option value="major">重大事件</Option>
                  <Option value="minor">一般事件</Option>
                  <Option value="milestone">里程碑</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="category"
                label="事件分类"
                rules={[{ required: true, message: '请选择事件分类' }]}
              >
                <Select>
                  <Option value="character">人物</Option>
                  <Option value="plot">剧情</Option>
                  <Option value="relationship">关系</Option>
                  <Option value="conflict">冲突</Option>
                  <Option value="cultivation">修炼</Option>
                  <Option value="world">世界</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="status"
                label="事件状态"
                rules={[{ required: true, message: '请选择事件状态' }]}
              >
                <Select>
                  <Option value="planned">计划中</Option>
                  <Option value="ongoing">进行中</Option>
                  <Option value="completed">已完成</Option>
                  <Option value="cancelled">已取消</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="importance"
                label="重要程度"
                rules={[{ required: true, message: '请选择重要程度' }]}
              >
                <Select>
                  <Option value={1}>1 - 很低</Option>
                  <Option value={2}>2 - 低</Option>
                  <Option value={3}>3 - 中等</Option>
                  <Option value={4}>4 - 高</Option>
                  <Option value={5}>5 - 很高</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="storyTime"
                label="故事时间"
                rules={[{ required: true, message: '请输入故事时间' }]}
              >
                <Input placeholder="如：第1年春" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="chapter"
                label="所在章节"
                rules={[{ required: true, message: '请输入章节' }]}
              >
                <InputNumber min={1} style={{ width: '100%' }} placeholder="章节号" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="realTime"
                label="现实时间"
              >
                <DatePicker style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="location"
            label="发生地点"
          >
            <Input placeholder="事件发生的地点" />
          </Form.Item>

          <Form.Item
            name="description"
            label="事件描述"
            rules={[{ required: true, message: '请输入事件描述' }]}
          >
            <TextArea
              rows={3}
              placeholder="请详细描述这个事件的内容"
            />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="participants"
                label="参与人物"
                tooltip="每行一个人物"
              >
                <TextArea
                  rows={3}
                  placeholder="如：林天&#10;苏雪儿&#10;云长老"
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="relatedPlots"
                label="相关剧情"
                tooltip="每行一个剧情"
              >
                <TextArea
                  rows={3}
                  placeholder="如：主线：修仙之路&#10;支线：情感线索"
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="consequences"
            label="事件后果"
          >
            <TextArea
              rows={2}
              placeholder="这个事件产生的影响和后果"
            />
          </Form.Item>
        </Form>
      </Modal>

      {/* 事件详情查看模态框 */}
      <Modal
        title="事件详情"
        open={detailModalVisible}
        onCancel={() => setDetailModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setDetailModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={800}
      >
        {viewingEvent && (
          <div>
            <Descriptions bordered column={2} style={{ marginBottom: 24 }}>
              <Descriptions.Item label="事件标题" span={2}>
                <Space>
                  {typeConfig[viewingEvent.type].icon}
                  <Text strong>{viewingEvent.title}</Text>
                  <Tag color={typeConfig[viewingEvent.type].color}>
                    {typeConfig[viewingEvent.type].text}
                  </Tag>
                  <Tag color={categoryConfig[viewingEvent.category].color}>
                    {categoryConfig[viewingEvent.category].text}
                  </Tag>
                  <Tag color={statusConfig[viewingEvent.status].color}>
                    {statusConfig[viewingEvent.status].text}
                  </Tag>
                </Space>
              </Descriptions.Item>

              <Descriptions.Item label="故事时间">{viewingEvent.storyTime}</Descriptions.Item>
              <Descriptions.Item label="所在章节">第{viewingEvent.chapter}章</Descriptions.Item>

              {viewingEvent.realTime && (
                <Descriptions.Item label="现实时间">{viewingEvent.realTime}</Descriptions.Item>
              )}
              {viewingEvent.location && (
                <Descriptions.Item label="发生地点">{viewingEvent.location}</Descriptions.Item>
              )}

              <Descriptions.Item label="重要程度">
                <Space>
                  {Array.from({ length: viewingEvent.importance }, (_, i) => (
                    <StarOutlined key={i} style={{ color: '#faad14' }} />
                  ))}
                  <Text>({viewingEvent.importance}/5)</Text>
                </Space>
              </Descriptions.Item>
              <Descriptions.Item label="创建时间">{viewingEvent.createdAt}</Descriptions.Item>

              <Descriptions.Item label="事件描述" span={2}>
                <Paragraph>{viewingEvent.description}</Paragraph>
              </Descriptions.Item>

              {viewingEvent.consequences && (
                <Descriptions.Item label="事件后果" span={2}>
                  <Paragraph>{viewingEvent.consequences}</Paragraph>
                </Descriptions.Item>
              )}
            </Descriptions>

            <Row gutter={16} style={{ marginTop: 16 }}>
              <Col span={12}>
                <Card title="参与人物" size="small">
                  {viewingEvent.participants && viewingEvent.participants.length > 0 ? (
                    <Space wrap>
                      {viewingEvent.participants.map((participant, index) => (
                        <Tag key={index} color="blue">{participant}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无参与人物</Text>
                  )}
                </Card>
              </Col>
              <Col span={12}>
                <Card title="相关剧情" size="small">
                  {viewingEvent.relatedPlots && viewingEvent.relatedPlots.length > 0 ? (
                    <Space wrap>
                      {viewingEvent.relatedPlots.map((plot, index) => (
                        <Tag key={index} color="green">{plot}</Tag>
                      ))}
                    </Space>
                  ) : (
                    <Text type="secondary">暂无相关剧情</Text>
                  )}
                </Card>
              </Col>
            </Row>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Timeline;