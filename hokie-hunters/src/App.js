import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import theme from './theme'
import Header from './components/Header'
import Login from './pages/login'
import Signup from './pages/signup'
import Landing from './pages/Landing'
import EntityPage from './pages/EntityPage'
import Account from './pages/Account'
import ChangePassword from './pages/changePassword'
function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/entity/:entityName" element={<EntityPage />} />
          <Route path="/account" element={<Account />} />
          <Route path="/change-password" element={<ChangePassword />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default App
