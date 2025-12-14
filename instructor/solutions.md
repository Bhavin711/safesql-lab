# SafeSQL-Lab Instructor Solutions Guide

## ⚠️ INSTRUCTOR ACCESS ONLY ⚠️

This document contains detailed solutions and explanations for all SafeSQL-Lab exercises. Use this guide to help students understand SQL injection vulnerabilities and proper mitigation techniques.

## Table of Contents

1. [Exercise 1: Basic Login Injection](#exercise-1-basic-login-injection)
2. [Exercise 2: Product Search Injection](#exercise-2-product-search-injection)
3. [Exercise 3: Item Detail Injection](#exercise-3-item-detail-injection)
4. [Exercise 4: Comment Form Injection](#exercise-4-comment-form-injection)
5. [Exercise 5: Boolean-based Blind Injection](#exercise-5-boolean-based-blind-injection)
6. [Exercise 6: Time-based Blind Injection](#exercise-6-time-based-blind-injection)
7. [General Mitigation Strategies](#general-mitigation-strategies)
8. [Detection and Monitoring](#detection-and-monitoring)

---

## Exercise 1: Basic Login Injection

### Vulnerability Description
The login form constructs SQL queries using string concatenation, allowing attackers to inject malicious SQL code through the username or password fields.

### Vulnerable Code
```python
# VULNERABLE: String concatenation in SQL query
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

### Exploitation Steps

1. **Basic Bypass**: Use `admin'--` in the username field
   - This comments out the password check
   - The query becomes: `SELECT * FROM users WHERE username = 'admin'--' AND password = ''`

2. **Universal Bypass**: Use `admin' OR '1'='1` in the username field
   - This creates a condition that's always true
   - The query becomes: `SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = ''`

3. **Alternative Bypass**: Use `' OR 1=1--` in the username field
   - This bypasses both username and password checks
   - The query becomes: `SELECT * FROM users WHERE username = '' OR 1=1--' AND password = ''`

### Secure Implementation
```python
# SECURE: Using parameterized queries (SQLAlchemy ORM)
user = User.query.filter_by(username=username, password=password).first()
```

### Key Learning Points
- String concatenation in SQL is dangerous
- Parameterized queries prevent injection
- Input validation is essential
- Authentication bypass is a critical vulnerability

---

## Exercise 2: Product Search Injection

### Vulnerability Description
The search functionality directly interpolates user input into SQL queries without proper sanitization, allowing data extraction and manipulation.

### Vulnerable Code
```python
# VULNERABLE: Direct string interpolation
sql_query = f"SELECT * FROM products WHERE name LIKE '%{query_param}%' OR description LIKE '%{query_param}%'"
```

### Exploitation Steps

1. **Information Disclosure**: Use `' UNION SELECT 1,2,3,4--`
   - This reveals the number of columns in the result set
   - Error messages may reveal database structure

2. **Data Extraction**: Use `' UNION SELECT username,password,role,4 FROM users--`
   - This extracts user credentials from the users table
   - Demonstrates how injection can access unrelated data

3. **Database Structure Discovery**: Use `' UNION SELECT sql,2,3,4 FROM sqlite_master--`
   - This reveals the database schema
   - Helps attackers understand the database structure

### Secure Implementation
```python
# SECURE: Using SQLAlchemy ORM with LIKE operator
products = Product.query.filter(
    db.or_(
        Product.name.like(f'%{query_param}%'),
        Product.description.like(f'%{query_param}%')
    )
).all()
```

### Key Learning Points
- UNION-based injection techniques
- Information disclosure through error messages
- Database schema discovery methods
- Importance of proper input sanitization

---

## Exercise 3: Item Detail Injection

### Vulnerability Description
Numeric parameters are used directly in SQL queries without proper validation, allowing stacked queries and data manipulation.

### Vulnerable Code
```python
# VULNERABLE: Numeric parameter without validation
sql_query = f"SELECT p.*, COUNT(c.id) as comment_count FROM products p LEFT JOIN comments c ON p.id = c.product_id WHERE p.id = {item_id} GROUP BY p.id"
```

### Exploitation Steps

1. **Stacked Queries**: Use `1; INSERT INTO users (username,password,role) VALUES ('hacker','password','admin');--`
   - This creates a new admin user
   - Demonstrates how injection can modify data

2. **Data Extraction**: Use `1 UNION SELECT username,password,role,4,5 FROM users--`
   - This extracts user data through the product detail view
   - Shows how injection can access unrelated tables

3. **Privilege Escalation**: Use `1; UPDATE users SET role='admin' WHERE username='alice';--`
   - This escalates a regular user to admin
   - Demonstrates the impact of injection vulnerabilities

### Secure Implementation
```python
# SECURE: Using ORM with proper type conversion
product_id = int(item_id)
product = Product.query.get(product_id)
```

### Key Learning Points
- Numeric parameter vulnerabilities
- Stacked query injection techniques
- Data modification through injection
- Importance of input validation and type checking

---

## Exercise 4: Comment Form Injection

### Vulnerability Description
Multiple form fields are vulnerable to injection, allowing attackers to manipulate the database through comment submission.

### Vulnerable Code
```python
# VULNERABLE: Multiple parameters without sanitization
sql_query = f"INSERT INTO comments (product_id, author, content) VALUES ({product_id}, '{author}', '{content}')"
```

### Exploitation Steps

1. **User Creation**: Use `'; INSERT INTO users (username,password,role) VALUES ('hacker','password','admin');--` in the author field
   - This creates a new admin user
   - Demonstrates how injection can create new accounts

2. **Data Modification**: Use `1; UPDATE users SET role='admin' WHERE username='alice';--` in the product_id field
   - This escalates user privileges
   - Shows how injection can modify existing data

3. **Table Manipulation**: Use `'; DROP TABLE users;--` in the author field
   - This destroys the users table
   - Demonstrates the destructive potential of injection

### Secure Implementation
```python
# SECURE: Using ORM to create new comment
comment = Comment(
    product_id=int(product_id),
    author=author.strip(),
    content=content.strip()
)
db.session.add(comment)
db.session.commit()
```

### Key Learning Points
- Multi-parameter injection vulnerabilities
- Data manipulation through form submission
- Importance of proper data validation
- ORM benefits for security

---

## Exercise 5: Boolean-based Blind Injection

### Vulnerability Description
The application returns different responses based on boolean conditions, allowing attackers to infer data through response analysis.

### Vulnerable Code
```python
# VULNERABLE: Boolean-based blind injection
sql_query = f"SELECT * FROM users WHERE id = {user_id} AND (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0"
```

### Exploitation Steps

1. **Condition Testing**: Use `1 AND 1=1` vs `1 AND 1=2`
   - This determines if the injection point is vulnerable
   - Different responses indicate successful injection

2. **Data Inference**: Use `1 AND (SELECT SUBSTR(username,1,1) FROM users WHERE role='admin') = 'a'`
   - This tests if the first character of the admin username is 'a'
   - Binary search can be used to determine the exact character

3. **Length Determination**: Use `1 AND (SELECT LENGTH(username) FROM users WHERE role='admin') = 5`
   - This determines the length of the admin username
   - Helps plan the extraction process

### Secure Implementation
```python
# SECURE: Using ORM with proper validation
user_id_int = int(user_id)
user = User.query.get(user_id_int)
admin_exists = User.query.filter_by(role='admin').count() > 0
```

### Key Learning Points
- Blind injection concepts
- Boolean-based inference techniques
- Data extraction without direct output
- Importance of consistent error handling

---

## Exercise 6: Time-based Blind Injection

### Vulnerability Description
The application uses timing to infer data, allowing attackers to extract information through response time analysis.

### Vulnerable Code
```python
# VULNERABLE: Time-based blind injection
sql_query = f"SELECT * FROM users WHERE id = {user_id} AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users WHERE role = 'admin') > 0 THEN 1 ELSE 0 END) = 1"
```

### Exploitation Steps

1. **Timing Confirmation**: Use `1 AND (SELECT COUNT(*) FROM users) > 0 AND SLEEP(5)--`
   - This confirms if the injection point is vulnerable
   - 5-second delay indicates successful injection

2. **Data Extraction**: Use `1 AND (SELECT SUBSTR(username,1,1) FROM users WHERE role='admin') = 'a' AND SLEEP(5)--`
   - This tests if the first character is 'a' with timing
   - Binary search can determine the exact character

3. **Automated Extraction**: Use tools like SQLMap or custom scripts
   - This automates the data extraction process
   - Demonstrates the efficiency of automated attacks

### Secure Implementation
```python
# SECURE: Using ORM with proper validation
user_id_int = int(user_id)
user = User.query.get(user_id_int)
admin_exists = User.query.filter_by(role='admin').count() > 0
```

### Key Learning Points
- Time-based injection techniques
- Automated exploitation methods
- Importance of consistent response times
- Detection and monitoring strategies

---

## General Mitigation Strategies

### 1. Parameterized Queries
- Use prepared statements or ORM
- Never concatenate user input into SQL
- Validate all input parameters

### 2. Input Validation
- Validate input types and formats
- Use whitelist validation where possible
- Implement proper error handling

### 3. Principle of Least Privilege
- Use database accounts with minimal permissions
- Separate read and write operations
- Implement proper access controls

### 4. Defense in Depth
- Multiple layers of security
- Input validation, output encoding, and database security
- Regular security testing and monitoring

---

## Detection and Monitoring

### 1. Logging
- Log all database queries
- Monitor for suspicious patterns
- Implement alerting for potential attacks

### 2. Input Monitoring
- Track unusual input patterns
- Monitor for SQL keywords in user input
- Implement rate limiting

### 3. Response Analysis
- Monitor for error messages
- Track response times
- Analyze access patterns

### 4. Automated Detection
- Use WAF (Web Application Firewall)
- Implement intrusion detection systems
- Regular vulnerability scanning

---

## Teaching Tips

1. **Start with Basics**: Begin with simple injection techniques before moving to advanced methods
2. **Compare and Contrast**: Always show both vulnerable and secure implementations
3. **Hands-on Practice**: Let students experiment in the controlled environment
4. **Real-world Context**: Explain how these vulnerabilities affect real applications
5. **Ethical Considerations**: Emphasize responsible disclosure and legal compliance
6. **Defense Strategies**: Focus on prevention and detection methods
7. **Continuous Learning**: Encourage ongoing security education and practice

---

## Additional Resources

- OWASP SQL Injection Prevention Cheat Sheet
- NIST Cybersecurity Framework
- SANS Security Training Resources
- OWASP Top 10 Web Application Security Risks
- SQL Injection Detection and Prevention Best Practices

Remember: These techniques are for educational purposes only. Always ensure proper authorization before testing any system.
