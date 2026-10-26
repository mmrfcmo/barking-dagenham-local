-- Barking Local directory foundation for Supabase
-- Apply only to a new/approved Supabase project after reviewing this file.
-- Public users can read verified, published listings. Public writes are deliberately disabled.
-- Listing submissions/claims should be accepted through a server-side Edge Function with validation and anti-spam protection.

create extension if not exists pgcrypto;

create table if not exists public.business_categories (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  slug text not null unique,
  description text,
  is_active boolean not null default true,
  sort_order integer not null default 100,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.businesses (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  slug text not null unique,
  summary text,
  description text,
  address_line_1 text,
  address_line_2 text,
  locality text,
  postcode text,
  borough text not null default 'Barking and Dagenham',
  phone text,
  public_email text,
  website_url text,
  opening_hours jsonb not null default '{}'::jsonb,
  logo_url text,
  image_url text,
  source_name text,
  source_url text,
  source_checked_at timestamptz,
  verification_status text not null default 'unverified'
    check (verification_status in ('unverified', 'needs_review', 'verified', 'rejected')),
  listing_status text not null default 'draft'
    check (listing_status in ('draft', 'published', 'hidden', 'archived')),
  is_featured boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint businesses_verified_source_check
    check (verification_status <> 'verified' or source_checked_at is not null)
);

create table if not exists public.business_category_links (
  business_id uuid not null references public.businesses(id) on delete cascade,
  category_id uuid not null references public.business_categories(id) on delete restrict,
  created_at timestamptz not null default now(),
  primary key (business_id, category_id)
);

create index if not exists businesses_public_name_idx
  on public.businesses (lower(name))
  where listing_status = 'published' and verification_status = 'verified';
create index if not exists businesses_public_borough_idx
  on public.businesses (borough, locality)
  where listing_status = 'published' and verification_status = 'verified';
create index if not exists business_category_links_category_idx
  on public.business_category_links (category_id, business_id);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists business_categories_set_updated_at on public.business_categories;
create trigger business_categories_set_updated_at
before update on public.business_categories
for each row execute function public.set_updated_at();

drop trigger if exists businesses_set_updated_at on public.businesses;
create trigger businesses_set_updated_at
before update on public.businesses
for each row execute function public.set_updated_at();

alter table public.business_categories enable row level security;
alter table public.businesses enable row level security;
alter table public.business_category_links enable row level security;

drop policy if exists "Public can read active categories" on public.business_categories;
create policy "Public can read active categories"
on public.business_categories for select
to anon, authenticated
using (
  is_active = true and exists (
    select 1 from public.business_category_links l
    join public.businesses b on b.id = l.business_id
    where l.category_id = business_categories.id
      and b.listing_status = 'published'
      and b.verification_status = 'verified'
  )
);

drop policy if exists "Public can read verified published businesses" on public.businesses;
create policy "Public can read verified published businesses"
on public.businesses for select
to anon, authenticated
using (listing_status = 'published' and verification_status = 'verified');

drop policy if exists "Public can read categories for visible businesses" on public.business_category_links;
create policy "Public can read categories for visible businesses"
on public.business_category_links for select
to anon, authenticated
using (
  exists (
    select 1 from public.businesses b
    join public.business_categories c on c.id = business_category_links.category_id
    where b.id = business_category_links.business_id
      and b.listing_status = 'published'
      and b.verification_status = 'verified'
      and c.is_active = true
  )
);

-- Intentionally no anonymous INSERT/UPDATE/DELETE policies.
-- Do not expose the Supabase service-role key in browser code.
-- Future listing/claim forms should call a server-side Edge Function, validate inputs,
-- apply rate limits/CAPTCHA, and record moderation status before any listing is published.
