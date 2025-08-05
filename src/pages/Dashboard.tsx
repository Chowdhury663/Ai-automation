import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  IconButton,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Button,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  AccountTree,
  SmartToy,
  Task,
  PlayArrow,
  CheckCircle,
  Error,
  Schedule,
  TrendingUp,
  Add,
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import axios from 'axios';

interface DashboardData {
  summary: {
    total_tasks: number;
    tasks_24h: number;
    completed_tasks: number;
    failed_tasks: number;
    success_rate: number;
    total_workflows: number;
    active_workflows: number;
    total_agents: number;
  };
  recent_activity: Array<{
    id: number;
    name: string;
    status: string;
    created_at: string;
    workflow_id?: number;
  }>;
  completion_rate_trend: Array<{
    date: string;
    total_tasks: number;
    completed_tasks: number;
    completion_rate: number;
  }>;
}

const Dashboard: React.FC = () => {
  const { data: dashboardData, isLoading } = useQuery<DashboardData>(
    'dashboard',
    () => axios.get('/api/analytics/dashboard').then(res => res.data),
    { refetchInterval: 30000 }
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'running': return 'warning';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle color="success" />;
      case 'failed': return <Error color="error" />;
      case 'running': return <PlayArrow color="warning" />;
      default: return <Schedule color="disabled" />;
    }
  };

  const pieData = dashboardData ? [
    { name: 'Completed', value: dashboardData.summary.completed_tasks, color: '#10b981' },
    { name: 'Failed', value: dashboardData.summary.failed_tasks, color: '#ef4444' },
    { name: 'Other', value: dashboardData.summary.total_tasks - dashboardData.summary.completed_tasks - dashboardData.summary.failed_tasks, color: '#6b7280' },
  ] : [];

  if (isLoading || !dashboardData) {
    return (
      <Box sx={{ width: '100%', mt: 2 }}>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Dashboard
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          sx={{ borderRadius: 2 }}
        >
          Create Workflow
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Total Tasks
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {dashboardData.summary.total_tasks}
                  </Typography>
                  <Typography color="textSecondary" variant="body2">
                    {dashboardData.summary.tasks_24h} in last 24h
                  </Typography>
                </Box>
                <IconButton sx={{ bgcolor: 'primary.light', color: 'primary.contrastText' }}>
                  <Task />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Success Rate
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {dashboardData.summary.success_rate.toFixed(1)}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={dashboardData.summary.success_rate}
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </Box>
                <IconButton sx={{ bgcolor: 'success.light', color: 'success.contrastText' }}>
                  <TrendingUp />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Active Workflows
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {dashboardData.summary.active_workflows}
                  </Typography>
                  <Typography color="textSecondary" variant="body2">
                    of {dashboardData.summary.total_workflows} total
                  </Typography>
                </Box>
                <IconButton sx={{ bgcolor: 'secondary.light', color: 'secondary.contrastText' }}>
                  <AccountTree />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    AI Agents
                  </Typography>
                  <Typography variant="h4" component="h2">
                    {dashboardData.summary.total_agents}
                  </Typography>
                  <Typography color="textSecondary" variant="body2">
                    Available
                  </Typography>
                </Box>
                <IconButton sx={{ bgcolor: 'warning.light', color: 'warning.contrastText' }}>
                  <SmartToy />
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Completion Rate Trend */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Task Completion Rate Trend
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={dashboardData.completion_rate_trend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="completion_rate"
                      stroke="#2563eb"
                      strokeWidth={2}
                      dot={{ fill: '#2563eb' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Task Status Distribution */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Task Status Distribution
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={pieData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <List>
                {dashboardData.recent_activity.map((activity) => (
                  <ListItem key={activity.id} divider>
                    <ListItemIcon>
                      {getStatusIcon(activity.status)}
                    </ListItemIcon>
                    <ListItemText
                      primary={activity.name}
                      secondary={new Date(activity.created_at).toLocaleString()}
                    />
                    <Chip
                      label={activity.status}
                      color={getStatusColor(activity.status) as any}
                      size="small"
                      variant="outlined"
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;