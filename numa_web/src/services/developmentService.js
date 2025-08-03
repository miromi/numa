import api from './api';

// 获取开发任务列表
export const getDevelopmentTasks = (params = {}) => {
  return api.get('/v1/development/', { params });
};

// 获取单个开发任务
export const getDevelopmentTask = (id) => {
  return api.get(`/v1/development/${id}`);
};

// 创建开发任务
export const createDevelopmentTask = (data) => {
  return api.post('/v1/development/', data);
};

// 更新开发任务
export const updateDevelopmentTask = (id, data) => {
  return api.put(`/v1/development/${id}`, data);
};

// 删除开发任务
export const deleteDevelopmentTask = (id) => {
  return api.delete(`/v1/development/${id}`);
};