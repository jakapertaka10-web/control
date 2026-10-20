// BACKEND PLACEHOLDER
// AKTIF PADA TAHAP 2
//
// Tujuan file ini adalah sebagai fondasi backend yang akan dikembangkan
// menjadi Express API untuk frontend yang nanti akan terhubung ke
// Supabase PostgreSQL.
//
// Saat ini tidak diperlukan untuk menjalankan aplikasi prototype dari
// file:// dan localStorage.
//
// Contoh struktur yang akan dikembangkan:
// GET    /api/materials
// POST   /api/materials
// PUT    /api/materials/:id
// DELETE /api/materials/:id
//
// GET    /api/suppliers
// POST   /api/suppliers
//
// GET    /api/stock
//
// POST   /api/receiving
// POST   /api/qc
// POST   /api/putaway
// POST   /api/issuing
// POST   /api/opname
//
// Backend placeholder only. This file can be extended later with Express.

const http = require('http');

const PORT = process.env.PORT || 3000;

const server = http.createServer(function (req, res) {
  if (req.url === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      mode: 'backend-placeholder',
      message: 'Backend akan aktif pada tahap 2',
      storage: 'localStorage prototype'
    }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({
    status: 'not_found',
    message: 'Backend placeholder hanya menyediakan endpoint /api/health'
  }));
});

server.listen(PORT, function () {
  console.log('WMS backend placeholder running on port ' + PORT);
});
