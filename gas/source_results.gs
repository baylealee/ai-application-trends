/**
 * Baylea AI Application Trends - Source Results Receiver
 *
 * 接收 GitHub Actions 產出的 Threads fetch JSON，寫入 Google Sheet。
 * 以 source_url 去重複：同一來源 URL 已存在時更新，不重複新增。
 */

const SOURCE_CONFIG = {
  SHEET_ID: '1ttqxo8a2N9WjBFId7tS4d_F0SgPgmIfrIFWoImnApeU',
  SHEET_NAME: 'source_fetch_results'
};

const SOURCE_HEADERS = [
  'source_url',
  'source_author',
  'status',
  'content_quality',
  'source_level_hint',
  'extraction_method',
  'extraction_source',
  'keyword_hits',
  'raw_content',
  'candidate_count',
  'fetch_notes',
  'first_seen_at',
  'last_seen_at',
  'last_run_id',
  'artifact_url',
  'updated_count'
];

function doPost(e) {
  try {
    const payload = JSON.parse((e.postData && e.postData.contents) || '{}');
    const rows = normalizeSourceResults_(payload.results || payload);
    const meta = payload.meta || {};
    const result = upsertSourceRows_(rows, meta);
    return jsonOutput_({ ok: true, ...result });
  } catch (err) {
    return jsonOutput_({ ok: false, message: String(err && err.message ? err.message : err) });
  }
}

function doGet() {
  return jsonOutput_({ ok: true, message: 'AI Application Trends source results API is running.' });
}

function normalizeSourceResults_(input) {
  if (Array.isArray(input)) return input;
  if (input && Array.isArray(input.results)) return input.results;
  if (input && input.source_url) return [input];
  return [];
}

function upsertSourceRows_(items, meta) {
  const sheet = getSourceSheet_();
  const existing = getExistingSourceMap_(sheet);
  const now = new Date();
  let inserted = 0;
  let updated = 0;
  let skipped = 0;

  items.forEach(item => {
    const sourceUrl = normalizeUrl_(item.source_url || '');
    if (!sourceUrl) {
      skipped += 1;
      return;
    }

    const existingRow = existing[sourceUrl];
    const rowValues = buildSourceRow_(item, meta, now, existingRow);

    if (existingRow) {
      sheet.getRange(existingRow.rowNumber, 1, 1, SOURCE_HEADERS.length).setValues([rowValues]);
      updated += 1;
    } else {
      sheet.appendRow(rowValues);
      inserted += 1;
    }
  });

  return { inserted, updated, skipped, total_received: items.length };
}

function buildSourceRow_(item, meta, now, existingRow) {
  const old = existingRow ? existingRow.values : {};
  const previousCount = Number(old.updated_count || 0);

  return [
    normalizeUrl_(item.source_url || ''),
    item.source_author || old.source_author || '',
    item.status || old.status || '',
    item.content_quality || old.content_quality || '',
    item.source_level_hint || old.source_level_hint || '',
    item.extraction_method || old.extraction_method || '',
    item.extraction_source || old.extraction_source || '',
    stringify_(item.keyword_hits || old.keyword_hits || []),
    item.raw_content || old.raw_content || '',
    item.candidate_count || old.candidate_count || 0,
    stringify_(item.fetch_notes || old.fetch_notes || []),
    old.first_seen_at || now,
    now,
    meta.run_id || old.last_run_id || '',
    meta.artifact_url || old.artifact_url || '',
    previousCount + 1
  ];
}

function getSourceSheet_() {
  const ss = SpreadsheetApp.openById(SOURCE_CONFIG.SHEET_ID);
  let sheet = ss.getSheetByName(SOURCE_CONFIG.SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(SOURCE_CONFIG.SHEET_NAME);

  const current = sheet.getRange(1, 1, 1, SOURCE_HEADERS.length).getValues()[0];
  if (current.join('') === '' || current[0] !== SOURCE_HEADERS[0]) {
    sheet.getRange(1, 1, 1, SOURCE_HEADERS.length).setValues([SOURCE_HEADERS]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function getExistingSourceMap_(sheet) {
  const lastRow = sheet.getLastRow();
  const map = {};
  if (lastRow < 2) return map;

  const values = sheet.getRange(2, 1, lastRow - 1, SOURCE_HEADERS.length).getValues();
  values.forEach((row, index) => {
    const obj = {};
    SOURCE_HEADERS.forEach((header, colIndex) => obj[header] = row[colIndex]);
    const url = normalizeUrl_(obj.source_url || '');
    if (url) map[url] = { rowNumber: index + 2, values: obj };
  });
  return map;
}

function normalizeUrl_(url) {
  return String(url || '')
    .trim()
    .replace('https://www.threads.net/', 'https://www.threads.com/')
    .replace(/\?.*$/, '');
}

function stringify_(value) {
  if (typeof value === 'string') return value;
  return JSON.stringify(value || []);
}

function jsonOutput_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
