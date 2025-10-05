import React, { useState } from "react";
import { uploadCV } from "../utilis/api";
import { useRouter } from "next/router";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    if (!file || !jobDesc) {
      setError("Please upload a CV and paste a job description.");
      return;
    }
    setLoading(true);
    try {
      const result = await uploadCV(file, jobDesc);
      localStorage.setItem("tmcv_result", JSON.stringify(result));
      router.push("/result");
    } catch (err) {
      setError("Failed to process CV. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-8">
        <h1 className="text-2xl font-bold mb-4 text-center">TailorMyCV</h1>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <label className="block">
            <span className="text-gray-700">Upload your CV (.pdf or .docx)</span>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={e => setFile(e.target.files?.[0] || null)}
              className="mt-1 block w-full border border-gray-300 rounded p-2"
              required
            />
          </label>
          <label className="block">
            <span className="text-gray-700">Paste Job Description</span>
            <textarea
              value={jobDesc}
              onChange={e => setJobDesc(e.target.value)}
              rows={6}
              className="mt-1 block w-full border border-gray-300 rounded p-2"
              required
            />
          </label>
          {error && <div className="text-red-500 text-sm">{error}</div>}
          <button
            type="submit"
            className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
            disabled={loading}
          >
            {loading ? "Processing..." : "Tailor My CV"}
          </button>
        </form>
      </div>
    </div>
  );
}
