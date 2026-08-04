"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Users } from "lucide-react";

interface StaffMember {
  id:          number;
  full_name:   string;
  email:       string;
  role:        string;
  total_jobs:  number;
  dispatched:  number;
  returned:    number;
  damages:     number;
  damage_cost: number;
  recent_jobs: {
    reference:  string;
    event_name: string;
    status:     string;
    created_at: string;
  }[];
}

const statusColors: Record<string, string> = {
  DRAFT:      "bg-slate-100 text-slate-600",
  DISPATCHED: "bg-blue-100 text-blue-700",
  RETURNED:   "bg-green-100 text-green-700",
  CLOSED:     "bg-purple-100 text-purple-700",
};

const roleColors: Record<string, string> = {
  ADMIN:         "bg-red-100 text-red-700",
  STORE_MANAGER: "bg-purple-100 text-purple-700",
  STORE_KEEPER:  "bg-blue-100 text-blue-700",
  FIELD_STAFF:   "bg-green-100 text-green-700",
};

export default function StaffPage() {
  const [staff, setStaff]     = useState<StaffMember[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/v1/users/")
      .then(res => setStaff(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div className="grid grid-cols-2 gap-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="h-48 bg-slate-100 rounded animate-pulse" />
      ))}
    </div>
  );

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Staff</h1>
        <p className="text-slate-500 text-sm mt-1">
          Accountability and dispatch history per employee
        </p>
      </div>

      {staff.length === 0 ? (
        <div className="text-center py-12 text-slate-500">
          <Users className="h-10 w-10 mx-auto mb-3 text-slate-300" />
          <p>No staff found</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4">
          {staff.map(s => {
            const initial    = s.full_name.charAt(0).toUpperCase();
            const scoreColor = s.damages === 0
              ? "text-green-600" : s.damages <= 2
              ? "text-amber-600" : "text-red-600";

            return (
              <Card key={s.id}>
                <CardContent className="pt-6">
                  {/* Header */}
                  <div className="flex items-center gap-4 mb-5">
                    <div
                      className="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold text-white flex-shrink-0"
                      style={{ background: "linear-gradient(135deg, #8A6E2A, #C9A84C)" }}
                    >
                      {initial}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-slate-900 text-base">{s.full_name}</h3>
                      <p className="text-slate-500 text-xs truncate">{s.email}</p>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block ${roleColors[s.role] || "bg-slate-100 text-slate-600"}`}>
                        {s.role.replace("_", " ")}
                      </span>
                    </div>
                    <div className="text-center">
                      <div className={`text-2xl font-bold font-mono ${scoreColor}`}>
                        {s.damages}
                      </div>
                      <div className="text-xs text-slate-400">damages</div>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="grid grid-cols-3 gap-3 mb-5">
                    {[
                      { label: "Total Jobs", value: s.total_jobs,  color: "text-blue-600"  },
                      { label: "Returned",   value: s.returned,    color: "text-green-600" },
                      { label: "Damage Cost",value: s.damage_cost > 0 ? `${(s.damage_cost/1000).toFixed(1)}K` : "0", color: s.damage_cost > 0 ? "text-red-600" : "text-slate-400" },
                    ].map(({ label, value, color }) => (
                      <div key={label} className="bg-slate-50 rounded-lg p-3 text-center">
                        <div className={`text-lg font-bold font-mono ${color}`}>{value}</div>
                        <div className="text-xs text-slate-400 mt-0.5">{label}</div>
                      </div>
                    ))}
                  </div>

                  {/* Recent Jobs */}
                  {s.recent_jobs.length > 0 && (
                    <div>
                      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2">
                        Recent Assignments
                      </p>
                      <div className="space-y-2">
                        {s.recent_jobs.map(job => (
                          <div
                            key={job.reference}
                            className="flex items-center justify-between py-1.5 border-b border-slate-100 last:border-0"
                          >
                            <div>
                              <span className="text-xs font-mono text-amber-600 mr-2">
                                {job.reference}
                              </span>
                              <span className="text-sm text-slate-700">
                                {job.event_name || "—"}
                              </span>
                            </div>
                            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${statusColors[job.status] || ""}`}>
                              {job.status}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
