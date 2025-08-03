import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createSolution } from '../services/solutionService';
import { getRequirements } from '../services/requirementService';

const NewSolutionPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    requirement_id: '',
  });
  const [requirements, setRequirements] = useState([]);
  const [loading, setLoading] = useState(false);
  const [requirementsLoading, setRequirementsLoading] = useState(true);

  useEffect(() => {
    fetchRequirements();
  }, []);

  const fetchRequirements = async () => {
    try {
      const response = await getRequirements();
      setRequirements(response.data);
      setRequirementsLoading(false);
    } catch (error) {
      console.error('获取需求列表失败:', error);
      setRequirementsLoading(false);
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
      const response = await createSolution(formData);
      navigate(`/solutions/${response.data.id}`);
    } catch (error) {
      console.error('创建方案失败:', error);
      setLoading(false);
    }
  };

  return (
    <div>
      <Button
        onClick={() => navigate('/solutions')}
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回方案列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          新建方案
        </Typography>
        
        {requirementsLoading ? (
          <Typography>加载需求列表中...</Typography>
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
              label="关联需求"
              name="requirement_id"
              value={formData.requirement_id}
              onChange={handleChange}
              fullWidth
              margin="normal"
              required
              SelectProps={{
                native: true,
              }}
            >
              <option value=""></option>
              {requirements.map((req) => (
                <option key={req.id} value={req.id}>
                  {req.id}: {req.title}
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
                {loading ? '创建中...' : '创建方案'}
              </Button>
            </div>
          </form>
        )}
      </Paper>
    </div>
  );
};

export default NewSolutionPage;