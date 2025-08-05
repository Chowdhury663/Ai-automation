import React from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  Grid,
  Chip,
  Avatar,
} from '@mui/material';
import {
  Add,
  SmartToy,
  Psychology,
  AutoAwesome,
} from '@mui/icons-material';

const Agents: React.FC = () => {
  // Mock data
  const agents = [
    {
      id: 1,
      name: 'Data Analyst',
      type: 'OpenAI GPT-4',
      description: 'Specialized in data analysis and insights generation',
      status: 'active',
      tasks_completed: 156,
      success_rate: 94.2,
      tools: ['data_analysis', 'web_search'],
    },
    {
      id: 2,
      name: 'Content Creator',
      type: 'Anthropic Claude',
      description: 'Expert in content creation and copywriting',
      status: 'active',
      tasks_completed: 89,
      success_rate: 97.8,
      tools: ['web_search', 'file_processor'],
    },
    {
      id: 3,
      name: 'Email Assistant',
      type: 'OpenAI GPT-4',
      description: 'Handles email automation and personalization',
      status: 'inactive',
      tasks_completed: 234,
      success_rate: 91.5,
      tools: ['email_sender', 'scheduler'],
    },
  ];

  const getAgentIcon = (type: string) => {
    if (type.includes('OpenAI')) return <Psychology />;
    if (type.includes('Anthropic')) return <AutoAwesome />;
    return <SmartToy />;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'default';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1" fontWeight={600}>
          AI Agents
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          sx={{ borderRadius: 2 }}
        >
          Create Agent
        </Button>
      </Box>

      <Grid container spacing={3}>
        {agents.map((agent) => (
          <Grid item xs={12} md={6} lg={4} key={agent.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    {getAgentIcon(agent.type)}
                  </Avatar>
                  <Box>
                    <Typography variant="h6" component="h2">
                      {agent.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {agent.type}
                    </Typography>
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {agent.description}
                </Typography>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Chip
                    label={agent.status}
                    color={getStatusColor(agent.status) as any}
                    size="small"
                  />
                  <Typography variant="body2" color="text.secondary">
                    {agent.tasks_completed} tasks
                  </Typography>
                </Box>

                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Success Rate: {agent.success_rate}%
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Tools:
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                    {agent.tools.map((tool) => (
                      <Chip
                        key={tool}
                        label={tool.replace('_', ' ')}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="outlined"
                    size="small"
                    fullWidth
                  >
                    Configure
                  </Button>
                  <Button
                    variant="contained"
                    size="small"
                    fullWidth
                  >
                    Test
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Agents;