create or replace trigger fill_update_fields
    before update on shopping_list_items
    for each row execute procedure fill_update_date();