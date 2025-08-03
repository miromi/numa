import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createRequirement } from '../services/requirementService';
import { getApplications } from '../services/applicationService';

const NewRequirementPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    user_id: '',
    application_id: '',
  });
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [appsLoading, setAppsLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await getApplications();
      setApplications(response.data);
      setAppsLoading(false);
    } catch (error) {
      console.error('获取应用列表失败:', error);
      setAppsLoading(false);
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
      // 转换application_id为整数或设置为null
      const requestData = {
        ...formData,
        user_id: parseInt(formData.user_id),
        application_id: formData.application_id ? parseInt(formData.application_id) : null
      };
      
      const response = await createRequirement(requestData);
      navigate(`/requirements/${response.data.id}`);
    } catch (error) {
      console.error('创建需求失败:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <Button
        onClick={() => navigate('/requirements')}
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回需求列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          新建需求
        </Typography>
        
        {appsLoading ? (
          <Typography>加载应用列表中...</Typography>
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
              label="用户ID"
              name="user_id"
              value={formData.user_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              type="number"
              required
            />
            
            <TextField
              select
              label="关联应用（可选）"
              name="application_id"
              value={formData.application_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              {applications.map((app) => (
                <option key={app.id} value={app.id}>
                  {app.id}: {app.name}
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
                {loading ? '创建中...' : '创建需求'}
              </Button>
            </div>
          </form>
        )}
      </Paper>
    </div>
  );
};

export default NewRequirementPage;