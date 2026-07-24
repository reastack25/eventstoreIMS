"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function LoginPage() {
  const { login, loading, error } = useAuth();
  const [email, setEmail]         = useState("");
  const [password, setPassword]   = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(email, password);
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-4"
      style={{ backgroundColor: "#0a0a0a" }}
    >
      <div className="w-full max-w-md">

        {/* Logo */}
        <div className="text-center mb-10">
          <div className="inline-flex flex-col items-center">
            <div className="relative mb-2">
              <span
                className="text-5xl font-black tracking-tight text-white"
                style={{ letterSpacing: "-0.02em" }}
              >
                elroyy
              </span>
              <span
                className="text-5xl font-black tracking-tight"
                style={{ color: "#e63329" }}
              >
                //
              </span>
            </div>
            <div className="flex items-center gap-3">
              <div className="h-px w-12" style={{ backgroundColor: "#e63329" }} />
              <span
                className="text-xs font-bold tracking-[0.3em] text-gray-400 uppercase"
              >
                Events
              </span>
              <div className="h-px w-12" style={{ backgroundColor: "#e63329" }} />
            </div>
            <p className="text-gray-500 text-sm mt-3 tracking-wider uppercase">
              Inventory Management
            </p>
          </div>
        </div>

        {/* Card */}
        <div
          className="rounded-xl p-8 border"
          style={{
            backgroundColor: "#111111",
            borderColor: "#2a2a2a"
          }}
        >
          <h2 className="text-white text-xl font-semibold mb-1">Sign in</h2>
          <p className="text-gray-500 text-sm mb-6">
            Enter your credentials to access the system
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">

            <div className="space-y-2">
              <Label className="text-gray-400 text-sm">Email</Label>
              <Input
                type="email"
                placeholder="you@elroyy.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="border text-white placeholder:text-gray-600 focus:ring-1"
                style={{
                  backgroundColor: "#1a1a1a",
                  borderColor: "#2a2a2a",
                }}
              />
            </div>

            <div className="space-y-2">
              <Label className="text-gray-400 text-sm">Password</Label>
              <Input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="border text-white placeholder:text-gray-600 focus:ring-1"
                style={{
                  backgroundColor: "#1a1a1a",
                  borderColor: "#2a2a2a",
                }}
              />
            </div>

            {error && (
              <div
                className="text-sm px-4 py-3 rounded-lg border"
                style={{
                  backgroundColor: "#2a0f0f",
                  borderColor: "#e63329",
                  color: "#f87171"
                }}
              >
                {error}
              </div>
            )}

            <Button
              type="submit"
              className="w-full font-semibold text-white transition-opacity hover:opacity-90"
              style={{ backgroundColor: "#e63329" }}
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
            </Button>

          </form>
        </div>

        <p className="text-center text-gray-600 text-xs mt-6">
          ElroyyIMS · Inventory Management System
        </p>
      </div>
    </div>
  );
}
