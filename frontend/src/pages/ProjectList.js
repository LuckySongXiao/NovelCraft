import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  Button,
  Space,
  Tag,
  Progress,
  Modal,
  Form,
  Input,
  Select,
  message,
  Popconfirm,
  Typography,
  Row,
  Col
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  CopyOutlined,
  ExportOutlined,
  ImportOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { projectAPI } from '../utils/api';

const { Title } = Typography;
const { Option } = Select;
const { TextArea } = Input;

const ProjectList = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [form] = Form.useForm();



  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const response = await projectAPI.getProjects();
      const projectsData = response.data.projects || [];

      // 格式化项目数据
      const formattedProjects = projectsData.map(project => ({
        id: project.id,
        name: project.name,
        title: project.title,
        author: project.author,
        type: project.project_type,
        status: project.status,
        summary: project.summary,
        wordCount: project.word_count || 0,
        chapterCount: project.chapter_count || 0,
        characterCount: project.character_count || 0,
        progress: project.progress?.completion_rate || 0,
        createdAt: new Date(project.created_at).toLocaleDateString(),
        updatedAt: new Date(project.updated_at).toLocaleDateString(),
        isPreset: project.is_preset || false
      }));

      setProjects(formattedProjects);
    } catch (error) {
      console.error('加载项目列表失败:', error);
      message.error('加载项目列表失败');
    } finally {
      setLoading(false);
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

  const handleCreate = () => {
    setEditingProject(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    form.setFieldsValue(project);
    setModalVisible(true);
  };

  const handleDelete = async (id) => {
    try {
      // 调用后端API删除项目
      await projectAPI.deleteProject(id);

      // 删除成功后重新加载项目列表
      message.success('项目删除成功');
      loadProjects();
    } catch (error) {
      console.error('删除项目失败:', error);
      message.error(error.response?.data?.detail || '删除项目失败');
    }
  };

  const handleSubmit = async (values) => {
    try {
      if (editingProject) {
        // 更新项目
        await projectAPI.updateProject(editingProject.id, {
          ...values,
          project_type: values.type
        });
        message.success('项目更新成功');
      } else {
        // 创建项目
        await projectAPI.createProject({
          ...values,
          project_type: values.type
        });
        message.success('项目创建成功');
      }
      setModalVisible(false);
      loadProjects(); // 重新加载项目列表
    } catch (error) {
      console.error('操作失败:', error);
      message.error(error.response?.data?.detail || '操作失败');
    }
  };

  const handleDuplicate = async (project) => {
    try {
      await projectAPI.duplicateProject(project.id, `${project.name} (副本)`);
      message.success('项目复制成功');
      loadProjects(); // 重新加载项目列表
    } catch (error) {
      console.error('复制项目失败:', error);
      message.error(error.response?.data?.detail || '复制项目失败');
    }
  };

  const columns = [
    {
      title: '项目名称',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <div>
          <div style={{ fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '8px' }}>
            {text}
            {record.isPreset && (
              <Tag color="blue" size="small">预置</Tag>
            )}
          </div>
          {record.title && (
            <div style={{ fontSize: '12px', color: '#666' }}>{record.title}</div>
          )}
        </div>
      ),
    },
    {
      title: '作者',
      dataIndex: 'author',
      key: 'author',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type) => <Tag>{getTypeText(type)}</Tag>,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>{getStatusText(status)}</Tag>
      ),
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
    },
    {
      title: '统计',
      key: 'stats',
      render: (_, record) => (
        <div style={{ fontSize: '12px' }}>
          <div>字数: {(record.wordCount / 10000).toFixed(1)}万</div>
          <div>章节: {record.chapterCount}</div>
          <div>人物: {record.characterCount}</div>
        </div>
      ),
    },
    {
      title: '最后修改',
      dataIndex: 'updatedAt',
      key: 'updatedAt',
    },
    {
      title: '操作',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => navigate(`/projects/${record.id}`)}
          >
            查看
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Button
            type="link"
            icon={<CopyOutlined />}
            onClick={() => handleDuplicate(record)}
          >
            复制
          </Button>
          <Popconfirm
            title="确定要删除这个项目吗？"
            onConfirm={() => handleDelete(record.id)}
            okText="确定"
            cancelText="取消"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div className="fade-in">
      <div className="page-header">
        <Title level={2} className="page-title">项目管理</Title>
      </div>

      <Card>
        <div className="toolbar">
          <div className="toolbar-left">
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleCreate}
            >
              新建项目
            </Button>
          </div>
          <div className="toolbar-right">
            <Space>
              <Button icon={<ImportOutlined />}>导入项目</Button>
              <Button icon={<ExportOutlined />}>导出项目</Button>
            </Space>
          </div>
        </div>

        <Table
          columns={columns}
          dataSource={projects}
          rowKey="id"
          loading={loading}
          pagination={{
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个项目`,
          }}
        />
      </Card>

      <Modal
        title={editingProject ? '编辑项目' : '新建项目'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        onOk={() => form.submit()}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
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
                name="type"
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

          <Form.Item
            name="summary"
            label="项目简介"
          >
            <TextArea
              rows={4}
              placeholder="请输入项目简介"
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ProjectList;
