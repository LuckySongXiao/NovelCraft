import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card,
  Button,
  Typography,
  Row,
  Col,
  Collapse
} from 'antd';
import {
  CaretRightOutlined,
  SettingOutlined,
  GlobalOutlined,
  ThunderboltOutlined,
  CrownOutlined,
  DollarOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Panel } = Collapse;

const SettingsManagement = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    // 可以在这里加载设定数据
  }, [id]);

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <SettingOutlined style={{ marginRight: '8px' }} />
          设定管理
        </Title>
        <Text type="secondary">管理小说的世界观、体系设定和规则</Text>
      </div>

      <Collapse
        defaultActiveKey={['world', 'power', 'society', 'economy']}
        expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
        ghost
      >
        <Panel header="世界观与基础设定" key="world" extra={<GlobalOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="世界设定"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/world-settings`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>世界观设定</Text>
                <br />
                <Text type="secondary">地理、历史、文化</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="地图结构"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/map-structures`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>地图结构</Text>
                <br />
                <Text type="secondary">地图、地形、区域</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="维度结构"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/dimension-structures`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>维度结构</Text>
                <br />
                <Text type="secondary">维度、法则、传送</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="种族类别"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/race-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>种族类别</Text>
                <br />
                <Text type="secondary">种族、特性、关系</Text>
              </Card>
            </Col>
          </Row>
        </Panel>

        <Panel header="力量与战斗体系" key="power" extra={<ThunderboltOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="修炼体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/cultivation-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>修炼体系</Text>
                <br />
                <Text type="secondary">能力、等级、方法</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="功法体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/martial-arts-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>功法体系</Text>
                <br />
                <Text type="secondary">功法、招式、传承</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="装备体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/equipment-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>装备体系</Text>
                <br />
                <Text type="secondary">装备、强化、套装</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="灵宝体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/spiritual-treasure-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>灵宝体系</Text>
                <br />
                <Text type="secondary">灵宝、器灵、炼制</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="宠物体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/pet-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>宠物体系</Text>
                <br />
                <Text type="secondary">宠物、进化、培养</Text>
              </Card>
            </Col>
          </Row>
        </Panel>

        <Panel header="社会与政治体系" key="society" extra={<CrownOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="政治体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/political-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>政治体系</Text>
                <br />
                <Text type="secondary">政府、法律、权力</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="司法体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/judicial-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>司法体系</Text>
                <br />
                <Text type="secondary">法院、执法、审判</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="生民体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/civilian-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>生民体系</Text>
                <br />
                <Text type="secondary">人口、社会、生活</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="职业体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/profession-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>职业体系</Text>
                <br />
                <Text type="secondary">职业、技能、组织</Text>
              </Card>
            </Col>
          </Row>
        </Panel>

        <Panel header="经济与商业体系" key="economy" extra={<DollarOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="货币体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/currency-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>货币体系</Text>
                <br />
                <Text type="secondary">货币、金融、经济</Text>
              </Card>
            </Col>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="商业体系"
                extra={<Button type="link">查看全部</Button>}
                onClick={() => navigate(`/projects/${id}/commerce-systems`)}
                style={{ cursor: 'pointer' }}
              >
                <Text>商业体系</Text>
                <br />
                <Text type="secondary">贸易、商会、市场</Text>
              </Card>
            </Col>
          </Row>
        </Panel>
      </Collapse>
    </div>
  );
};

export default SettingsManagement;
