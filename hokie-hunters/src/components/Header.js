import React from 'react'
import { AppBar, Toolbar, Typography, Box, Button } from '@mui/material'
import { Link } from 'react-router-dom'

function Header() {
  return (
    <AppBar position="static" color="primary" elevation={0}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Typography variant="h5" component={Link} to="/" color="inherit" sx={{ textDecoration: 'none' }}>
          Hokie Hunters
        </Typography>
        <Box>
          <Button component={Link} to="/login" color="inherit" sx={{ mr: 2 }}>
            Log In
          </Button>
          <Button component={Link} to="/signup" color="secondary" variant="outlined">
            Sign Up
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header
