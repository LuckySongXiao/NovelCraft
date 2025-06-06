import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Button,
  Space,
  Typography,
  Row,
  Col,
  Statistic,
  Progress,
  Tag,
  Descriptions,
  message,
  Modal,
  Form,
  Input,
  Select,
  Spin
} from 'antd';
import { projectAPI } from '../utils/api';
import {
  EditOutlined,
  SettingOutlined,
  ExportOutlined,
  BackwardOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editModalVisible, setEditModalVisible] = useState(false);
  const [form] = Form.useForm();

  const loadProject = useCallback(async () => {
    setLoading(true);
    try {
      const response = await projectAPI.getProject(id);
      const projectData = response.data;

      // 格式化项目数据
      const formattedProject = {
        ...projectData,
        createdAt: new Date(projectData.created_at).toLocaleDateString(),
        updatedAt: new Date(projectData.updated_at).toLocaleDateString(),
        wordCount: projectData.word_count || 0,
        chapterCount: projectData.chapter_count || 0,
        characterCount: projectData.character_count || 0,
        factionCount: projectData.faction_count || 0,
        volumeCount: projectData.volume_count || 0,
        progress: projectData.progress?.completion_percentage || 0,
        type: projectData.project_type,
        status: projectData.status
      };

      setProject(formattedProject);
    } catch (error) {
      console.error('加载项目详情失败:', error);
      message.error('加载项目详情失败');
      navigate('/projects');
    } finally {
      setLoading(false);
    }
  }, [id, navigate]);

  useEffect(() => {
    loadProject();
  }, [loadProject]);

  // 处理编辑项目
  const handleEdit = () => {
    form.setFieldsValue({
      name: project.name,
      title: project.title,
      author: project.author,
      project_type: project.type,
      status: project.status,
      summary: project.summary,
      description: project.description
    });
    setEditModalVisible(true);
  };

  // 提交编辑
  const handleEditSubmit = async (values) => {
    try {
      await projectAPI.updateProject(id, values);
      message.success('项目更新成功');
      setEditModalVisible(false);
      loadProject(); // 重新加载项目数据
    } catch (error) {
      console.error('更新项目失败:', error);
      message.error(error.response?.data?.detail || '更新项目失败');
    }
  };

  // 导出项目
  const handleExport = async () => {
    try {
      const response = await projectAPI.exportProject(id, 'json');
      message.success('项目导出成功');
      // 这里可以添加下载逻辑
    } catch (error) {
      console.error('导出项目失败:', error);
      message.error('导出项目失败');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      planning: 'blue',
      writing: 'green',
      reviewing: 'orange',
      completed: 'purple',
      published: 'gold'
    };
    return colors[status] || 'default';
  };

  const getStatusText = (status) => {
    const texts = {
      planning: '规划中',
      writing: '写作中',
      reviewing: '审阅中',
      completed: '已完成',
      published: '已发布'
    };
    return texts[status] || status;
  };

  const getTypeText = (type) => {
    const texts = {
      fantasy: '奇幻',
      xianxia: '仙侠',
      wuxia: '武侠',
      scifi: '科幻',
      modern: '现代',
      historical: '历史',
      romance: '言情'
    };
    return texts[type] || type;
  };

  if (loading) {
    return (
      <div className="fade-in" style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text>正在加载项目详情...</Text>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="fade-in" style={{ textAlign: 'center', padding: '50px' }}>
        <Text>项目不存在</Text>
      </div>
    );
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <Space>
          <Button
            icon={<BackwardOutlined />}
            onClick={() => navigate('/projects')}
          >
            返回项目列表
          </Button>
          <Title level={2} className="page-title">{project.name}</Title>
          <Tag color={getStatusColor(project.status)}>
            {getStatusText(project.status)}
          </Tag>
          <Tag>{getTypeText(project.type)}</Tag>
        </Space>

        <Space style={{ marginTop: 16 }}>
          <Button type="primary" icon={<EditOutlined />} onClick={handleEdit}>
            编辑项目
          </Button>
          <Button icon={<SettingOutlined />} onClick={() => navigate(`/projects/${id}/settings`)}>
            项目设置
          </Button>
          <Button icon={<ExportOutlined />} onClick={handleExport}>
            导出项目
          </Button>
        </Space>
      </div>

      {/* 项目统计 */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总字数"
              value={project.wordCount}
              formatter={(value) => `${(value / 10000).toFixed(1)}万`}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="章节数"
              value={project.chapterCount}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="人物数"
              value={project.characterCount}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="完成进度"
              value={project.progress}
              suffix="%"
              valueStyle={{ color: '#fa8c16' }}
            />
            <Progress
              percent={project.progress}
              size="small"
              status={project.progress === 100 ? 'success' : 'active'}
              style={{ marginTop: 8 }}
            />
          </Card>
        </Col>
      </Row>

      {/* 项目概览 */}
      <Card title="项目概览">
        <Descriptions bordered column={2}>
          <Descriptions.Item label="项目名称">{project.name}</Descriptions.Item>
          <Descriptions.Item label="小说标题">{project.title}</Descriptions.Item>
          <Descriptions.Item label="作者">{project.author}</Descriptions.Item>
          <Descriptions.Item label="项目类型">{getTypeText(project.type)}</Descriptions.Item>
          <Descriptions.Item label="创建时间">{project.createdAt}</Descriptions.Item>
          <Descriptions.Item label="最后修改">{project.updatedAt}</Descriptions.Item>
          <Descriptions.Item label="项目简介" span={2}>
            {project.summary}
          </Descriptions.Item>
          <Descriptions.Item label="详细描述" span={2}>
            {project.description}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      {/* 快速访问 */}
      <Card title="快速访问" style={{ marginTop: 24 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="卷宗管理"
              extra={<Button type="link">进入</Button>}
              onClick={() => navigate(`/projects/${id}/volumes`)}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Statistic value={project.volumeCount || 0} suffix="个卷宗" />
              <Text type="secondary">管理小说卷宗和章节</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="内容管理"
              extra={<Button type="link">进入</Button>}
              onClick={() => navigate(`/projects/${id}/content`)}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Statistic value={project.characterCount + project.factionCount} suffix="个内容项" />
              <Text type="secondary">管理角色、势力、剧情</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="设定管理"
              extra={<Button type="link">进入</Button>}
              onClick={() => navigate(`/projects/${id}/settings`)}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Text>体系设定</Text>
              <br />
              <Text type="secondary">管理世界观和各类体系</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="AI助手"
              extra={<Button type="link">使用</Button>}
              onClick={() => navigate('/ai-assistant')}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Text>AI辅助创作</Text>
              <br />
              <Text type="secondary">智能生成、续写、分析</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="时间线"
              extra={<Button type="link">查看</Button>}
              onClick={() => navigate(`/projects/${id}/timeline`)}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Text>项目时间线</Text>
              <br />
              <Text type="secondary">事件、发展、历史</Text>
            </Card>
          </Col>
          <Col xs={24} sm={12} md={8}>
            <Card
              title="关系网络"
              extra={<Button type="link">查看</Button>}
              onClick={() => navigate(`/projects/${id}/relations`)}
              style={{ cursor: 'pointer' }}
              hoverable
            >
              <Text>人物关系图谱</Text>
              <br />
              <Text type="secondary">人物、势力、关系</Text>
            </Card>
          </Col>
        </Row>
      </Card>

      {/* 编辑项目模态框 */}
      <Modal
        title="编辑项目"
        open={editModalVisible}
        onCancel={() => setEditModalVisible(false)}
        onOk={() => form.submit()}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleEditSubmit}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="项目名称"
                rules={[{ required: true, message: '请输入项目名称' }]}
              >
                <Input placeholder="请输入项目名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="title"
                label="小说标题"
              >
                <Input placeholder="请输入小说标题" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="author"
                label="作者"
              >
                <Input placeholder="请输入作者名称" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="project_type"
                label="项目类型"
                rules={[{ required: true, message: '请选择项目类型' }]}
              >
                <Select placeholder="请选择项目类型">
                  <Option value="fantasy">奇幻</Option>
                  <Option value="xianxia">仙侠</Option>
                  <Option value="wuxia">武侠</Option>
                  <Option value="scifi">科幻</Option>
                  <Option value="modern">现代</Option>
                  <Option value="historical">历史</Option>
                  <Option value="romance">言情</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={24}>
              <Form.Item
                name="status"
                label="项目状态"
              >
                <Select placeholder="请选择项目状态">
                  <Option value="planning">规划中</Option>
                  <Option value="writing">写作中</Option>
                  <Option value="reviewing">审阅中</Option>
                  <Option value="completed">已完成</Option>
                  <Option value="published">已发布</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="summary"
            label="项目简介"
          >
            <TextArea
              rows={3}
              placeholder="请输入项目简介"
            />
          </Form.Item>

          <Form.Item
            name="description"
            label="详细描述"
          >
            <TextArea
              rows={4}
              placeholder="请输入详细描述"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ProjectDetail;
