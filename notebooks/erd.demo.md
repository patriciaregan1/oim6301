```mermaid
erDiagram
  COUNTIES ||--o{ TOWNS : contains
  COUNTIES {
    string name PK
    int founded_year
  }
  TOWNS {
    string name PK
    string county FK
  }
```