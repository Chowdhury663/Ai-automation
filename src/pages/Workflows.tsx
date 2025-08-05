import React from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add,
  PlayArrow,
  Pause,
  MoreVert,
  Edit,
  Delete,
  AccountTree,
} from '@mui/icons-material';

const Workflows: React.FC = () => {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  // Mock data
  const workflows = [
    {
      id: 1,
      name: 'Data Analysis Workflow',
      description: 'Automated data analysis and reporting',
      status: 'active',
      tasks: 3,
      lastRun: '2024-01-15T10:30:00Z',
    },
    {
      id: 2,
      name: 'Content Generation',
      description: 'AI-powered content creation',
      status: 'paused',
      tasks: 4,
      lastRun: '2024-01-14T15:45:00Z',
    },
    {
      id: 3,
      name: 'Email Automation',
      description: 'Automated email campaigns',
      status: 'active',
      tasks: 2,
      lastRun: '2024-01-15T09:15:00Z',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'paused': return 'warning';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          Workflows
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          sx={{ borderRadius: 2 }}
        >
          Create Workflow
        </Button>
      </Box>

      <Grid container spacing={3}>
        {workflows.map((workflow) => (
          <Grid item xs={12} md={6} lg={4} key={workflow.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <AccountTree sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="h6" component="h2">
                      {workflow.name}
                    </Typography>
                  </Box>
                  <IconButton size="small" onClick={handleMenuClick}>
                    <MoreVert />
                  </IconButton>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {workflow.description}
                </Typography>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Chip
                    label={workflow.status}
                    color={getStatusColor(workflow.status) as any}
                    size="small"
                  />
                  <Typography variant="body2" color="text.secondary">
                    {workflow.tasks} tasks
                  </Typography>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Last run: {new Date(workflow.lastRun).toLocaleString()}
                </Typography>

                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={workflow.status === 'active' ? <Pause /> : <PlayArrow />}
                  >
                    {workflow.status === 'active' ? 'Pause' : 'Run'}
                  </Button>
                  <Button
                    variant="outlined"
                    size="small"
                    startIcon={<Edit />}
                  >
                    Edit
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>
          <Edit sx={{ mr: 1 }} />
          Edit
        </MenuItem>
        <MenuItem onClick={handleMenuClose}>
          <Delete sx={{ mr: 1 }} />
          Delete
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Workflows;