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
import { getSolutions } from '../services/solutionService';
import { getRequirements } from '../services/requirementService';

const SolutionsPage = () => {
  const [solutions, setSolutions] = useState([]);
  const [requirements, setRequirements] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSolutions();
  }, []);

  const fetchSolutions = async () => {
    try {
      const [solutionsResponse, requirementsResponse] = await Promise.all([
        getSolutions(),
        getRequirements()
      ]);
      
      setSolutions(solutionsResponse.data);
      
      // 将需求存储为映射以便快速查找
      const requirementsMap = {};
      requirementsResponse.data.forEach(req => {
        requirementsMap[req.id] = req;
      });
      setRequirements(requirementsMap);
      
      setLoading(false);
    } catch (error) {
      console.error('获取数据失败:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>加载中...</Typography>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <Typography variant="h4">方案管理</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          component={Link}
          to="/solutions/new"
        >
          新建方案
        </Button>
      </div>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>标题</TableCell>
              <TableCell>状态</TableCell>
              <TableCell>关联需求</TableCell>
              <TableCell>创建时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {solutions.map((solution) => (
              <TableRow key={solution.id}>
                <TableCell>{solution.id}</TableCell>
                <TableCell>{solution.title}</TableCell>
                <TableCell>{solution.status}</TableCell>
                <TableCell>
                  {requirements[solution.requirement_id] 
                    ? `${requirements[solution.requirement_id].id}: ${requirements[solution.requirement_id].title}` 
                    : solution.requirement_id}
                </TableCell>
                <TableCell>{new Date(solution.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/solutions/${solution.id}`}
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

export default SolutionsPage;