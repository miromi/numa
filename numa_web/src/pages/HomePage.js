import React from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import AssignmentIcon from '@material-ui/icons/Assignment';
import EmojiObjectsIcon from '@material-ui/icons/EmojiObjects';
import BuildIcon from '@material-ui/icons/Build';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';

const HomePage = () => {
  const features = [
    {
      title: '需求管理',
      description: '提交和管理项目需求',
      icon: <AssignmentIcon fontSize="large" />,
      link: '/requirements',
    },
    {
      title: '方案设计',
      description: '设计技术实现方案',
      icon: <EmojiObjectsIcon fontSize="large" />,
      link: '/solutions',
    },
    {
      title: '开发任务',
      description: '跟踪开发进度和任务',
      icon: <BuildIcon fontSize="large" />,
      link: '/development',
    },
    {
      title: '部署管理',
      description: '管理应用部署和发布',
      icon: <CloudUploadIcon fontSize="large" />,
      link: '/deployment',
    },
  ];

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        欢迎使用 Numa
      </Typography>
      <Typography variant="subtitle1" gutterBottom>
        自动化DevOps流程工具，帮助您高效完成从需求到部署的整个开发流程。
      </Typography>
      
      <Grid container spacing={3} style={{ marginTop: 20 }}>
        {features.map((feature, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Paper elevation={3} style={{ padding: 20, height: '100%', display: 'flex', flexDirection: 'column' }}>
              <div style={{ textAlign: 'center', marginBottom: 15 }}>
                {feature.icon}
              </div>
              <Typography variant="h6" gutterBottom>
                {feature.title}
              </Typography>
              <Typography variant="body2" style={{ flex: 1, marginBottom: 15 }}>
                {feature.description}
              </Typography>
              <Button
                variant="contained"
                color="primary"
                component={Link}
                to={feature.link}
                fullWidth
              >
                进入
              </Button>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default HomePage;