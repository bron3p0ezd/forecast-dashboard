import {
  Box,
  CircularProgress,
  Link,
  List,
  ListItem,
  ListItemText,
  Paper,
  Typography,
} from '@mui/material';
import type { Item } from '../../types/itemTypes';

type ItemsListProps = {
  items: Item[];
  isLoading: boolean;
  isLoadingMore: boolean;
};

const navigateTo = (path: string) => {
  window.history.pushState(null, '', path);
  window.dispatchEvent(new PopStateEvent('popstate'));
};

export function ItemsList({
  items,
  isLoading,
  isLoadingMore,
}: ItemsListProps) {
  return (
    <Paper variant="outlined">
      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <List disablePadding>
            {items.length > 0 ? (
              items.map((item) => (
                <ListItem divider key={item.sku}>
                  <ListItemText
                    primary={
                      <Link
                        href={`/items/${encodeURIComponent(item.sku)}`}
                        onClick={(event) => {
                          event.preventDefault();
                          navigateTo(`/items/${encodeURIComponent(item.sku)}`);
                        }}
                      >
                        {item.sku}
                      </Link>
                    }
                    secondary={
                      <Box component="span" sx={{ display: 'block' }}>
                        <Typography
                          color="text.secondary"
                          component="span"
                          display="block"
                          variant="body2"
                        >
                          {item.name}
                        </Typography>
                        <Typography
                          color="text.secondary"
                          component="span"
                          display="block"
                          variant="body2"
                        >
                          Подкатегория: {item.subcategory}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
              ))
            ) : (
              <ListItem>
                <ListItemText primary="Товары не найдены" />
              </ListItem>
            )}
          </List>

          {isLoadingMore ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
              <CircularProgress size={24} />
            </Box>
          ) : null}
        </>
      )}
    </Paper>
  );
}
