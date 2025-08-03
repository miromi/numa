import api from './api';

// 获取用户列表
export const getUsers = (params = {}) => {
  return api.get('/v1/users/', { params });
};

// 获取单个用户
export const getUser = (id) => {
  return api.get(`/v1/users/${id}`);
};

// 创建用户
export const createUser = (data) => {
  return api.post('/v1/users/', data);
};

// 更新用户
export const updateUser = (id, data) => {
  return api.put(`/v1/users/${id}`, data);
};

// 删除用户
export const deleteUser = (id) => {
  return api.delete(`/v1/users/${id}`);
};