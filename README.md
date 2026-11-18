# Partner-Dashboard-

The Gen Academy partner dashboard: net partners, cohort boards, search, CSV import/export, and shared partner editing.

## Source

- `web/`: dashboard interface and company branding.
- `server/api.mjs`: shared records API and editor authorization.
- `drizzle/`: database migration.
- `build-shared.mjs`: builds the deployable Worker and assets.

## Checks and build

Requires Node.js 24 (the tests use built-in SQLite).

```sh
node --check web/app.js
node server/api.test.mjs
node build-shared.mjs
```

## Hosting

The current deployment uses ChatGPT Sites, Cloudflare D1 (`DB`), and Sites-provided authenticated identity headers. Editing is restricted server-side to Barkath and Sumukh's authorized TGA email addresses.

Vercel now serves the dashboard via `node build-vercel.mjs` and the `public` output directory. `/api/partners` reads the live Sites board through a read-only server function; it does not copy the seed or overwrite saved records. Edit and Add buttons open the existing authenticated Sites editor in a new tab. Return to Vercel and click Refresh board (or wait for the 20-second refresh) to view saved changes.

This is a staged migration: storage and editor authentication still depend on Sites. Do not delete the Sites project. Moving editing fully onto Vercel requires a replacement durable database and verified login. No client-supplied identity headers are trusted by the Vercel functions, and writes through the read-only proxy are rejected.

Partner data in `web/data.json` is the original seed; current shared records reside in the hosted database. Export current records before migrating hosts. No live Google Sheets synchronization is configured.
