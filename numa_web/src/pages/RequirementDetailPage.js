import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { 
  getRequirement, 
  assignRequirement, 
  confirmRequirement, 
  clarifyRequirement,
  updateRequirement,
  getQuestionsByRequirement,
  createQuestion,
  answerQuestion,
  clarifyQuestion
} from '../services/requirementService';

const RequirementDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [requirement, setRequirement] = useState(null);
  const [loading, setLoading] = useState(true);
  const [assigning, setAssigning] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [clarifying, setClarifying] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [assignedTo, setAssignedTo] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [questions, setQuestions] = useState([]);
  const [newQuestion, setNewQuestion] = useState('');
  const [answeringQuestionId, setAnsweringQuestionId] = useState(null);
  const [answerText, setAnswerText] = useState('');
  const [clarifyingQuestionId, setClarifyingQuestionId] = useState(null);
  const [currentUser, setCurrentUser] = useState(1); // 默认当前用户ID为1，实际应用中应从认证系统获取

  useEffect(() => {
    fetchRequirement();
    fetchQuestions();
  }, [id]);

  const fetchRequirement = async () => {
    try {
      const response = await getRequirement(id);
      setRequirement(response.data);
      setNewDescription(response.data.description);
      setLoading(false);
    } catch (error) {
      console.error('获取需求详情失败:', error);
      setLoading(false);
    }
  };

  const fetchQuestions = async () => {
    try {
      const response = await getQuestionsByRequirement(id);
      setQuestions(response.data);
    } catch (error) {
      console.error('获取问题列表失败:', error);
    }
  };

  const handleAssign = async () => {
    if (!assignedTo) {
      alert('请输入接手人ID');
      return;
    }

    setAssigning(true);
    try {
      const response = await assignRequirement(id, assignedTo);
      setRequirement(response.data);
      setAssignedTo('');
      alert('需求分配成功');
    } catch (error) {
      console.error('分配需求失败:', error);
      alert('分配需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setAssigning(false);
    }
  };

  const handleConfirm = async () => {
    setConfirming(true);
    try {
      const response = await confirmRequirement(id);
      setRequirement(response.data);
      alert('需求确认成功');
    } catch (error) {
      console.error('确认需求失败:', error);
      alert('确认需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setConfirming(false);
    }
  };

  const handleClarify = async (clarified = true) => {
    setClarifying(true);
    try {
      const response = await clarifyRequirement(id, clarified);
      setRequirement(response.data);
      alert(`需求${clarified ? '已澄清' : '未澄清'}`);
    } catch (error) {
      console.error('标记需求失败:', error);
      alert('标记需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setClarifying(false);
    }
  };

  const handleUpdate = async () => {
    if (!newDescription) {
      alert('请输入新的需求描述');
      return;
    }

    setUpdating(true);
    try {
      const response = await updateRequirement(id, { description: newDescription });
      setRequirement(response.data);
      alert('需求更新成功');
    } catch (error) {
      console.error('更新需求失败:', error);
      alert('更新需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setUpdating(false);
    }
  };

  const handleCreateQuestion = async () => {
    if (!newQuestion) {
      alert('请输入问题内容');
      return;
    }

    try {
      await createQuestion(
        { content: newQuestion, requirement_id: id, created_by: currentUser },
        currentUser
      );
      setNewQuestion('');
      fetchQuestions(); // 刷新问题列表
      alert('问题创建成功');
    } catch (error) {
      console.error('创建问题失败:', error);
      alert('创建问题失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleAnswerQuestion = async (questionId) => {
    if (!answerText) {
      alert('请输入回答内容');
      return;
    }

    try {
      await answerQuestion(questionId, answerText, currentUser, currentUser);
      setAnsweringQuestionId(null);
      setAnswerText('');
      fetchQuestions(); // 刷新问题列表
      alert('问题回答成功');
    } catch (error) {
      console.error('回答问题失败:', error);
      alert('回答问题失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  const handleClarifyQuestion = async (questionId) => {
    try {
      await clarifyQuestion(questionId, requirement.assigned_to, currentUser);
      setClarifyingQuestionId(null);
      fetchQuestions(); // 刷新问题列表
      alert('问题标记为已澄清');
    } catch (error) {
      console.error('标记问题失败:', error);
      alert('标记问题失败: ' + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  if (!requirement) {
    return <Typography>未找到该需求</Typography>;
  }

  return (
    <div>
      <Button
        component={Link}
        to="/requirements"
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回需求列表
      </Button>
      
      <Paper style={{ padding: 20, marginBottom: 20 }}>
        <Typography variant="h4" gutterBottom>
          {requirement.title}
        </Typography>
        
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1" color="textSecondary">
            ID: {requirement.id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            状态: {requirement.status}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(requirement.created_at).toLocaleString()}
          </Typography>
          {requirement.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(requirement.updated_at).toLocaleString()}
            </Typography>
          )}
          {requirement.assigned_to && (
            <Typography variant="subtitle1" color="textSecondary">
              接手人: {requirement.assigned_to}
            </Typography>
          )}
          {requirement.branch_name && (
            <Typography variant="subtitle1" color="textSecondary">
              分支名称: {requirement.branch_name}
            </Typography>
          )}
          <Typography variant="subtitle1" color="textSecondary">
            澄清状态: {requirement.clarified ? '已澄清' : '未澄清'}
          </Typography>
        </div>
        
        {/* 关联应用信息 */}
        {requirement.application && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="h6" gutterBottom>
              关联应用
            </Typography>
            <Paper style={{ padding: 15 }}>
              <Typography variant="subtitle1">
                <Link to={`/applications/${requirement.application.id}`}>
                  {requirement.application.name}
                </Link>
              </Typography>
              <Typography variant="body2" color="textSecondary">
                ID: {requirement.application.id} | 所有者: {requirement.application.owner}
              </Typography>
            </Paper>
          </div>
        )}
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        {!requirement.clarified ? (
          <div style={{ marginBottom: 20 }}>
            <TextField
              label="需求描述"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
              multiline
              rows={4}
              fullWidth
              variant="outlined"
              style={{ marginBottom: 10 }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpdate}
              disabled={updating}
            >
              {updating ? '更新中...' : '更新需求'}
            </Button>
          </div>
        ) : (
          <Typography variant="body1" paragraph>
            {requirement.description}
          </Typography>
        )}
        
        {requirement.spec_document && (
          <>
            <Typography variant="h6" gutterBottom>
              需求规范文档
            </Typography>
            <Paper style={{ padding: 15, backgroundColor: '#f5f5f5' }}>
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                {requirement.spec_document}
              </pre>
            </Paper>
          </>
        )}
      </Paper>
      
      {/* 操作按钮 */}
      <Paper style={{ padding: 20, marginBottom: 20 }}>
        <Typography variant="h6" gutterBottom>
          操作
        </Typography>
        
        {requirement.status === 'pending' && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="subtitle1">分配需求</Typography>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 10 }}>
              <TextField
                label="接手人ID"
                value={assignedTo}
                onChange={(e) => setAssignedTo(e.target.value)}
                type="number"
                style={{ marginRight: 10 }}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleAssign}
                disabled={assigning}
              >
                {assigning ? '分配中...' : '分配需求'}
              </Button>
            </div>
          </div>
        )}
        
        {requirement.status === 'clarifying' && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="subtitle1">确认需求</Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleConfirm}
              disabled={confirming}
              style={{ marginTop: 10, marginRight: 10 }}
            >
              {confirming ? '确认中...' : '确认需求澄清完毕'}
            </Button>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleClarify(true)}
              disabled={clarifying}
              style={{ marginTop: 10 }}
            >
              {clarifying ? '标记中...' : '标记需求为已澄清'}
            </Button>
          </div>
        )}
      </Paper>
      
      {/* 问题管理 */}
      <Paper style={{ padding: 20 }}>
        <Typography variant="h6" gutterBottom>
          问题管理
        </Typography>
        
        {/* 创建问题 */}
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1">提出新问题</Typography>
          <TextField
            label="问题内容"
            value={newQuestion}
            onChange={(e) => setNewQuestion(e.target.value)}
            multiline
            rows={2}
            fullWidth
            variant="outlined"
            style={{ marginTop: 10, marginBottom: 10 }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleCreateQuestion}
          >
            提出问题
          </Button>
        </div>
        
        {/* 问题列表 */}
        <div>
          <Typography variant="subtitle1">问题列表</Typography>
          {questions.length === 0 ? (
            <Typography style={{ marginTop: 10 }}>暂无问题</Typography>
          ) : (
            questions.map((question) => (
              <Paper key={question.id} style={{ padding: 15, marginTop: 10 }}>
                <Typography variant="subtitle2">
                  问题: {question.content}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  提问人: {question.created_by} | 
                  状态: {question.clarified ? '已澄清' : '未澄清'}
                </Typography>
                
                {question.answer && (
                  <div style={{ marginTop: 10 }}>
                    <Typography variant="subtitle2">回答:</Typography>
                    <Typography variant="body2">{question.answer}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      回答人: {question.answered_by}
                    </Typography>
                  </div>
                )}
                
                {/* 回答问题 */}
                {!question.answer && (
                  <div style={{ marginTop: 10 }}>
                    {answeringQuestionId === question.id ? (
                      <div>
                        <TextField
                          label="回答内容"
                          value={answerText}
                          onChange={(e) => setAnswerText(e.target.value)}
                          multiline
                          rows={2}
                          fullWidth
                          variant="outlined"
                          style={{ marginBottom: 10 }}
                        />
                        <Button
                          variant="contained"
                          color="primary"
                          onClick={() => handleAnswerQuestion(question.id)}
                          style={{ marginRight: 10 }}
                        >
                          提交回答
                        </Button>
                        <Button
                          variant="outlined"
                          onClick={() => setAnsweringQuestionId(null)}
                        >
                          取消
                        </Button>
                      </div>
                    ) : (
                      <Button
                        variant="outlined"
                        onClick={() => setAnsweringQuestionId(question.id)}
                      >
                        回答问题
                      </Button>
                    )}
                  </div>
                )}
                
                {/* 澄清问题 */}
                {question.answer && !question.clarified && requirement.assigned_to === currentUser && (
                  <div style={{ marginTop: 10 }}>
                    {clarifyingQuestionId === question.id ? (
                      <div>
                        <Button
                          variant="contained"
                          color="primary"
                          onClick={() => handleClarifyQuestion(question.id)}
                          style={{ marginRight: 10 }}
                        >
                          确认澄清
                        </Button>
                        <Button
                          variant="outlined"
                          onClick={() => setClarifyingQuestionId(null)}
                        >
                          取消
                        </Button>
                      </div>
                    ) : (
                      <Button
                        variant="outlined"
                        color="secondary"
                        onClick={() => setClarifyingQuestionId(question.id)}
                      >
                        标记为已澄清
                      </Button>
                    )}
                  </div>
                )}
              </Paper>
            ))
          )}
        </div>
      </Paper>
    </div>
  );
};

export default RequirementDetailPage;