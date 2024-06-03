create or replace function throw.category_not_found() returns void as $$
begin raise exception 'Nie znaleziono podanej kategorii' using errcode = 'C0001'; end;
$$ language plpgsql;