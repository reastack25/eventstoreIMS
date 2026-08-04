"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { DashboardSummary } from "@/types/inventory";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Package, Tags, AlertTriangle,
  Wrench, Clock, Truck, Calendar
} from "lucide-react";

export default function DashboardPage() {
  const [summary, setSummary]   = useState<DashboardSummary | null>(null);
  const [overdue, setOverdue]   = useState<any[]>([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/api/v1/dashboard/summary"),
      api.get("/api/v1/job-cards/", { params: { page: 1, per_page: 50 } })
    ]).then(([sumRes, jcRes]) => {
      setSummary(sumRes.data);
      // Find dispatched job cards (overdue = dispatched and older than 1 day)
      const dispatched = jcRes.data.job_cards.filter((jc: any) => jc.status === "DISPATCHED");
      const now        = new Date();
      const overdueJCs = dispatched.filter((jc: any) => {
        const created = new Date(jc.created_at);
        const diff    = (now.getTime() - created.getTime()) / (1000 * 60 * 60 * 24);
        return diff > 1;
      });
      setOverdue(overdueJCs);
    }).catch(console.error)
    .finally(() => setLoading(false));
  }, []);

  const stats = summary ? [
    { label: "Total Items",      value: summary.total_items,      icon: Package,       color: "text-blue-600",   bg: "bg-blue-50"   },
    { label: "Categories",       value: summary.total_categories, icon: Tags,          color: "text-purple-600", bg: "bg-purple-50" },
    { label: "Items Out",        value: (summary as any).items_out || 0, icon: Truck,  color: "text-blue-600",   bg: "bg-blue-50"   },
    { label: "Low Stock",        value: summary.low_stock,        icon: AlertTriangle, color: "text-yellow-600", bg: "bg-yellow-50" },
    { label: "Damaged Items",    value: summary.damaged_items,    icon: Wrench,        color: "text-red-600",    bg: "bg-red-50"    },
    { label: "Pending Returns",  value: summary.pending_returns,  icon: Clock,         color: "text-orange-600", bg: "bg-orange-50" },
    { label: "Active Events",    value: (summary as any).active_events || 0, icon: Calendar, color: "text-green-600", bg: "bg-green-50" },
  ] : [];

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500 text-sm mt-1">Overview of your inventory system</p>
      </div>

      {loading ? (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
          {[...Array(7)].map((_, i) => (
            <Card key={i} className="animate-pulse"><CardContent className="h-24" /></Card>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4 mb-6">
          {stats.map(({ label, value, icon: Icon, color, bg }) => (
            <Card key={label}>
              <CardHeader className="pb-2">
                <CardTitle className="text-xs font-medium text-slate-500">{label}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-2xl font-bold text-slate-900">{value}</span>
                  <div className={`${bg} p-2 rounded-lg`}>
                    <Icon className={`h-4 w-4 ${color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Overdue Returns Alert */}
      {overdue.length > 0 && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="h-5 w-5 text-red-600" />
            <h3 className="font-semibold text-red-700">
              ⚠ {overdue.length} Overdue Return{overdue.length > 1 ? "s" : ""}
            </h3>
          </div>
          <div className="space-y-2">
            {overdue.map(jc => (
              <div
                key={jc.id}
                className="flex items-center justify-between bg-white border border-red-100 rounded-lg px-4 py-2"
              >
                <span className="font-mono text-sm font-medium text-red-700">{jc.reference}</span>
                <span className="text-sm text-slate-600">{jc.event_name || `Event #${jc.event_id}`}</span>
                <span className="text-xs text-red-500">
                  Dispatched {new Date(jc.created_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
