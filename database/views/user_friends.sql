CREATE OR REPLACE VIEW user_friends AS
-- Pierwsza część: relacje, gdzie user_1_id jest użytkownikiem, a user_2_id jest jego znajomym
SELECT
    ur.user_1_id AS user_id,              -- Identyfikator użytkownika
    ur.user_2_id AS friend_id,            -- Identyfikator znajomego
    u.username AS friend_username,        -- Nazwa użytkownika znajomego
    u.email AS friend_email               -- Email znajomego
FROM
    user_relationships ur
JOIN
    users u ON ur.user_2_id = u.id        -- Dołączenie tabeli users, aby uzyskać dane znajomego

UNION

-- Druga część: relacje, gdzie user_2_id jest użytkownikiem, a user_1_id jest jego znajomym
SELECT
    ur.user_2_id AS user_id,              -- Identyfikator użytkownika
    ur.user_1_id AS friend_id,            -- Identyfikator znajomego
    u.username AS friend_username,        -- Nazwa użytkownika znajomego
    u.email AS friend_email               -- Email znajomego
FROM
    user_relationships ur
JOIN
    users u ON ur.user_1_id = u.id;       -- Dołączenie tabeli users, aby uzyskać dane znajomego
