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
import { getRequirements } from '../services/requirementService';

const RequirementsPage = () => {
  const [requirements, setRequirements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRequirements();
  }, []);

  const fetchRequirements = async () => {
    try {
      const response = await getRequirements();
      setRequirements(response.data);
      setLoading(false);
    } catch (error) {
      console.error('获取需求列表失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Typography variant="h4">需求管理</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          component={Link}
          to="/requirements/new"
        >
          新建需求
        </Button>
      </div>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>标题</TableCell>
              <TableCell>状态</TableCell>
              <TableCell>接手人</TableCell>
              <TableCell>创建时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requirements.map((requirement) => (
              <TableRow key={requirement.id}>
                <TableCell>{requirement.id}</TableCell>
                <TableCell>{requirement.title}</TableCell>
                <TableCell>{requirement.status}</TableCell>
                <TableCell>{requirement.assigned_to || '-'}</TableCell>
                <TableCell>{new Date(requirement.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/requirements/${requirement.id}`}
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

export default RequirementsPage;