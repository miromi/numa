import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import AddIcon from '@material-ui/icons/Add';
import { getDevelopmentTasks } from '../services/developmentService';
import { getSolutions } from '../services/solutionService';
import { getUsers } from '../services/userService';

const DevelopmentTaskListPage = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [solutions, setSolutions] = useState({});
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const [tasksResponse, solutionsResponse, usersResponse] = await Promise.all([
        getDevelopmentTasks(),
        getSolutions(),
        getUsers()
      ]);
      
      setTasks(tasksResponse.data);
      
      // 将方案存储为映射以便快速查找
      const solutionsMap = {};
      solutionsResponse.data.forEach(sol => {
        solutionsMap[sol.id] = sol;
      });
      setSolutions(solutionsMap);
      
      // 将用户存储为映射以便快速查找
      const usersMap = {};
      usersResponse.data.forEach(user => {
        usersMap[user.id] = user;
      });
      setUsers(usersMap);
      
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
        <Typography variant="h4">开发任务列表</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          // component={Link}
          // to="/development/new"
        >
          新建任务
        </Button>
      </div>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>标题</TableCell>
              <TableCell>状态</TableCell>
              <TableCell>代码分支</TableCell>
              <TableCell>关联方案</TableCell>
              <TableCell>分配给</TableCell>
              <TableCell>创建时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task) => (
              <TableRow key={task.id}>
                <TableCell>{task.id}</TableCell>
                <TableCell>{task.title}</TableCell>
                <TableCell>{task.status}</TableCell>
                <TableCell>{task.code_branch || '未指定'}</TableCell>
                <TableCell>
                  {task.solution 
                    ? <Link to={`/solutions/${task.solution.id}`}>{task.solution.title}</Link>
                    : task.solution_id}
                </TableCell>
                <TableCell>
                  {users[task.assigned_to] 
                    ? `${users[task.assigned_to].name}` 
                    : task.assigned_to || '未分配'}
                </TableCell>
                <TableCell>{new Date(task.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/development/${task.id}`}
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

export default DevelopmentTaskListPage;