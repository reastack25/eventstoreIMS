"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Calendar, Plus, X } from "lucide-react";
import {
  Table, TableBody, TableCell,
  TableHead, TableHeader, TableRow,
} from "@/components/ui/table";

interface Event {
  id:          number;
  name:        string;
  client_name: string;
  event_date:  string;
  venue:       string;
  status:      string;
}

const statusColors: Record<string, string> = {
  UPCOMING:  "bg-blue-100 text-blue-700",
  ONGOING:   "bg-green-100 text-green-700",
  COMPLETED: "bg-slate-100 text-slate-600",
  CANCELLED: "bg-red-100 text-red-700",
};

const empty = { name:"", client_name:"", event_date:"", venue:"", return_date:"" };

export default function EventsPage() {
  const [events, setEvents]     = useState<Event[]>([]);
  const [loading, setLoading]   = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm]         = useState(empty);
  const [saving, setSaving]     = useState(false);
  const [error, setError]       = useState<string|null>(null);

  const fetchEvents = () => {
    setLoading(true);
    api.get("/api/v1/events/")
      .then(res => setEvents(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchEvents(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api.post("/api/v1/events/", form);
      setShowForm(false);
      setForm(empty);
      fetchEvents();
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to create event");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Events</h1>
          <p className="text-slate-500 text-sm mt-1">All scheduled events</p>
        </div>
        <Button onClick={() => setShowForm(true)} className="gap-2">
          <Plus className="h-4 w-4" /> New Event
        </Button>
      </div>

      {/* Create Event Form */}
      {showForm && (
        <Card className="mb-6 border-blue-200">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-slate-900">Create New Event</h2>
              <button onClick={() => { setShowForm(false); setForm(empty); setError(null); }}>
                <X className="h-4 w-4 text-slate-400 hover:text-slate-600" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Event Name *</Label>
                <Input
                  placeholder="e.g. Kamau Wedding"
                  value={form.name}
                  onChange={e => setForm(f => ({...f, name: e.target.value}))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label>Client Name</Label>
                <Input
                  placeholder="e.g. John Kamau"
                  value={form.client_name}
                  onChange={e => setForm(f => ({...f, client_name: e.target.value}))}
                />
              </div>

              <div className="space-y-2">
                <Label>Event Date *</Label>
                <Input
                  type="date"
                  value={form.event_date}
                  onChange={e => setForm(f => ({...f, event_date: e.target.value}))}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label>Venue</Label>
                <Input
                  placeholder="e.g. Nairobi Safari Club"
                  value={form.venue}
                  onChange={e => setForm(f => ({...f, venue: e.target.value}))}
                />
              </div>

              {error && (
                <div className="col-span-2 text-sm text-red-600 bg-red-50 border border-red-200 px-3 py-2 rounded">
                  {error}
                </div>
              )}

              <div className="col-span-2 flex gap-3 justify-end">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => { setShowForm(false); setForm(empty); }}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={saving}>
                  {saving ? "Creating..." : "Create Event"}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Events Table */}
      <Card>
        <CardContent className="pt-4">
          {loading ? (
            <div className="space-y-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-12 bg-slate-100 rounded animate-pulse" />
              ))}
            </div>
          ) : events.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <Calendar className="h-10 w-10 mx-auto mb-3 text-slate-300" />
              <p className="mb-3">No events found</p>
              <Button onClick={() => setShowForm(true)} variant="outline" size="sm">
                Create your first event
              </Button>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Event</TableHead>
                  <TableHead>Client</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>Venue</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {events.map(event => (
                  <TableRow key={event.id}>
                    <TableCell className="font-medium">{event.name}</TableCell>
                    <TableCell className="text-slate-500">{event.client_name}</TableCell>
                    <TableCell className="text-slate-500">
                      {new Date(event.event_date).toLocaleDateString()}
                    </TableCell>
                    <TableCell className="text-slate-500">{event.venue}</TableCell>
                    <TableCell>
                      <span className={`text-xs px-2 py-1 rounded-full font-medium ${statusColors[event.status] || ""}`}>
                        {event.status}
                      </span>
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
