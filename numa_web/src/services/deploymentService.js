import api from './api';

// 获取部署记录列表
export const getDeployments = (params = {}) => {
  return api.get('/v1/deployment/', { params });
};

// 获取单个部署记录
export const getDeployment = (id) => {
  return api.get(`/v1/deployment/${id}`);
};

// 创建部署记录
export const createDeployment = (data) => {
  return api.post('/v1/deployment/', data);
};

// 更新部署记录
export const updateDeployment = (id, data) => {
  return api.put(`/v1/deployment/${id}`, data);
};

// 删除部署记录
export const deleteDeployment = (id) => {
  return api.delete(`/v1/deployment/${id}`);
};