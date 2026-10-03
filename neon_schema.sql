--
-- PostgreSQL database dump
--

\restrict i8lJTszXTOHOLakMZBjNLrph9QlWpegCA4ONTQeeRpcLyBYqiJHQSZ6FkKgLK8U

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: llm_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.llm_requests (
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    prompt_hash character varying(64) NOT NULL,
    complexity_level character varying(20) NOT NULL,
    complexity_score integer NOT NULL,
    complexity_features json NOT NULL,
    selected_model character varying(255) NOT NULL,
    selected_provider character varying(50) NOT NULL,
    routing_reason text NOT NULL,
    fallback_used boolean NOT NULL,
    input_tokens integer NOT NULL,
    output_tokens integer NOT NULL,
    latency_ms double precision NOT NULL,
    cost double precision NOT NULL,
    quality_score double precision,
    escalated boolean NOT NULL,
    error_type character varying(100),
    error_message text,
    verification_status character varying(30) DEFAULT 'pending'::character varying NOT NULL,
    verification_model character varying(255),
    verification_reason text,
    escalated_model character varying(255),
    escalation_cost_delta double precision,
    quality_gap double precision,
    user_id integer,
    prompt_preview character varying(200),
    generation_cost double precision DEFAULT 0 NOT NULL,
    verification_cost double precision DEFAULT 0 NOT NULL,
    escalation_cost double precision DEFAULT 0 NOT NULL,
    thinking_tokens integer DEFAULT 0 NOT NULL
);


--
-- Name: llm_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.llm_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: llm_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.llm_requests_id_seq OWNED BY public.llm_requests.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: llm_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llm_requests ALTER COLUMN id SET DEFAULT nextval('public.llm_requests_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: llm_requests llm_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llm_requests
    ADD CONSTRAINT llm_requests_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_llm_requests_prompt_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_llm_requests_prompt_hash ON public.llm_requests USING btree (prompt_hash);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: llm_requests fk_llm_requests_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.llm_requests
    ADD CONSTRAINT fk_llm_requests_user FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict i8lJTszXTOHOLakMZBjNLrph9QlWpegCA4ONTQeeRpcLyBYqiJHQSZ6FkKgLK8U

