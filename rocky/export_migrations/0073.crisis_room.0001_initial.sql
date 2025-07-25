CREATE TABLE public.crisis_room_dashboard
(
  "id"              bigint       NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  "name"            varchar(126) NOT NULL,
  "organization_id" bigint NULL
);
ALTER TABLE public.crisis_room_dashboard OWNER TO rocky_dba;
GRANT ALL ON public.crisis_room_dashboard TO rocky;

CREATE TABLE public.crisis_room_dashboarddata
(
  "id"                     bigint       NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
  "recipe"                 uuid NULL,
  "template"               varchar(126) NOT NULL,
  "position"               smallint     NOT NULL CHECK ("position" >= 0),
  "display_in_crisis_room" boolean      NOT NULL,
  "display_in_dashboard"   boolean      NOT NULL,
  "findings_dashboard"     boolean      NOT NULL,
  "dashboard_id"           bigint NULL
);
ALTER TABLE public.crisis_room_dashboarddata OWNER TO rocky_dba;
GRANT ALL ON public.crisis_room_dashboarddata TO rocky;

ALTER TABLE public.crisis_room_dashboard
  ADD CONSTRAINT "crisis_room_dashboard_name_organization_id_d2f1c1ec_uniq" UNIQUE ("name", "organization_id");
ALTER TABLE public.crisis_room_dashboard
  ADD CONSTRAINT "crisis_room_dashboar_organization_id_34198e46_fk_tools_org" FOREIGN KEY ("organization_id")
    REFERENCES "tools_organization" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "crisis_room_dashboard_organization_id_34198e46" ON public.crisis_room_dashboard ("organization_id");

ALTER TABLE public.crisis_room_dashboarddata
  ADD CONSTRAINT "crisis_room_dashboarddata_dashboard_id_position_79fd8cba_uniq" UNIQUE ("dashboard_id", "position");
ALTER TABLE public.crisis_room_dashboarddata
  ADD CONSTRAINT "crisis_room_dashboarddat_dashboard_id_findings_da_253a8abf_uniq" UNIQUE ("dashboard_id", "findings_dashboard");

ALTER TABLE public.crisis_room_dashboarddata
  ADD CONSTRAINT "crisis_room_dashboar_dashboard_id_5950f9a4_fk_crisis_ro" FOREIGN KEY ("dashboard_id")
    REFERENCES public.crisis_room_dashboard ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "crisis_room_dashboarddata_dashboard_id_5950f9a4" ON public.crisis_room_dashboarddata ("dashboard_id");

-- This merges migrations 0001-0003 for the crisis_room app to avoid having to make this migration backward compatible.
-- To conform (at least partly) to the original migrations, these operations are not merged with the ones above.

ALTER TABLE public.crisis_room_dashboard ADD COLUMN "created_at" timestamp with time zone NOT NULL;
ALTER TABLE public.crisis_room_dashboard ADD COLUMN "updated_at" timestamp with time zone NOT NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "created_at" timestamp with time zone NOT NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "name" varchar(126) NOT NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "query" varchar NOT NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "query_from" varchar(32) NOT NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "settings" jsonb NULL;
ALTER TABLE public.crisis_room_dashboarddata ADD COLUMN "updated_at" timestamp with time zone NOT NULL;

ALTER TABLE public.crisis_room_dashboarddata DROP CONSTRAINT "crisis_room_dashboarddat_dashboard_id_findings_da_253a8abf_uniq";
-- Replaced by the DEFERRED "unique dashboard position" version below
ALTER TABLE public.crisis_room_dashboarddata DROP CONSTRAINT "crisis_room_dashboarddata_dashboard_id_position_79fd8cba_uniq";

ALTER TABLE public.crisis_room_dashboarddata
  ADD CONSTRAINT "unique dashboard position" UNIQUE ("dashboard_id", "position") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE public.crisis_room_dashboarddata
  ADD CONSTRAINT "unique dashboard name" UNIQUE ("dashboard_id", "name") DEFERRABLE INITIALLY DEFERRED;
