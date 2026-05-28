/**
 * Baylea AI Application Trends - Subscriber + Mailer API
 * 支援 GitHub Pages 前端 JSONP/GET 訂閱，避免 CORS 問題。
 */

const CONFIG = {
  SHEET_ID: '1ttqxo8a2N9WjBFId7tS4d_F0SgPgmIfrIFWoImnApeU',
  SHEET_NAME: 'subscribers',
  SITE_BASE_URL: 'https://baylealee.github.io/ai-application-trends',
  DEFAULT_RECIPIENT: 'Btokaa@msn.com',
  SENDER_NAME: 'Baylea AI Application Trends'
};

const HEADERS = ['email','status','subscribe_at','unsubscribe_at','last_sent_at','source','token'];

function doGet(e) {
  const action = String(e.parameter.action || '').toLowerCase();
  const callback = e.parameter.callback || '';
  let result;

  if (action === 'list') {
    result = { ok: true, subscribers: getActiveSubscribers_() };
  } else if (action === 'subscribe' || action === 'unsubscribe') {
    result = handleSubscriptionData_({
      action: action,
      email: e.parameter.email || '',
      token: e.parameter.token || '',
      source: e.parameter.source || 'github_pages'
    });
  } else {
    result = { ok: true, message: 'AI Application Trends subscriber API is running.' };
  }

  return output_(result, callback);
}

function doPost(e) {
  let payload = {};
  try {
    payload = JSON.parse(e.postData.contents || '{}');
  } catch (err) {
    return jsonOutput({ ok: false, message: 'Invalid JSON payload.' });
  }
  return jsonOutput(handleSubscriptionData_(payload));
}

function handleSubscriptionData_(payload) {
  const action = String(payload.action || '').toLowerCase();
  const email = normalizeEmail_(payload.email || '');
  const source = payload.source || 'github_pages';

  if (!isValidEmail_(email)) return { ok: false, message: 'Email 格式不正確。' };

  const sheet = getSheet_();
  const rows = getRows_(sheet);
  const now = new Date();
  const rowIndex = rows.findIndex(row => normalizeEmail_(row.email) === email);

  if (action === 'subscribe') {
    const token = Utilities.getUuid();
    if (rowIndex >= 0) {
      const targetRow = rowIndex + 2;
      sheet.getRange(targetRow, 2).setValue('active');
      sheet.getRange(targetRow, 3).setValue(now);
      sheet.getRange(targetRow, 4).setValue('');
      sheet.getRange(targetRow, 6).setValue(source);
      if (!rows[rowIndex].token) sheet.getRange(targetRow, 7).setValue(token);
    } else {
      sheet.appendRow([email, 'active', now, '', '', source, token]);
    }
    return { ok: true, message: '訂閱成功，之後會收到每日 AI 應用趨勢整理。' };
  }

  if (action === 'unsubscribe') {
    if (rowIndex < 0) return { ok: true, message: '此 Email 不在訂閱名單中。' };
    const target = rows[rowIndex];
    if (payload.token && target.token && payload.token !== target.token) return { ok: false, message: '取消訂閱連結無效。' };
    const targetRow = rowIndex + 2;
    sheet.getRange(targetRow, 2).setValue('inactive');
    sheet.getRange(targetRow, 4).setValue(now);
    return { ok: true, message: '已取消訂閱。' };
  }

  return { ok: false, message: 'Unknown action. Use subscribe or unsubscribe.' };
}

function sendDailyDigest() {
  const subscribers = getActiveSubscribers_();
  const recipients = Array.from(new Set([CONFIG.DEFAULT_RECIPIENT].concat(subscribers.map(s => s.email))));
  const today = Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd');
  const digestUrl = CONFIG.SITE_BASE_URL + '/daily/' + today + '.html';
  const subject = 'AI 應用趨勢日報｜' + today;

  recipients.forEach(email => {
    const subscriber = findSubscriberByEmail_(email);
    const unsubscribeUrl = buildUnsubscribeUrl_(email, subscriber ? subscriber.token : '');
    const htmlBody = buildEmailHtml_(today, digestUrl, unsubscribeUrl);
    MailApp.sendEmail({ to: email, subject, htmlBody, name: CONFIG.SENDER_NAME });
    updateLastSentAt_(email);
  });
}

function installDailyTrigger() {
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === 'sendDailyDigest') ScriptApp.deleteTrigger(trigger);
  });
  ScriptApp.newTrigger('sendDailyDigest').timeBased().everyDays(1).atHour(8).nearMinute(45).inTimezone('Asia/Taipei').create();
}

function buildEmailHtml_(today, digestUrl, unsubscribeUrl) {
  return `<div style="background:#f3eee7;padding:28px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans TC',sans-serif;color:#3f3a36;"><div style="max-width:680px;margin:auto;background:#fffaf3;border:1px solid #ded3c7;border-radius:24px;padding:28px;"><div style="display:inline-block;background:#eee4d8;border-radius:999px;padding:6px 12px;font-size:13px;color:#695f57;">Baylea AI Application Trends</div><h1 style="font-size:28px;line-height:1.25;margin:18px 0 8px;">AI 應用趨勢日報｜${today}</h1><p style="color:#8a8178;font-size:16px;line-height:1.7;">今天的 GPT、Claude、Gemini AI workflow 已更新。點擊下方按鈕閱讀完整日報與分類標籤。</p><p style="margin:24px 0;"><a href="${digestUrl}" style="background:#5f6861;color:#fff;text-decoration:none;border-radius:999px;padding:12px 18px;display:inline-block;">閱讀今日完整日報</a></p><p style="font-size:13px;color:#8a8178;">不想再收到信？<a href="${unsubscribeUrl}" style="color:#5f6861;">取消訂閱</a></p></div></div>`;
}

function buildUnsubscribeUrl_(email, token) {
  return ScriptApp.getService().getUrl() + '?action=unsubscribe&email=' + encodeURIComponent(email) + '&token=' + encodeURIComponent(token || '');
}

function getActiveSubscribers_() { return getRows_(getSheet_()).filter(row => row.status === 'active' && isValidEmail_(row.email)); }
function findSubscriberByEmail_(email) { return getRows_(getSheet_()).find(row => normalizeEmail_(row.email) === normalizeEmail_(email)); }
function updateLastSentAt_(email) { const sheet = getSheet_(); const rows = getRows_(sheet); const idx = rows.findIndex(row => normalizeEmail_(row.email) === normalizeEmail_(email)); if (idx >= 0) sheet.getRange(idx + 2, 5).setValue(new Date()); }

function getSheet_() {
  const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
  let sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  if (!sheet) sheet = ss.insertSheet(CONFIG.SHEET_NAME);
  const headerValues = sheet.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  if (headerValues.join('') === '' || headerValues[0] !== HEADERS[0]) sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
  return sheet;
}

function getRows_(sheet) {
  const lastRow = sheet.getLastRow();
  if (lastRow < 2) return [];
  const values = sheet.getRange(2, 1, lastRow - 1, HEADERS.length).getValues();
  return values.map(row => Object.fromEntries(HEADERS.map((header, index) => [header, row[index]])));
}

function normalizeEmail_(email) { return String(email || '').trim().toLowerCase(); }
function isValidEmail_(email) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizeEmail_(email)); }
function jsonOutput(obj) { return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON); }
function output_(obj, callback) {
  const body = callback ? `${callback}(${JSON.stringify(obj)});` : JSON.stringify(obj);
  return ContentService.createTextOutput(body).setMimeType(callback ? ContentService.MimeType.JAVASCRIPT : ContentService.MimeType.JSON);
}
