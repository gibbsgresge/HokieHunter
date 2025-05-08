import React from 'react';
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const role = localStorage.getItem('role');

  const handleLogout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Typography
          variant="h5"
          component={Link}
          to="/"
          color="inherit"
          sx={{ textDecoration: 'none' }}
        >
          Hokie Hunters
        </Typography>
        <Box>
          {username ? (
            <>
              <Typography
                variant="body1"
                color="inherit"
                sx={{ display: 'inline', mr: 2 }}
              >
                Hello, {username}
              </Typography>

              {(role === 'landlord' || role === 'student' || role === 'admin') && (
                <Button
                  onClick={() => navigate('/account')}
                  color="inherit"
                  sx={{ mr: 2 }}
                >
                  My Account
                </Button>
              )}

              <Button
                onClick={() => navigate('/change-password')}
                color="inherit"
                sx={{ mr: 2 }}
              >
                Change Password
              </Button>

              <Button
                onClick={handleLogout}
                color="secondary"
                variant="outlined"
              >
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Button
                component={Link}
                to="/login"
                color="inherit"
                sx={{ mr: 2 }}
              >
                Log In
              </Button>
              <Button
                component={Link}
                to="/signup"
                color="secondary"
                variant="outlined"
              >
                Sign Up
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
