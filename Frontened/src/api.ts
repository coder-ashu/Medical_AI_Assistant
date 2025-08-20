export async function queryBackend(userQuery: string) {
  const response = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: userQuery, k: 3 }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch from backend");
  }

  return response.json(); 
}
