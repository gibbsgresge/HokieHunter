import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper
} from '@mui/material';

function ChangePassword() {
  const navigate = useNavigate();
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [username, setUsername] = useState(localStorage.getItem('username') || '');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      username,
      old_password: oldPassword,
      new_password: newPassword,
    };

    try {
      const res = await fetch('http://localhost:5000/reset_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        alert('Password changed successfully.');
        navigate('/');
      } else {
        alert(`Error: ${data.error}`);
      }
    } catch (err) {
      console.error(err);
      alert('Server error. Please try again.');
    }
  };

  return (
    <Box sx={{ mt: 12, display: 'flex', justifyContent: 'center' }}>
      <Paper elevation={3} sx={{ p: 5, width: 400, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom align="center">
          Change Password
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            margin="normal"
            disabled // assume user is logged in
          />
          <TextField
            fullWidth
            type="password"
            label="Old Password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
            margin="normal"
          />
          <TextField
            fullWidth
            type="password"
            label="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
            margin="normal"
          />
          <Button fullWidth variant="contained" type="submit" sx={{ mt: 2 }}>
            Update Password
          </Button>
        </form>
      </Paper>
    </Box>
  );
}

export default ChangePassword;
