// src/pages/Landing.js
import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Grid,
  Card,
  CardActionArea,
  CardContent,
  Typography,
  Box
} from '@mui/material'

// master list of entity types
const entities = [
  'users', 'students', 'landlords', 'admin', 'property',
  'review', 'favorite', 'roommatesearch', 'list', 'amenities',
  'leasetransfer', 'commute', 'movingservices', 'safetyfeatures', 'message'
]

function Landing() {
  const navigate = useNavigate()

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" align="center" gutterBottom>
        Hokie Hunters Database GUI
      </Typography>
      <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
        Click a table below to view its records
      </Typography>

      <Grid container spacing={3}>
        {entities.map((entity) => (
          <Grid item xs={12} sm={6} md={4} key={entity}>
            <Card sx={{ height: 120 }}>
              <CardActionArea
                onClick={() => navigate(`/${entity}`)}
                sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
              >
                <CardContent>
                  <Typography variant="h6" align="center" sx={{ textTransform: 'capitalize' }}>
                    {entity}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

export default Landing
