export default function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  // Identity headers supplied by callers are never trusted on Vercel.
  return res.status(200).json({email: null, canEdit: false});
}
