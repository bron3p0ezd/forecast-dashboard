import { useEffect, useLayoutEffect, useMemo, useState } from 'react';
import {
  Box,
  CssBaseline,
  FormControlLabel,
  Switch,
  ThemeProvider,
} from '@mui/material';
import type { PaletteMode } from '@mui/material';
import { ItemDetailPage } from '../pages/items/ItemDetailPage';
import { ItemsPage } from '../pages/items/ItemsPage';
import { NotFoundPage } from '../pages/not-found/NotFoundPage';
import { createAppTheme } from './theme';

const ITEMS_PATH = '/items';
const THEME_STORAGE_KEY = 'forecast-dashboard-theme';

const useIsomorphicLayoutEffect = typeof window === 'undefined' ? useEffect : useLayoutEffect;

const getInitialThemeMode = (): PaletteMode => {
  const storedMode = window.localStorage.getItem(THEME_STORAGE_KEY);

  if (storedMode === 'light' || storedMode === 'dark') {
    return storedMode;
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

function AppRoutes() {
  const [path, setPath] = useState(() => window.location.pathname);
  const itemMatch = path.match(/^\/items\/([^/]+)\/?$/);

  useIsomorphicLayoutEffect(() => {
    if (path === '/') {
      window.history.replaceState(null, '', ITEMS_PATH);
      setPath(ITEMS_PATH);
    }
  }, [path]);

  useEffect(() => {
    const handlePopState = () => {
      setPath(window.location.pathname);
    };

    window.addEventListener('popstate', handlePopState);

    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, []);

  if (path === '/') {
    return null;
  }

  if (path === ITEMS_PATH) {
    return <ItemsPage />;
  }

  if (itemMatch) {
    return <ItemDetailPage sku={decodeURIComponent(itemMatch[1])} />;
  }

  return <NotFoundPage />;
}

function App() {
  const [mode, setMode] = useState<PaletteMode>(getInitialThemeMode);
  const theme = useMemo(() => createAppTheme(mode), [mode]);

  const handleThemeChange = () => {
    setMode((currentMode) => {
      const nextMode = currentMode === 'light' ? 'dark' : 'light';
      window.localStorage.setItem(THEME_STORAGE_KEY, nextMode);
      return nextMode;
    });
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          position: 'fixed',
          right: 24,
          top: 16,
          zIndex: (currentTheme) => currentTheme.zIndex.tooltip,
        }}
      >
        <FormControlLabel
          control={<Switch checked={mode === 'dark'} onChange={handleThemeChange} />}
          label="Тёмная тема"
        />
      </Box>
      <AppRoutes />
    </ThemeProvider>
  );
}

export default App;
