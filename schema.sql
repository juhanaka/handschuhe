drop table if exists images;
create table images (
  id integer primary key autoincrement,
  filename text unique not null,
  labeled boolean not null,
  face_top_left integer,
  face_bottom_right integer
);

