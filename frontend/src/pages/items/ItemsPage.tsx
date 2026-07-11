import { useCallback, useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { Alert, Container, Stack, Typography } from '@mui/material';
import { getItems } from '../../api/itemsApi';
import type { Item } from '../../types/itemTypes';
import { ItemsFilterForm } from './ItemsFilterForm';
import { ItemsList } from './ItemsList';

export function ItemsPage() {
  const [subcategory, setSubcategory] = useState('');
  const [items, setItems] = useState<Item[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadItems = useCallback(async (value: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const loadedItems = await getItems(value);
      setItems(loadedItems);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : 'Не удалось загрузить товары');
      setItems([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadItems('');
  }, [loadItems]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    void loadItems(subcategory);
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

        <ItemsList items={items} isLoading={isLoading} />
      </Stack>
    </Container>
  );
}
