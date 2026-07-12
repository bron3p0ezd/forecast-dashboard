import { get } from './fetchClient';
import type { Item, ItemRowsResponse, ItemsResponse } from '../types/itemTypes';

type GetItemsParams = {
  subcategory: string;
  page: number;
  pageSize: number;
};

export const getItem = async (sku: string): Promise<Item> =>
  get<Item>(`/items/${encodeURIComponent(sku)}`);

export const getItems = async ({
  subcategory,
  page,
  pageSize,
}: GetItemsParams): Promise<ItemsResponse> =>
  get<ItemsResponse>('/items', {
    query: {
      subcategory,
      page,
      page_size: pageSize,
    },
  });

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
