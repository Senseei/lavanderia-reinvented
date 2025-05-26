CREATE TABLE IF NOT EXISTS "cards"
(
    id       INTEGER
        primary key,
    user_id  INTEGER not null
        references users,
    brand    TEXT    not null,
    number   TEXT    not null,
    method   TEXT    not null,
    due_date TEXT    not null,
    cvv      INTEGER not null
, titular TEXT not null);
CREATE TABLE IF NOT EXISTS "tickets"
(
    id         INTEGER
        primary key,
    code       TEXT                not null
        constraint tickets_pk
            unique,
    discount   NUMERIC             not null,
    expires_at TIMESTAMP default 0 not null,
    type       TEXT                not null
);
CREATE TABLE IF NOT EXISTS "used_tickets"
(
    id        INTEGER
        primary key,
    user_id   INTEGER
        references users,
    ticket_id INTEGER
        references discounts (id),
    constraint used_tickets_pk
        unique (user_id, ticket_id)
);
CREATE TABLE IF NOT EXISTS "cycles"
(
    id    INTEGER
        primary key,
    price NUMERIC default 0 not null,
    time  INTEGER           not null
);
CREATE TABLE IF NOT EXISTS "machines"
(
    id         INTEGER
        constraint machines_pk
            primary key,
    type       TEXT          not null,
    locked     BIT default 0 not null,
    unit_id    INTEGER
        references units,
    identifier TEXT          not null
        constraint machines_pk_2
            unique
);
CREATE TABLE IF NOT EXISTS "units"
(
    id    INTEGER
        primary key,
    local TEXT not null
);
CREATE TABLE IF NOT EXISTS "users"
(
    id       INTEGER
        primary key,
    username TEXT                    not null
        constraint users_pk
            unique,
    name     TEXT                    not null,
    password TEXT                    not null,
    cash     NUMERIC default 2000.00 not null
);

-- INITIAL DATA

-- units
INSERT INTO "units" (id, local) VALUES (1, 'Unidade de São Paulo');

-- cycles
INSERT INTO "cycles" (id, price, time) VALUES
   (1, 14.90, 900),
   (2, 16.90, 1800),
   (3, 18.90, 2700);

-- machines
INSERT INTO "machines" (type, unit_id, identifier) VALUES
   ('Lavadora', 1, '540'),
   ('Lavadora', 1, '541'),
   ('Lavadora', 1, '542'),
   ('Secadora', 1, '537'),
   ('Secadora', 1, '538'),
   ('Secadora', 1, '539');