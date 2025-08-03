import axios from 'axios';

const API_BASE_URL = `${process.env.REACT_APP_API_BASE_URL}/v1`;

// 获取所有应用
export const getApplications = () => {
  return axios.get(`${API_BASE_URL}/applications/`);
};

// 获取单个应用
export const getApplication = (id) => {
  return axios.get(`${API_BASE_URL}/applications/${id}`);
};

// 根据app_id获取应用
export const getApplicationByAppId = (appId) => {
  return axios.get(`${API_BASE_URL}/applications/by_app_id/${appId}`);
};

// 创建新应用
export const createApplication = (applicationData) => {
  return axios.post(`${API_BASE_URL}/applications/`, applicationData);
};

// 更新应用状态
export const updateApplicationStatus = (id, status) => {
  return axios.patch(`${API_BASE_URL}/applications/${id}/status`, { status });
};