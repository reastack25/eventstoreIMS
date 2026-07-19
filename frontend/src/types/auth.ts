// src/types/auth.ts

export interface User {
  id:        number;
  full_name: string;
  email:     string;
  role:      "ADMIN" | "STORE_MANAGER" | "STORE_KEEPER" | "FIELD_STAFF";
}

export interface LoginResponse {
  access_token: string;
  user:         User;
  message:      string;
}

export interface AuthState {
  user:  User | null;
  token: string | null;
}