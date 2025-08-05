import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Paper,
} from '@mui/material';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
} from 'recharts';

const Analytics: React.FC = () => {
  // Mock data
  const taskTrendData = [
    { date: '2024-01-01', completed: 45, failed: 5, total: 50 },
    { date: '2024-01-02', completed: 52, failed: 3, total: 55 },
    { date: '2024-01-03', completed: 48, failed: 7, total: 55 },
    { date: '2024-01-04', completed: 61, failed: 4, total: 65 },
    { date: '2024-01-05', completed: 58, failed: 2, total: 60 },
    { date: '2024-01-06', completed: 67, failed: 3, total: 70 },
    { date: '2024-01-07', completed: 72, failed: 8, total: 80 },
  ];

  const agentPerformanceData = [
    { name: 'Data Analyst', tasks: 156, success_rate: 94.2 },
    { name: 'Content Creator', tasks: 89, success_rate: 97.8 },
    { name: 'Email Assistant', tasks: 234, success_rate: 91.5 },
    { name: 'Web Scraper', tasks: 67, success_rate: 88.1 },
  ];

  const workflowDistributionData = [
    { name: 'Data Analysis', value: 35, color: '#2563eb' },
    { name: 'Content Generation', value: 25, color: '#7c3aed' },
    { name: 'Email Automation', value: 20, color: '#10b981' },
    { name: 'Web Scraping', value: 15, color: '#f59e0b' },
    { name: 'Other', value: 5, color: '#6b7280' },
  ];

  const executionTimeData = [
    { hour: '00:00', avg_time: 2.3 },
    { hour: '04:00', avg_time: 1.8 },
    { hour: '08:00', avg_time: 4.2 },
    { hour: '12:00', avg_time: 5.1 },
    { hour: '16:00', avg_time: 3.7 },
    { hour: '20:00', avg_time: 2.9 },
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" fontWeight={600} sx={{ mb: 4 }}>
        Analytics
      </Typography>

      <Grid container spacing={3}>
        {/* Task Completion Trend */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Task Completion Trend
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={taskTrendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="completed"
                      stackId="1"
                      stroke="#10b981"
                      fill="#10b981"
                      fillOpacity={0.6}
                    />
                    <Area
                      type="monotone"
                      dataKey="failed"
                      stackId="1"
                      stroke="#ef4444"
                      fill="#ef4444"
                      fillOpacity={0.6}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Workflow Distribution */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Workflow Distribution
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={workflowDistributionData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={5}
                      dataKey="value"
                    >
                      {workflowDistributionData.map((entry, index) => (
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

        {/* Agent Performance */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Agent Performance
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={agentPerformanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="success_rate" fill="#2563eb" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Average Execution Time */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Execution Time by Hour
              </Typography>
              <Box sx={{ height: 300, mt: 2 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={executionTimeData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="avg_time"
                      stroke="#7c3aed"
                      strokeWidth={2}
                      dot={{ fill: '#7c3aed' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* System Health Metrics */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Health Metrics
              </Typography>
              <Grid container spacing={3} sx={{ mt: 1 }}>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="success.main">
                      98.5%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Uptime
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary.main">
                      2.3s
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Avg Response Time
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="warning.main">
                      1,234
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Active Tasks
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="error.main">
                      0.8%
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Error Rate
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;