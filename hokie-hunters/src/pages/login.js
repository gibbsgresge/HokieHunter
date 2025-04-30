import React, { useState } from 'react'
import {
  Container, TextField, Button, Typography, Alert, Box
} from '@mui/material'
import api from '../api'

function Login() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleLogin = async () => {
    try {
      await api.post('/login', form)
      setError(null)
      setSuccess(true)
    } catch (err) {
      setSuccess(false)
      setError(err.response?.data?.error || 'Login failed.')
    }
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 10 }}>
      <Box
        sx={{
          p: 4,
          border: '1px solid #ccc',
          borderRadius: 2,
          backgroundColor: '#fff',
          boxShadow: 3
        }}
      >
        <Typography variant="h5" sx={{ fontWeight: 600, fontFamily: 'Georgia, serif' }} gutterBottom>
          Welcome Back
        </Typography>

        {success && <Alert severity="success" sx={{ mb: 2 }}>Logged in successfully!</Alert>}
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Box display="flex" flexDirection="column" gap={2}>
          <TextField label="Username" name="username" value={form.username} onChange={handleChange} />
          <TextField label="Password" name="password" type="password" value={form.password} onChange={handleChange} />
          <Button onClick={handleLogin} variant="contained" color="primary" size="large">
            Log In
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

export default Login
