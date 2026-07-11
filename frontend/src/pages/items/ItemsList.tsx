import { Box, CircularProgress, List, ListItem, ListItemText, Paper } from '@mui/material';
import type { Item } from '../../types/itemTypes';

type ItemsListProps = {
  items: Item[];
  isLoading: boolean;
};

export function ItemsList({ items, isLoading }: ItemsListProps) {
  return (
    <Paper variant="outlined">
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <List disablePadding>
          {items.length > 0 ? (
            items.map((item) => (
              <ListItem divider key={item.sku}>
                <ListItemText
                  primary={item.name}
                  secondary={`SKU: ${item.sku} | Subcategory: ${item.subcategory}`}
                />
              </ListItem>
            ))
          ) : (
            <ListItem>
              <ListItemText primary="Товары не найдены" />
            </ListItem>
          )}
        </List>
      )}
    </Paper>
  );
}
