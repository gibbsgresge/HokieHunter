import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#861F41' // Chicago Maroon
    },
    secondary: {
      main: '#E5751F' // Burnt Orange
    },
    background: {
      default: '#f5f1eb' // old-money parchment style
    }
  },
  typography: {
    fontFamily: 'Georgia, serif',
    h5: {
      fontWeight: 600
    }
  }
})

export default theme
