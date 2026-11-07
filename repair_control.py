#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
APP = ROOT / "app.js"

required = [
    "data.js", "utils.js", "dashboard.js", "materials.js",
    "suppliers.js", "locations.js", "receiving.js", "qc.js",
    "putaway.js", "issuing.js", "stock.js", "movement.js",
    "opname.js", "reports.js", "app.js", "style.css", "logo.svg", "favicon.svg"
]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    print("ERROR: File tidak ditemukan di root repository:")
    print("\n".join(" - " + item for item in missing))
    print("Jalankan script dari folder utama repository control.")
    sys.exit(1)

index = INDEX.read_text(encoding="utf-8")
app = APP.read_text(encoding="utf-8")

# Correct asset paths: assets are stored in repository root.
index = index.replace('href="assets/favicon.svg"', 'href="./favicon.svg"')
index = index.replace('href="css/style.css"', 'href="./style.css"')
index = index.replace('src="assets/logo.svg"', 'src="./logo.svg"')

script_block = '''    <script src="./data.js"></script>
    <script src="./utils.js"></script>
    <script src="./dashboard.js"></script>
    <script src="./materials.js"></script>
    <script src="./suppliers.js"></script>
    <script src="./locations.js"></script>
    <script src="./receiving.js"></script>
    <script src="./qc.js"></script>
    <script src="./putaway.js"></script>
    <script src="./issuing.js"></script>
    <script src="./stock.js"></script>
    <script src="./movement.js"></script>
    <script src="./opname.js"></script>
    <script src="./reports.js"></script>
    <script src="./app.js"></script>'''

if 'src="js/data.js"' in index and 'src="js/app.js"' in index:
    index, count = re.subn(
        r'    <script src="js/data\.js"></script>.*?    <script src="js/app\.js"></script>',
        script_block, index, flags=re.S
    )
    if count != 1:
        print("ERROR: Tidak dapat mengenali blok script lama. Tidak ada file yang diubah.")
        sys.exit(1)
else:
    index = re.sub(
        r'^\s*<script src="(?:\./|js/)?(?:data|utils|dashboard|materials|suppliers|locations|receiving|qc|putaway|issuing|stock|movement|opname|reports|app)\.js"></script>\s*$',
        '', index, flags=re.M
    )
    index = index.replace("</body>", script_block + "\n  </body>")

# Add the missing navigation buttons.
if 'data-view="suppliers"' not in index:
    index = index.replace(
        '<button class="nav-btn" type="button" data-view="materials"><span class="nav-icon">▤</span>Master Bahan Baku</button>',
        '<button class="nav-btn" type="button" data-view="materials"><span class="nav-icon">▤</span>Master Bahan Baku</button>\n'
        '          <button class="nav-btn" type="button" data-view="suppliers"><span class="nav-icon">♙</span>Suppliers</button>\n'
        '          <button class="nav-btn" type="button" data-view="locations"><span class="nav-icon">⌖</span>Locations</button>'
    )
if 'data-view="qc"' not in index:
    index = index.replace(
        '<button class="nav-btn" type="button" data-view="receiving"><span class="nav-icon">↓</span>Barang Masuk</button>',
        '<button class="nav-btn" type="button" data-view="receiving"><span class="nav-icon">↓</span>Barang Masuk</button>\n'
        '          <button class="nav-btn" type="button" data-view="qc"><span class="nav-icon">✓</span>Quality Control</button>\n'
        '          <button class="nav-btn" type="button" data-view="putaway"><span class="nav-icon">⇲</span>Putaway</button>'
    )

