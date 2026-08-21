import { useState } from 'react';
import { Youtube, ArrowRight, Loader2, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function VideoInput({ onVideoProcessed }) {
  const [url, setUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!url.trim()) {
      setError('Please enter a YouTube URL');
      return;
    }

    setIsLoading(true);
    try {
      await api.processVideo(url);
      setSuccess(true);
      setTimeout(() => {
        onVideoProcessed(url);
      }, 1500); // Give user time to see the success message
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to process video');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-8 rounded-2xl bg-surface shadow-2xl border border-slate-700/50">
      <div className="flex flex-col items-center mb-8">
        <div className="p-4 bg-primary/10 rounded-full mb-4">
          <Youtube className="w-12 h-12 text-primary" />
        </div>
        <h1 className="text-3xl font-bold text-white mb-2">Chat with YouTube</h1>
        <p className="text-slate-400 text-center">
          Paste any YouTube video URL to analyze its transcript and start asking questions.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://youtube.com/watch?v=..."
            className="w-full bg-slate-900 border border-slate-700 text-white rounded-xl px-4 py-4 pr-12 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            disabled={isLoading || success}
          />
          {error && (
            <p className="text-red-400 text-sm mt-2 font-medium">{error}</p>
          )}
        </div>

        <button
          type="submit"
          disabled={isLoading || success}
          className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-blue-600 disabled:bg-slate-700 text-white font-medium py-4 rounded-xl transition-all"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Processing Video...
            </>
          ) : success ? (
            <>
              <CheckCircle2 className="w-5 h-5 text-green-400" />
              Ready!
            </>
          ) : (
            <>
              Analyze Video
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
