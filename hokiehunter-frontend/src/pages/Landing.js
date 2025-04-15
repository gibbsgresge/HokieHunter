// src/pages/Landing.js
import React from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardActionArea, CardContent, Typography, Grid } from '@mui/material'

function Landing() {
  const navigate = useNavigate()

  const cards = [
    { title: 'Users', path: '/users' },
    { title: 'Properties', path: '/properties' },
    { title: 'Reviews (Coming soon)', path: '/reviews', disabled: true }
  ]

  return (
    <Grid container spacing={2} sx={{ mt: 4 }}>
      <Grid item xs={12}>
        <Typography variant="h4" align="center" gutterBottom>
          Hokie Hunters
        </Typography>
      </Grid>
      {cards.map((c) => (
        <Grid item xs={12} sm={4} key={c.title}>
          <Card>
            <CardActionArea
              onClick={() => !c.disabled && navigate(c.path)}
              disabled={c.disabled}
              sx={{ p: 2 }}
            >
              <CardContent>
                <Typography variant="h6" align="center">
                  {c.title}
                </Typography>
                {c.disabled && (
                  <Typography variant="body2" color="text.secondary" align="center">
                    Coming Soon
                  </Typography>
                )}
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
      ))}
    </Grid>
  )
}

export default Landing
