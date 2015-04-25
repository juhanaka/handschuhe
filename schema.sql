drop table if exists images;
create table images (
  id integer primary key autoincrement,
  filename text unique not null,
  size text,
  face_coordinates text,
  left_eye_coordinates text,
  right_eye_coordinates text,
  mouth_coordinates text,
  nose_coordinates text
);

