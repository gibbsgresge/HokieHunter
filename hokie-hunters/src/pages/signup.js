import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  MenuItem
} from '@mui/material';

const roles = ['student', 'landlord'];

function Signup() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('');
  const [major, setMajor] = useState('');
  const [graduationYear, setGraduationYear] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = { username, email, password };
    let endpoint = '';

    if (role === 'student') {
      endpoint = '/signup/student';
      payload.major = major;
      payload.graduation_year = parseInt(graduationYear);
    } else if (role === 'landlord') {
      endpoint = '/signup/landlord';
    } else {
      alert('❌ Invalid role selected.');
      return;
    }

    try {
      const res = await fetch(`http://localhost:5000${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        alert('✅ Signup successful! You can now log in.');
        navigate('/login');
      } else {
        alert(`❌ Signup failed: ${data.error}`);
      }
    } catch (err) {
      console.error(err);
      alert('❌ Server error. Please try again.');
    }
  };

  return (
    <Box sx={{ mt: 12, display: 'flex', justifyContent: 'center' }}>
      <Paper elevation={3} sx={{ p: 5, width: 400, borderRadius: 3 }}>
        <Typography variant="h5" gutterBottom align="center">
          Create Your Account
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
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
            helperText="Use at least 8 characters, including a number and special symbol"
            margin="normal"
          />
          <TextField
            fullWidth
            select
            label="Role"
            value={role}
            onChange={(e) => setRole(e.target.value)}
            required
            margin="normal"
          >
            {roles.map((r) => (
              <MenuItem key={r} value={r}>{r}</MenuItem>
            ))}
          </TextField>

          {role === 'student' && (
            <>
              <TextField
                fullWidth
                label="Major"
                value={major}
                onChange={(e) => setMajor(e.target.value)}
                margin="normal"
              />
              <TextField
                fullWidth
                label="Graduation Year"
                type="number"
                value={graduationYear}
                onChange={(e) => setGraduationYear(e.target.value)}
                margin="normal"
              />
            </>
          )}

          <Button fullWidth variant="contained" type="submit" sx={{ mt: 2 }}>
            Sign Up
          </Button>
          <Button fullWidth sx={{ mt: 1 }} onClick={() => navigate('/login')}>
            Already have an account? Log in
          </Button>
        </form>
      </Paper>
    </Box>
  );
}

export default Signup;
