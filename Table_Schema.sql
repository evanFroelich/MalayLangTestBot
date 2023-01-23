create table if not exists Questions(
    Question text,
    Reversable integer,
    NumAnswers integer,
    Answer1 text,
    Answer2 text,
    Answer3 text

);

create table if not exists Statistics(
    UserName text,
    UserID integer,
    SessionTime text,
    Streak integer,
    TimePerQuestion real,
    FailQuestion text
);