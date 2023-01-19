CREATE TABLE answer
(
    answer_id INTEGER PRIMARY KEY IDENTITY(1,1),
    submission_time INTEGER NOT NULL,
    vote_number INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    msg CHARACTER VARYING(800) NOT NULL,
    img CHARACTER VARYING(255),
);

CREATE TABLE question
(
    question_id INTEGER PRIMARY KEY IDENTITY(1,1)
    submission_time INTEGER NOT NULL,
    view_number INTEGER NOT NULL,
    vote_number INTEGER NOT NULL,
    title CHARACTER VARYING(255) NOT NULL,
    msg CHARACTER VARYING(800) NOT NULL,
    img CHARACTER VARYING(255),
);


INSERT INTO answer VALUES
(1493398154,4,1,'You need to use brackets: my_list = []',NULL),
(1493088154,35,1,'Look it up in the Python docs',NULL),
(1673739903,0,5,'Step 1 - Apply to a course at Codecool',NULL),
(1673739911,0,28p,'Step 2 - Git gud',NULL);



INSERT INTO question VALUES
(1493368154,29,7,"How to make lists in Python?","I am totally new to this, any hints?", NULL),
(1493068124,15,9,"Wordpress loading multiple jQuery Versions","I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $('.myBook').booklet();

BUT in my theme i also using jquery via webpack so the loading order is now following:

jquery
booklet
app.js (bundled file with webpack, including jquery)",'images/image1.png'),
(1493015432,1364,57,"Drawing canvas with an image picked with Cordova Camera Plugin","I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.

This is the code I'm using to draw the image (that works on web/desktop but not cordova built ios app)",NULL),
(1672706037,2137,71,"Lorem ipsum dolor, sit amet consectetur adipisicing elit","Lorem ipsum dolor, sit amet consectetur adipisicing elit. Eaque corrupti adipisci architecto veritatis, cupiditate libero aperiam impedit ea magni eius.",NULL)
(1673739872,0,-2,'OMG How do you make a site like this?!',"I really want to know! I'm just starting and this looks like a valuable learning project!
Someone please tell me!",NULL);