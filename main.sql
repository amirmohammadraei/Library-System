-- table for user_account
create table user_account(
    userid int not null PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) BINARY NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, 
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    money integer default 0,
    delay integer default 0
);


-- trigger for username length > 8
delimiter $$
CREATE TRIGGER usernamegsix BEFORE insert ON user_account
    FOR EACH row 
        BEGIN
            DECLARE numLength INT;
            SET numLength = (SELECT LENGTH(NEW.username));
            IF (numLength < 6) THEN
                SIGNAL SQLSTATE '45000' set message_text='Username must consist of 6 characters at least!!!';
            END IF;
end;


-- username complexity
delimiter $$
CREATE TRIGGER usernamecomplexity BEFORE INSERT ON user_account
    FOR EACH ROW
        BEGIN
            IF NOT (SELECT NEW.username REGEXP '[A-Za-z]' and NEW.username REGEXP '[0-9]') THEN
                SIGNAL sqlstate '45000' set message_text = 'Username must have both alphabets an numbers!!';
            END IF;
END;


-- password length > 8
delimiter $$
CREATE TRIGGER passwordg8 BEFORE insert ON user_account
    FOR EACH row 
        BEGIN
            DECLARE numLength INT;
            SET numLength = (SELECT LENGTH(NEW.password));
            IF (numLength < 8) THEN
                SIGNAL SQLSTATE '45000' set message_text='Password must consist of 8 characters at least!!!';
            END IF;
end;


-- password complexity
delimiter $$
CREATE TRIGGER passwordcomplexity BEFORE INSERT ON user_account
    FOR EACH ROW
        BEGIN
            IF NOT (SELECT NEW.password REGEXP '[A-Za-z]' and NEW.password REGEXP '[0-9]') THEN
                SIGNAL sqlstate '45000' set message_text = 'Password must have both alphabets an numbers!!';
            else
                set new.password = SHA2(new.password, 224);
            END IF;
END;


--table `user_information`
create table user_information (
    address varchar(512) not null, 
    fname varchar(50) not null, 
    surname varchar(50) not null, 
    role varchar(50) not null,
    userid int not null,
    FOREIGN KEY (`userid`) REFERENCES `user_account` (`userid`) ON DELETE CASCADE
);


-- table `book`
create table book(
    bookid int not null PRIMARY KEY AUTO_INCREMENT,
    types varchar(40) not null,
    name VARCHAR(50) BINARY NOT NULL UNIQUE,
    writer VARCHAR(50) NOT NULL,
    date date not null, 
    verion int,
    count int,
    price int
);


-- insert money > 0
delimiter $$
CREATE TRIGGER checkvalue BEFORE insert ON user_account
    FOR EACH row 
        BEGIN
            IF (select sign(new.money)) < 1 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The money that you insert must be over 0 toman.';
            END IF;
end;

CREATE TRIGGER checkbvalue BEFORE update ON user_account
    FOR EACH row 
        BEGIN
            IF (select sign(new.money)) < 1 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The money that you insert must be over 0 toman.';
            END IF;
end;


-- check count of book > 0
delimiter $$
CREATE TRIGGER bookcount BEFORE update ON book
    FOR EACH row 
        BEGIN
            IF (select sign(new.count) = -1) and (select sign(old.count) = 0) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This book is not currently available.';
            END IF;
end;


-- reduce moneydelimiter $$
CREATE TRIGGER reduce_money BEFORE update ON user_account
    FOR EACH row 
        BEGIN
            IF (select sign(new.money) = -1) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You do not have enough money.';
            END IF;
end;


-- table of all operations
create table getbook_opt (
    message varchar(512) not null, 
    operation BOOLEAN not null,
    userid int not null,
    FOREIGN KEY (`userid`) REFERENCES `user_account` (`userid`) ON DELETE CASCADE
);


-- accepted reservation
create table inbox (
    inboxid int not null PRIMARY KEY AUTO_INCREMENT,
    message varchar(512) not null, 
    operation BOOLEAN not null default True,
    userid int not null,
    bookid int not null,
    FOREIGN KEY (`userid`) REFERENCES `user_account` (`userid`) ON DELETE CASCADE,
    FOREIGN KEY (`bookid`) REFERENCES `book` (`bookid`) ON DELETE CASCADE,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- deliver delay
delimiter $$
CREATE TRIGGER check_delay BEFORE update ON `inbox`
    FOR EACH row 
        BEGIN
            IF old.deliver_date > CURDATE() THEN
                set new.delays = False;
            END IF;
END;

-- deliver book table
create table deliver_book (
    deliver_id int not null PRIMARY KEY AUTO_INCREMENT,
    message varchar(512) not null, 
    userid int not null,
    bookid int not null,
    FOREIGN KEY (`userid`) REFERENCES `user_account` (`userid`) ON DELETE CASCADE,
    FOREIGN KEY (`bookid`) REFERENCES `book` (`bookid`) ON DELETE CASCADE,
    date_delivered TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- count and version insertion > 0
delimiter $$
CREATE TRIGGER count_version_book BEFORE insert ON book
    FOR EACH row 
        BEGIN
            IF (select sign(new.count) = -1) or (select sign(new.count) = 0) or (select sign(new.verion) = -1) or (select sign(new.verion) = 0) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'نسخه و تعداد کتاب وارد شده باید بزرگتر از صفر باشد';
            END IF;
end;


-- count of book after update
delimiter $$
CREATE TRIGGER count_version_book1 BEFORE update ON book
    FOR EACH row 
        BEGIN
            IF (select sign(new.count) = -1) or (select sign(new.count) = 0) or (select sign(new.verion) = -1) or (select sign(new.verion) = 0) THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'نسخه و تعداد کتاب وارد شده باید بزرگتر از صفر باشد';
            END IF;
end;