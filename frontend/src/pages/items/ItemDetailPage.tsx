import { useCallback, useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Container,
  Link,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { FetchError } from '../../api/fetchClient';
import { getItem, getItemRows } from '../../api/itemsApi';
import { NotFoundPage } from '../not-found/NotFoundPage';
import type { Item, ItemRowsResponse } from '../../types/itemTypes';

type ItemDetailPageProps = {
  sku: string;
};

const navigateTo = (path: string) => {
  window.history.pushState(null, '', path);
  window.dispatchEvent(new PopStateEvent('popstate'));
};

const formatBiasDirection = (direction: 'up' | 'down') => (direction === 'up' ? '↑' : '↓');

export function ItemDetailPage({ sku }: ItemDetailPageProps) {
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [item, setItem] = useState<Item | null>(null);
  const [rowsResponse, setRowsResponse] = useState<ItemRowsResponse | null>(null);
  const [isItemLoading, setIsItemLoading] = useState(false);
  const [isRowsLoading, setIsRowsLoading] = useState(false);
  const [isNotFound, setIsNotFound] = useState(false);
  const [itemError, setItemError] = useState<string | null>(null);
  const [rowsError, setRowsError] = useState<string | null>(null);

  const isDateRangeValid =
    dateFrom &&
    dateTo &&
    new Date(dateFrom) <= new Date(dateTo);

  useEffect(() => {
    let isActive = true;

    const loadItem = async () => {
      setIsItemLoading(true);
      setIsNotFound(false);
      setItem(null);
      setRowsResponse(null);
      setItemError(null);
      setRowsError(null);

      try {
        const loadedItem = await getItem(sku);

        if (isActive) {
          setItem(loadedItem);
        }
      } catch (caughtError) {
        if (isActive) {
          if (caughtError instanceof FetchError && caughtError.status === 404) {
            setIsNotFound(true);
          } else {
            setItemError(
              caughtError instanceof Error ? caughtError.message : 'Failed to load item.',
            );
          }
          setItem(null);
        }
      } finally {
        if (isActive) {
          setIsItemLoading(false);
        }
      }
    };

    void loadItem();

    return () => {
      isActive = false;
    };
  }, [sku]);

  const chartRows =
    rowsResponse?.rows.map((row) => ({
      ...row,
      fact: row.fact ?? undefined,
      sales: row.sales ?? undefined,
      ruki: row.ruki ?? undefined,
  })) ?? [];

  const handleSubmit = useCallback(
    async (event: FormEvent<HTMLFormElement>) => {
      event.preventDefault();
      setIsRowsLoading(true);
      setRowsError(null);

      try {
        const loadedRows = await getItemRows(sku, dateFrom, dateTo);
        setRowsResponse(loadedRows);
      } catch (caughtError) {
        setRowsError(caughtError instanceof Error ? caughtError.message : 'Failed to load rows.');
        setRowsResponse(null);
      } finally {
        setIsRowsLoading(false);
      }
    },
    [dateFrom, dateTo, sku],
  );

  if (isNotFound) {
    return <NotFoundPage />;
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Stack spacing={3}>
        <Box>
          <Link
            href="/items"
            onClick={(event) => {
              event.preventDefault();
              navigateTo('/items');
            }}
          >
            Вернуться к товарам
          </Link>
        </Box>

        <Stack spacing={1}>
          <Typography component="h1" variant="h4">
            Товар {sku}
          </Typography>
          {isItemLoading ? (
            <Box sx={{ display: 'flex', py: 1 }}>
              <CircularProgress size={24} />
            </Box>
          ) : null}
          {item ? (
            <Paper variant="outlined" sx={{ p: 2 }}>
              <Stack spacing={0.5}>
                <Typography variant="h6">{item.name}</Typography>
                <Typography color="text.secondary" variant="body2">
                  SKU: {item.sku}
                </Typography>
                <Typography color="text.secondary" variant="body2">
                  Подкатегория: {item.subcategory}
                </Typography>
              </Stack>
            </Paper>
          ) : null}
          {itemError ? <Alert severity="warning">{itemError}</Alert> : null}
        </Stack>

        <Paper component="form" onSubmit={handleSubmit} variant="outlined" sx={{ p: 2 }}>
          <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
            <TextField
              fullWidth
              InputLabelProps={{ shrink: true }}
              label="От"
              name="date_from"
              type="date"
              value={dateFrom}
              onChange={(event) => setDateFrom(event.target.value)}
            />
            <TextField
              fullWidth
              type="date"
              label="До"
              InputLabelProps={{ shrink: true }}
              value={dateTo}
              onChange={(event) => setDateTo(event.target.value)}
              error={Boolean(dateFrom && dateTo && !isDateRangeValid)}
              helperText={
                  dateFrom && dateTo && !isDateRangeValid
                  ? 'Дата окончания должна быть не раньше даты начала'
                  : ' '
              }
            />
            <Button
              disabled={isRowsLoading || !dateFrom || !dateTo || !isDateRangeValid }
              sx={{ minWidth: 140 }}
              type="submit"
              variant="contained"
            >
              Загрузить график
            </Button>
          </Stack>
        </Paper>

        {rowsError ? <Alert severity="error">{rowsError}</Alert> : null}

        {isRowsLoading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : null}

        {rowsResponse ? (
          <Stack spacing={3}>
            <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
              <Paper variant="outlined" sx={{ flex: 1, p: 2 }}>
                <Typography color="text.secondary" variant="body2">
                  FA
                </Typography>
                <Typography variant="h5">{rowsResponse.metrics.fa}%</Typography>
              </Paper>
              <Paper variant="outlined" sx={{ flex: 1, p: 2 }}>
                <Typography color="text.secondary" variant="body2">
                  Bias
                </Typography>
                <Typography variant="h5">{rowsResponse.metrics.bias}%</Typography>
              </Paper>
              <Paper variant="outlined" sx={{ flex: 1, p: 2 }}>
                <Typography color="text.secondary" variant="body2">
                  Направление
                </Typography>
                <Typography variant="h5">
                  {formatBiasDirection(rowsResponse.metrics.bias_direction)}
                </Typography>
              </Paper>
            </Stack>

            <Paper variant="outlined" sx={{ height: 420, p: 2 }}>
              {chartRows.length > 0 ? (
                <ResponsiveContainer height="100%" width="100%">
                  <LineChart data={chartRows} margin={{ bottom: 8, left: 0, right: 16, top: 12 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" minTickGap={28} />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line dataKey="fact" name="Fact" stroke="#1976d2" type="monotone" />
                    <Line dataKey="sales" name="Sales" stroke="#2e7d32" type="monotone" />
                    <Line dataKey="math" name="Math" stroke="#ed6c02" type="monotone" />
                    <Line dataKey="ml" name="ML" stroke="#9c27b0" type="monotone" />
                    <Line dataKey="ruki" name="Ruki" stroke="#d32f2f" type="monotone" />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <Box
                  sx={{
                    alignItems: 'center',
                    display: 'flex',
                    height: '100%',
                    justifyContent: 'center',
                  }}
                >
                  <Typography color="text.secondary">Нет данных за этот период.</Typography>
                </Box>
              )}
            </Paper>
          </Stack>
        ) : null}
      </Stack>
    </Container>
  );
}
