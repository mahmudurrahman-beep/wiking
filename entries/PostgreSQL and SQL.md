# PostgreSQL and SQL

# PostgreSQL and SQL

## SQL (Structured Query Language)
- **Definition:** SQL is the standard language used to interact with relational databases.  
- **Purpose:** It allows users to create, read, update, and delete data (CRUD operations).  
- **Key Features:**
  - **Data Definition Language (DDL):** Create and modify database structures (e.g., `CREATE TABLE`).  
  - **Data Manipulation Language (DML):** Insert, update, delete, and query data (e.g., `INSERT`, `UPDATE`, `SELECT`).  
  - **Data Control Language (DCL):** Manage permissions and access (e.g., `GRANT`, `REVOKE`).  
  - **Transaction Control Language (TCL):** Handle transactions (e.g., `COMMIT`, `ROLLBACK`).  
- **Usage:** SQL is universal across relational databases like MySQL, PostgreSQL, Oracle, and SQL Server.

## PostgreSQL
- **Definition:** PostgreSQL (often called **Postgres**) is a powerful, open-source relational database system.  
- **Core Strengths:**
  - Fully compliant with SQL standards.  
  - Advanced features like **ACID compliance**, **foreign keys**, **joins**, **views**, and **stored procedures**.  
  - Support for **JSON** and **NoSQL-like queries** alongside relational data.  
  - Extensible with custom functions, data types, and extensions (e.g., PostGIS for geospatial data).  
- **Performance & Reliability:**
  - Strong concurrency control using **MVCC (Multi-Version Concurrency Control)**.  
  - Robust replication and backup options.  
  - Scales from small applications to large enterprise systems.  
- **Community & Ecosystem:**
  - Large open-source community.  
  - Rich ecosystem of tools for monitoring, migration, and integration.  

## Relationship Between SQL and PostgreSQL
- SQL is the **language** used to query and manage data.  
- PostgreSQL is a **database system** that implements SQL (and extends it with advanced features).  
- Example:
  ```sql
  -- SQL query in PostgreSQL
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      name VARCHAR(100),
      email VARCHAR(100) UNIQUE
  );

  INSERT INTO users (name, email)
  VALUES ('Alice', 'alice@example.com');

  SELECT * FROM users;