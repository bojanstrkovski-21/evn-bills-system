import os
import sqlite3

from flask import g
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'bills.db')

TAX_TYPES = [
    ('Без данок', 0),
    ('5%', 0.05),
    ('10%', 0.10),
    ('15%', 0.15),
    ('18%', 0.18),
]

PARTNERS = [
    {
        'name': 'Електродистрибуција ДООЕЛ Скопје',
        'edb': '4080016560608',
        'embs': '',
        'address': 'ул. Лазар Личеноски бр. 11',
        'city': 'Скопје',
        'country': 'Република Северна Македонија',
        'phone': '02 3205 300',
        'mobile': '',
        'email': 'info@dso.mk',
        'notes': 'НЛБ Банка 210071492390127; Халк Банка 270071492390134',
    },
    {
        'name': 'ЕСМ Продажба ДООЕЛ Скопје',
        'edb': '4080009508269',
        'embs': '6548474',
        'address': 'ул. 11-ти Октомври бр. 9',
        'city': 'Скопје',
        'country': 'Република Северна Македонија',
        'phone': '02 3149 128',
        'mobile': '',
        'email': 'infofakturi@esm-prodazba.mk',
        'notes': 'elemtrejd@elem.com.mk',
    },
]

ARTICLES = [
    ('Електродистрибуција ДООЕЛ Скопје', 'АВТ', 'Дистрибуција на електрична енергија-АВТ', 'kWh', '18%'),
    ('Електродистрибуција ДООЕЛ Скопје', 'АНТ', 'Дистрибуција на електрична енергија-АНТ', 'kWh', '18%'),
    ('Електродистрибуција ДООЕЛ Скопје', '', 'Надомест за пристап на електродистрибутивниот систем', '', '18%'),
    ('Електродистрибуција ДООЕЛ Скопје', '', 'Комунална такса за јавно осветлување', '', 'Без данок'),
    ('Електродистрибуција ДООЕЛ Скопје', '', 'Законска казнена камата', '', 'Без данок'),
    ('ЕСМ Продажба ДООЕЛ Скопје', 'А ВТ', 'Активна висока тарифа', 'kWh', '18%'),
    ('ЕСМ Продажба ДООЕЛ Скопје', 'А НТ', 'Активна ниска тарифа', 'kWh', '18%'),
    ('ЕСМ Продажба ДООЕЛ Скопје', 'ППЕЕ', 'Повластени производители', 'kWh', '18%'),
    ('ЕСМ Продажба ДООЕЛ Скопје', 'ОПЕЕ', 'Надоместок за користење на пазарот на ел. енергија', 'kWh', '18%'),
]

