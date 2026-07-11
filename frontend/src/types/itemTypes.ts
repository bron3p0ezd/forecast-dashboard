export type Item = {
  sku: string;
  name: string;
  subcategory: string;
};

export type ItemsResponse = {
  items: Item[];
};
