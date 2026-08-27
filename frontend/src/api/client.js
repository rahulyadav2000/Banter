const API_URL = "http://127.0.0.1:8000";

export const authRequests = async (
  endpoints,
  { method = "GET", body, token } = {},
) => {
  const headers = { "Content-Type": "application/json" };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoints}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(data?.message || "Something went wrong!");
  }

  return data;
};
