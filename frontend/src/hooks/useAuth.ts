// src/hooks/useAuth.ts

"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Cookies from "js-cookie";
import api from "@/lib/api";
import { User, LoginResponse } from "@/types/auth";

export function useAuth() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState<string | null>(null);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      const res = await api.post<LoginResponse>("/api/v1/auth/login", {
        email,
        password,
      });

      const { access_token, user } = res.data;

      // Store token and user
      Cookies.set("access_token", access_token, { expires: 1 });
      localStorage.setItem("user", JSON.stringify(user));

      router.push("/dashboard");
    } catch (err: any) {
      setError(
        err.response?.data?.error || "Login failed. Check your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    Cookies.remove("access_token");
    localStorage.removeItem("user");
    router.push("/login");
  };

  const getUser = (): User | null => {
    if (typeof window === "undefined") return null;
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  };

  return { login, logout, getUser, loading, error };
}