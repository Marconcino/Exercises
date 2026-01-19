START TRANSACTION;

-- Create the schema (database)
CREATE SCHEMA IF NOT EXISTS restaurant
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

-- Use it
USE restaurant;

-- Drop tables for a clean re-run
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS tables;

-- =========================================================
-- 1) TABLES
-- =========================================================
CREATE TABLE tables (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  table_number  INT NOT NULL UNIQUE,
  max_capacity  INT NOT NULL CHECK (max_capacity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================================
-- 2) CLIENTS
-- =========================================================
CREATE TABLE clients (
  id        BIGINT AUTO_INCREMENT PRIMARY KEY,
  name      VARCHAR(120) NOT NULL,
  phone     VARCHAR(30)  NOT NULL,
  email     VARCHAR(254) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =========================================================
-- 3) BOOKINGS
-- =========================================================
CREATE TABLE bookings (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  client_id BIGINT NOT NULL,
  table_id  BIGINT NOT NULL,
  reservation_date DATE NOT NULL,
  day_of_week ENUM(
    'Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'
  ) NOT NULL,
  reservation_time TIME NOT NULL,
  guest_count INT NOT NULL CHECK (guest_count > 0),
  status ENUM(
    'confirmed','pending','completed','cancelled'
  ) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_bookings_client
    FOREIGN KEY (client_id) REFERENCES clients(id)
    ON DELETE RESTRICT,

  CONSTRAINT fk_bookings_table
    FOREIGN KEY (table_id) REFERENCES tables(id)
    ON DELETE RESTRICT,

  -- Prevent double-booking for the same table at the same date/time
  UNIQUE KEY ux_table_date_time (table_id, reservation_date, reservation_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Helpful indexes (FIXED: bookings, not reservations)
CREATE INDEX idx_bookings_date_time ON bookings (reservation_date, reservation_time);
CREATE INDEX idx_bookings_client    ON bookings (client_id);
CREATE INDEX idx_bookings_table     ON bookings (table_id);

-- =========================================================
-- SEED DATA (10 tables only)
-- =========================================================
INSERT INTO tables (table_number, max_capacity) VALUES
(1, 2),
(2, 2),
(3, 2),
(4, 4),
(5, 4),
(6, 4),
(7, 6),
(8, 6),
(9, 8),
(10, 8);

-- Sample clients
INSERT INTO clients (name, phone, email) VALUES
('Marco Bianchi',       '+39 366 266 2801', 'marco.bianchi@example.com'),
('Giulia Rossi',        '+39 353 715 1861', 'giulia.rossi@example.com'),
('Luca Ferris',         '+39 323 100 3478', 'luca.ferri@example.com'),
('Sara Contini',        '+39 398 124 7460', 'sara.conti@example.com'),
('Ciro Esposito',       '+39 316 742 9778', 'alessandro.de.luca@example.com'),
('Francesca Romano',    '+39 365 189 1950', 'francesca.romano@example.com'),
('Matteo Greco',        '+39 343 171 4517', 'matteo.greco@example.com'),
('Chiara Colombari',    '+39 327 223 1618', 'chiara.colombo@example.com'),
('Davide Rinaldi',      '+39 399 426 2144', 'davide.rinaldi@example.com'),
('Elena Gallona',       '+39 312 138 4943', 'elena.gallo@example.com');

-- Sample bookings
INSERT INTO bookings
(client_id, table_id, reservation_date, day_of_week, reservation_time, guest_count, status)
VALUES
(1, 4,  '2025-12-10', 'Wednesday', '20:30', 4, 'confirmed'),
(2, 9,  '2026-01-10', 'Saturday',  '20:00', 6, 'confirmed'),
(3, 1,  '2026-01-18', 'Sunday',    '19:30', 2, 'pending'),
(4, 7,  '2025-12-21', 'Sunday',    '13:30', 6, 'confirmed'),
(5, 5,  '2025-12-16', 'Tuesday',   '20:00', 3, 'cancelled');

COMMIT;
