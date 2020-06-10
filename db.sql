-- Table: public.historical_data

-- DROP TABLE public.historical_data;

CREATE TABLE public.historical_data
(
    symbol text COLLATE pg_catalog."default" NOT NULL,
    series text COLLATE pg_catalog."default" NOT NULL,
    tod_open numeric NOT NULL,
    high numeric NOT NULL,
    low numeric NOT NULL,
    tod_close numeric NOT NULL,
    last_price numeric NOT NULL,
    prev_close numeric NOT NULL,
    tot_trd_qty bigint NOT NULL,
    tot_trd_val numeric NOT NULL,
    trd_date date NOT NULL,
    total_trades integer NOT NULL,
    isin text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT historical_data_pkey PRIMARY KEY (symbol, series, trd_date)
)

TABLESPACE pg_default;

ALTER TABLE public.historical_data
    OWNER to postgres;
	
	
###################################################################################################


-- Table: public.future_historical_data

-- DROP TABLE public.future_historical_data;

CREATE TABLE public.future_historical_data
(
    instrument character(10) COLLATE pg_catalog."default" NOT NULL,
    symbol text COLLATE pg_catalog."default" NOT NULL,
    expiry_dt date NOT NULL,
    strike_pr numeric NOT NULL,
    option_typ character(10) COLLATE pg_catalog."default" NOT NULL,
    tod_open numeric,
    high numeric,
    low numeric,
    tod_close numeric,
    settle_pr numeric,
    contracts numeric,
    val_inlakh numeric,
    open_int numeric,
    chg_in_oi numeric,
    trd_date date NOT NULL,
    CONSTRAINT future_historical_data_pkey PRIMARY KEY (instrument, symbol, expiry_dt, strike_pr, option_typ, trd_date)
)

TABLESPACE pg_default;

ALTER TABLE public.future_historical_data
    OWNER to postgres;
	
	
###################################################################################################


-- Table: public.index_data

-- DROP TABLE public.index_data;

CREATE TABLE public.index_data
(
    idx_name text COLLATE pg_catalog."default" NOT NULL,
    trd_date date NOT NULL,
    tod_open numeric,
    high numeric,
    low numeric,
    tod_close numeric,
    pts_change numeric,
    percent_change numeric,
    volume numeric,
    turnover numeric,
    pe numeric,
    pb numeric,
    div_yield numeric,
    CONSTRAINT index_data_pkey PRIMARY KEY (idx_name, trd_date)
)

TABLESPACE pg_default;

ALTER TABLE public.index_data
    OWNER to postgres;