import re

SKILL_DATABASE = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "R", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala",
        "MATLAB", "Julia", "SAS", "Bash", "Shell", "Perl", "Dart"
    ],
    "Web Development": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
        "Next.js", "Django", "Flask", "FastAPI", "Spring Boot",
        "Laravel", "Bootstrap", "Tailwind CSS", "jQuery", "REST API",
        "GraphQL", "Sass", "Redux", "Webpack"
    ],
    "Mobile Development": [
        "Android", "iOS", "React Native", "Flutter", "Swift", "Kotlin",
        "Xamarin", "Ionic", "Firebase"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Neural Networks", "Random Forest", "XGBoost",
        "LightGBM", "Linear Regression", "Logistic Regression",
        "Decision Tree", "SVM", "K-Means", "PCA",
        "Feature Engineering", "A/B Testing", "Time Series", "Forecasting",
        "Recommendation System", "Sentiment Analysis", "Text Classification",
        "Reinforcement Learning", "Transfer Learning"
    ],
    "ML Frameworks": [
        "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "Hugging Face",
        "OpenCV", "NLTK", "spaCy", "Gensim", "Statsmodels", "Prophet"
    ],
    "Data Analysis": [
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
        "Data Wrangling", "Data Cleaning", "EDA", "Statistical Analysis",
        "Hypothesis Testing", "Data Mining", "Data Preprocessing",
        "Feature Selection", "Exploratory Data Analysis"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "SQLite", "Oracle", "MS SQL Server",
        "MongoDB", "Cassandra", "Redis", "DynamoDB", "Firebase",
        "Elasticsearch", "NoSQL", "Database Design", "Query Optimization",
        "ETL", "Data Pipeline", "Data Warehouse", "MariaDB"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
        "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible",
        "Linux", "Nginx", "Prometheus", "Grafana", "ELK Stack"
    ],
    "Big Data": [
        "Hadoop", "Spark", "PySpark", "Kafka", "Airflow", "Databricks",
        "Snowflake", "BigQuery", "Redshift", "Hive", "MapReduce"
    ],
    "BI & Visualization": [
        "Power BI", "Tableau", "Looker", "Excel", "Google Sheets",
        "DAX", "Power Query", "Dashboard", "Reporting", "SSRS"
    ],
    "Cybersecurity": [
        "Cybersecurity", "Ethical Hacking", "Penetration Testing",
        "Network Security", "Vulnerability Assessment",
        "SIEM", "Firewall", "Wireshark", "Metasploit",
        "Nmap", "Burp Suite", "OWASP", "Cryptography", "SOC",
        "Incident Response", "Kali Linux", "Splunk"
    ],
    "Networking": [
        "Networking", "TCP/IP", "DNS", "DHCP", "VPN", "LAN", "WAN",
        "Cisco", "Router", "Switch", "Firewall", "CCNA",
        "BGP", "OSPF", "Network Monitoring"
    ],
    "Testing & QA": [
        "Manual Testing", "Automation Testing", "Selenium", "Cypress",
        "JUnit", "TestNG", "Pytest", "Postman", "API Testing",
        "Performance Testing", "JMeter", "Appium",
        "Cucumber", "BDD", "TDD", "JIRA",
        "Test Planning", "Test Cases", "Regression Testing", "UAT"
    ],
    "UI/UX Design": [
        "Figma", "Adobe XD", "Sketch", "Wireframing",
        "Prototyping", "UI Design", "UX Design", "User Research",
        "Design Thinking", "Canva", "Adobe Photoshop",
        "Adobe Illustrator", "Material Design"
    ],
    "Project Management": [
        "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Trello",
        "Asana", "Project Management", "PMP", "Waterfall",
        "Risk Management", "Stakeholder Management", "Sprint Planning"
    ],
    "General & Tools": [
        "Git", "GitHub", "GitLab", "VS Code", "IntelliJ",
        "Jupyter", "Postman", "Linux", "Windows Server",
        "Bash", "PowerShell", "Microservices",
        "System Design", "Design Patterns", "OOP",
        "Technical Writing", "Documentation"
    ],
    "ERP & Enterprise": [
        "SAP", "Oracle ERP", "Salesforce", "ServiceNow",
        "Microsoft Dynamics", "SAP ABAP", "SAP MM",
        "SAP SD", "SAP FI", "CRM", "ERP"
    ],
    "Game Development": [
        "Unity", "Unreal Engine", "Game Design",
        "3D Modeling", "Blender", "OpenGL", "Godot",
        "AR", "VR"
    ]
}

ALL_SKILLS = [skill for skills in SKILL_DATABASE.values() for skill in skills]

