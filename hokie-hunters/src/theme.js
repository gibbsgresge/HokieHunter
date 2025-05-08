import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#861F41'
    },
    secondary: {
      main: '#E5751F' 
    },
    background: {
      default: '#f5f1eb' 
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
