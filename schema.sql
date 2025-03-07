-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS referrals;

-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     email TEXT UNIQUE NOT NULL,
--     name TEXT NOT NULL,
--     mobile TEXT NOT NULL,
--     city TEXT NOT NULL,
--     referral_code TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL
-- );

-- CREATE TABLE referrals (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     referrer_id INTEGER NOT NULL,
--     referee_id INTEGER NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
--     FOREIGN KEY (referee_id) REFERENCES users(id) ON DELETE CASCADE
-- );


DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS referrals;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    city TEXT NOT NULL,
    referral_code TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id INTEGER NOT NULL,
    referee_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (referrer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (referee_id) REFERENCES users(id) ON DELETE CASCADE
);
