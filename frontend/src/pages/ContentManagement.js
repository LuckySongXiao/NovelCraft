import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Button,
  Typography,
  Row,
  Col,
  Statistic,
  Collapse
} from 'antd';
import {
  CaretRightOutlined,
  UserOutlined,
  BookOutlined,
  GlobalOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Panel } = Collapse;

const ContentManagement = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // 模拟项目数据
  const mockProject = {
    characterCount: 25,
    factionCount: 8,
    plotCount: 12,
    resourceCount: 15,
    raceCount: 6,
    secretRealmCount: 4
  };

  useEffect(() => {
    // 可以在这里加载项目统计数据
  }, [id]);

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <BookOutlined style={{ marginRight: '8px' }} />
          内容管理
        </Title>
        <Text type="secondary">管理小说的角色、势力、剧情和世界分布</Text>
      </div>

      <Collapse
        defaultActiveKey={['characters', 'distribution']}
        expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
        ghost
      >
        <Panel header="角色与势力管理" key="characters" extra={<UserOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="人物管理"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/characters`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.characterCount} suffix="个人物" />
                <Text type="secondary">管理角色档案</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="势力管理"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/factions`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.factionCount} suffix="个势力" />
                <Text type="secondary">管理势力组织</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="剧情管理"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/plots`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.plotCount} suffix="个剧情" />
                <Text type="secondary">管理剧情线索</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="关系网络"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/relations`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.relationCount || 18} suffix="个关系" />
                <Text type="secondary">管理人物关系</Text>
              </Card>
            </Col>
          </Row>
        </Panel>

        <Panel header="世界分布管理" key="distribution" extra={<GlobalOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="资源分布"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/resource-distribution`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.resourceCount} suffix="个资源点" />
                <Text type="secondary">管理资源分布</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="种族分布"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/race-distribution`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.raceCount} suffix="个种族区域" />
                <Text type="secondary">管理种族分布</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="秘境分布"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/secret-realms`)}
                style={{ cursor: 'pointer' }}
              >
                <Statistic value={mockProject.secretRealmCount} suffix="个秘境" />
                <Text type="secondary">管理秘境分布</Text>
              </Card>
            </Col>
          </Row>
        </Panel>
      </Collapse>
    </div>
  );
};

export default ContentManagement;
