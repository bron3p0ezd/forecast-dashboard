import { useEffect, useLayoutEffect, useState } from 'react';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { ItemDetailPage } from '../pages/items/ItemDetailPage';
import { ItemsPage } from '../pages/items/ItemsPage';
import { NotFoundPage } from '../pages/not-found/NotFoundPage';
import { theme } from './theme';

const ITEMS_PATH = '/items';

const useIsomorphicLayoutEffect = typeof window === 'undefined' ? useEffect : useLayoutEffect;

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
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppRoutes />
    </ThemeProvider>
  );
}

export default App;
