import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  AccountTree,
  SmartToy,
  Task,
  Analytics,
  Settings,
} from '@mui/icons-material';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const menuItems = [
  {
    text: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
  },
  {
    text: 'Workflows',
    icon: <AccountTree />,
    path: '/workflows',
  },
  {
    text: 'AI Agents',
    icon: <SmartToy />,
    path: '/agents',
  },
  {
    text: 'Tasks',
    icon: <Task />,
    path: '/tasks',
  },
  {
    text: 'Analytics',
    icon: <Analytics />,
    path: '/analytics',
  },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleNavigation = (path: string) => {
    navigate(path);
  };

  const drawerContent = (
    <Box sx={{ width: 240, pt: 1 }}>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => handleNavigation(item.path)}
              sx={{
                mx: 1,
                borderRadius: 1,
                '&.Mui-selected': {
                  backgroundColor: 'primary.main',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'primary.dark',
                  },
                  '& .MuiListItemIcon-root': {
                    color: 'white',
                  },
                },
                '&:hover': {
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <ListItemIcon
                sx={{
                  color: location.pathname === item.path ? 'white' : 'text.secondary',
                }}
              >
                {item.icon}
              </ListItemIcon>
              <ListItemText
                primary={item.text}
                sx={{
                  '& .MuiListItemText-primary': {
                    fontWeight: location.pathname === item.path ? 600 : 400,
                  },
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      
      <Divider sx={{ mx: 2, my: 2 }} />
      
      <List>
        <ListItem disablePadding>
          <ListItemButton
            sx={{
              mx: 1,
              borderRadius: 1,
              '&:hover': {
                backgroundColor: 'action.hover',
              },
            }}
          >
            <ListItemIcon>
              <Settings />
            </ListItemIcon>
            <ListItemText primary="Settings" />
          </ListItemButton>
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          mt: 8,
          borderRight: '1px solid',
          borderColor: 'divider',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;