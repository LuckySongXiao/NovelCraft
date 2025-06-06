/**
 * API 配置和工具函数
 */
import axios from 'axios';
import { message } from 'antd';

// 创建axios实例
const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 对响应数据做点什么
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    // 对响应错误做点什么
    console.error('Response Error:', error);
    
    if (error.response) {
      // 服务器响应了错误状态码
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          message.error(data.detail || '请求参数错误');
          break;
        case 401:
          message.error('未授权访问');
          break;
        case 403:
          message.error('禁止访问');
          break;
        case 404:
          message.error('资源不存在');
          break;
        case 500:
          message.error('服务器内部错误');
          break;
        default:
          message.error(data.detail || '请求失败');
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      message.error('网络连接失败，请检查网络设置');
    } else {
      // 其他错误
      message.error('请求配置错误');
    }
    
    return Promise.reject(error);
  }
);

// API方法
export const projectAPI = {
  // 获取项目列表
  getProjects: (params = {}) => api.get('/projects', { params }),
  
  // 获取项目详情
  getProject: (id) => api.get(`/projects/${id}`),
  
  // 创建项目
  createProject: (data) => api.post('/projects', data),
  
  // 更新项目
  updateProject: (id, data) => api.put(`/projects/${id}`, data),
  
  // 删除项目
  deleteProject: (id) => api.delete(`/projects/${id}`),
  
  // 复制项目
  duplicateProject: (id, newName) => api.post(`/projects/${id}/duplicate`, null, {
    params: { new_name: newName }
  }),
  
  // 导出项目
  exportProject: (id, format = 'json') => api.post(`/projects/${id}/export`, { format }),
  
  // 获取项目统计
  getProjectStatistics: (id) => api.get(`/projects/${id}/statistics`),
};

export const projectDataAPI = {
  // 获取项目数据
  getProjectData: (projectId, modelName = null) => {
    const params = modelName ? { model_name: modelName } : {};
    return api.get(`/project-data/projects/${projectId}/data`, { params });
  },
  
  // 创建项目数据
  createProjectData: (projectId, modelName, data) => 
    api.post(`/project-data/projects/${projectId}/data/${modelName}`, data),
  
  // 更新项目数据
  updateProjectData: (projectId, modelName, itemId, data) => 
    api.put(`/project-data/projects/${projectId}/data/${modelName}/${itemId}`, data),
  
  // 删除项目数据
  deleteProjectData: (projectId, modelName, itemId) => 
    api.delete(`/project-data/projects/${projectId}/data/${modelName}/${itemId}`),
};

export const aiAPI = {
  // 获取AI提供商列表
  getProviders: () => api.get('/ai/providers'),
  
  // 获取AI状态
  getStatus: () => api.get('/ai/status'),
  
  // 获取AI配置
  getConfig: (provider) => api.get(`/ai/config/${provider}`),
  
  // 保存AI配置
  saveConfig: (data) => api.post('/ai/config', data),
  
  // AI对话
  chat: (data) => api.post('/ai/chat', data),
  
  // 获取Ollama模型列表
  getOllamaModels: () => api.get('/ai/ollama/models'),
};

export default api;
