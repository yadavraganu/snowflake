create database Snowflake_ecommerce;
use Snowflake_ecommerce;

create or replace table Customer(
   Id                   NUMBER                  ,
   FirstName            VARCHAR(40)         not null,
   LastName             VARCHAR(40)         not null,
   City                 VARCHAR(40)         ,
   Country              VARCHAR(40)         ,
   Phone                VARCHAR(20)       ,
 primary key (Id));

create or replace  table Customer (
   Id                   NUMBER                  ,
   FirstName            VARCHAR(40)         not null,
   LastName             VARCHAR(40)         not null,
   City                 VARCHAR(40)         null,
   Country              VARCHAR(40)         null,
   Phone                VARCHAR(20)         null,
  primary key (Id)
);

create or replace  table "Order" (
   Id                   NUMBER                  ,
   OrderDate            datetime             not null default CURRENT_TIMESTAMP,
   OrderNumber          VARCHAR(10)         null,
   CustomerId           NUMBER                  not null,
   TotalAmount          decimal(12,2)        null default 0,
   primary key (Id)
);

create or replace  table OrderItem (
   Id                   NUMBER                  ,
   OrderId              NUMBER                  not null,
   ProductId            NUMBER                  not null,
   UnitPrice            decimal(12,2)        not null default 0,
   Quantity             NUMBER                  not null default 1,
     primary key (Id)
);

create or replace  table Product (
   Id                   NUMBER                  ,
   ProductName          VARCHAR(50)         not null,
   SupplierId           NUMBER                  not null,
   UnitPrice            decimal(12,2)        null default 0,
   Package              VARCHAR(30)         null,
   IsDiscontinued       INT                  not null default 0,
     primary key (Id)
);

create or replace  table Supplier (
   Id                   NUMBER                  ,
   CompanyName          VARCHAR(40)         not null,
   ContactName          VARCHAR(50)         null,
   ContactTitle         VARCHAR(40)         null,
   City                 VARCHAR(40)         null,
   Country              VARCHAR(40)         null,
   Phone                VARCHAR(30)         null,
   Fax                  VARCHAR(30)         null,
     primary key (Id)
);


ALTER TABLE "Order" ADD FOREIGN KEY (CustomerId) REFERENCES Customer(id);

ALTER TABLE OrderItem ADD FOREIGN KEY (OrderId) REFERENCES "Order"(id);

ALTER TABLE OrderItem ADD FOREIGN KEY (ProductId) REFERENCES Product(id);

ALTER TABLE Product ADD FOREIGN KEY (SupplierId) REFERENCES Supplier(id);

commit;

select get_ddl('TABLE', '"Order"');