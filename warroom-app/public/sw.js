self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()));

self.addEventListener('push', (e) => {
  const d = e.data.json();
  e.waitUntil(self.registration.showNotification(d.title, {
    body: d.body, tag: d.taskId, data: d,
    actions: [{ action: 'done', title: '✅ Done' }, { action: 'miss', title: '❌ Not yet' }],
  }));
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const d = e.notification.data;
  if ((e.action === 'done' || e.action === 'miss') && d.taskId !== 'test') {
    e.waitUntil((async () => {
      const cache = await caches.open('warroom-key');
      const keyRes = await cache.match('key');
      const key = keyRes ? await keyRes.text() : '';
      await fetch('/api/tick', {
        method: 'POST',
        headers: { 'x-warroom-key': key, 'Content-Type': 'application/json' },
        body: JSON.stringify({ date: d.date, taskId: d.taskId, done: e.action === 'done' }),
      });
    })());
  } else {
    // iOS has no action buttons — tap opens the app focused on the task with big ✅/❌
    e.waitUntil(clients.openWindow(d.taskId && d.taskId !== 'test' ? '/?focus=' + d.taskId : '/'));
  }
});
