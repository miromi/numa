import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getSolution } from '../services/solutionService';

const SolutionDetailPage = () => {
  const { id } = useParams();
  const [solution, setSolution] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSolution();
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
      
      <Paper style={{ padding: 20 }}>
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
            关联需求: {solution.requirement_id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(solution.created_at).toLocaleString()}
          </Typography>
          {solution.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(solution.updated_at).toLocaleString()}
            </Typography>
          )}
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {solution.description}
        </Typography>
      </Paper>
    </div>
  );
};

export default SolutionDetailPage;