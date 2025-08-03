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
import { getApplications } from '../services/applicationService';
import { getDevelopmentTasks } from '../services/developmentService';
import { getUsers } from '../services/userService';

const ApplicationsPage = () => {
  const [applications, setApplications] = useState([]);
  const [tasks, setTasks] = useState({});
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const [applicationsResponse, tasksResponse, usersResponse] = await Promise.all([
        getApplications(),
        getDevelopmentTasks(),
        getUsers()
      ]);
      
      setApplications(applicationsResponse.data);
      
      // 将任务存储为映射以便快速查找
      const tasksMap = {};
      tasksResponse.data.forEach(task => {
        tasksMap[task.id] = task;
      });
      setTasks(tasksMap);
      
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
        <Typography variant="h4">应用管理</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          component={Link}
          to="/applications/new"
        >
          新建应用
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
              <TableCell>创建者</TableCell>
              <TableCell>创建时间</TableCell>
              <TableCell>操作</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {applications.map((application) => (
              <TableRow key={application.id}>
                <TableCell>{application.id}</TableCell>
                <TableCell>{application.name}</TableCell>
                <TableCell>{application.status}</TableCell>
                <TableCell>
                  {tasks[application.development_task_id] 
                    ? `${tasks[application.development_task_id].id}: ${tasks[application.development_task_id].title}` 
                    : application.development_task_id}
                </TableCell>
                <TableCell>
                  {users[application.created_by] 
                    ? `${users[application.created_by].id}: ${users[application.created_by].name}` 
                    : application.created_by}
                </TableCell>
                <TableCell>{new Date(application.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Button
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/applications/${application.id}`}
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

export default ApplicationsPage;