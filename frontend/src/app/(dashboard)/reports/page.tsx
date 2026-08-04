"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Download, TrendingUp, TrendingDown } from "lucide-react";
import Cookies from "js-cookie";

interface WeeklyReport {
  period:           string;
  events_serviced:  number;
  items_dispatched: number;
  items_returned:   number;
  shortfalls:       number;
  damages_logged:   number;
  damage_cost:      number;
}

interface MonthlyReport {
  period:            string;
  total_events:      number;
  items_moved:       number;
  return_rate:       number;
  damage_incidents:  number;
  damage_cost:       number;
  top_items:         { name: string; total: number }[];
}

export default function ReportsPage() {
  const [weekly, setWeekly]   = useState<WeeklyReport | null>(null);
  const [monthly, setMonthly] = useState<MonthlyReport | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get("/api/v1/dashboard/weekly"),
      api.get("/api/v1/dashboard/monthly"),
    ]).then(([wRes, mRes]) => {
      setWeekly(wRes.data);
      setMonthly(mRes.data);
    }).catch(console.error)
    .finally(() => setLoading(false));
  }, []);

  const handleExport = async (type: "inventory" | "damages") => {
    const token = Cookies.get("access_token");
    const res   = await fetch(
      `http://localhost:5000/api/v1/dashboard/export/${type}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href     = url;
    a.download = `${type}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (loading) return (
    <div className="space-y-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="h-48 bg-slate-100 rounded animate-pulse" />
      ))}
    </div>
  );

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Reports</h1>
          <p className="text-slate-500 text-sm mt-1">Weekly and monthly analytics</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2" onClick={() => handleExport("inventory")}>
            <Download className="h-4 w-4" /> Export Inventory
          </Button>
          <Button variant="outline" className="gap-2 text-red-600 border-red-200 hover:bg-red-50" onClick={() => handleExport("damages")}>
            <Download className="h-4 w-4" /> Export Damages
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-6">
        {/* Weekly Report */}
        <Card className="border-l-4 border-l-amber-400">
          <CardHeader className="pb-2">
            <div className="text-xs font-mono text-amber-600 uppercase tracking-widest">
              Weekly Report
            </div>
            <CardTitle className="text-lg">{weekly?.period}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {weekly && [
                { label: "Events serviced",  value: weekly.events_serviced,  color: "text-blue-600"  },
                { label: "Items dispatched", value: weekly.items_dispatched, color: "text-slate-700" },
                { label: "Items returned",   value: weekly.items_returned,   color: "text-green-600" },
                { label: "Shortfalls",       value: weekly.shortfalls,       color: "text-orange-600"},
                { label: "Damages logged",   value: weekly.damages_logged,   color: "text-red-600"   },
                { label: "Est. damage cost", value: `KES ${weekly.damage_cost.toLocaleString()}`, color: "text-red-600" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex justify-between items-center py-1.5 border-b border-slate-100 last:border-0">
                  <span className="text-sm text-slate-500">{label}</span>
                  <span className={`text-sm font-bold font-mono ${color}`}>{value}</span>
                </div>
              ))}
            </div>
            <Button
              className="w-full mt-4 bg-amber-500 hover:bg-amber-600 text-white gap-2"
              onClick={() => handleExport("inventory")}
            >
              <Download className="h-4 w-4" /> Export CSV
            </Button>
          </CardContent>
        </Card>

        {/* Monthly Report */}
        <Card className="border-l-4 border-l-blue-500">
          <CardHeader className="pb-2">
            <div className="text-xs font-mono text-blue-600 uppercase tracking-widest">
              Monthly Report
            </div>
            <CardTitle className="text-lg">{monthly?.period}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {monthly && [
                { label: "Total events",      value: monthly.total_events,    color: "text-blue-600"  },
                { label: "Items moved",        value: monthly.items_moved,     color: "text-slate-700" },
                { label: "Return rate",        value: `${monthly.return_rate}%`, color: monthly.return_rate > 90 ? "text-green-600" : "text-orange-600" },
                { label: "Damage incidents",   value: monthly.damage_incidents, color: "text-orange-600"},
                { label: "Total damage cost",  value: `KES ${monthly.damage_cost.toLocaleString()}`, color: "text-red-600" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex justify-between items-center py-1.5 border-b border-slate-100 last:border-0">
                  <span className="text-sm text-slate-500">{label}</span>
                  <span className={`text-sm font-bold font-mono ${color}`}>{value}</span>
                </div>
              ))}
            </div>
            <Button
              className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white gap-2"
              onClick={() => handleExport("damages")}
            >
              <Download className="h-4 w-4" /> Export Damages CSV
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Top Items */}
      {monthly && monthly.top_items.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Top 5 Most Dispatched Items</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {monthly.top_items.map((item, i) => {
                const max = monthly.top_items[0].total;
                const pct = Math.round((item.total / max) * 100);
                return (
                  <div key={i} className="flex items-center gap-3">
                    <span className="text-sm font-mono text-slate-400 w-4">{i + 1}</span>
                    <span className="text-sm text-slate-700 w-40 truncate">{item.name}</span>
                    <div className="flex-1 h-2 bg-slate-100 rounded-full">
                      <div
                        className="h-2 bg-blue-500 rounded-full"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className="text-sm font-mono text-slate-500 w-16 text-right">
                      {item.total} out
                    </span>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
