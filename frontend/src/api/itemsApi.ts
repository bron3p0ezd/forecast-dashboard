import { get } from './fetchClient';
import type { Item, ItemRowsResponse, ItemsResponse } from '../types/itemTypes';

export const getItem = async (sku: string): Promise<Item> =>
  get<Item>(`/items/${encodeURIComponent(sku)}`);

export const getItems = async (subcategory: string): Promise<Item[]> => {
  const data = await get<ItemsResponse>('/items', {
    query: {
      subcategory,
    },
  });

  return data.items;
};

export const getItemRows = async (
  sku: string,
  dateFrom: string,
  dateTo: string,
): Promise<ItemRowsResponse> =>
  get<ItemRowsResponse>(`/items/${encodeURIComponent(sku)}/rows`, {
    query: {
      date_from: dateFrom,
      date_to: dateTo,
    },
  });
