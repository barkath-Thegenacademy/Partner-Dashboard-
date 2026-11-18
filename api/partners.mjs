const upstream = 'https://barkath-partner-tracker-20261111.barkath296986.chatgpt.site/api/partners';
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') {
    res.setHeader('Allow', 'GET');
    return res.status(405).json({error: 'Open the authenticated shared editor to save changes.'});
  }
  try {
    // Do not forward cookies, authorization, or user-supplied identity headers.
    const response = await fetch(upstream, {cache: 'no-store', signal: AbortSignal.timeout(15000)});
    if (!response.ok) throw new Error('Upstream unavailable');
    const data = await response.json();
    if (!Array.isArray(data.partners) || !Number.isInteger(data.revision)) throw new Error('Invalid board');
    return res.status(200).json({partners: data.partners, revision: data.revision});
  } catch {
    return res.status(503).json({error: 'Shared records are temporarily unavailable. Please refresh to retry.'});
  }
}
