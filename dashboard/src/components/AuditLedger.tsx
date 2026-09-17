'use client';

import React, { useState } from 'react';
import { Database, ShieldCheck, Download, Check, Copy, Hash } from 'lucide-react';
import { AuditBlock } from '../lib/types';

interface AuditLedgerProps {
  blocks: AuditBlock[];
}

export const AuditLedger: React.FC<AuditLedgerProps> = ({ blocks }) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopyHash = (hash: string, idx: number) => {
    navigator.clipboard.writeText(hash);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 1500);
  };

  const handleDownloadLedger = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(blocks, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', 'raipur_police_synchroclear_audit_ledger.json');
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="bg-c2-card border border-c2-border rounded-xl p-4 flex flex-col h-full shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-c2-border/70 pb-3 mb-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-1.5 rounded-lg bg-police-navy border border-police-cyan/30">
            <Database className="w-4 h-4 text-police-cyan" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-c2-textBright flex items-center gap-2">
              Cryptographic Audit Ledger
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1">
                <ShieldCheck className="w-2.5 h-2.5" /> SHA-256 Chained
              </span>
            </h2>
            <p className="text-xs text-c2-textDim">
              Append-only tamper-evident logs for citizen e-challan immunity
            </p>
          </div>
        </div>

        <button
          onClick={handleDownloadLedger}
          className="text-xs font-mono font-bold px-2.5 py-1 rounded bg-c2-surface hover:bg-c2-hover text-c2-textBright border border-c2-border transition flex items-center gap-1.5 shadow"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export JSON</span>
        </button>
      </div>

      {/* Ledger Table */}
      <div className="flex-1 overflow-y-auto max-h-[260px] border border-c2-border rounded-lg bg-c2-obsidian">
        <table className="w-full text-left font-mono text-[11px]">
          <thead className="bg-c2-surface text-c2-textDim text-[10px] sticky top-0 border-b border-c2-border">
            <tr>
              <th className="p-2">Block #</th>
              <th className="p-2">Timestamp (UTC)</th>
              <th className="p-2">Junction</th>
              <th className="p-2">Emergency Vehicle</th>
              <th className="p-2">Whitelisted Citizens</th>
              <th className="p-2">SHA-256 Block Hash</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-c2-border/40 text-c2-textBright">
            {blocks.map((b, idx) => (
              <tr key={b.blockHeight} className="hover:bg-c2-card/60 transition-colors">
                <td className="p-2 font-bold text-police-gold">#{b.blockHeight}</td>
                <td className="p-2 text-c2-textDim text-[10px]">{b.timestamp}</td>
                <td className="p-2 text-c2-textMuted">{b.junctionId}</td>
                <td className="p-2">
                  <span className="font-bold text-police-cyan">{b.primaryPlate}</span>
                  <span className="text-[9px] text-c2-textDim block">{b.vehicleClass}</span>
                </td>
                <td className="p-2">
                  <div className="flex flex-wrap gap-1">
                    {b.whitelistedPlates.map((plate) => (
                      <span
                        key={plate}
                        className="px-1 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[9px]"
                      >
                        {plate}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="p-2">
                  <button
                    onClick={() => handleCopyHash(b.blockHash, idx)}
                    className="flex items-center gap-1 text-[10px] text-c2-textDim hover:text-police-cyan transition-colors"
                  >
                    <Hash className="w-3 h-3" />
                    <span>{b.blockHash.slice(0, 10)}...{b.blockHash.slice(-6)}</span>
                    {copiedIndex === idx ? (
                      <Check className="w-3 h-3 text-emerald-400" />
                    ) : (
                      <Copy className="w-3 h-3 opacity-50" />
                    )}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
