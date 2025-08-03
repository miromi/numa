import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getDeployment } from '../services/deploymentService';

const DeploymentDetailPage = () => {
  const { id } = useParams();
  const [deployment, setDeployment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDeployment();
  }, [id]);

  const fetchDeployment = async () => {
    try {
      const response = await getDeployment(id);
      setDeployment(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取部署记录详情失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  if (!deployment) {
    return <Typography>未找到该部署记录</Typography>;
  }

  return (
    <div>
      <Button
        component={Link}
        to="/deployment"
        startIcon={<ArrowBackIcon />}
        style={{ marginBottom: 20 }}
      >
        返回部署列表
      </Button>
      
      <Paper style={{ padding: 20 }}>
        <Typography variant="h4" gutterBottom>
          {deployment.name}
        </Typography>
        
        <div style={{ marginBottom: 20 }}>
          <Typography variant="subtitle1" color="textSecondary">
            ID: {deployment.id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            状态: {deployment.status}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            关联任务: {deployment.development_task_id}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            部署者: {deployment.deployed_by || '未指定'}
          </Typography>
          <Typography variant="subtitle1" color="textSecondary">
            创建时间: {new Date(deployment.created_at).toLocaleString()}
          </Typography>
          {deployment.updated_at && (
            <Typography variant="subtitle1" color="textSecondary">
              更新时间: {new Date(deployment.updated_at).toLocaleString()}
            </Typography>
          )}
          {deployment.deployed_at && (
            <Typography variant="subtitle1" color="textSecondary">
              部署时间: {new Date(deployment.deployed_at).toLocaleString()}
            </Typography>
          )}
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {deployment.description}
        </Typography>
      </Paper>
    </div>
  );
};

export default DeploymentDetailPage;