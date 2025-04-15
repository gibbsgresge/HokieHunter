// src/App.js
import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing'
import EntityPage from './pages/EntityPage'
import Navbar from './components/Navbar'
import { Container } from '@mui/material'

function App() {
  return (
    <>
      <Navbar />
      <Container maxWidth="md" sx={{ my: 4 }}>
        <Routes>
          <Route path="/" element={<Landing />} />
          {/* Dynamic route: /users, /properties, /anything */}
          <Route path="/:entity" element={<EntityPage />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
