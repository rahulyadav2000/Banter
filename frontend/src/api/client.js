const API_URL = import.meta.env.VITE_API_URL;
console.log(import.meta.env);
console.log(import.meta.env.API_URL);
console.log("API_URL:", API_URL);
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
