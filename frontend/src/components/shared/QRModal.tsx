"use client";

import { useEffect, useRef } from "react";
import QRCode from "qrcode";
import { X, Download } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Props {
  item: { id: number; code: string; name: string } | null;
  onClose: () => void;
}

export default function QRModal({ item, onClose }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!item || !canvasRef.current) return;
    QRCode.toCanvas(canvasRef.current, `ELROYY-IMS:${item.code}`, {
      width: 200,
      margin: 2,
      color: { dark: "#0a0a0a", light: "#ffffff" }
    });
  }, [item]);

  if (!item) return null;

  const handleDownload = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const url = canvas.toDataURL("image/png");
    const a   = document.createElement("a");
    a.href    = url;
    a.download = `${item.code}-qr.png`;
    a.click();
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-72 shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-slate-900">QR Code</h3>
          <button onClick={onClose}>
            <X className="h-4 w-4 text-slate-400 hover:text-slate-600" />
          </button>
        </div>
        <div className="flex flex-col items-center gap-3">
          <canvas ref={canvasRef} className="rounded-lg border border-slate-100" />
          <p className="font-mono text-sm font-bold text-slate-700">{item.code}</p>
          <p className="text-sm text-slate-500 text-center">{item.name}</p>
          <Button className="w-full gap-2" onClick={handleDownload}>
            <Download className="h-4 w-4" /> Download QR
          </Button>
        </div>
      </div>
    </div>
  );
}
