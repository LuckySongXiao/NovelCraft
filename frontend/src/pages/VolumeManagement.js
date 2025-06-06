import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Card,
  Button,
  Space,
  Typography,
  Row,
  Col,
  Progress,
  Tag,
  Descriptions,
  message,
  Collapse
} from 'antd';
import {
  EditOutlined,
  ExportOutlined,
  CaretRightOutlined,
  FileTextOutlined,
  BookOutlined,
  PlusOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Panel } = Collapse;

const VolumeManagement = () => {
  const { id } = useParams();
  const [loading, setLoading] = useState(false);
  const [volumes, setVolumes] = useState([]);

  // 模拟数据
  const mockVolumes = [
    {
      id: 1,
      title: '第一卷：初入江湖',
      description: '主角初入江湖的故事',
      chapterCount: 12,
      wordCount: 120000,
      status: '已完成',
      progress: 100
    },
    {
      id: 2,
      title: '第二卷：修炼之路',
      description: '主角踏上修炼之路',
      chapterCount: 8,
      wordCount: 80000,
      status: '进行中',
      progress: 60
    }
  ];

  const loadVolumes = async () => {
    setLoading(true);
    try {
      // 模拟API调用
      setTimeout(() => {
        setVolumes(mockVolumes);
        setLoading(false);
      }, 1000);
    } catch (error) {
      message.error('加载卷宗列表失败');
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVolumes();
  }, [id]);

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <Title level={2}>
          <FileTextOutlined style={{ marginRight: '8px' }} />
          卷宗管理
        </Title>
        <Text type="secondary">管理小说的卷宗和章节结构</Text>
      </div>

      <Collapse
        defaultActiveKey={['volumes', 'chapters']}
        expandIcon={({ isActive }) => <CaretRightOutlined rotate={isActive ? 90 : 0} />}
        ghost
      >
        <Panel header="卷宗列表" key="volumes" extra={<BookOutlined />}>
          <div style={{ marginBottom: '16px' }}>
            <Button type="primary" icon={<PlusOutlined />}>
              新建卷宗
            </Button>
          </div>

          <Row gutter={[16, 16]}>
            {mockVolumes.map(volume => (
              <Col xs={24} sm={12} md={8} key={volume.id}>
                <Card
                  title={volume.title}
                  extra={
                    <Space>
                      <Button type="link" icon={<EditOutlined />} size="small">
                        编辑
                      </Button>
                    </Space>
                  }
                  actions={[
                    <Button type="link" key="chapters">
                      章节管理
                    </Button>,
                    <Button type="link" key="export">
                      导出
                    </Button>
                  ]}
                >
                  <div style={{ marginBottom: '12px' }}>
                    <Text type="secondary">{volume.description}</Text>
                  </div>

                  <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text>章节数量：</Text>
                      <Text strong>{volume.chapterCount}</Text>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text>字数：</Text>
                      <Text strong>{volume.wordCount.toLocaleString()}</Text>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Text>状态：</Text>
                      <Tag color={volume.status === '已完成' ? 'green' : 'blue'}>
                        {volume.status}
                      </Tag>
                    </div>
                    <div>
                      <Text>进度：</Text>
                      <Progress
                        percent={volume.progress}
                        size="small"
                        style={{ marginTop: '4px' }}
                      />
                    </div>
                  </Space>
                </Card>
              </Col>
            ))}
          </Row>
        </Panel>

        <Panel header="章节管理" key="chapters" extra={<FileTextOutlined />}>
          <div style={{ marginBottom: '16px' }}>
            <Button type="primary" icon={<PlusOutlined />}>
              新建章节
            </Button>
          </div>

          <Card>
            <Descriptions title="章节统计" bordered column={3}>
              <Descriptions.Item label="总章节数">20</Descriptions.Item>
              <Descriptions.Item label="已完成">15</Descriptions.Item>
              <Descriptions.Item label="进行中">3</Descriptions.Item>
              <Descriptions.Item label="总字数">200,000</Descriptions.Item>
              <Descriptions.Item label="平均字数">10,000</Descriptions.Item>
              <Descriptions.Item label="完成度">75%</Descriptions.Item>
            </Descriptions>
          </Card>

          <div style={{ marginTop: '16px' }}>
            <Text type="secondary">
              章节详细管理功能正在开发中...
            </Text>
          </div>
        </Panel>

        <Panel header="导出与发布" key="export" extra={<ExportOutlined />}>
          <Row gutter={[16, 16]}>
            <Col xs={24} sm={12} md={8}>
              <Card
                title="导出格式"
                actions={[
                  <Button type="primary" key="export">导出</Button>
                ]}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Button block>导出为 TXT</Button>
                  <Button block>导出为 DOCX</Button>
                  <Button block>导出为 PDF</Button>
                  <Button block>导出为 EPUB</Button>
                </Space>
              </Card>
            </Col>

            <Col xs={24} sm={12} md={8}>
              <Card
                title="发布平台"
                actions={[
                  <Button type="primary" key="publish">发布</Button>
                ]}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Button block>起点中文网</Button>
                  <Button block>晋江文学城</Button>
                  <Button block>纵横中文网</Button>
                  <Button block>自定义平台</Button>
                </Space>
              </Card>
            </Col>

            <Col xs={24} sm={12} md={8}>
              <Card
                title="版本管理"
                actions={[
                  <Button type="primary" key="version">管理</Button>
                ]}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text>当前版本：</Text>
                    <Text strong>v1.2.0</Text>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Text>最后更新：</Text>
                    <Text>2024-01-15</Text>
                  </div>
                  <Button block>创建新版本</Button>
                  <Button block>版本历史</Button>
                </Space>
              </Card>
            </Col>
          </Row>
        </Panel>
      </Collapse>
    </div>
  );
};

export default VolumeManagement;
