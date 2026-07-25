export interface JobCardItem {
  id:                 number;
  item_id:            number;
  item_name:          string;
  quantity_requested: number;
  quantity_returned:  number;
  quantity_damaged:   number;
}

export interface JobCard {
  id:         number;
  reference:  string;
  event_id:   number;
  event_name: string | null;
  status:     "DRAFT" | "DISPATCHED" | "RETURNED" | "CLOSED";
  notes:      string;
  created_at: string;
  items:      JobCardItem[];
}
