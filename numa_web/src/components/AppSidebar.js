import React from 'react';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import HomeIcon from '@material-ui/icons/Home';
import AssignmentIcon from '@material-ui/icons/Assignment';
import LightbulbIcon from '@material-ui/icons/Lightbulb';
import BuildIcon from '@material-ui/icons/Build';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { Link } from 'react-router-dom';

const AppSidebar = () => {
  const menuItems = [
    { text: '首页', icon: <HomeIcon />, path: '/' },
    { text: '需求管理', icon: <AssignmentIcon />, path: '/requirements' },
    { text: '方案管理', icon: <LightbulbIcon />, path: '/solutions' },
    { text: '开发管理', icon: <BuildIcon />, path: '/development' },
    { text: '部署管理', icon: <CloudUploadIcon />, path: '/deployment' },
  ];

  return (
    <Drawer
      variant="permanent"
      anchor="left"
      style={{ width: 240 }}
      PaperProps={{ style: { width: 240 } }}
    >
      <div style={{ height: 64 }} /> {/* 为AppBar留出空间 */}
      <List>
        {menuItems.map((item) => (
          <ListItem button key={item.text} component={Link} to={item.path}>
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default AppSidebar;