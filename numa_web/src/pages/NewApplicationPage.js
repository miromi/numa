import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createApplication } from '../services/applicationService';
import { getDevelopmentTasks } from '../services/developmentService';
import { getUsers } from '../services/userService';

const NewApplicationPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    development_task_id: '',
    created_by: '',
  });
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [usersLoading, setUsersLoading] = useState(true);

  useEffect(() => {
    fetchTasksAndUsers();
  }, []);

  const fetchTasksAndUsers = async () => {
    try {
      const [tasksResponse, usersResponse] = await Promise.all([
        getDevelopmentTasks(),
        getUsers()
      ]);
      
      setTasks(tasksResponse.data);
      setTasksLoading(false);
      
      setUsers(usersResponse.data);
      setUsersLoading(false);
    } catch (error) {
      console.error('获取数据失败:', error);
      setTasksLoading(false);
      setUsersLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await createApplication(formData);
      navigate(`/applications/${response.data.id}`);
    } catch (error) {
      console.error('创建应用失败:', error);
      setLoading(false);
    }
  };

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
          新建应用
        </Typography>
        
        {(tasksLoading || usersLoading) ? (
          <Typography>加载数据中...</Typography>
        ) : (
          <form onSubmit={handleSubmit}>
            <TextField
              label="名称"
              name="name"
              value={formData.name}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
            />
            
            <TextField
              label="描述"
              name="description"
              value={formData.description}
              onChange={handleChange}
              fullWidth
              margin="normal"
              multiline
              rows={4}
              required
            />
            
            <TextField
              select
              label="关联开发任务"
              name="development_task_id"
              value={formData.development_task_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              {tasks.map((task) => (
                <option key={task.id} value={task.id}>
                  {task.id}: {task.title}
                </option>
              ))}
            </TextField>
            
            <TextField
              select
              label="创建者"
              name="created_by"
              value={formData.created_by}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.id}: {user.name}
                </option>
              ))}
            </TextField>
            
            <div style={{ marginTop: 20 }}>
              <Button
                variant="contained"
                color="primary"
                type="submit"
                disabled={loading}
              >
                {loading ? '创建中...' : '创建应用'}
              </Button>
            </div>
          </form>
        )}
      </Paper>
    </div>
  );
};

export default NewApplicationPage;