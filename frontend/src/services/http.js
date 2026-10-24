// Base HTTP client. Every service goes through here; components never call fetch.
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

function errorMessage(data, status) {
  if (Array.isArray(data?.detail)) return data.detail.map((d) => d.msg).join(', ')
  return data?.detail || `Permintaan gagal (${status})`
}

async function request(method, path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    const data = await res.json().catch(() => null)
    throw new ApiError(errorMessage(data, res.status), res.status)
  }
  return res.status === 204 ? null : res.json()
}

export const http = {
  get: (path) => request('GET', path),
  post: (path, body) => request('POST', path, body),
  delete: (path) => request('DELETE', path),
}
