import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createApplication } from '../services/applicationService';
import { getUsers } from '../services/userService';

const NewApplicationPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    created_by: '',
    repository_url: '',
    owner: '',
    app_id: '',
  });
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [usersLoading, setUsersLoading] = useState(true);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const usersResponse = await getUsers();
      setUsers(usersResponse.data);
      setUsersLoading(false);
    } catch (error) {
      console.error('获取用户失败:', error);
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
        
        {usersLoading ? (
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
              label="Git仓库地址"
              name="repository_url"
              value={formData.repository_url}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
            />
            
            <TextField
              label="应用所有者"
              name="owner"
              value={formData.owner}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
            />
            
            <TextField
              label="应用ID"
              name="app_id"
              value={formData.app_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
            />
            
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