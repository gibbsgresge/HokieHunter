// src/components/CrudDialog.js
import React, { useState, useEffect } from 'react'
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField
} from '@mui/material'

function CrudDialog({ open, onClose, mode, data, onSubmit, fields }) {
  const [form, setForm] = useState({})

  useEffect(() => {
    if (data) {
      setForm(data)
    } else {
      setForm({})
    }
  }, [data])

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = () => {
    onSubmit(form)
  }

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>{mode === 'create' ? 'Create' : 'Update'}</DialogTitle>
      <DialogContent
        sx={{
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
          mt: 1
        }}
      >
        {fields.map((field) => (
          <TextField
            key={field}
            label={field}
            name={field}
            value={form[field] || ''}
            onChange={handleChange}
          />
        ))}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button variant="contained" onClick={handleSubmit}>
          {mode === 'create' ? 'Create' : 'Update'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}

export default CrudDialog
