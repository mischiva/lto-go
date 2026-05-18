-- test account natin ito
-- username: admin.lto@gov.ph
-- password: endthesem

CREATE TABLE IF NOT EXISTS app_users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

INSERT INTO app_users (username, password)
VALUES ('admin.lto@gov.ph', 'endthesem')
ON CONFLICT (username)
DO UPDATE SET password = EXCLUDED.password;
