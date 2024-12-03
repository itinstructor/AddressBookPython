BEGIN TRANSACTION;
CREATE TABLE tbl_address_book(
            id          INTEGER PRIMARY KEY,
            first_name  TEXT,
            last_name   TEXT,
            phone       TEXT,
            email       TEXT
        );
INSERT INTO "tbl_address_book" VALUES(4,'Phantom','Menace','123.365.2589','phantom@starwars.com');
INSERT INTO "tbl_address_book" VALUES(8,'Fozzie','Bear','301.258.3656','fozzie@funnybear.com');
INSERT INTO "tbl_address_book" VALUES(9,'Fozzie','Bear Jr','301.258.3656','fozziejr@funnybear.com');
INSERT INTO "tbl_address_book" VALUES(11,'Woody the','Cowboy','125.365.1476','woody@toystory.com');
INSERT INTO "tbl_address_book" VALUES(12,'William','Loring','123.456.7890','williamloring@coldmail.com');
INSERT INTO "tbl_address_book" VALUES(15,'Chuck','Berry','125.254.2145','chuck@berry.com');
INSERT INTO "tbl_address_book" VALUES(16,'Kermit the','Frog','547.214.3654','kermit@thefrog.swamp');
INSERT INTO "tbl_address_book" VALUES(17,'Mr','Minecraft','222.032.3254','minecraft@minecraft.com');
INSERT INTO "tbl_address_book" VALUES(18,'Bill','Loring','253.147.2365','loringw@wncc.edu');
INSERT INTO "tbl_address_book" VALUES(19,'Dick','Tracy','302.157.4845','dicktracy@detective.org');
INSERT INTO "tbl_address_book" VALUES(20,'Miss','Kitty','547.214.3654','misskitty@gunsmoke.com');
INSERT INTO "tbl_address_book" VALUES(21,'Marilyn','Monroe','111.111.1111','marilyn@blonde.com');
INSERT INTO "tbl_address_book" VALUES(22,'Winnie the','Pooh','125.478.5236','pooh@poohcorner.com');
INSERT INTO "tbl_address_book" VALUES(23,'Mickey','Mouse','321.689.5247','mickey@disney.com');
INSERT INTO "tbl_address_book" VALUES(24,'Chat','GPT','124.256.3621','chat@gpt.com');
COMMIT;
