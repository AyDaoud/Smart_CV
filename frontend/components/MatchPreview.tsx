import React from "react";

type Props = { before: string[]; after: string[] };

function diffHighlight(before: string, after: string) {
  // Simple diff: highlight if different
  if (before !== after) {
    return <span className="bg-yellow-100 text-yellow-900">{after}</span>;
  }
  return <span>{after}</span>;
}

export default function MatchPreview({ before, after }: Props) {
  const maxLen = Math.max(before.length, after.length);
  return (
    <div className="grid grid-cols-2 gap-4 border rounded p-4 bg-gray-50">
      <div>
        <h4 className="font-semibold mb-2">Before</h4>
        <ul className="list-disc pl-5 space-y-1">
          {Array.from({ length: maxLen }).map((_, i) => (
            <li key={i} className="text-gray-700">
              {before[i] || <span className="text-gray-400 italic">(none)</span>}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h4 className="font-semibold mb-2">After</h4>
        <ul className="list-disc pl-5 space-y-1">
          {Array.from({ length: maxLen }).map((_, i) => (
            <li key={i} className="text-gray-700">
              {after[i] ? diffHighlight(before[i] || "", after[i]) : <span className="text-gray-400 italic">(none)</span>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
