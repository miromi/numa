import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { createSolution } from '../services/solutionService';

const NewSolutionPage = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [requirementId, setRequirementId] = useState('');
  const [createdBy, setCreatedBy] = useState('');
  const [creating, setCreating] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title || !description || !requirementId || !createdBy) {
      alert('请填写所有必填字段');
      return;
    }

    setCreating(true);
    try {
      const response = await createSolution({
        title,
        description,
        requirement_id: parseInt(requirementId),
        created_by: parseInt(createdBy)
      });
      
      alert('方案创建成功');
      navigate(`/solutions/${response.data.id}`);
    } catch (error) {
      console.error('创建方案失败:', error);
      alert('创建方案失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setCreating(false);
    }
  };

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
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          创建新方案
        </Typography>
        
        <form onSubmit={handleSubmit}>
          <TextField
            label="方案标题"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            fullWidth
            required
            style={{ marginBottom: 20 }}
          />
          
          <TextField
            label="方案描述"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            multiline
            rows={4}
            fullWidth
            required
            style={{ marginBottom: 20 }}
          />
          
          <TextField
            label="关联需求ID"
            value={requirementId}
            onChange={(e) => setRequirementId(e.target.value)}
            type="number"
            fullWidth
            required
            style={{ marginBottom: 20 }}
          />
          
          <TextField
            label="创建人ID"
            value={createdBy}
            onChange={(e) => setCreatedBy(e.target.value)}
            type="number"
            fullWidth
            required
            style={{ marginBottom: 20 }}
          />
          
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={creating}
          >
            {creating ? '创建中...' : '创建方案'}
          </Button>
        </form>
      </Paper>
    </div>
  );
};

export default NewSolutionPage;