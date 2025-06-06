import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, List, Button, Progress, Tag, Space, Typography, message, Spin } from 'antd';
import {
  ProjectOutlined,
  UserOutlined,
  BookOutlined,
  FileTextOutlined,
  PlusOutlined,
  EditOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { projectAPI } from '../utils/api';

const { Title, Text } = Typography;

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalProjects: 0,
    totalCharacters: 0,
    totalVolumes: 0,
    totalWords: 0
  });

  const [recentProjects, setRecentProjects] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);

  // 获取仪表盘数据
  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      // 获取项目列表
      const projectsResponse = await projectAPI.getProjects({ limit: 5 });
      const projects = projectsResponse.data.projects || [];

      // 计算统计数据
      const totalProjects = projectsResponse.data.total || 0;
      let totalCharacters = 0;
      let totalVolumes = 0;
      let totalWords = 0;

      // 为每个项目获取详细统计
      for (const project of projects) {
        totalCharacters += project.character_count || 0;
        totalVolumes += project.volume_count || 0;
        totalWords += project.word_count || 0;
      }

      setStats({
        totalProjects,
        totalCharacters,
        totalVolumes,
        totalWords
      });

      // 设置最近项目（格式化数据）
      const formattedProjects = projects.map(project => ({
        id: project.id,
        name: project.name,
        type: project.project_type,
        status: project.status,
        progress: project.progress?.completion_percentage || 0,
        lastModified: new Date(project.updated_at).toLocaleDateString(),
        wordCount: project.word_count || 0
      }));

      setRecentProjects(formattedProjects);

      // 生成最近活动（基于项目更新时间）
      const activities = projects.slice(0, 4).map((project, index) => ({
        id: index + 1,
        type: 'project',
        action: '更新了项目',
        target: project.name,
        project: '',
        time: getRelativeTime(project.updated_at)
      }));

      setRecentActivities(activities);

    } catch (error) {
      console.error('获取仪表盘数据失败:', error);
      message.error('获取仪表盘数据失败');
    } finally {
      setLoading(false);
    }
  };

  // 计算相对时间
  const getRelativeTime = (dateString) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffMs = now - date;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return `${diffDays}天前`;
    } else if (diffHours > 0) {
      return `${diffHours}小时前`;
    } else {
      return '刚刚';
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

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

  const getActivityIcon = (type) => {
    const icons = {
      project: <ProjectOutlined />,
      character: <UserOutlined />,
      chapter: <FileTextOutlined />,
      plot: <BookOutlined />
    };
    return icons[type] || <EditOutlined />;
  };

  if (loading) {
    return (
      <div className="fade-in" style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text>正在加载仪表盘数据...</Text>
        </div>
      </div>
    );
  }

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">仪表盘</Title>
        <Text className="page-description">欢迎回来！查看您的创作概况和最近活动。</Text>
      </div>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} className="stats-grid">
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="项目总数"
              value={stats.totalProjects}
              prefix={<ProjectOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="人物总数"
              value={stats.totalCharacters}
              prefix={<UserOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="卷宗总数"
              value={stats.totalVolumes}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="总字数"
              value={stats.totalWords}
              prefix={<BookOutlined />}
              valueStyle={{ color: '#fa8c16' }}
              formatter={(value) => `${(value / 10000).toFixed(1)}万`}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        {/* 最近项目 */}
        <Col xs={24} lg={14}>
          <Card
            title="最近项目"
            extra={
              <Button
                type="primary"
                icon={<PlusOutlined />}
                onClick={() => navigate('/projects')}
              >
                新建项目
              </Button>
            }
          >
            <List
              dataSource={recentProjects}
              renderItem={(project) => (
                <List.Item
                  actions={[
                    <Button
                      type="link"
                      onClick={() => navigate(`/projects/${project.id}`)}
                    >
                      查看详情
                    </Button>
                  ]}
                >
                  <List.Item.Meta
                    title={
                      <Space>
                        <span>{project.name}</span>
                        <Tag color={getStatusColor(project.status)}>
                          {getStatusText(project.status)}
                        </Tag>
                        <Tag>{getTypeText(project.type)}</Tag>
                      </Space>
                    }
                    description={
                      <Space direction="vertical" style={{ width: '100%' }}>
                        <div>
                          <Text type="secondary">
                            字数: {(project.wordCount / 10000).toFixed(1)}万 |
                            最后修改: {project.lastModified}
                          </Text>
                        </div>
                        <Progress
                          percent={project.progress}
                          size="small"
                          status={project.progress === 100 ? 'success' : 'active'}
                        />
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>

        {/* 最近活动 */}
        <Col xs={24} lg={10}>
          <Card title="最近活动">
            <List
              dataSource={recentActivities}
              renderItem={(activity) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={getActivityIcon(activity.type)}
                    title={
                      <Space>
                        <span>{activity.action}</span>
                        <Text strong>{activity.target}</Text>
                      </Space>
                    }
                    description={
                      <Space>
                        {activity.project && (
                          <Text type="secondary">项目: {activity.project}</Text>
                        )}
                        <Text type="secondary">
                          <ClockCircleOutlined /> {activity.time}
                        </Text>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      {/* 快速操作 */}
      <Card title="快速操作" style={{ marginTop: 24 }}>
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={12} md={6}>
            <Button
              type="dashed"
              block
              size="large"
              icon={<ProjectOutlined />}
              onClick={() => navigate('/projects')}
            >
              创建新项目
            </Button>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Button
              type="dashed"
              block
              size="large"
              icon={<UserOutlined />}
              onClick={() => navigate('/characters')}
            >
              添加人物
            </Button>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Button
              type="dashed"
              block
              size="large"
              icon={<FileTextOutlined />}
              onClick={() => navigate('/volumes')}
            >
              管理卷宗
            </Button>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Button
              type="dashed"
              block
              size="large"
              icon={<BookOutlined />}
              onClick={() => navigate('/ai-assistant')}
            >
              AI助手
            </Button>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Dashboard;
