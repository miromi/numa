import api from './api';

// 获取方案列表
export const getSolutions = (params = {}) => {
  return api.get('/v1/solutions/', { params });
};

// 获取单个方案
export const getSolution = (id) => {
  return api.get(`/v1/solutions/${id}`);
};

// 创建方案
export const createSolution = (data) => {
  return api.post('/v1/solutions/', data);
};

// 更新方案
export const updateSolution = (id, data) => {
  return api.put(`/v1/solutions/${id}`, data);
};

// 删除方案
export const deleteSolution = (id) => {
  return api.delete(`/v1/solutions/${id}`);
};