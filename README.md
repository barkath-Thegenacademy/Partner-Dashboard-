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

This version is not yet Vercel-compatible. A Vercel migration must replace the D1 binding and Sites authentication with persistent storage and verified authentication. Never trust client-supplied identity headers on another hosting platform.

Partner data in `web/data.json` is the original seed; current shared records reside in the hosted database. Export current records before migrating hosts. No live Google Sheets synchronization is configured.
