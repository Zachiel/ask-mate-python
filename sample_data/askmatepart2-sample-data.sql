--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS pk_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_user DROP CONSTRAINT IF EXISTS pk_question_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_user DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_user DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer_user DROP CONSTRAINT IF EXISTS pk_answer_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer_user DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer_user DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment_user DROP CONSTRAINT IF EXISTS pk_comment_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment_user DROP CONSTRAINT IF EXISTS fk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment_user DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;


DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    votes_up integer NOT NULL,
    votes_down integer NOT NULL,
    title text,
    message text,
    image text
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    votes_up integer NOT NULL,
    votes_down integer NOT NULL,
    question_id integer,
    message text,
    image text,
    accepted boolean NOT NULL,
    edited_count integer
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.accounts;
CREATE TABLE accounts (
    id serial NOT NULL,
    username varchar(50) NOT NULL,
    password varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    fname varchar(100),
    lname varchar(100),
    registrationDate date
);

DROP TABLE IF EXISTS public.question_user;
CREATE TABLE question_user (
    question_id integer NOT NULL,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.answer_user;
CREATE TABLE answer_user (
    answer_id integer NOT NULL,
    user_id integer NOT NULL
);

DROP TABLE IF EXISTS public.comment_user;
CREATE TABLE comment_user (
    comment_id integer NOT NULL,
    user_id integer NOT NULL
);



ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

ALTER TABLE ONLY accounts
    ADD CONSTRAINT pk_id PRIMARY KEY (id);

ALTER TABLE ONLY question_user
    ADD CONSTRAINT pk_question_user_id PRIMARY KEY (question_id, user_id);

ALTER TABLE ONLY question_user
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_user
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES accounts(id);

ALTER TABLE ONLY answer_user
    ADD CONSTRAINT pk_answer_user_id PRIMARY KEY (answer_id, user_id);

ALTER TABLE ONLY answer_user
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer_user
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES accounts(id);

ALTER TABLE ONLY comment_user
    ADD CONSTRAINT pk_comment_user_id PRIMARY KEY (comment_id, user_id);

ALTER TABLE ONLY comment_user
    ADD CONSTRAINT fk_comment_id FOREIGN KEY (comment_id) REFERENCES comment(id);

ALTER TABLE ONLY comment_user
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES accounts(id);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 2, 'How to make lists in Python?', 'I am totally new to this, any hints?', NULL);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 1, 'Wordpress loading multiple jQuery Versions', 'I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();

I could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)', 'static\uploads\197ddde3d1d54ee4b5509e3b36fb88c6.png');
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 5, 'Drawing canvas with an image picked with Cordova Camera Plugin', 'I''m getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I''m on IOS, it throws errors such as cross origin issue, or that I''m trying to use an unknown format.
', NULL);
SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 0, 'You need to use brackets: my_list = []', NULL, false, 0);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 5, 0, 'Look it up in the Python docs', 'static\uploads\8b3c75974759436d9e90d2a73cf018fa.png', true, 0);
SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (1, 0, NULL, 'Please clarify the question as it is too vague!', '2017-05-01 05:49:00');
INSERT INTO comment VALUES (2, NULL, 1, 'I think you could use my_list = list() as well.', '2017-05-02 16:55:00');
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'python');
INSERT INTO tag VALUES (2, 'sql');
INSERT INTO tag VALUES (3, 'css');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);

INSERT INTO accounts VALUES (0, 'HeadAdmin', '$2b$12$4.mUGwYVt9yAFNysWPcdR.1IOrLkQzXSFClCADK9/P6mEbg5wFPk.', 'admin@admin.com', 'AskMate', 'Admin', '1666-06-09');
INSERT INTO accounts VALUES (1, 'JohnnyP', '$2b$12$aOQ2SzqwfC3DCrWNRaa7xe6fIFPeMvPtf3m3ArHZMl2QUXhD3Mfxu', 'test@test.com', 'Iwan', 'Pavluczenko', '2005-04-02');
SELECT pg_catalog.setval('accounts_id_seq', 1, true);

INSERT INTO question_user VALUES (0, 0);
INSERT INTO question_user VALUES (2, 1);

INSERT INTO answer_user VALUES (1, 0);
INSERT INTO answer_user VALUES (2, 1);

INSERT INTO comment_user VALUES (1, 0);
INSERT INTO comment_user VALUES (2, 1);
