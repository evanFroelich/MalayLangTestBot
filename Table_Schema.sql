create table if not exists Questions(
    Question text,
    Answer1 text,
    Answer2 text,
    Asnwer3 text,
    Reversable integer,
    NumAnswers integer

);

create table if not exists Statistics(
    UserName text,
    UserID integer,
    SessionTime text,
    Streak integer,
    TimePerQuestion real,
    FailQuestion text
);