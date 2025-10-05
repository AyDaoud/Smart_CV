// Helper for calling FastAPI backend
export type RewriteResponse = {
  match_score: number;
  before: string[];
  after: string[];
};

export async function uploadCV(file: File, jobDescription: string): Promise<RewriteResponse> {
  const formData = new FormData();
  formData.append("cv_file", file);
  formData.append("job_description", jobDescription);

  const res = await fetch("http://localhost:8000/api/rewrite", {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    throw new Error("Failed to upload CV");
  }
  return res.json();
}