views = r'''
        <section id="suppliers-view" class="view">
          <div class="page-intro"><div><h2>Suppliers</h2><p>Kelola data pemasok bahan baku.</p></div></div>
          <div class="two-column-layout">
            <section class="panel"><div class="panel-header"><h3>Data Supplier</h3></div>
              <form id="supplierForm" class="stack-form">
                <input id="supplierId" type="hidden" />
                <label>Nama Supplier<input id="supplierName" type="text" required /></label>
                <label>Contact Person<input id="supplierContact" type="text" /></label>
                <label>Telepon<input id="supplierPhone" type="text" /></label>
                <label>Email<input id="supplierEmail" type="email" /></label>
                <div class="actions-row"><button class="primary-btn" type="submit">Simpan Supplier</button><button id="cancelSupplierEdit" class="secondary-btn hidden" type="button">Batal</button></div>
              </form>
            </section>
            <section class="panel"><div class="panel-header"><h3>Daftar Supplier</h3></div>
              <div class="table-scroll"><table class="data-table"><thead><tr><th>Nama</th><th>Contact</th><th>Telepon</th><th>Email</th><th>Aksi</th></tr></thead><tbody id="suppliersTableBody"></tbody></table></div>
            </section>
          </div>
        </section>

        <section id="locations-view" class="view">
          <div class="page-intro"><div><h2>Locations</h2><p>Kelola zona, rak, dan lokasi penyimpanan gudang.</p></div></div>
          <div class="two-column-layout">
            <section class="panel"><div class="panel-header"><h3>Data Lokasi</h3></div>
              <form id="locationForm" class="stack-form">
                <input id="locationId" type="hidden" />
                <label>Nama Lokasi<input id="locationName" type="text" required /></label>
                <label>Zona<input id="locationZone" type="text" required /></label>
                <label>Rak<input id="locationRack" type="text" /></label>
                <div class="actions-row"><button class="primary-btn" type="submit">Simpan Lokasi</button><button id="cancelLocationEdit" class="secondary-btn hidden" type="button">Batal</button></div>
              </form>
            </section>
            <section class="panel"><div class="panel-header"><h3>Daftar Lokasi</h3></div>
              <div class="table-scroll"><table class="data-table"><thead><tr><th>Nama</th><th>Zona</th><th>Rak</th><th>Aksi</th></tr></thead><tbody id="locationsTableBody"></tbody></table></div>
            </section>
          </div>
        </section>

        <section id="qc-view" class="view">
          <div class="page-intro"><div><h2>Quality Control</h2><p>Catat hasil pemeriksaan kualitas bahan baku.</p></div></div>
          <section class="panel form-panel"><div class="panel-header"><h3>Input QC</h3></div>
            <form id="qcForm" class="stack-form">
              <div class="field-row">
                <label>Material<select id="qcMaterial" required></select></label>
                <label>Status<select id="qcStatus"><option>Pass</option><option>Fail</option><option>Hold</option></select></label>
                <label>Inspector<input id="qcInspector" type="text" /></label>
              </div>
              <label>Catatan<input id="qcRemarks" type="text" /></label>
              <button class="primary-btn" type="submit">Simpan QC</button>
            </form>
          </section>
          <section class="panel"><div class="panel-header"><h3>Riwayat QC</h3></div>
            <div class="table-scroll"><table class="data-table"><thead><tr><th>Tanggal</th><th>Material</th><th>Status</th><th>Inspector</th><th>Catatan</th></tr></thead><tbody id="qcTableBody"></tbody></table></div>
          </section>
        </section>

        <section id="putaway-view" class="view">
          <div class="page-intro"><div><h2>Putaway</h2><p>Tempatkan bahan baku pada lokasi penyimpanan gudang.</p></div></div>
          <section class="panel form-panel"><div class="panel-header"><h3>Input Putaway</h3></div>
            <form id="putawayForm" class="stack-form">
              <div class="field-row">
                <label>Material<select id="putawayMaterial" required></select></label>
                <label>Lokasi<select id="putawayLocation" required></select></label>
                <label>Qty<input id="putawayQty" type="number" min="0.01" step="any" required /></label>
              </div>
              <label>Catatan<input id="putawayRemarks" type="text" /></label>
              <button class="primary-btn" type="submit">Simpan Putaway</button>
            </form>
          </section>
          <section class="panel"><div class="panel-header"><h3>Riwayat Putaway</h3></div>
            <div class="table-scroll"><table class="data-table"><thead><tr><th>Tanggal</th><th>Material</th><th>Lokasi</th><th>Qty</th></tr></thead><tbody id="putawayTableBody"></tbody></table></div>
          </section>
        </section>
'''
if 'id="suppliers-view"' not in index:
    marker = '        <section id="receiving-view"'
    if marker not in index:
        print("ERROR: Tidak menemukan lokasi untuk menambahkan view. Tidak ada file yang diubah.")
        sys.exit(1)
    index = index.replace(marker, views + "\n" + marker, 1)

module_block = '''  var appModules = [
    window.WMS.dashboardModule,
    window.WMS.materialsModule,
    window.WMS.suppliersModule,
    window.WMS.locationsModule,
    window.WMS.receivingModule,
    window.WMS.qcModule,
    window.WMS.putawayModule,
    window.WMS.issuingModule,
    window.WMS.stockModule,
    window.WMS.movementModule,
    window.WMS.opnameModule,
    window.WMS.reportsModule
  ].filter(Boolean);'''
app, count = re.subn(
    r'  var appModules = \[.*?\]\.filter\(Boolean\);',
    module_block, app, count=1, flags=re.S
)
if count != 1:
    print("ERROR: Deklarasi appModules tidak dikenali. Tidak ada file yang diubah.")
    sys.exit(1)

checks = {
    "CSS root": 'href="./style.css"' in index,
    "logo root": 'src="./logo.svg"' in index,
    "favicon root": 'href="./favicon.svg"' in index,
    "tidak ada script js/": 'src="js/' not in index,
    "view Suppliers": 'id="suppliers-view"' in index,
    "view Locations": 'id="locations-view"' in index,
    "view QC": 'id="qc-view"' in index,
    "view Putaway": 'id="putaway-view"' in index,
    "modul suppliers terdaftar": "window.WMS.suppliersModule" in app,
    "modul locations terdaftar": "window.WMS.locationsModule" in app,
    "modul QC terdaftar": "window.WMS.qcModule" in app,
    "modul putaway terdaftar": "window.WMS.putawayModule" in app,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    print("ERROR: Pemeriksaan akhir gagal:")
    for item in failed:
        print(" -", item)
    print("Tidak ada perubahan yang disimpan.")
    sys.exit(1)

# Keep backups before writing.
INDEX.with_suffix(".html.bak").write_text(INDEX.read_text(encoding="utf-8"), encoding="utf-8")
APP.with_suffix(".js.bak").write_text(APP.read_text(encoding="utf-8"), encoding="utf-8")
INDEX.write_text(index, encoding="utf-8")
APP.write_text(app, encoding="utf-8")

print("BERHASIL: index.html dan app.js telah diperbaiki.")
print("Backup awal tersedia sebagai index.html.bak dan app.js.bak.")
print("\nValidasi:")
for name in checks:
    print(" - OK:", name)
print("\nCommit kedua file tersebut ke branch main setelah meninjau hasilnya.")
