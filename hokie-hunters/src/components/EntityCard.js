// src/components/EntityCard.js
import React from 'react'
import { Card, Typography, Box, CardActionArea, Avatar } from '@mui/material'
import { Home, Reviews, Group, Favorite, DirectionsBus, LocalShipping, Shield, SwapHoriz, Spa } from '@mui/icons-material'

const iconMap = {
  'Browse Properties': <Home sx={{ fontSize: 32 }} />,
  'Lease Transfers': <SwapHoriz sx={{ fontSize: 32 }} />,
  'Reviews': <Reviews sx={{ fontSize: 32 }} />,
  'Favorites': <Favorite sx={{ fontSize: 32 }} />,
  'Roommate Search': <Group sx={{ fontSize: 32 }} />,
  'Commute Info': <DirectionsBus sx={{ fontSize: 32 }} />,
  'Moving Services': <LocalShipping sx={{ fontSize: 32 }} />,
  'Safety Features': <Shield sx={{ fontSize: 32 }} />,
  'Amenities': <Spa sx={{ fontSize: 32 }} /> 
}


function EntityCard({ label, imageUrl, onClick }) {
  return (
    <Card
      sx={{
        height: '100%',
        border: '1px solid #ccc',
        borderRadius: 2,
        backgroundColor: '#fff',
        boxShadow: 2,
        fontFamily: 'Georgia, serif'
      }}
    >
      <CardActionArea onClick={onClick} sx={{ p: 2 }}>
        <Box display="flex" alignItems="center" gap={2}>
          <Avatar sx={{ bgcolor: 'primary.main', width: 56, height: 56 }}>
            {iconMap[label] || '?'}
          </Avatar>
          <Box>
            <Typography variant="h6" color="primary" gutterBottom>
              {label}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Click to explore or manage.
            </Typography>
          </Box>
        </Box>
        {imageUrl && (
          <Box mt={2}>
            <img
              src={imageUrl}
              alt={label}
              style={{ width: '100%', height: 120, objectFit: 'cover', borderRadius: '8px' }}
            />
          </Box>
        )}
      </CardActionArea>
    </Card>
  )
}

export default EntityCard
