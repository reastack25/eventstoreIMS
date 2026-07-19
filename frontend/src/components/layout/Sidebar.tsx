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
import { Badge } from "@/components/ui/badge";

const navItems = [
  { href: "/dashboard", label: "Dashboard",  icon: LayoutDashboard },
  { href: "/inventory", label: "Inventory",  icon: Package },
  { href: "/job-cards", label: "Job Cards",  icon: ClipboardList },
  { href: "/events",    label: "Events",     icon: Calendar },
];

export default function Sidebar({ user }: { user: User }) {
  const pathname    = usePathname();
  const { logout }  = useAuth();

  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col h-screen">

      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-2">
          <div className="bg-white text-slate-900 p-1.5 rounded-md">
            <Package className="h-5 w-5" />
          </div>
          <span className="font-bold text-lg">ElroyyIMS</span>
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
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                active
                  ? "bg-white text-slate-900"
                  : "text-slate-400 hover:text-white hover:bg-slate-800"
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
              {active && <ChevronRight className="h-4 w-4 ml-auto" />}
            </Link>
          );
        })}
      </nav>

      {/* User */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-3 mb-3">
          <div className="bg-slate-700 rounded-full h-8 w-8 flex items-center justify-center text-sm font-bold">
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user.full_name}</p>
            <Badge variant="secondary" className="text-xs mt-0.5">
              {user.role}
            </Badge>
          </div>
        </div>
        <Button
          variant="ghost"
          size="sm"
          className="w-full text-slate-400 hover:text-white hover:bg-slate-800 justify-start"
          onClick={logout}
        >
          <LogOut className="h-4 w-4 mr-2" />
          Sign out
        </Button>
      </div>

    </aside>
  );
}
