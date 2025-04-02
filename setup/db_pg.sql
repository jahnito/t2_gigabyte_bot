CREATE TABLE IF NOT EXISTS "public"."users" (
  "id" serial NOT NULL,
  PRIMARY KEY ("id"),
  "tg_id" integer NOT NULL,
  "create_user" timestamp NOT NULL,
  "update_user" timestamp NOT NULL,
  "status" integer NOT NULL,
  "role" character(10) NOT NULL,
  "username" character(128) NOT NULL,
  "firstname" character(128) NOT NULL,
  "lastname" character(128) NOT NULL
);

