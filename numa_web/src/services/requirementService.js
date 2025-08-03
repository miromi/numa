import api from './api';

// 获取需求列表
export const getRequirements = (params = {}) => {
  return api.get('/v1/requirements/', { params });
};

// 获取单个需求
export const getRequirement = (id) => {
  return api.get(`/v1/requirements/${id}`);
};

// 创建需求
export const createRequirement = (data) => {
  return api.post('/v1/requirements/', data);
};

// 更新需求
export const updateRequirement = (id, data) => {
  return api.put(`/v1/requirements/${id}`, data);
};

// 删除需求
export const deleteRequirement = (id) => {
  return api.delete(`/v1/requirements/${id}`);
};