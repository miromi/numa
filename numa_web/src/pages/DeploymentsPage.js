import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import { getDeployments } from '../services/deploymentService';

const DeploymentsPage = () => {
  const [deployments, setDeployments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDeployments();
  }, []);

  const fetchDeployments = async () => {
    try {
      const response = await getDeployments();
      setDeployments(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取部署记录列表失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Typography variant="h4">部署管理</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          component={Link}
          to="/deployment/new"
        >
          新建部署
        </Button>
      </div>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>名称</TableCell>
              <TableCell>状态</TableCell>
              <TableCell>关联任务</TableCell>
              <TableCell>部署者</TableCell>
              <TableCell>创建时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {deployments.map((deployment) => (
              <TableRow key={deployment.id}>
                <TableCell>{deployment.id}</TableCell>
                <TableCell>{deployment.name}</TableCell>
                <TableCell>{deployment.status}</TableCell>
                <TableCell>{deployment.development_task_id}</TableCell>
                <TableCell>{deployment.deployed_by || '未指定'}</TableCell>
                <TableCell>{new Date(deployment.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/deployment/${deployment.id}`}
                  >
                    查看
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default DeploymentsPage;