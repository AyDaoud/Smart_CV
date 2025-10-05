// frontend/pages/result.tsx
import React, { useEffect, useState } from "react";
import MatchPreview from "../components/MatchPreview";

export default function Result() {
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const stored = localStorage.getItem("tmcv_result");
    if (stored) {
      setResult(JSON.parse(stored));
    } else {
      setError("No result found. Please upload your CV first.");
    }
  }, []);

  // UPDATED DOWNLOAD HANDLER
  const handleDownload = () => {
    if (!result?.download_url) return;
    // Simply open the Supabase URL, the browser will handle the download
    window.open(result.download_url, '_blank');
  };

  if (error) {
    return <div className="min-h-screen flex items-center justify-center text-red-500">{error}</div>;
  }
  if (!result) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-50 p-4">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow p-8 mt-8">
        <h2 className="text-xl font-bold mb-2 text-center">Match Score</h2>
        {/* Make sure score is displayed correctly as percentage */}
        <div className="text-3xl text-center text-blue-600 font-bold mb-6">{Math.round(result.match_score * 100)}%</div>
        <h3 className="text-lg font-semibold mb-2">Before vs After</h3>
        <MatchPreview before={result.before} after={result.after} />
        <div className="flex justify-end mt-6">
          <button
            onClick={handleDownload}
            disabled={!result.download_url}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-400"
          >
            Download Tailored CV (.docx)
          </button>
        </div>
      </div>
    </div>
  );
}