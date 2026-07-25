"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import { AlertTriangle, Plus, X } from "lucide-react";

interface Damage {
  id:             number;
  item_id:        number;
  item_name:      string;
  item_code:      string;
  quantity:       number;
  reason:         string;
  reporter_name:  string;
  estimated_cost: number;
  job_card_ref:   string;
  created_at:     string;
}

interface Item { id: number; name: string; code: string; available: number; }

const emptyForm = {
  item_id:        "",
  quantity:       "",
  reason:         "",
  estimated_cost: "",
  job_card_ref:   ""
};

export default function DamagePage() {
  const [damages, setDamages]     = useState<Damage[]>([]);
  const [items, setItems]         = useState<Item[]>([]);
  const [totalCost, setTotalCost] = useState(0);
  const [loading, setLoading]     = useState(true);
  const [showForm, setShowForm]   = useState(false);
  const [saving, setSaving]       = useState(false);
  const [error, setError]         = useState<string | null>(null);
  const [form, setForm]           = useState(emptyForm);

  const fetchDamages = () => {
    setLoading(true);
    Promise.all([
      api.get("/api/v1/damages/"),
      api.get("/api/v1/inventory/", { params: { page: 1, per_page: 100 } })
    ]).then(([dmgRes, invRes]) => {
      setDamages(dmgRes.data.damages);
      setTotalCost(dmgRes.data.total_cost);
      setItems(invRes.data.items);
    }).catch(console.error)
    .finally(() => setLoading(false));
  };

  useEffect(() => { fetchDamages(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.post("/api/v1/damages/", {
        item_id:        parseInt(form.item_id),
        quantity:       parseInt(form.quantity),
        reason:         form.reason,
        estimated_cost: parseFloat(form.estimated_cost) || 0,
        job_card_ref:   form.job_card_ref
      });
      setShowForm(false);
      setForm(emptyForm);
      fetchDamages();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to report damage");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Damage Log</h1>
          <p className="text-slate-500 text-sm mt-1">
            Track damaged and lost items
          </p>
        </div>
        <Button
          onClick={() => setShowForm(true)}
          className="gap-2 bg-red-600 hover:bg-red-700"
        >
          <Plus className="h-4 w-4" /> Report Damage
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <Card>
          <CardContent className="pt-4">
            <p className="text-sm text-slate-500">Total Incidents</p>
            <p className="text-3xl font-bold text-slate-900 mt-1">{damages.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <p className="text-sm text-slate-500">Est. Total Cost</p>
            <p className="text-3xl font-bold text-red-600 mt-1">
              KES {totalCost.toLocaleString()}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4">
            <p className="text-sm text-slate-500">This Month</p>
            <p className="text-3xl font-bold text-orange-600 mt-1">
              {damages.filter(d => new Date(d.created_at).getMonth() === new Date().getMonth()).length}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Report Damage Form */}
      {showForm && (
        <Card className="mb-6 border-red-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-900">Report Damage</h2>
              <button onClick={() => { setShowForm(false); setError(null); }}>
                <X className="h-4 w-4 text-slate-400 hover:text-slate-600" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">

              <div className="space-y-2">
                <Label>Item *</Label>
                <select
                  className="w-full border border-slate-200 rounded-md px-3 py-2 text-sm bg-white"
                  value={form.item_id}
                  onChange={e => setForm(f => ({...f, item_id: e.target.value}))}
                  required
                >
                  <option value="">Select item...</option>
                  {items.map(item => (
                    <option key={item.id} value={item.id}>
                      {item.code} — {item.name} (avail: {item.available})
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <Label>Quantity Damaged *</Label>
                <Input
                  type="number" min={1} placeholder="0"
                  value={form.quantity}
                  onChange={e => setForm(f => ({...f, quantity: e.target.value}))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label>Reason *</Label>
                <Input
                  placeholder="e.g. Broken during transport"
                  value={form.reason}
                  onChange={e => setForm(f => ({...f, reason: e.target.value}))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label>Estimated Cost (KES)</Label>
                <Input
                  type="number" min={0} placeholder="0"
                  value={form.estimated_cost}
                  onChange={e => setForm(f => ({...f, estimated_cost: e.target.value}))}
                />
              </div>

              <div className="space-y-2">
                <Label>Job Card Reference</Label>
                <Input
                  placeholder="e.g. JC-001"
                  value={form.job_card_ref}
                  onChange={e => setForm(f => ({...f, job_card_ref: e.target.value}))}
                />
              </div>

              {error && (
                <div className="col-span-2 text-sm text-red-600 bg-red-50 border border-red-200 px-3 py-2 rounded">
                  {error}
                </div>
              )}

              <div className="col-span-2 flex gap-3 justify-end">
                <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                  Cancel
                </Button>
                <Button
                  type="submit"
                  className="bg-red-600 hover:bg-red-700"
                  disabled={saving}
                >
                  {saving ? "Reporting..." : "Report Damage"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Damage Table */}
      <Card>
        <CardContent className="pt-4">
          {loading ? (
            <div className="space-y-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-12 bg-slate-100 rounded animate-pulse" />
              ))}
            </div>
          ) : damages.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <AlertTriangle className="h-10 w-10 mx-auto mb-3 text-slate-300" />
              <p>No damage records found</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Item</TableHead>
                  <TableHead>Qty</TableHead>
                  <TableHead>Reason</TableHead>
                  <TableHead>Job Card</TableHead>
                  <TableHead>Reported By</TableHead>
                  <TableHead className="text-right">Est. Cost (KES)</TableHead>
                  <TableHead>Date</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {damages.map(d => (
                  <TableRow key={d.id}>
                    <TableCell>
                      <div className="font-medium text-slate-900">{d.item_name}</div>
                      <div className="text-xs text-slate-400 font-mono">{d.item_code}</div>
                    </TableCell>
                    <TableCell>
                      <span className="text-red-600 font-bold">{d.quantity}</span>
                    </TableCell>
                    <TableCell className="text-slate-600 max-w-xs truncate">
                      {d.reason || "—"}
                    </TableCell>
                    <TableCell className="font-mono text-sm text-slate-500">
                      {d.job_card_ref || "—"}
                    </TableCell>
                    <TableCell className="text-slate-600">
                      {d.reporter_name || "—"}
                    </TableCell>
                    <TableCell className="text-right font-mono font-medium text-red-600">
                      {d.estimated_cost > 0 ? d.estimated_cost.toLocaleString() : "—"}
                    </TableCell>
                    <TableCell className="text-slate-500 text-sm">
                      {new Date(d.created_at).toLocaleDateString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
