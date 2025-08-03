import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getRequirement } from '../services/requirementService';

const RequirementDetailPage = () => {
  const { id } = useParams();
  const [requirement, setRequirement] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequirement();
  }, [id]);

  const fetchRequirement = async () => {
    try {
      const response = await getRequirement(id);
      setRequirement(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取需求详情失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  if (!requirement) {
    return <Typography>未找到该需求</Typography>;
  }

  return (
    <div>
      <Button
        component={Link}
        to="/requirements"
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回需求列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          {requirement.title}
        </Typography>
        
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1" color="textSecondary">
            ID: {requirement.id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            状态: {requirement.status}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(requirement.created_at).toLocaleString()}
          </Typography>
          {requirement.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(requirement.updated_at).toLocaleString()}
            </Typography>
          )}
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {requirement.description}
        </Typography>
      </Paper>
    </div>
  );
};

export default RequirementDetailPage;