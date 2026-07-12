import { useCallback, useEffect, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { Alert, Container, Stack, Typography } from '@mui/material';
import { getItems } from '../../api/itemsApi';
import type { Item } from '../../types/itemTypes';
import { ItemsFilterForm } from './ItemsFilterForm';
import { ItemsList } from './ItemsList';

const ITEMS_PAGE_SIZE = 20;

export function ItemsPage() {
  const [subcategory, setSubcategory] = useState('');
  const [items, setItems] = useState<Item[]>([]);
  const [page, setPage] = useState(1);
  const [hasNextPage, setHasNextPage] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loaderRef = useRef<HTMLDivElement | null>(null);

  const loadItems = useCallback(
    async (pageToLoad: number, reset = false) => {
      if (isLoading) return;
      if (!hasNextPage && !reset) return;

      setIsLoading(true);
      setError(null);

      try {
        const loadedItems = await getItems({
          subcategory,
          page: pageToLoad,
          pageSize: ITEMS_PAGE_SIZE,
        });

        setItems((current) =>
          reset ? loadedItems.items : [...current, ...loadedItems.items]
        );

        setHasNextPage(loadedItems.has_next);
        setPage(pageToLoad);
      } catch (caughtError) {
        setError(
          caughtError instanceof Error
            ? caughtError.message
            : 'Не удалось загрузить товары'
        );
      } finally {
        setIsLoading(false);
      }
    },
    [subcategory, isLoading, hasNextPage]
  );

  useEffect(() => {
    void loadItems(1, true);
  }, []);

  useEffect(() => {
    const node = loaderRef.current;

    if (!node) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (
          entries[0].isIntersecting &&
          hasNextPage &&
          !isLoading
        ) {
          void loadItems(page + 1);
        }
      },
      {
        rootMargin: '200px',
      }
    );

    observer.observe(node);

    return () => observer.disconnect();
  }, [page, hasNextPage, isLoading, loadItems]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setPage(1);
    setHasNextPage(true);

    void loadItems(1, true);
  };

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Typography component="h1" variant="h4">
          Товары
        </Typography>
    
        <ItemsFilterForm
          subcategory={subcategory}
          isLoading={isLoading}
          onSubcategoryChange={setSubcategory}
          onSubmit={handleSubmit}
        />

        {error ? <Alert severity="error">{error}</Alert> : null}

        <ItemsList
          items={items}
          isLoading={isLoading && items.length === 0}
          isLoadingMore={isLoading && items.length > 0}
        />

        <div ref={loaderRef} />
      </Stack>
    </Container>
  );
}
