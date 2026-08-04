"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { User } from "@/types/auth";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard, Package, ClipboardList,
  Calendar, AlertTriangle, BarChart2, LogOut, ChevronRight
} from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard",  icon: LayoutDashboard },
  { href: "/inventory", label: "Inventory",  icon: Package },
  { href: "/job-cards", label: "Job Cards",  icon: ClipboardList },
  { href: "/events",    label: "Events",     icon: Calendar },
  { href: "/damages",   label: "Damage Log", icon: AlertTriangle },
  { href: "/reports",   label: "Reports",    icon: BarChart2 },
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
      <div className="p-5 border-b flex justify-center" style={{ borderColor: "#1a1a1a" }}>
        <Image
          src="/elroyy-logo.png"
          alt="Elroyy Events"
          width={140} height={60}
          className="object-contain"
          priority
        />
      </div>

      <div className="px-5 py-2 border-b" style={{ borderColor: "#1a1a1a" }}>
        <p className="text-xs tracking-widest text-gray-600 uppercase text-center">
          Inventory Management
        </p>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map(({ href, label, icon: Icon }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                active ? "text-white" : "text-gray-500 hover:text-white hover:bg-white/5"
              )}
              style={active ? {
                backgroundColor: "#1a0808",
                borderLeft: `3px solid ${BRAND_RED}`,
                paddingLeft: "calc(0.75rem - 3px)"
              } : {}}
            >
              <Icon className="h-4 w-4 flex-shrink-0" style={active ? { color: BRAND_RED } : {}} />
              {label}
              {active && <ChevronRight className="h-3 w-3 ml-auto" style={{ color: BRAND_RED }} />}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t" style={{ borderColor: "#1a1a1a" }}>
        <div className="flex items-center gap-3 mb-3">
          <div
            className="rounded-full h-8 w-8 flex items-center justify-center text-sm font-bold text-white flex-shrink-0"
            style={{ backgroundColor: BRAND_RED }}
          >
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-white truncate">{user.full_name}</p>
            <span
              className="text-xs px-1.5 py-0.5 rounded font-medium"
              style={{ backgroundColor: "#1a0808", color: BRAND_RED, border: `1px solid ${BRAND_RED}33` }}
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
