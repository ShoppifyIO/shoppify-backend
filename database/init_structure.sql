create table if not exists users (
    id serial primary key,
    username varchar(50) not null unique,
    email varchar(500) not null unique,
    password_hash text not null,
    is_active boolean not null
);

create table if not exists categories (
    id serial primary key,
    owner_id integer not null references users (id),
    type integer not null,
    title varchar(100) not null,
    description text null,
    color char(7) not null
);

create table if not exists user_items (
    id serial primary key,
    owner_id integer not null references users (id),
    category_id integer null references categories (id),
    name varchar(200) not null
);

create table if not exists shopping_lists (
    id serial primary key,
    owner_id integer not null references users (id),
    category_id integer null references categories (id),
    title varchar(100) not null,
    creation_date timestamp with time zone not null default now(),
    update_date timestamp with time zone null default null,
    updated_by integer null references users (id) default null,
    is_completed boolean not null default false
);

create table if not exists shopping_list_items (
    id serial primary key,
    shopping_list_id integer not null references shopping_lists (id),
    category_id integer null references categories (id),
    name varchar(200) not null,
    quantity integer null,
    is_completed boolean not null,
    added_date timestamp with time zone not null,
    added_by integer not null references users (id),
    completion_date timestamp with time zone null,
    completed_by integer null references users (id)
);

create table if not exists user_relationships (
    id serial primary key,
    user_1_id integer not null references users (id),
    user_2_id integer not null references users (id)
);

create table if not exists list_sharings (
    id serial primary key,
    user_relationship_id integer not null references user_relationships (id),
    shopping_list_id integer not null references shopping_lists (id),
    permission_level integer not null,
    share_date timestamp with time zone not null
);



