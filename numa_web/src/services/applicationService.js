import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// 获取所有应用
export const getApplications = () => {
  return axios.get(`${API_BASE_URL}/applications/`);
};

// 获取单个应用
export const getApplication = (id) => {
  return axios.get(`${API_BASE_URL}/applications/${id}`);
};

// 创建新应用
export const createApplication = (applicationData) => {
  return axios.post(`${API_BASE_URL}/applications/`, applicationData);
};

// 更新应用状态
export const updateApplicationStatus = (id, status) => {
  return axios.patch(`${API_BASE_URL}/applications/${id}/status`, { status });
};