PLACES = [
    ('Електродистрибуција ДООЕЛ Скопје', 'Димитар Илиевски Мурато, ББ/ЛОК5',
     '003367219', '1309150010005', 'MK0001000000000000000132091500105',
     'ДИМИТАР ИЛИЕВСКИ МУРАТО 0 ББ/Л5/a0, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Б. Кидрич 37',
     '003367435', '1309450010001', 'MK0001000000000000000132094500101',
     'Б.КИДРИЧ 37, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Борис Кидрич бр. 37',
     '003367440', '1309460010001', 'MK0001000000000000000132094600101',
     'ДИМИТАР ИЛИЕВСКИ МУРАТО 37, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Борис Кидрич 37 /a*1',
     '003367454', '1309470010001', 'MK0001000000000000000132094700101',
     'ДИМИТАР ИЛИЕВСКИ МУРАТО 37 /a*1, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Б. Кидрич ББ, графичка работилница',
     '003367469', '1309480010001', 'MK0001000000000000000132094800101',
     'Б.КИДРИЧ 0 ББ/a*1, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Таки Даскалот',
     '003367473', '1309490010002', 'MK0001000000000000000132094900102',
     'ТАКИ ДАСКАЛОТ 0 /a**, Битола 7000'),
    ('Електродистрибуција ДООЕЛ Скопје', 'Таки Даскалот /a*1',
     '003367488', '1309500010009', 'MK0001000000000000000132095000109',
     'ТАКИ ДАСКАЛОТ 0 /a*1, Битола 7000'),
]


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
    return db


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY,
                username        TEXT UNIQUE NOT NULL,
                password_hash   TEXT NOT NULL,
                role            TEXT NOT NULL DEFAULT 'user',
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS tax_types (
                id          INTEGER PRIMARY KEY,
                name        TEXT UNIQUE NOT NULL,
                rate        REAL NOT NULL,
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS partners (
                id          INTEGER PRIMARY KEY,
                name        TEXT NOT NULL,
                edb         TEXT,
                embs        TEXT,
                address     TEXT,
                city        TEXT,
                country     TEXT,
                phone       TEXT,
                mobile      TEXT,
                email       TEXT,
                notes       TEXT,
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS places (
                id                  INTEGER PRIMARY KEY,
                partner_id          INTEGER NOT NULL REFERENCES partners(id),
                name                TEXT NOT NULL,
                customer_number     TEXT NOT NULL,
                consumption_place   TEXT NOT NULL,
                metering_point      TEXT NOT NULL,
                address             TEXT,
                created_at          TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (partner_id, customer_number)
            );

            CREATE TABLE IF NOT EXISTS articles (
                id          INTEGER PRIMARY KEY,
                partner_id  INTEGER NOT NULL REFERENCES partners(id),
                code         TEXT,
                name         TEXT NOT NULL,
                unit         TEXT,
                tax_type_id  INTEGER REFERENCES tax_types(id),
                created_at   TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS invoices (
                id              INTEGER PRIMARY KEY,
                invoice_number  TEXT NOT NULL,
                issue_date      TEXT NOT NULL,
                due_date        TEXT,
                period_from     TEXT,
                period_to       TEXT,
                partner_id      INTEGER NOT NULL REFERENCES partners(id),
                place_id        INTEGER REFERENCES places(id),
                payment_ref     TEXT,
                rounding        REAL NOT NULL DEFAULT 0,
                payment_status  TEXT NOT NULL DEFAULT 'unpaid'
                                CHECK (payment_status IN ('unpaid', 'paid', 'cancelled')),
                notes           TEXT,
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (partner_id, invoice_number)
            );

            CREATE TABLE IF NOT EXISTS invoice_lines (
                id                  INTEGER PRIMARY KEY,
                invoice_id          INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
                line_no             INTEGER NOT NULL,
                article_id          INTEGER REFERENCES articles(id),
                article_code        TEXT,
                description         TEXT NOT NULL,
                quantity            REAL,
                unit                TEXT,
                unit_price          REAL,
                amount_without_tax  REAL NOT NULL,
                tax_type_id         INTEGER REFERENCES tax_types(id),
                tax_rate            REAL NOT NULL,
                tax_amount          REAL NOT NULL,
                amount_with_tax     REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_invoices_partner ON invoices(partner_id);
            CREATE INDEX IF NOT EXISTS idx_invoices_place ON invoices(place_id);
            CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(issue_date);
            CREATE INDEX IF NOT EXISTS idx_lines_invoice ON invoice_lines(invoice_id);
            CREATE INDEX IF NOT EXISTS idx_articles_partner ON articles(partner_id);
        ''')
        line_cols = {row[1] for row in conn.execute('PRAGMA table_info(invoice_lines)')}
        if 'article_id' not in line_cols:
            conn.execute('ALTER TABLE invoice_lines ADD COLUMN article_id INTEGER REFERENCES articles(id)')
        article_cols = {row[1] for row in conn.execute('PRAGMA table_info(articles)')}
        if 'tax_type_id' not in article_cols:
            conn.execute('ALTER TABLE articles ADD COLUMN tax_type_id INTEGER REFERENCES tax_types(id)')
        users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        if users == 0:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
                ('admin', generate_password_hash('admin123')),
            )
            print('  Администратор: admin / admin123 — сменете ја лозинката по првото најавување.')
        if conn.execute('SELECT COUNT(*) FROM tax_types').fetchone()[0] == 0:
            conn.executemany(
                'INSERT INTO tax_types (name, rate) VALUES (?, ?)',
                TAX_TYPES,
            )
        if conn.execute('SELECT COUNT(*) FROM partners').fetchone()[0] == 0:
            for partner in PARTNERS:
                conn.execute(
                    '''INSERT INTO partners
                       (name, edb, embs, address, city, country, phone, mobile, email, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (
                        partner['name'], partner['edb'], partner['embs'],
                        partner['address'], partner['city'], partner['country'],
                        partner['phone'], partner['mobile'], partner['email'],
                        partner['notes'],
                    ),
                )
            for partner_name, name, customer, consumption, meter, address in PLACES:
                partner_id = conn.execute(
                    'SELECT id FROM partners WHERE name = ?', (partner_name,)
                ).fetchone()[0]
                conn.execute(
                    '''INSERT INTO places
                       (partner_id, name, customer_number, consumption_place,
                        metering_point, address)
                       VALUES (?, ?, ?, ?, ?, ?)''',
                    (partner_id, name, customer, consumption, meter, address),
                )
        old = conn.execute(
            "SELECT id, partner_id FROM articles WHERE name = 'Дистрибуција на електрична енергија'"
        ).fetchone()
        if old:
            used = conn.execute(
                'SELECT COUNT(*) FROM invoice_lines WHERE article_id = ?', (old[0],)
            ).fetchone()[0]
            if not used:
                conn.execute('DELETE FROM articles WHERE id = ?', (old[0],))
                tax18 = conn.execute("SELECT id FROM tax_types WHERE name = '18%'").fetchone()[0]
                conn.executemany(
                    '''INSERT INTO articles (partner_id, code, name, unit, tax_type_id)
                       VALUES (?, ?, ?, ?, ?)''',
                    [
                        (old[1], 'АВТ', 'Дистрибуција на електрична енергија-АВТ', 'kWh', tax18),
                        (old[1], 'АНТ', 'Дистрибуција на електрична енергија-АНТ', 'kWh', tax18),
                    ],
                )
        if conn.execute('SELECT COUNT(*) FROM articles').fetchone()[0] == 0:
            for partner_name, code, name, unit, tax_name in ARTICLES:
                partner = conn.execute(
                    'SELECT id FROM partners WHERE name = ?', (partner_name,)
                ).fetchone()
                tax = conn.execute('SELECT id FROM tax_types WHERE name = ?', (tax_name,)).fetchone()
                if partner:
                    conn.execute(
                        '''INSERT INTO articles (partner_id, code, name, unit, tax_type_id)
                           VALUES (?, ?, ?, ?, ?)''',
                        (partner[0], code, name, unit, tax[0] if tax else None),
                    )
        for name, tax_name in (
            ('Надомест за пристап на електродистрибутивниот систем', '18%'),
            ('Комунална такса за јавно осветлување', 'Без данок'),
            ('Законска казнена камата', 'Без данок'),
            ('Активна висока тарифа', '18%'),
            ('Активна ниска тарифа', '18%'),
            ('Повластени производители', '18%'),
            ('Надоместок за користење на пазарот на ел. енергија', '18%'),
            ('Дистрибуција на електрична енергија-АВТ', '18%'),
            ('Дистрибуција на електрична енергија-АНТ', '18%'),
        ):
            conn.execute(
                '''UPDATE articles SET tax_type_id = (
                       SELECT id FROM tax_types WHERE name = ?
                   ) WHERE name = ? AND tax_type_id IS NULL''',
                (tax_name, name),
            )
        conn.commit()
