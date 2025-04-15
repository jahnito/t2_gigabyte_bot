CREATE TABLE IF NOT EXISTS "public"."users" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "tg_id" integer NOT NULL,
  "create_user" timestamp NOT NULL,
  "update_user" timestamp NOT NULL,
  "status" integer NOT NULL,
  "role" character(10) NOT NULL,
  "username" character(64) NOT NULL,
  "firstname" character(64) NOT NULL,
  "lastname" character(64) NOT NULL,
  "usertz" integer DEFAULT '2' NOT NULL
);


CREATE TABLE IF NOT EXISTS "public"."notifier" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "tg_id" integer NOT NULL,
  "start_time" time,
  "end_time" time,
  "volume" integer NOT NULL,
  "tz" integer,
  "threshold" real,
  "status" integer
);