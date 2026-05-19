create schema if not exists raw;
create schema if not exists mart;
create schema if not exists measures;

create table if not exists raw.fhir_resource (
  resource_id text primary key,
  resource_type text not null,
  patient_id text,
  source_bundle text,
  payload jsonb not null,
  ingested_at timestamptz not null default now()
);

create table if not exists mart.dim_patient (
  patient_id text primary key,
  birth_date date,
  sex text,
  race text,
  ethnicity text,
  city text,
  state text
);

create table if not exists mart.fact_observation (
  observation_id text primary key,
  patient_id text not null,
  loinc_code text,
  display text,
  value_numeric numeric,
  unit text,
  effective_date date
);

create table if not exists mart.fact_condition (
  condition_id text primary key,
  patient_id text not null,
  code text,
  code_system text,
  display text,
  onset_date date
);

create table if not exists mart.fact_procedure (
  procedure_id text primary key,
  patient_id text not null,
  code text,
  code_system text,
  display text,
  performed_date date
);

create table if not exists measures.fact_measure_results (
  run_id text not null,
  measure_id text not null,
  denominator_count integer not null,
  numerator_count integer not null,
  performance_rate numeric not null,
  created_at timestamptz not null default now(),
  primary key (run_id, measure_id)
);

