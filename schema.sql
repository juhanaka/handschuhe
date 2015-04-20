drop table if exists images;
create table images (
  id integer primary key autoincrement,
  filename text unique not null,
  face_coordinates text,
  eye_coordinates text,
  mouth_coordinates text,
  nose_coordinates text
);

