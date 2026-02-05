const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '';

export async function register(
  username: string,
  email: string,
  password: string
) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password })
  });

  if (!res.ok) {
    const error = await res.json();
    throw error;
  }

  return res.json();
}

export async function login(username: string, password: string) {
  const body = new URLSearchParams({
    username,
    password,
    grant_type: 'password',
  });

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  if (!res.ok) {
    throw await res.json();
  }

  return res.json(); // { access_token, token_type }
}
