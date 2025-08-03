import api from './api';

// 获取方案详情
export const getSolution = (solutionId) => {
  return api.get(`/v1/solutions/${solutionId}`);
};

// 获取方案列表
export const getSolutions = (params = {}) => {
  return api.get(`/v1/solutions/`, { params });
};

// 根据需求ID获取方案列表
export const getSolutionsByRequirement = (requirementId) => {
  return api.get(`/v1/solutions/requirement/${requirementId}`);
};

// 创建方案
export const createSolution = (solutionData) => {
  return api.post(`/v1/solutions/`, solutionData);
};

// 确认方案
export const confirmSolution = (solutionId, confirmed = true) => {
  return api.patch(`/v1/solutions/${solutionId}/confirm`, null, {
    params: { confirmed }
  });
};

// 创建方案问题
export const createSolutionQuestion = (questionData, currentUserId) => {
  return api.post(`/v1/solutions/questions/`, questionData, {
    params: { current_user_id: currentUserId }
  });
};

// 获取方案问题列表
export const getSolutionQuestionsBySolution = (solutionId) => {
  return api.get(`/v1/solutions/questions/solution/${solutionId}`);
};

// 回答方案问题
export const answerSolutionQuestion = (questionId, answer, answeredBy, currentUserId) => {
  return api.patch(`/v1/solutions/questions/${questionId}/answer`, null, {
    params: { answer, answered_by: answeredBy, current_user_id: currentUserId }
  });
};

// 标记方案问题为已澄清
export const clarifySolutionQuestion = (questionId, clarifiedBy, currentUserId) => {
  return api.patch(`/v1/solutions/questions/${questionId}/clarify`, null, {
    params: { clarified_by: clarifiedBy, current_user_id: currentUserId }
  });
};