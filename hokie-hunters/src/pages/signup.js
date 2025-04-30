import React, { useState } from 'react'
import {
  Box, Button, Container, TextField, Typography, MenuItem, Alert
} from '@mui/material'
import api from '../api'

const roles = ['student', 'landlord']

function Signup() {
  const [form, setForm] = useState({
    username: '', email: '', password: '', role: 'student'
  })
  const [message, setMessage] = useState(null)
  const [errors, setErrors] = useState([])

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const validate = () => {
    const err = []
    if (!form.username.match(/^[a-zA-Z0-9_]{3,}$/)) {
      err.push('Username must be at least 3 characters and contain only letters, numbers, or underscores.')
    }
    if (!form.email.includes('@')) {
      err.push('Enter a valid email.')
    }
    if (form.password.length < 8) {
      err.push('Password must be at least 8 characters.')
    }
    if (!form.password.match(/[A-Z]/) || !form.password.match(/[0-9]/) || !form.password.match(/[\W]/)) {
      err.push('Password must include an uppercase letter, number, and symbol.')
    }
    return err
  }

  const handleSubmit = async () => {
    const validationErrors = validate()
    if (validationErrors.length > 0) {
      setErrors(validationErrors)
      return
    }

    try {
      await api.post('/signup', form)
      setMessage('Account created! You may now log in.')
      setErrors([])
    } catch (err) {
      setMessage(null)
      setErrors([err.response?.data?.error || 'Signup failed.'])
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
          Create an Account
        </Typography>

        {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}
        {errors.length > 0 && errors.map((err, i) => (
          <Alert key={i} severity="error" sx={{ mb: 1 }}>{err}</Alert>
        ))}

        <Box display="flex" flexDirection="column" gap={2}>
          <TextField label="Username" name="username" value={form.username} onChange={handleChange} required />
          <TextField label="Email" name="email" type="email" value={form.email} onChange={handleChange} required />
          <TextField label="Password" name="password" type="password" value={form.password} onChange={handleChange} required />
          <TextField
            select label="Role" name="role" value={form.role} onChange={handleChange}
          >
            {roles.map((role) => (
              <MenuItem key={role} value={role}>
                {role.charAt(0).toUpperCase() + role.slice(1)}
              </MenuItem>
            ))}
          </TextField>
          <Button onClick={handleSubmit} variant="contained" color="primary" size="large">
            Sign Up
          </Button>
        </Box>
      </Box>
    </Container>
  )
}

export default Signup
