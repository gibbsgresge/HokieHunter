import React from 'react'
import { Container, Typography, Box } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import EntityCard from '../components/EntityCard'

const sections = [
  { label: 'Browse Properties', path: '/entity/property', image: '/images/apartment.jpg' },
  { label: 'Lease Transfers', path: '/entity/leasetransfer', image: '/images/leasetransfer.jpg' },
  { label: 'Reviews', path: '/entity/review', image: '/images/review.jpg' },
  { label: 'Favorites', path: '/entity/favorite', image: '/images/favorite.jpg' },
  { label: 'Roommate Search', path: '/entity/roommatesearch', image: '/images/roomate.jpg' },
  { label: 'Commute Info', path: '/entity/commute', image: '/images/commute.jpg' },
  { label: 'Moving Services', path: '/entity/movingservices', image: '/images/movingservice.jpg' },
  { label: 'Safety Features', path: '/entity/safetyfeatures', image: '/images/safety.jpg' }
]

function Landing() {
  const navigate = useNavigate()

  return (
    <Container maxWidth="lg" sx={{ mt: 10 }}>
      <Box
        sx={{
          p: 4,
          border: '1px solid #ccc',
          borderRadius: 2,
          backgroundColor: '#fff',
          boxShadow: 3,
          mb: 4
        }}
      >
        <Typography
          variant="h4"
          sx={{
            fontWeight: 600,
            fontFamily: 'Georgia, serif',
            color: 'primary.main',
            mb: 2
          }}
        >
          Hi! What can we help you find today?
        </Typography>
        <Typography sx={{ fontFamily: 'Georgia, serif', color: 'text.secondary' }}>
          Explore housing options, lease transfers, reviews, and more, all in one place.
        </Typography>
      </Box>

      <Box
  sx={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: 3,
    mt: 4
  }}
>
  {sections.map((section) => (
    <Box key={section.label} sx={{ width: 300 }}>
      <EntityCard
        label={section.label}
        imageUrl={section.image}
        onClick={() => navigate(section.path)}
      />
    </Box>
  ))}
</Box>

    </Container>
  )
}

export default Landing
