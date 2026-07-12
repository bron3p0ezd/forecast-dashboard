export type Item = {
  sku: string;
  name: string;
  subcategory: string;
};

export type ItemsResponse = {
  items: Item[];
  has_next: boolean;
};

export type ItemRow = {
  date: string;
  fact: number | null;
  sales: number | null;
  math: number;
  ml: number;
  ruki: number | null;
};

export type ItemMetrics = {
  fa: number;
  bias: number;
  bias_direction: 'up' | 'down';
};

export type ItemRowsResponse = {
  rows: ItemRow[];
  metrics: ItemMetrics;
};
