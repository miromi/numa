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

// 分配需求
export const assignRequirement = (id, assignedTo) => {
  return api.post(`/v1/requirements/${id}/assign`, null, {
    params: { assigned_to: assignedTo }
  });
};

// 确认需求
export const confirmRequirement = (id) => {
  return api.post(`/v1/requirements/${id}/confirm`);
};

// 标记需求为已澄清
export const clarifyRequirement = (id, clarified = true) => {
  return api.patch(`/v1/requirements/${id}/clarify`, null, {
    params: { clarified }
  });
};

// 问题相关API
// 创建问题
export const createQuestion = (data, currentUserId) => {
  return api.post('/v1/questions/', data, {
    params: { current_user_id: currentUserId }
  });
};

// 获取问题详情
export const getQuestion = (id) => {
  return api.get(`/v1/questions/${id}`);
};

// 获取需求的所有问题
export const getQuestionsByRequirement = (requirementId) => {
  return api.get(`/v1/questions/requirement/${requirementId}`);
};

// 回答问题
export const answerQuestion = (id, answer, answeredBy, currentUserId) => {
  return api.patch(`/v1/questions/${id}/answer`, null, {
    params: { answer, answered_by: answeredBy, current_user_id: currentUserId }
  });
};

// 标记问题为已澄清
export const clarifyQuestion = (id, clarifiedBy, currentUserId) => {
  return api.patch(`/v1/questions/${id}/clarify`, null, {
    params: { clarified_by: clarifiedBy, current_user_id: currentUserId }
  });
};

// 事件日志相关API
// 获取所有事件日志
export const getEventLogs = (params = {}) => {
  return api.get('/v1/event_logs/', { params });
};

// 获取需求的事件日志
export const getEventLogsByRequirement = (requirementId) => {
  return api.get(`/v1/event_logs/requirement/${requirementId}`);
};

// 获取问题的事件日志
export const getEventLogsByQuestion = (questionId) => {
  return api.get(`/v1/event_logs/question/${questionId}`);
};