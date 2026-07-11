import type { FormEvent } from 'react';
import { Box, Button, Stack, TextField } from '@mui/material';

type ItemsFilterFormProps = {
  subcategory: string;
  isLoading: boolean;
  onSubcategoryChange: (value: string) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
};

export function ItemsFilterForm({
  subcategory,
  isLoading,
  onSubcategoryChange,
  onSubmit,
}: ItemsFilterFormProps) {
  return (
    <Box component="form" onSubmit={onSubmit}>
      <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
        <TextField
          fullWidth
          label="Введите: подкатегорию"
          name="subcategory"
          value={subcategory}
          onChange={(event) => onSubcategoryChange(event.target.value)}
        />
        <Button disabled={isLoading} type="submit" variant="contained">
          Найти
        </Button>
      </Stack>
    </Box>
  );
}
