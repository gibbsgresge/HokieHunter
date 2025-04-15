// src/components/DataCard.js
import React from 'react'
import { Card, CardContent, Typography, IconButton, Stack } from '@mui/material'
import EditIcon from '@mui/icons-material/Edit'
import DeleteIcon from '@mui/icons-material/Delete'

function DataCard({ itemData, onEdit, onDelete }) {
  const entries = Object.entries(itemData || {})

  return (
    <Card
      sx={{
        height: 250, 
        width: 250,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        borderRadius: 2,
        boxShadow: 2,
      }}
    >
      <CardContent sx={{ overflow: 'auto' }}>
        {entries.map(([key, val]) => (
          <Typography key={key} variant="body2" noWrap>
            <strong>{key}:</strong> {val}
          </Typography>
        ))}
      </CardContent>
      <Stack direction="row" spacing={1} sx={{ ml: 1.5, mb: 1.5 }}>
        <IconButton onClick={onEdit}>
          <EditIcon />
        </IconButton>
        <IconButton onClick={onDelete} color="error">
          <DeleteIcon />
        </IconButton>
      </Stack>
    </Card>
  )
}

export default DataCard
