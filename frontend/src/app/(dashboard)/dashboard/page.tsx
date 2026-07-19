"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { DashboardSummary } from "@/types/inventory";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Package,
  Tags,
  AlertTriangle,
  Wrench,
  Clock
} from "lucide-react";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/v1/dashboard/summary")
      .then((res) => setSummary(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const stats = summary
    ? [
        {
          label: "Total Items",
          value: summary.total_items,
          icon:  Package,
          color: "text-blue-600",
          bg:    "bg-blue-50"
        },
        {
          label: "Categories",
          value: summary.total_categories,
          icon:  Tags,
          color: "text-purple-600",
          bg:    "bg-purple-50"
        },
        {
          label: "Low Stock",
          value: summary.low_stock,
          icon:  AlertTriangle,
          color: "text-yellow-600",
          bg:    "bg-yellow-50"
        },
        {
          label: "Damaged Items",
          value: summary.damaged_items,
          icon:  Wrench,
          color: "text-red-600",
          bg:    "bg-red-50"
        },
        {
          label: "Pending Returns",
          value: summary.pending_returns,
          icon:  Clock,
          color: "text-orange-600",
          bg:    "bg-orange-50"
        },
      ]
    : [];

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <p className="text-slate-500 text-sm mt-1">
          Overview of your inventory system
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[...Array(5)].map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="h-24" />
            </Card>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {stats.map(({ label, value, icon: Icon, color, bg }) => (
            <Card key={label}>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-slate-500">
                  {label}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-3xl font-bold text-slate-900">
                    {value}
                  </span>
                  <div className={`${bg} p-2 rounded-lg`}>
                    <Icon className={`h-5 w-5 ${color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
