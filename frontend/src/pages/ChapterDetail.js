import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Typography,
  Button,
  Form,
  Input,
  Select,
  message,
  Space,
  Tag,
  Row,
  Col,
  Statistic,
  Divider,
  Breadcrumb
} from 'antd';
import {
  SaveOutlined,
  ArrowLeftOutlined,
  FileTextOutlined,
  RobotOutlined,
  EyeOutlined,
  EditOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const ChapterDetail = () => {
  const { projectId, volumeId, chapterId } = useParams();
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [chapter, setChapter] = useState(null);
  const [volume, setVolume] = useState(null);
  const [editMode, setEditMode] = useState(false);

  // 状态配置
  const statusConfig = {
    planning: { color: 'blue', text: '规划中' },
    draft: { color: 'orange', text: '草稿' },
    writing: { color: 'processing', text: '写作中' },
    completed: { color: 'green', text: '已完成' },
    published: { color: 'success', text: '已发布' }
  };

  // 模拟数据
  useEffect(() => {
    // 模拟获取章节数据
    const mockChapter = {
      id: parseInt(chapterId),
      volumeId: parseInt(volumeId),
      title: '第一章：觉醒',
      chapterNumber: 1,
      content: `在这个充满灵气的世界里，少年林天踏上了修仙之路...

这是一个神奇的世界，天地间充满了灵气，修炼者可以通过吸收灵气来提升自己的实力。

林天从小就对修炼充满了向往，今天终于有机会踏上这条道路。

师父告诉他："修炼之路虽然艰难，但只要有恒心，终能成就大道。"

林天点了点头，眼中闪烁着坚定的光芒。`,
      outline: '主角初次接触修仙世界，遇到第一位师父，开始修炼之路',
      summary: '林天踏上修仙之路，遇到师父，开始修炼',
      wordCount: 156,
      status: 'completed',
      notes: '这一章主要是世界观的介绍和主角的出场',
      createdAt: '2024-01-15',
      updatedAt: '2024-01-16'
    };

    const mockVolume = {
      id: parseInt(volumeId),
      title: '第一卷：初入修仙界',
      volumeNumber: 1
    };

    setChapter(mockChapter);
    setVolume(mockVolume);
    form.setFieldsValue(mockChapter);
  }, [chapterId, volumeId, form]);

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      // 计算字数
      const wordCount = values.content ? values.content.replace(/\s/g, '').length : 0;
      
      const updatedChapter = {
        ...chapter,
        ...values,
        wordCount,
        updatedAt: new Date().toISOString().split('T')[0]
      };

      setChapter(updatedChapter);
      setEditMode(false);
      message.success('章节保存成功');
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAIContinue = () => {
    message.info('AI续写功能开发中...');
  };

  const handleBack = () => {
    navigate(`/projects/${projectId}/volumes`);
  };

  if (!chapter || !volume) {
    return <div>加载中...</div>;
  }

  return (
    <div className="fade-in">
      {/* 面包屑导航 */}
      <Breadcrumb style={{ marginBottom: 16 }}>
        <Breadcrumb.Item>
          <Button type="link" onClick={handleBack} style={{ padding: 0 }}>
            卷宗管理
          </Button>
        </Breadcrumb.Item>
        <Breadcrumb.Item>{volume.title}</Breadcrumb.Item>
        <Breadcrumb.Item>{chapter.title}</Breadcrumb.Item>
      </Breadcrumb>

      <div className="page-header">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <Title level={2} className="page-title">
              <Space>
                <Button 
                  type="text" 
                  icon={<ArrowLeftOutlined />} 
                  onClick={handleBack}
                />
                {chapter.title}
                <Tag color={statusConfig[chapter.status].color}>
                  {statusConfig[chapter.status].text}
                </Tag>
              </Space>
            </Title>
            <Text type="secondary">
              {volume.title} - 第{chapter.chapterNumber}章
            </Text>
          </div>
          <Space>
            {editMode ? (
              <>
                <Button onClick={() => setEditMode(false)}>取消</Button>
                <Button 
                  type="primary" 
                  icon={<SaveOutlined />}
                  loading={loading}
                  onClick={handleSave}
                >
                  保存
                </Button>
              </>
            ) : (
              <>
                <Button 
                  icon={<RobotOutlined />}
                  onClick={handleAIContinue}
                >
                  AI续写
                </Button>
                <Button 
                  type="primary"
                  icon={<EditOutlined />}
                  onClick={() => setEditMode(true)}
                >
                  编辑
                </Button>
              </>
            )}
          </Space>
        </div>
      </div>

      {/* 统计信息 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="字数"
              value={chapter.wordCount}
              suffix="字"
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="章节序号"
              value={chapter.chapterNumber}
              prefix={<EyeOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="创建时间"
              value={chapter.createdAt}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="更新时间"
              value={chapter.updatedAt}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        {/* 章节内容 */}
        <Col span={16}>
          <Card title="章节内容">
            <Form form={form} layout="vertical">
              <Form.Item
                name="title"
                label="章节标题"
                rules={[{ required: true, message: '请输入章节标题' }]}
              >
                <Input 
                  placeholder="请输入章节标题" 
                  disabled={!editMode}
                />
              </Form.Item>

              <Form.Item
                name="content"
                label="正文内容"
              >
                <TextArea
                  rows={20}
                  placeholder="开始写作..."
                  disabled={!editMode}
                  showCount
                />
              </Form.Item>

              <Form.Item
                name="notes"
                label="作者备注"
              >
                <TextArea
                  rows={3}
                  placeholder="记录创作思路、待修改内容等..."
                  disabled={!editMode}
                />
              </Form.Item>
            </Form>
          </Card>
        </Col>

        {/* 章节信息 */}
        <Col span={8}>
          <Card title="章节信息" style={{ marginBottom: 16 }}>
            <Form form={form} layout="vertical">
              <Form.Item
                name="chapterNumber"
                label="章节序号"
                rules={[{ required: true, message: '请输入章节序号' }]}
              >
                <Input 
                  type="number" 
                  placeholder="1" 
                  disabled={!editMode}
                />
              </Form.Item>

              <Form.Item
                name="status"
                label="状态"
                rules={[{ required: true, message: '请选择章节状态' }]}
              >
                <Select disabled={!editMode}>
                  {Object.entries(statusConfig).map(([key, config]) => (
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
                  disabled={!editMode}
                />
              </Form.Item>

              <Form.Item
                name="summary"
                label="章节摘要"
              >
                <TextArea
                  rows={3}
                  placeholder="一句话总结本章内容"
                  disabled={!editMode}
                />
              </Form.Item>
            </Form>
          </Card>

          {/* 写作提示 */}
          <Card title="写作提示" size="small">
            <div style={{ fontSize: '12px', color: '#666' }}>
              <p>• 建议每章字数控制在2000-5000字</p>
              <p>• 注意情节的连贯性和节奏感</p>
              <p>• 可以使用AI续写功能辅助创作</p>
              <p>• 及时保存避免内容丢失</p>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ChapterDetail;
