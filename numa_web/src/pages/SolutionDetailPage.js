import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import {
  getSolution,
  confirmSolution,
  getSolutionQuestionsBySolution,
  createSolutionQuestion,
  answerSolutionQuestion,
  clarifySolutionQuestion
} from '../services/solutionService';

const SolutionDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(true);
  const [confirming, setConfirming] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [newQuestion, setNewQuestion] = useState('');
  const [answeringQuestionId, setAnsweringQuestionId] = useState(null);
  const [answerText, setAnswerText] = useState('');
  const [clarifyingQuestionId, setClarifyingQuestionId] = useState(null);
  const [currentUser, setCurrentUser] = useState(1); // 默认当前用户ID为1，实际应用中应从认证系统获取

  useEffect(() => {
    fetchSolution();
    fetchQuestions();
  }, [id]);

  const fetchSolution = async () => {
    try {
      const response = await getSolution(id);
      setSolution(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取方案详情失败:', error);
      setLoading(false);
    }
  };

  const fetchQuestions = async () => {
    try {
      const response = await getSolutionQuestionsBySolution(id);
      setQuestions(response.data);
    } catch (error) {
      console.error('获取问题列表失败:', error);
    }
  };

  const handleConfirm = async (confirmed = true) => {
    setConfirming(true);
    try {
      const response = await confirmSolution(id, confirmed);
      setSolution(response.data);
      alert(`方案${confirmed ? '已确认' : '取消确认'}`);
    } catch (error) {
      console.error('确认方案失败:', error);
      alert('确认方案失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setConfirming(false);
    }
  };

  const handleCreateQuestion = async () => {
    if (!newQuestion) {
      alert('请输入问题内容');
      return;
    }

    try {
      await createSolutionQuestion(
        { content: newQuestion, solution_id: id, created_by: currentUser },
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
      await answerSolutionQuestion(questionId, answerText, currentUser, currentUser);
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
      await clarifySolutionQuestion(questionId, solution.created_by, currentUser);
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

  if (!solution) {
    return <Typography>未找到该方案</Typography>;
  }

  return (
    <div>
      <Button
        component={Link}
        to="/solutions"
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回方案列表
      </Button>
      
      <Paper style={{ padding: 20, marginBottom: 20 }}>
        <Typography variant="h4" gutterBottom>
          {solution.title}
        </Typography>
        
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1" color="textSecondary">
            ID: {solution.id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            状态: {solution.status}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(solution.created_at).toLocaleString()}
          </Typography>
          {solution.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(solution.updated_at).toLocaleString()}
            </Typography>
          )}
          <Typography variant="subtitle1" color="textSecondary">
            方案负责人: {solution.created_by}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            澄清状态: {solution.clarified ? '已澄清' : '未澄清'}
          </Typography>
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {solution.description}
        </Typography>
      </Paper>
      
      {/* 操作按钮 */}
      <Paper style={{ padding: 20, marginBottom: 20 }}>
        <Typography variant="h6" gutterBottom>
          操作
        </Typography>
        
        {solution.status === 'clarifying' && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="subtitle1">确认方案</Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleConfirm(true)}
              disabled={confirming}
              style={{ marginTop: 10, marginRight: 10 }}
            >
              {confirming ? '确认中...' : '确认方案'}
            </Button>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => handleConfirm(false)}
              disabled={confirming}
              style={{ marginTop: 10 }}
            >
              {confirming ? '取消确认中...' : '取消确认'}
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
                {question.answer && !question.clarified && solution.created_by === currentUser && (
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

export default SolutionDetailPage;