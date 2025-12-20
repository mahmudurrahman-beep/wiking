# Django

# Django

**Django** is a high-level, open-source **Python web framework** that enables rapid development of secure and maintainable websites. It emphasizes the principles of **reusability**, **scalability**, and the **Don't Repeat Yourself (DRY)** philosophy.

## History
- Created in **2003** by Adrian Holovaty and Simon Willison while working at the Lawrence Journal-World newspaper.  
- Released publicly in **2005** under a BSD license.  
- Named after the jazz guitarist **Django Reinhardt**.  
- Maintained by the **Django Software Foundation (DSF)**.

## Key Features
- **MVT Architecture (Model–View–Template):**  
  - **Model:** Defines data structure and database schema.  
  - **View:** Handles business logic and request/response.  
  - **Template:** Controls presentation layer (HTML).  
- **Built-in Admin Interface:** Auto-generated admin panel for managing data.  
- **ORM (Object-Relational Mapper):** Interact with databases using Python objects instead of raw SQL.  
- **Authentication System:** User accounts, sessions, permissions, and security features.  
- **Security:** Protection against common attacks (CSRF, SQL injection, XSS).  
- **Scalability:** Suitable for small projects and large-scale applications.  
- **Extensibility:** Thousands of reusable apps and packages available.

## Advantages
- Rapid development with minimal boilerplate.  
- Strong documentation and large community.  
- Easy database switching and migrations.  
- Encourages clean, pragmatic design.  

## Example
```python
# views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, world!")