CREATE TABLE users (id INTEGER, username TEXT, name TEXT, password TEXT, cash NUMERIC DEFAULT 2000.00, PRIMARY KEY(id));
CREATE TABLE cycles (id INTEGER, price NUMERIC, time INTEGER, PRIMARY KEY(id));
CREATE TABLE units (id INTEGER, local TEXT, PRIMARY KEY(id));
CREATE TABLE history (id INTEGER, user_id INTEGER,  unit_id INTEGER, machine_id INTEGER, cycle_id INTEGER, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(unit_id) REFERENCES units(id), FOREIGN KEY(cycle_id) REFERENCES cycles(id));
CREATE TABLE IF NOT EXISTS "machines"
(
    id         INTEGER,
    type       TEXT,
    locked     BIT,
    unit_id    INTEGER
        references units,
    identifier TEXT
        constraint machines_pk
            unique
);
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
