-- Samantha Voigt
-- Clears out the login table, to be run at the end of every semester


use svoigt_db;


drop table if exists profile_info;
drop table if exists login; 

create table login(
    login_id varchar(50) not null primary key, 
    passhash char(40), -- for sha1 hash
    INDEX(login_id)
    )
    ENGINE = InnoDB;

create table profile_info(
    login_id varchar(50) not null primary key, 
    name varchar(50),
    about text,
    class_year char(4),
    url varchar(50),
    INDEX (login_id),
    foreign key (login_id) references login (login_id) on delete cascade
    )
    ENGINE = InnoDB;