ROLE_SKILLS = {
    "Data Analyst": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Pandas", "Statistics", "EDA", "Data Cleaning", "Reporting", "Dashboard"],
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics", "TensorFlow", "Scikit-learn", "NLP", "Feature Engineering", "NumPy", "Pandas"],
    "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Docker", "REST API", "AWS", "Git", "Spark", "Kubernetes"],
    "AI/ML Intern": ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "Deep Learning", "Git", "Statistics", "Jupyter"],
    "Data Engineer": ["Python", "SQL", "Spark", "Airflow", "Kafka", "AWS", "ETL", "Data Pipeline", "Docker", "Hadoop", "PostgreSQL"],
    "BI Developer": ["Power BI", "Tableau", "SQL", "DAX", "Power Query", "Excel", "Data Warehouse", "ETL", "Dashboard", "Reporting"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Statistics", "Reporting", "Dashboard", "Agile", "JIRA", "Stakeholder Management"],
    "Research Analyst": ["Python", "R", "Statistics", "Hypothesis Testing", "Excel", "Reporting", "Matplotlib", "Seaborn"],
    "Software Developer": ["Python", "Java", "C++", "Git", "OOP", "REST API", "SQL", "Agile", "Design Patterns"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Bootstrap", "Tailwind CSS", "Git", "Figma", "Redux"],
    "Backend Developer": ["Python", "Java", "Node.js", "SQL", "REST API", "Docker", "Git", "PostgreSQL", "MongoDB", "Microservices"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "Git", "Docker", "REST API"],
    "Mobile App Developer": ["Android", "iOS", "React Native", "Flutter", "Swift", "Kotlin", "Firebase", "Git", "REST API"],
    "Python Developer": ["Python", "Django", "Flask", "FastAPI", "REST API", "SQL", "Git", "Docker", "PostgreSQL", "NumPy", "Pandas"],
    "Java Developer": ["Java", "Spring Boot", "SQL", "Git", "REST API", "Microservices", "Docker", "JUnit"],
    "JavaScript Developer": ["JavaScript", "TypeScript", "React", "Node.js", "Express.js", "Git", "REST API", "MongoDB", "HTML", "CSS"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "Bootstrap", "REST API"],
    "UI/UX Designer": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "UI Design", "UX Design", "User Research", "Design Thinking", "Canva"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux", "CI/CD", "Python", "Bash"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible", "AWS", "Linux", "Python", "Bash"],
    "Site Reliability Engineer": ["Linux", "Docker", "Kubernetes", "Python", "Prometheus", "Grafana", "AWS", "CI/CD", "Bash"],
    "Cybersecurity Analyst": ["Cybersecurity", "Network Security", "SIEM", "Firewall", "Vulnerability Assessment", "Wireshark", "SOC", "Splunk", "Linux"],
    "Ethical Hacker": ["Ethical Hacking", "Penetration Testing", "Kali Linux", "Metasploit", "Nmap", "Burp Suite", "OWASP", "Networking", "Python"],
    "Security Engineer": ["Cybersecurity", "Cryptography", "Network Security", "AWS", "Docker", "Python", "Risk Assessment"],
    "QA Engineer": ["Manual Testing", "Automation Testing", "Selenium", "JIRA", "Test Cases", "API Testing", "Regression Testing", "Postman", "Python", "SQL"],
    "Automation Test Engineer": ["Selenium", "Cypress", "Python", "Java", "TestNG", "JUnit", "Pytest", "CI/CD", "Git", "API Testing", "BDD"],
    "Manual Tester": ["Manual Testing", "Test Cases", "JIRA", "Regression Testing", "UAT", "Test Planning", "Agile", "Postman"],
    "Network Engineer": ["Networking", "Cisco", "TCP/IP", "Router", "Switch", "Firewall", "VPN", "CCNA", "BGP", "OSPF"],
    "System Administrator": ["Linux", "Windows Server", "Networking", "Bash", "PowerShell", "DNS", "DHCP"],
    "IT Support Engineer": ["Networking", "Windows", "Linux", "Troubleshooting", "DNS", "DHCP"],
    "Database Administrator": ["SQL", "MySQL", "PostgreSQL", "Oracle", "MongoDB", "Database Design", "Query Optimization", "Linux"],
    "ERP Consultant": ["SAP", "Oracle ERP", "SAP ABAP", "SAP MM", "SAP SD", "SQL", "ERP", "CRM"],
    "IT Project Manager": ["Project Management", "Agile", "Scrum", "JIRA", "Risk Management", "Stakeholder Management", "PMP"],
    "Scrum Master": ["Scrum", "Agile", "JIRA", "Sprint Planning", "Kanban", "Confluence", "Stakeholder Management"],
    "Technical Writer": ["Technical Writing", "Documentation", "Confluence", "Git", "Postman"],
    "Game Developer": ["Unity", "Unreal Engine", "C#", "C++", "Game Design", "Git", "Blender", "AR", "VR"]
}


def extract_skills(text):
    if not text:
        return []
    text_lower = text.lower()
    found = set()
    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)
    return sorted(list(found))


def get_missing_skills(extracted_skills, job_role):
    required = ROLE_SKILLS.get(job_role, [])
    extracted_lower = [s.lower() for s in extracted_skills]
    return [skill for skill in required if skill.lower() not in extracted_lower]