"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { JobCard } from "@/types/job-card";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ClipboardList, ChevronDown, ChevronUp } from "lucide-react";

const statusColors: Record<string, string> = {
  DRAFT:      "bg-slate-100 text-slate-600",
  DISPATCHED: "bg-blue-100 text-blue-700",
  RETURNED:   "bg-green-100 text-green-700",
  CLOSED:     "bg-purple-100 text-purple-700",
};

export default function JobCardsPage() {
  const [jobCards, setJobCards]   = useState<JobCard[]>([]);
  const [loading, setLoading]     = useState(true);
  const [expanded, setExpanded]   = useState<number | null>(null);
  const [page, setPage]           = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchJobCards = (p = 1) => {
    setLoading(true);
    api.get("/api/v1/job-cards/", { params: { page: p, per_page: 20 } })
      .then((res) => {
        setJobCards(res.data.job_cards);
        setTotalPages(res.data.meta.total_pages);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchJobCards(); }, []);

  const handleDispatch = async (id: number) => {
    try {
      await api.post(`/api/v1/job-cards/${id}/dispatch`);
      fetchJobCards(page);
    } catch (err: any) {
      alert(err.response?.data?.error || "Dispatch failed");
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Job Cards</h1>
          <p className="text-slate-500 text-sm mt-1">
            Track item dispatches per event
          </p>
        </div>
      </div>

      <Card>
        <CardContent className="pt-4">
          {loading ? (
            <div className="space-y-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-14 bg-slate-100 rounded animate-pulse" />
              ))}
            </div>
          ) : jobCards.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <ClipboardList className="h-10 w-10 mx-auto mb-3 text-slate-300" />
              <p>No job cards found</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Reference</TableHead>
                  <TableHead>Event</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                  <TableHead></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {jobCards.map((jc) => (
                  <>
                    <TableRow key={jc.id}>
                      <TableCell className="font-mono font-medium">
                        {jc.reference}
                      </TableCell>
                      <TableCell className="text-slate-500">
                        Event #{jc.event_id}
                      </TableCell>
                      <TableCell>
                        <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusColors[jc.status]}`}>
                          {jc.status}
                        </span>
                      </TableCell>
                      <TableCell className="text-slate-500 text-sm">
                        {new Date(jc.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        {jc.status === "DRAFT" && (
                          <Button
                            size="sm"
                            onClick={() => handleDispatch(jc.id)}
                          >
                            Dispatch
                          </Button>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => setExpanded(expanded === jc.id ? null : jc.id)}
                        >
                          {expanded === jc.id
                            ? <ChevronUp className="h-4 w-4" />
                            : <ChevronDown className="h-4 w-4" />
                          }
                        </Button>
                      </TableCell>
                    </TableRow>

                    {/* Expanded items */}
                    {expanded === jc.id && (
                      <TableRow key={`${jc.id}-items`}>
                        <TableCell colSpan={6} className="bg-slate-50 p-4">
                          <p className="text-sm font-medium text-slate-700 mb-2">
                            Items
                          </p>
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="text-slate-500 text-left">
                                <th className="pb-1">Item</th>
                                <th className="pb-1 text-right">Requested</th>
                                <th className="pb-1 text-right">Returned</th>
                                <th className="pb-1 text-right">Damaged</th>
                              </tr>
                            </thead>
                            <tbody>
                              {jc.items.map((item) => (
                                <tr key={item.id} className="border-t border-slate-200">
                                  <td className="py-1">{item.item_name}</td>
                                  <td className="py-1 text-right">{item.quantity_requested}</td>
                                  <td className="py-1 text-right text-green-600">{item.quantity_returned}</td>
                                  <td className="py-1 text-right text-red-600">{item.quantity_damaged}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                          {jc.notes && (
                            <p className="text-sm text-slate-500 mt-2">
                              Notes: {jc.notes}
                            </p>
                          )}
                        </TableCell>
                      </TableRow>
                    )}
                  </>
                ))}
              </TableBody>
            </Table>
          )}

          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4 pt-4 border-t">
              <p className="text-sm text-slate-500">Page {page} of {totalPages}</p>
              <div className="flex gap-2">
                <Button
                  variant="outline" size="sm"
                  onClick={() => { setPage(p => p - 1); fetchJobCards(page - 1); }}
                  disabled={page === 1}
                >
                  Previous
                </Button>
                <Button
                  variant="outline" size="sm"
                  onClick={() => { setPage(p => p + 1); fetchJobCards(page + 1); }}
                  disabled={page === totalPages}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
