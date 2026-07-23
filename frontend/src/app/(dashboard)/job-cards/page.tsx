"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { JobCard } from "@/types/job-card";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import { ClipboardList, ChevronDown, ChevronUp, Plus, X, Trash2 } from "lucide-react";

const statusColors: Record<string, string> = {
  DRAFT:      "bg-slate-100 text-slate-600",
  DISPATCHED: "bg-blue-100 text-blue-700",
  RETURNED:   "bg-green-100 text-green-700",
  CLOSED:     "bg-purple-100 text-purple-700",
};

interface Event { id: number; name: string; }
interface Item  { id: number; name: string; code: string; available: number; }
interface LineItem { item_id: string; quantity: string; }

export default function JobCardsPage() {
  const [jobCards, setJobCards]     = useState<JobCard[]>([]);
  const [events, setEvents]         = useState<Event[]>([]);
  const [items, setItems]           = useState<Item[]>([]);
  const [loading, setLoading]       = useState(true);
  const [expanded, setExpanded]     = useState<number | null>(null);
  const [showForm, setShowForm]     = useState(false);
  const [saving, setSaving]         = useState(false);
  const [error, setError]           = useState<string | null>(null);

  const [form, setForm] = useState({
    event_id: "",
    notes: "",
    lines: [{ item_id: "", quantity: "" }] as LineItem[]
  });

  const fetchAll = () => {
    setLoading(true);
    Promise.all([
      api.get("/api/v1/job-cards/", { params: { page: 1, per_page: 20 } }),
      api.get("/api/v1/events/"),
      api.get("/api/v1/inventory/", { params: { page: 1, per_page: 100 } }),
    ]).then(([jcRes, evRes, invRes]) => {
      setJobCards(jcRes.data.job_cards);
      setEvents(evRes.data);
      setItems(invRes.data.items);
    }).catch(console.error)
    .finally(() => setLoading(false));
  };

  useEffect(() => { fetchAll(); }, []);

  const addLine = () => setForm(f => ({ ...f, lines: [...f.lines, { item_id: "", quantity: "" }] }));

  const removeLine = (i: number) => setForm(f => ({ ...f, lines: f.lines.filter((_, idx) => idx !== i) }));

  const updateLine = (i: number, field: keyof LineItem, value: string) =>
    setForm(f => ({ ...f, lines: f.lines.map((l, idx) => idx === i ? { ...l, [field]: value } : l) }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.post("/api/v1/job-cards/", {
        event_id: parseInt(form.event_id),
        notes:    form.notes,
        items:    form.lines.map(l => ({ item_id: parseInt(l.item_id), quantity: parseInt(l.quantity) }))
      });
      setShowForm(false);
      setForm({ event_id: "", notes: "", lines: [{ item_id: "", quantity: "" }] });
      fetchAll();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to create job card");
    } finally {
      setSaving(false);
    }
  };

  const handleDispatch = async (id: number) => {
    try {
      await api.post(`/api/v1/job-cards/${id}/dispatch`);
      fetchAll();
    } catch (err: any) {
      alert(err.response?.data?.error || "Dispatch failed");
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Job Cards</h1>
          <p className="text-slate-500 text-sm mt-1">Track item dispatches per event</p>
        </div>
        <Button onClick={() => setShowForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> New Job Card
        </Button>
      </div>

      {/* Create Job Card Form */}
      {showForm && (
        <Card className="mb-6 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-900">Create Job Card</h2>
              <button onClick={() => { setShowForm(false); setError(null); }}>
                <X className="h-4 w-4 text-slate-400 hover:text-slate-600" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Event *</Label>
                  <select
                    className="w-full border border-slate-200 rounded-md px-3 py-2 text-sm bg-white"
                    value={form.event_id}
                    onChange={e => setForm(f => ({...f, event_id: e.target.value}))}
                    required
                  >
                    <option value="">Select event...</option>
                    {events.map(ev => (
                      <option key={ev.id} value={ev.id}>{ev.name}</option>
                    ))}
                  </select>
                </div>

                <div className="space-y-2">
                  <Label>Notes</Label>
                  <Input
                    placeholder="e.g. Setup team: Brian"
                    value={form.notes}
                    onChange={e => setForm(f => ({...f, notes: e.target.value}))}
                  />
                </div>
              </div>

              {/* Line Items */}
              <div>
                <Label className="mb-2 block">Items to Dispatch *</Label>
                <div className="space-y-2">
                  {form.lines.map((line, i) => (
                    <div key={i} className="flex gap-2 items-center">
                      <select
                        className="flex-1 border border-slate-200 rounded-md px-3 py-2 text-sm bg-white"
                        value={line.item_id}
                        onChange={e => updateLine(i, "item_id", e.target.value)}
                        required
                      >
                        <option value="">Select item...</option>
                        {items.map(item => (
                          <option key={item.id} value={item.id}>
                            {item.code} — {item.name} (avail: {item.available})
                          </option>
                        ))}
                      </select>
                      <Input
                        type="number"
                        placeholder="Qty"
                        className="w-24"
                        value={line.quantity}
                        onChange={e => updateLine(i, "quantity", e.target.value)}
                        required
                        min={1}
                      />
                      {form.lines.length > 1 && (
                        <button type="button" onClick={() => removeLine(i)}>
                          <Trash2 className="h-4 w-4 text-red-400 hover:text-red-600" />
                        </button>
                      )}
                    </div>
                  ))}
                </div>
                <Button type="button" variant="outline" size="sm" className="mt-2 gap-1" onClick={addLine}>
                  <Plus className="h-3 w-3" /> Add Item
                </Button>
              </div>

              {error && (
                <div className="text-sm text-red-600 bg-red-50 border border-red-200 px-3 py-2 rounded">
                  {error}
                </div>
              )}

              <div className="flex gap-3 justify-end">
                <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={saving}>
                  {saving ? "Creating..." : "Create Job Card"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Job Cards Table */}
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
              <p className="mb-3">No job cards found</p>
              <Button onClick={() => setShowForm(true)} variant="outline" size="sm">
                Create your first job card
              </Button>
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
                {jobCards.map(jc => (
                  <>
                    <TableRow key={jc.id}>
                      <TableCell className="font-mono font-medium">{jc.reference}</TableCell>
                      <TableCell className="text-slate-500">Event #{jc.event_id}</TableCell>
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
                          <Button size="sm" onClick={() => handleDispatch(jc.id)}>
                            Dispatch
                          </Button>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost" size="sm"
                          onClick={() => setExpanded(expanded === jc.id ? null : jc.id)}
                        >
                          {expanded === jc.id
                            ? <ChevronUp className="h-4 w-4" />
                            : <ChevronDown className="h-4 w-4" />}
                        </Button>
                      </TableCell>
                    </TableRow>

                    {expanded === jc.id && (
                      <TableRow key={`${jc.id}-items`}>
                        <TableCell colSpan={6} className="bg-slate-50 p-4">
                          <p className="text-sm font-medium text-slate-700 mb-2">Items</p>
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
                              {jc.items.map(item => (
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
                            <p className="text-sm text-slate-500 mt-2">Notes: {jc.notes}</p>
                          )}
                        </TableCell>
                      </TableRow>
                    )}
                  </>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
