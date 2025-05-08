import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper
} from '@mui/material';

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  //  Redirect if already logged in
  useEffect(() => {
    const isLoggedIn = localStorage.getItem('username');
    if (isLoggedIn) {
      navigate('/');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = { username, password };

    try {
      const res = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
      
        localStorage.setItem('username', data.username || username);
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('role', data.role);

        alert(` Welcome, ${data.username || username}!`);
        navigate('/');
      } else {
        alert(` Login failed: ${data.error}`);
      }
    } catch (err) {
      console.error(err);
      alert(' Server error. Please try again.');
    }
  };

  return (
    <Box sx={{ mt: 12, display: 'flex', justifyContent: 'center' }}>
      <Paper elevation={3} sx={{ p: 5, width: 400, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom align="center">
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            margin="normal"
          />
          <TextField
            fullWidth
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            margin="normal"
          />
          <Button fullWidth variant="contained" type="submit" sx={{ mt: 2 }}>
            Log In
          </Button>
          <Button fullWidth sx={{ mt: 1 }} onClick={() => navigate('/signup')}>
            Don't have an account? Sign up
          </Button>
        </form>
      </Paper>
    </Box>
  );
}

export default Login;
