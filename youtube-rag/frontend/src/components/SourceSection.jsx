import { ChevronDown, ChevronRight, FileText } from 'lucide-react';
import { useState } from 'react';

export default function SourceSection({ sources }) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-4 bg-slate-900/50 rounded-xl border border-slate-700/50 overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between p-3 hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-2 text-sm font-medium text-slate-300">
          <FileText className="w-4 h-4 text-primary" />
          <span>{sources.length} Sources Retrieved</span>
        </div>
        {isExpanded ? (
          <ChevronDown className="w-4 h-4 text-slate-400" />
        ) : (
          <ChevronRight className="w-4 h-4 text-slate-400" />
        )}
      </button>

      {isExpanded && (
        <div className="p-3 pt-0 space-y-3">
          {sources.map((source, index) => (
            <div key={index} className="bg-slate-800 rounded-lg p-3 text-sm">
              <div className="text-xs font-semibold text-primary mb-1">
                Chunk {source.chunk_index}
              </div>
              <p className="text-slate-300 leading-relaxed">
                {source.content}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
