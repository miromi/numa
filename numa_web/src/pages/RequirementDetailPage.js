import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { getRequirement, assignRequirement, confirmRequirement } from '../services/requirementService';

const RequirementDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [requirement, setRequirement] = useState(null);
  const [loading, setLoading] = useState(true);
  const [assigning, setAssigning] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [assignedTo, setAssignedTo] = useState('');

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

  const handleAssign = async () => {
    if (!assignedTo) {
      alert('请输入接手人ID');
      return;
    }

    setAssigning(true);
    try {
      const response = await assignRequirement(id, assignedTo);
      setRequirement(response.data);
      setAssignedTo('');
      alert('需求分配成功');
    } catch (error) {
      console.error('分配需求失败:', error);
      alert('分配需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setAssigning(false);
    }
  };

  const handleConfirm = async () => {
    setConfirming(true);
    try {
      const response = await confirmRequirement(id);
      setRequirement(response.data);
      alert('需求确认成功');
    } catch (error) {
      console.error('确认需求失败:', error);
      alert('确认需求失败: ' + (error.response?.data?.detail || error.message));
    } finally {
      setConfirming(false);
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
      
      <Paper style={{ padding: 20, marginBottom: 20 }}>
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
          {requirement.assigned_to && (
            <Typography variant="subtitle1" color="textSecondary">
              接手人: {requirement.assigned_to}
            </Typography>
          )}
          {requirement.branch_name && (
            <Typography variant="subtitle1" color="textSecondary">
              分支名称: {requirement.branch_name}
            </Typography>
          )}
        </div>
        
        <Typography variant="h6" gutterBottom>
          描述
        </Typography>
        <Typography variant="body1" paragraph>
          {requirement.description}
        </Typography>
        
        {requirement.spec_document && (
          <>
            <Typography variant="h6" gutterBottom>
              需求规范文档
            </Typography>
            <Paper style={{ padding: 15, backgroundColor: '#f5f5f5' }}>
              <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                {requirement.spec_document}
              </pre>
            </Paper>
          </>
        )}
      </Paper>
      
      {/* 操作按钮 */}
      <Paper style={{ padding: 20 }}>
        <Typography variant="h6" gutterBottom>
          操作
        </Typography>
        
        {requirement.status === 'pending' && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="subtitle1">分配需求</Typography>
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 10 }}>
              <TextField
                label="接手人ID"
                value={assignedTo}
                onChange={(e) => setAssignedTo(e.target.value)}
                type="number"
                style={{ marginRight: 10 }}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleAssign}
                disabled={assigning}
              >
                {assigning ? '分配中...' : '分配需求'}
              </Button>
            </div>
          </div>
        )}
        
        {requirement.status === 'clarifying' && (
          <div style={{ marginBottom: 20 }}>
            <Typography variant="subtitle1">确认需求</Typography>
            <Button
              variant="contained"
              color="primary"
              onClick={handleConfirm}
              disabled={confirming}
              style={{ marginTop: 10 }}
            >
              {confirming ? '确认中...' : '确认需求澄清完毕'}
            </Button>
          </div>
        )}
      </Paper>
    </div>
  );
};

export default RequirementDetailPage;