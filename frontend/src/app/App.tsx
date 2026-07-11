import { CssBaseline, ThemeProvider } from '@mui/material';
import { ItemsPage } from '../pages/items/ItemsPage';
import { theme } from './theme';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ItemsPage />
    </ThemeProvider>
  );
}

export default App;
