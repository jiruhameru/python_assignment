CREATE TABLE IF NOT EXISTS financial_data (
  id serial,
  symbol character varying(256),
  date date,
  open_price double precision,
  close_price double precision,
  volume double precision,
  CONSTRAINT financial_data_pkey PRIMARY KEY (id),
  UNIQUE (symbol, date, open_price, close_price, volume)
);  