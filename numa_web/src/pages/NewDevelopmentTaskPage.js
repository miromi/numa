import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createDevelopmentTask } from '../services/developmentService';
import { getSolutions } from '../services/solutionService';
import { getUsers } from '../services/userService';

const NewDevelopmentTaskPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    solution_id: '',
    assigned_to: '',
  });
  const [solutions, setSolutions] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [solutionsLoading, setSolutionsLoading] = useState(true);
  const [usersLoading, setUsersLoading] = useState(true);

  useEffect(() => {
    fetchSolutionsAndUsers();
  }, []);

  const fetchSolutionsAndUsers = async () => {
    try {
      const [solutionsResponse, usersResponse] = await Promise.all([
        getSolutions(),
        getUsers()
      ]);
      
      setSolutions(solutionsResponse.data);
      setSolutionsLoading(false);
      
      setUsers(usersResponse.data);
      setUsersLoading(false);
    } catch (error) {
      console.error('获取数据失败:', error);
      setSolutionsLoading(false);
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
      const response = await createDevelopmentTask(formData);
      navigate(`/development/${response.data.id}`);
    } catch (error) {
      console.error('创建开发任务失败:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <Button
        onClick={() => navigate('/development')}
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回任务列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          新建开发任务
        </Typography>
        
        {(solutionsLoading || usersLoading) ? (
          <Typography>加载数据中...</Typography>
        ) : (
          <form onSubmit={handleSubmit}>
            <TextField
              label="标题"
              name="title"
              value={formData.title}
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
              label="关联方案"
              name="solution_id"
              value={formData.solution_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              {solutions.map((solution) => (
                <option key={solution.id} value={solution.id}>
                  {solution.id}: {solution.title}
                </option>
              ))}
            </TextField>
            
            <TextField
              select
              label="分配给"
              name="assigned_to"
              value={formData.assigned_to}
              onChange={handleChange}
              fullWidth
              margin="normal"
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
                {loading ? '创建中...' : '创建任务'}
              </Button>
            </div>
          </form>
        )}
      </Paper>
    </div>
  );
};

export default NewDevelopmentTaskPage;