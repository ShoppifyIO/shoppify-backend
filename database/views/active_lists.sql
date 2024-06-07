CREATE OR REPLACE VIEW active_shopping_lists AS
SELECT
    sl.id AS shopping_list_id,            -- Identyfikator listy zakupów
    sl.title AS title,                    -- Tytuł listy zakupów
    sl.creation_date as creation_date,
    coalesce(sl.update_date, sl.creation_date) AS update_date,        -- Data ostatniej aktualizacji
    c.title AS category_name,             -- Nazwa kategorii
    c.color AS category_color,            -- Kolor kategorii
    u.username AS updated_by,             -- Kto ostatnio zaktualizował
    ou.username as owner_username,
    COALESCE(ur.user_2_id, sl.owner_id) AS user_id, -- Id użytkownika (właściciela lub komu udostępniono)
    CASE
        WHEN sl.owner_id = COALESCE(ur.user_2_id, sl.owner_id) THEN 1
        ELSE 0
    END AS is_user_owner                  -- Czy użytkownik jest właścicielem (1) lub nie (0)
FROM
    shopping_lists sl
join
    users ou on sl.owner_id = ou.id
LEFT JOIN
    categories c ON sl.category_id = c.id
LEFT JOIN
    users u ON sl.updated_by = u.id
LEFT JOIN
    list_sharings ls ON sl.id = ls.shopping_list_id
LEFT JOIN
    user_relationships ur ON ls.user_relationship_id = ur.id
WHERE
    sl.is_completed = false
ORDER BY
    sl.update_date desc;
