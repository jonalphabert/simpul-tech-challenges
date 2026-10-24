-- Delivery Planning: initial data (PostgreSQL)
-- Run after schema.sql.

INSERT INTO product (name, category, need_refrigerator) VALUES
    ('Surgical Gloves',          'Medical Supplies', FALSE),
    ('Disposable Syringe',       'Medical Supplies', FALSE),
    ('Paracetamol',              'Medicine',         FALSE),
    ('Vaccine — Hepatitis B',    'Vaccine',          TRUE),
    ('Vaccine — Tetanus Toxoid', 'Vaccine',          TRUE);

-- Note: W02 and W06 have refrigerated storage but only a standard van,
-- so they cannot ship vaccines (constraint 1 in idea.md).
INSERT INTO warehouse (code, location, distance, refrigerated_storage_available, delivery_fleet) VALUES
    ('W01', 'Surabaya',   5, FALSE, 'standard'),
    ('W02', 'Surabaya',  12, TRUE,  'standard'),
    ('W03', 'Sidoarjo',  25, FALSE, 'standard'),
    ('W04', 'Gresik',    30, TRUE,  'refrigerated'),
    ('W05', 'Malang',    90, FALSE, 'standard'),
    ('W06', 'Malang',    95, TRUE,  'standard'),
    ('W07', 'Pasuruan',  45, TRUE,  'refrigerated'),
    ('W08', 'Jember',   150, TRUE,  'refrigerated');

INSERT INTO warehouse_stock (id_warehouse, id_product, quantity)
SELECT w.id, p.id, s.quantity
FROM (VALUES
    ('W01', 'Surgical Gloves',          200),
    ('W01', 'Disposable Syringe',       500),
    ('W01', 'Paracetamol',              300),

    ('W02', 'Surgical Gloves',           50),
    ('W02', 'Vaccine — Hepatitis B',     30),
    ('W02', 'Vaccine — Tetanus Toxoid',  20),

    ('W03', 'Surgical Gloves',          300),
    ('W03', 'Disposable Syringe',       200),

    ('W04', 'Vaccine — Hepatitis B',     40),
    ('W04', 'Vaccine — Tetanus Toxoid',  25),
    ('W04', 'Paracetamol',              100),

    ('W05', 'Surgical Gloves',          400),
    ('W05', 'Disposable Syringe',       300),
    ('W05', 'Paracetamol',              500),

    ('W06', 'Vaccine — Hepatitis B',     20),
    ('W06', 'Vaccine — Tetanus Toxoid',  30),
    ('W06', 'Disposable Syringe',       100),

    ('W07', 'Vaccine — Hepatitis B',      8),
    ('W07', 'Vaccine — Tetanus Toxoid',  10),
    ('W07', 'Surgical Gloves',          150),

    ('W08', 'Vaccine — Hepatitis B',     60),
    ('W08', 'Vaccine — Tetanus Toxoid',  50),
    ('W08', 'Paracetamol',              200)
) AS s (warehouse_code, product_name, quantity)
JOIN warehouse w ON w.code = s.warehouse_code
JOIN product   p ON p.name = s.product_name;
