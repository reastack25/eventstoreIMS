// src/types/inventory.ts

export interface Item {
  id:        number;
  code:      string;
  name:      string;
  quantity:  number;
  available: number;
  unit:      string;
  status:    string;
  image_url: string | null;
}

export interface PaginatedItems {
  items: Item[];
  meta: {
    page:        number;
    per_page:    number;
    total_items: number;
    total_pages: number;
    has_next:    boolean;
    has_prev:    boolean;
  };
}

export interface DashboardSummary {
  total_items:      number;
  total_categories: number;
  low_stock:        number;
  damaged_items:    number;
  pending_returns:  number;
}