import React, { useState, useEffect } from 'react';
import { Layout as AntLayout, Menu, Avatar, Dropdown, Button, Space } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  ProjectOutlined,
  UserOutlined,
  BookOutlined,
  RobotOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  LogoutOutlined,
  BellOutlined,
  FolderOutlined,
  DatabaseOutlined,
  ControlOutlined,
  EyeOutlined
} from '@ant-design/icons';
import { projectAPI } from '../utils/api';

const { Header, Sider, Content } = AntLayout;

const Layout = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const [projects, setProjects] = useState([]);
  const [, setLoading] = useState(false);
  const [openKeys, setOpenKeys] = useState(['project-management']);
  const navigate = useNavigate();
  const location = useLocation();

  // 获取当前项目ID（如果在项目页面中）
  const getProjectId = () => {
    const pathParts = location.pathname.split('/');
    if (pathParts[1] === 'projects' && pathParts[2]) {
      return pathParts[2];
    }
    return null;
  };

  const projectId = getProjectId();

  // 加载项目列表
  useEffect(() => {
    loadProjects();
  }, []);

  // 监听路径变化，如果在项目页面则重新加载项目列表
  useEffect(() => {
    if (location.pathname.includes('/projects')) {
      loadProjects();
    }
  }, [location.pathname]);

  // 监听路径变化，更新菜单展开状态
  useEffect(() => {
    const pathname = location.pathname;
    const newOpenKeys = ['project-management'];

    // 如果在项目页面，展开对应的项目菜单
    if (pathname.startsWith('/projects/') && projectId) {
      newOpenKeys.push(`project-${projectId}`);

      // 如果在工具相关页面，展开工具菜单
      if (pathname.includes('/tools') ||
          pathname.includes('/ai-assistant') ||
          pathname.includes('/ai-test') ||
          pathname.includes('/settings')) {
        newOpenKeys.push(`project-${projectId}-tools`);
      }
    }

    setOpenKeys(newOpenKeys);
  }, [location.pathname, projectId]);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const response = await projectAPI.getProjects();
      const projectsData = response.data.projects || [];

      setProjects(projectsData);
    } catch (error) {
      console.error('加载项目列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  // 构建项目子菜单
  const buildProjectSubMenu = (project) => [
    {
      key: `/projects/${project.id}`,
      icon: <EyeOutlined />,
      label: '项目概览',
    },
    {
      key: `/projects/${project.id}/volumes`,
      icon: <FolderOutlined />,
      label: '卷宗管理',
    },
    {
      key: `/projects/${project.id}/content`,
      icon: <DatabaseOutlined />,
      label: '内容管理',
    },
    {
      key: `/projects/${project.id}/settings`,
      icon: <ControlOutlined />,
      label: '设定管理',
    },
    {
      key: `project-${project.id}-tools`,
      icon: <RobotOutlined />,
      label: '工具',
      children: [
        {
          key: `/ai-assistant?project=${project.id}`,
          icon: <RobotOutlined />,
          label: 'Agent-AI助手',
        },
        {
          key: `/ai-test?project=${project.id}`,
          icon: <RobotOutlined />,
          label: 'Agent-AI测试',
        },
        {
          key: `/settings?project=${project.id}`,
          icon: <SettingOutlined />,
          label: '系统设置',
        },
      ],
    },
  ];

  // 主菜单项
  const mainMenuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: 'project-management',
      icon: <ProjectOutlined />,
      label: '项目管理',
      children: [
        {
          key: '/projects',
          icon: <ProjectOutlined />,
          label: '项目列表',
        },
        ...projects.map(project => ({
          key: `project-${project.id}`,
          icon: <BookOutlined />,
          label: project.name,
          children: buildProjectSubMenu(project),
        })),
      ],
    },
  ];



  // 获取当前选中的菜单key
  const getSelectedKeys = () => {
    const pathname = location.pathname;

    // 如果是项目相关页面，返回具体的路径
    if (pathname.startsWith('/projects/')) {
      return [pathname];
    }

    // 其他页面直接返回路径
    return [pathname];
  };



  // 用户菜单
  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人资料',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '偏好设置',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
    },
  ];

  const handleMenuClick = ({ key }) => {
    // 如果是项目管理、项目分组或工具分组的key，不进行导航
    if (key === 'project-management' ||
        (key.startsWith('project-') && key.endsWith('-tools')) ||
        (key.startsWith('project-') && !key.includes('/'))) {
      return;
    }
    navigate(key);
  };

  // 处理菜单展开/折叠
  const handleOpenChange = (keys) => {
    setOpenKeys(keys);
  };

  const handleUserMenuClick = ({ key }) => {
    switch (key) {
      case 'profile':
        navigate('/profile');
        break;
      case 'settings':
        navigate('/settings');
        break;
      case 'logout':
        // 处理退出登录
        console.log('退出登录');
        break;
      default:
        break;
    }
  };

  return (
    <AntLayout className="layout-container">
      <Header className="layout-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{ marginRight: 16 }}
            />
            <h1 style={{ margin: 0, color: '#1890ff', fontSize: '20px', fontWeight: 'bold' }}>
              NovelCraft
            </h1>
          </div>

          <Space>
            <Button type="text" icon={<BellOutlined />} />
            <Dropdown
              menu={{
                items: userMenuItems,
                onClick: handleUserMenuClick,
              }}
              placement="bottomRight"
            >
              <Space style={{ cursor: 'pointer' }}>
                <Avatar icon={<UserOutlined />} />
                <span>用户</span>
              </Space>
            </Dropdown>
          </Space>
        </div>
      </Header>

      <AntLayout className="layout-content">
        <Sider
          className="layout-sider"
          collapsed={collapsed}
          width={240}
          collapsedWidth={80}
          theme="light"
        >
          <div style={{ height: '100%', overflowY: 'auto' }}>
            {/* 主菜单 */}
            <Menu
              mode="inline"
              selectedKeys={getSelectedKeys()}
              items={mainMenuItems}
              onClick={handleMenuClick}
              onOpenChange={handleOpenChange}
              style={{ borderRight: 0 }}
              openKeys={openKeys}
            />
          </div>
        </Sider>

        <Content className="layout-main">
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
