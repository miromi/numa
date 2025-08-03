import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';

// 页面组件
import HomePage from './pages/HomePage';
import RequirementsPage from './pages/RequirementsPage';
import RequirementDetailPage from './pages/RequirementDetailPage';
import SolutionsPage from './pages/SolutionsPage';
import SolutionDetailPage from './pages/SolutionDetailPage';
import DevelopmentTasksPage from './pages/DevelopmentTasksPage';
import DevelopmentTaskDetailPage from './pages/DevelopmentTaskDetailPage';
import DeploymentsPage from './pages/DeploymentsPage';
import DeploymentDetailPage from './pages/DeploymentDetailPage';

// 组件
import AppHeader from './components/AppHeader';
import AppSidebar from './components/AppSidebar';

// 创建主题
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#e57373',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div style={{ display: 'flex' }}>
          <AppSidebar />
          <div style={{ flex: 1 }}>
            <AppHeader />
            <div style={{ padding: '20px' }}>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/requirements" element={<RequirementsPage />} />
                <Route path="/requirements/:id" element={<RequirementDetailPage />} />
                <Route path="/solutions" element={<SolutionsPage />} />
                <Route path="/solutions/:id" element={<SolutionDetailPage />} />
                <Route path="/development" element={<DevelopmentTasksPage />} />
                <Route path="/development/:id" element={<DevelopmentTaskDetailPage />} />
                <Route path="/deployment" element={<DeploymentsPage />} />
                <Route path="/deployment/:id" element={<DeploymentDetailPage />} />
              </Routes>
            </div>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;