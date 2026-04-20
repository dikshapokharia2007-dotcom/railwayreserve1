-- ============================================================
--  Railway Reservation System — MySQL Schema
--  Database: railway_system
-- ============================================================

CREATE DATABASE IF NOT EXISTS railway_system;
USE railway_system;

-- ─────────────────────────────────────────
--  TABLE 1: trains
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS trains (
    train_id    INT           PRIMARY KEY AUTO_INCREMENT,
    train_name  VARCHAR(100)  NOT NULL,
    source      VARCHAR(100)  NOT NULL,
    destination VARCHAR(100)  NOT NULL,
    schedule    VARCHAR(100)  NOT NULL,
    seats       INT           NOT NULL DEFAULT 200
);

-- ─────────────────────────────────────────
--  TABLE 2: bookings
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bookings (
    ticket_id      INT          PRIMARY KEY AUTO_INCREMENT,
    train_name     VARCHAR(100) NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    age            INT          NOT NULL,
    class          VARCHAR(50)  NOT NULL,
    journey_date   DATE         NOT NULL,
    fare           FLOAT        NOT NULL,
    status         VARCHAR(50)  NOT NULL DEFAULT 'Confirmed'
);

-- ─────────────────────────────────────────
--  SAMPLE DATA: trains
-- ─────────────────────────────────────────
INSERT INTO trains (train_name, source, destination, schedule, seats) VALUES
    ('Rajdhani Express',    'New Delhi',      'Mumbai Central', '16:00 - 08:00', 180),
    ('Shatabdi Express',    'New Delhi',      'Chandigarh',     '06:00 - 08:30', 120),
    ('Duronto Express',     'Mumbai Central', 'Kolkata',        '22:30 - 10:30', 200),
    ('Vande Bharat Express','New Delhi',      'Varanasi',       '06:00 - 14:00', 150),
    ('Garib Rath Express',  'Chennai',        'Bengaluru',      '09:00 - 13:30',  90);

-- ─────────────────────────────────────────
--  SAMPLE DATA: bookings
-- ─────────────────────────────────────────
INSERT INTO bookings (train_name, passenger_name, age, class, journey_date, fare, status) VALUES
    ('Rajdhani Express', 'Arjun Sharma', 28, 'AC 2-Tier',  '2024-12-15', 800.00, 'Confirmed'),
    ('Shatabdi Express', 'Priya Mehta',  24, 'Sleeper',    '2024-12-20', 300.00, 'Confirmed'),
    ('Duronto Express',  'Rahul Gupta',  35, 'AC 3-Tier',  '2024-11-30', 500.00, 'Pending');

-- ─────────────────────────────────────────
--  Verification queries (run manually)
-- ─────────────────────────────────────────
-- SELECT * FROM trains;
-- SELECT * FROM bookings;
