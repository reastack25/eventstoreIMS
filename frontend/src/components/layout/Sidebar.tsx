"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { User } from "@/types/auth";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Package,
  ClipboardList,
  Calendar,
  LogOut,
  ChevronRight
} from "lucide-react";
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/dashboard", label: "Dashboard",  icon: LayoutDashboard },
  { href: "/inventory", label: "Inventory",  icon: Package },
  { href: "/job-cards", label: "Job Cards",  icon: ClipboardList },
  { href: "/events",    label: "Events",     icon: Calendar },
];

const BRAND_RED = "#e63329";

export default function Sidebar({ user }: { user: User }) {
  const pathname   = usePathname();
  const { logout } = useAuth();

  return (
    <aside
      className="w-64 flex flex-col h-screen border-r"
      style={{ backgroundColor: "#0a0a0a", borderColor: "#1a1a1a" }}
    >
      {/* Logo */}
      <div
        className="p-6 border-b"
        style={{ borderColor: "#1a1a1a" }}
      >
        <div className="flex flex-col">
          <div className="flex items-baseline gap-0.5">
            <span className="text-2xl font-black text-white tracking-tight">
              elroyy
            </span>
            <span
              className="text-2xl font-black"
              style={{ color: BRAND_RED }}
            >
              //
            </span>
          </div>
          <div className="flex items-center gap-2 mt-0.5">
            <div
              className="h-px flex-1"
              style={{ backgroundColor: BRAND_RED }}
            />
            <span className="text-xs tracking-[0.25em] text-gray-500 uppercase">
              Events
            </span>
            <div
              className="h-px flex-1"
              style={{ backgroundColor: BRAND_RED }}
            />
          </div>
          <p className="text-gray-600 text-xs mt-1 tracking-widest uppercase">
            IMS
          </p>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                active
                  ? "text-white"
                  : "text-gray-500 hover:text-white hover:bg-white/5"
              )}
              style={active ? {
                backgroundColor: "#1a0a0a",
                borderLeft: `3px solid ${BRAND_RED}`,
                paddingLeft: "calc(0.75rem - 3px)"
              } : {}}
            >
              <Icon
                className="h-4 w-4 flex-shrink-0"
                style={active ? { color: BRAND_RED } : {}}
              />
              {label}
              {active && (
                <ChevronRight
                  className="h-3 w-3 ml-auto"
                  style={{ color: BRAND_RED }}
                />
              )}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div
        className="p-4 border-t"
        style={{ borderColor: "#1a1a1a" }}
      >
        <div className="flex items-center gap-3 mb-3">
          <div
            className="rounded-full h-8 w-8 flex items-center justify-center text-sm font-bold text-white flex-shrink-0"
            style={{ backgroundColor: BRAND_RED }}
          >
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">
              {user.full_name}
            </p>
            <span
              className="text-xs px-1.5 py-0.5 rounded font-medium"
              style={{
                backgroundColor: "#1a0a0a",
                color: BRAND_RED,
                border: `1px solid ${BRAND_RED}33`
              }}
            >
              {user.role}
            </span>
          </div>
        </div>
        <button
          onClick={logout}
          className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-500 hover:text-white hover:bg-white/5 transition-colors"
        >
          <LogOut className="h-4 w-4" />
          Sign out
        </button>
      </div>
    </aside>
  );
}
