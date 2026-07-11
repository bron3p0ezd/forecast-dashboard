import { get } from './fetchClient';
import type { Item, ItemsResponse } from '../types/itemTypes';

export const getItems = async (subcategory: string): Promise<Item[]> => {
  const data = await get<ItemsResponse>('/items', {
    query: {
      subcategory,
    },
  });

  return data.items;
};
