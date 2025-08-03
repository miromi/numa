import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getApplication } from '../services/applicationService';
import { getDevelopmentTask } from '../services/developmentService';
import { getUser } from '../services/userService';

const ApplicationDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState(null);
  const [task, setTask] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplication();
  }, [id]);

  const fetchApplication = async () => {
    try {
      const applicationResponse = await getApplication(id);
      setApplication(applicationResponse.data);
      
      // 获取关联的开发任务
      if (applicationResponse.data.development_task_id) {
        const taskResponse = await getDevelopmentTask(applicationResponse.data.development_task_id);
        setTask(taskResponse.data);
      }
      
      // 获取创建者信息
      if (applicationResponse.data.created_by) {
        const userResponse = await getUser(applicationResponse.data.created_by);
        setUser(userResponse.data);
      }
      
      setLoading(false);
    } catch (error) {
      console.error('获取应用详情失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  if (!application) {
    return <Typography>未找到该应用</Typography>;
  }

  return (
    <div>
      <Button
        onClick={() => navigate('/applications')}
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回应用列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          应用详情
        </Typography>
        
        <div style={{ marginBottom: 15 }}>
          <Typography variant="h6">基本信息</Typography>
          <Typography><strong>ID:</strong> {application.id}</Typography>
          <Typography><strong>名称:</strong> {application.name}</Typography>
          <Typography><strong>描述:</strong> {application.description}</Typography>
          <Typography><strong>状态:</strong> {application.status}</Typography>
          <Typography><strong>创建时间:</strong> {new Date(application.created_at).toLocaleString()}</Typography>
          {application.built_at && (
            <Typography><strong>构建时间:</strong> {new Date(application.built_at).toLocaleString()}</Typography>
          )}
        </div>
        
        <div style={{ marginBottom: 15 }}>
          <Typography variant="h6">关联信息</Typography>
          {task ? (
            <Typography>
              <strong>开发任务:</strong> 
              <Button 
                size="small" 
                onClick={() => navigate(`/development/${task.id}`)}
                style={{ marginLeft: 10 }}
              >
                {task.id}: {task.title}
              </Button>
            </Typography>
          ) : (
            <Typography><strong>开发任务:</strong> 未关联</Typography>
          )}
          
          {user ? (
            <Typography>
              <strong>创建者:</strong> 
              <Button 
                size="small" 
                onClick={() => navigate(`/users/${user.id}`)}
                style={{ marginLeft: 10 }}
              >
                {user.id}: {user.name}
              </Button>
            </Typography>
          ) : (
            <Typography><strong>创建者:</strong> 未知</Typography>
          )}
        </div>
      </Paper>
    </div>
  );
};

export default ApplicationDetailPage;