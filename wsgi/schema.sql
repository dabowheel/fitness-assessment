drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  sex text,
  weight text,
  weightUnit text,
  mileTime text,
  heartRate text,
  vo2max text
);

drop table if exists profile;
create table profile (
  id integer primary key autoincrement,
  sex text,
  weight text,
  weightUnit text
);