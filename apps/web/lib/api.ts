export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const url = API_BASE ? `${API_BASE}${path}` : path;
  const res = await fetch(url, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`API ${res.status}`);
  return (await res.json()) as T;
}
