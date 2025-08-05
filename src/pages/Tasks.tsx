import React from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  PlayArrow,
  Schedule,
  Visibility,
} from '@mui/icons-material';

const Tasks: React.FC = () => {
  // Mock data
  const tasks = [
    {
      id: 1,
      name: 'Analyze Sales Data',
      workflow: 'Data Analysis Workflow',
      agent: 'Data Analyst',
      status: 'completed',
      created_at: '2024-01-15T10:30:00Z',
      completed_at: '2024-01-15T10:35:00Z',
      duration: 5,
    },
    {
      id: 2,
      name: 'Generate Blog Post',
      workflow: 'Content Generation',
      agent: 'Content Creator',
      status: 'running',
      created_at: '2024-01-15T11:00:00Z',
      completed_at: null,
      duration: null,
    },
    {
      id: 3,
      name: 'Send Welcome Emails',
      workflow: 'Email Automation',
      agent: 'Email Assistant',
      status: 'failed',
      created_at: '2024-01-15T09:15:00Z',
      completed_at: '2024-01-15T09:18:00Z',
      duration: 3,
    },
    {
      id: 4,
      name: 'Process Customer Feedback',
      workflow: 'Data Analysis Workflow',
      agent: 'Data Analyst',
      status: 'pending',
      created_at: '2024-01-15T11:30:00Z',
      completed_at: null,
      duration: null,
    },
    {
      id: 5,
      name: 'Create Product Description',
      workflow: 'Content Generation',
      agent: 'Content Creator',
      status: 'completed',
      created_at: '2024-01-15T08:45:00Z',
      completed_at: '2024-01-15T08:52:00Z',
      duration: 7,
    },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle color="success" />;
      case 'failed': return <Error color="error" />;
      case 'running': return <PlayArrow color="warning" />;
      default: return <Schedule color="disabled" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'failed': return 'error';
      case 'running': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Tasks
        </Typography>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Task</TableCell>
              <TableCell>Workflow</TableCell>
              <TableCell>Agent</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Duration</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task) => (
              <TableRow key={task.id} hover>
                <TableCell>
                  <Typography variant="body2" fontWeight={500}>
                    {task.name}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="text.secondary">
                    {task.workflow}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="text.secondary">
                    {task.agent}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {getStatusIcon(task.status)}
                    <Chip
                      label={task.status}
                      color={getStatusColor(task.status) as any}
                      size="small"
                      sx={{ ml: 1 }}
                    />
                  </Box>
                </TableCell>
                <TableCell>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(task.created_at).toLocaleString()}
                  </Typography>
                </TableCell>
                <TableCell>
                  {task.duration ? (
                    <Typography variant="body2" color="text.secondary">
                      {task.duration}m
                    </Typography>
                  ) : task.status === 'running' ? (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LinearProgress sx={{ width: 60, mr: 1 }} />
                      <Typography variant="body2" color="text.secondary">
                        Running
                      </Typography>
                    </Box>
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      -
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <IconButton size="small">
                    <Visibility />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default Tasks;