import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getDevelopmentTask } from '../services/developmentService';

const DevelopmentTaskDetailPage = () => {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      const response = await getDevelopmentTask(id);
      setTask(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取开发任务详情失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  if (!task) {
    return <Typography>未找到该开发任务</Typography>;
  }

  return (
    <div>
      <Button
        component={Link}
        to="/development"
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回任务列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          {task.title}
        </Typography>
        
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1" color="textSecondary">
            ID: {task.id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            状态: {task.status}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            关联方案: {task.solution_id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            分配给: {task.assigned_to || '未分配'}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(task.created_at).toLocaleString()}
          </Typography>
          {task.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(task.updated_at).toLocaleString()}
            </Typography>
          )}
          {task.started_at && (
            <Typography variant="subtitle1" color="textSecondary">
              开始时间: {new Date(task.started_at).toLocaleString()}
            </Typography>
          )}
          {task.completed_at && (
            <Typography variant="subtitle1" color="textSecondary">
              完成时间: {new Date(task.completed_at).toLocaleString()}
            </Typography>
          )}
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {task.description}
        </Typography>
      </Paper>
    </div>
  );
};

export default DevelopmentTaskDetailPage;