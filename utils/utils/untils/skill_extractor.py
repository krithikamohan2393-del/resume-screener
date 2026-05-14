import re

SKILL_DATABASE = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "R", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Scala",
        "MATLAB", "Julia", "SAS", "Bash", "Shell", "Perl", "Dart",
        "Assembly", "COBOL", "Fortran", "Groovy", "Lua", "Haskell"
    ],
    "Web Development": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
        "Next.js", "Nuxt.js", "Django", "Flask", "FastAPI", "Spring Boot",
        "Laravel", "Bootstrap", "Tailwind CSS", "jQuery", "REST API",
        "GraphQL", "WebSocket", "Sass", "Redux", "Webpack"
    ],
    "Mobile Development": [
        "Android", "iOS", "React Native", "Flutter", "Swift", "Kotlin",
        "Xamarin", "Ionic", "Cordova", "Firebase"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing",
        "Computer Vision", "Neural Networks", "Random Forest", "XGBoost",
        "LightGBM", "CatBoost", "Linear Regression", "Logistic Regression",
        "Decision Tree", "SVM", "K-Means", "DBSCAN", "PCA",
        "Feature Engineering", "A/B Testing", "Time Series", "Forecasting",
        "Recommendation System", "Sentiment Analysis", "Text Classification",
        "Reinforcement Learning", "Transfer Learning", "GANs"
    ],
    "ML Frameworks": [
        "TensorFlow", "Keras", "PyTorch", "Scikit-learn", "Hugging Face",
        "OpenCV", "NLTK", "spaCy", "Gensim", "FastAI", "Statsmodels", "Prophet"
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
        "Stored Procedures", "ETL", "Data Pipeline", "Data Warehouse",
        "MariaDB", "CouchDB", "Neo4j", "InfluxDB"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud", "S3", "EC2", "Lambda",
        "Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions",
        "Terraform", "Ansible", "Chef", "Puppet", "Helm", "ArgoCD",
        "Linux", "Nginx", "Apache", "Vagrant", "Prometheus", "Grafana",
        "ELK Stack", "Datadog", "CloudFormation", "Pulumi"
    ],
    "Big Data": [
        "Hadoop", "Spark", "PySpark", "Kafka", "Airflow", "Databricks",
        "Snowflake", "BigQuery", "Redshift", "Hive", "MapReduce",
        "Flink", "Storm", "HBase", "Pig", "Sqoop", "Flume"
    ],
    "BI & Visualization": [
        "Power BI", "Tableau", "Looker", "Excel", "Google Sheets",
        "Data Studio", "Metabase", "Grafana", "QlikView", "QlikSense",
        "DAX", "Power Query", "Dashboard", "Reporting", "SSRS", "SSAS"
    ],
    "Cybersecurity": [
        "Cybersecurity", "Ethical Hacking", "Penetration Testing",
        "Network Security", "Information Security", "Vulnerability Assessment",
        "SIEM", "Firewall", "IDS", "IPS", "Wireshark", "Metasploit",
        "Nmap", "Burp Suite", "OWASP", "Cryptography", "SOC",
        "Incident Response", "Digital Forensics", "Risk Assessment",
        "Kali Linux", "Nessus", "Splunk", "Zero Trust", "IAM"
    ],
    "Networking": [
        "Networking", "TCP/IP", "DNS", "DHCP", "VPN", "LAN", "WAN",
        "Cisco", "Router", "Switch", "Firewall", "OSI Model",
        "CCNA", "CCNP", "BGP", "OSPF", "SDN", "Network Monitoring",
        "Wireshark", "Network Administration"
    ],
    "Testing & QA": [
        "Manual Testing", "Automation Testing", "Selenium", "Cypress",
        "JUnit", "TestNG", "Pytest", "Postman", "API Testing",
        "Performance Testing", "Load Testing", "JMeter", "Appium",
        "Robot Framework", "Cucumber", "BDD", "TDD", "JIRA",
        "Test Planning", "Test Cases", "Regression Testing", "UAT"
    ],
    "UI/UX Design": [
        "Figma", "Adobe XD", "Sketch", "InVision", "Wireframing",
        "Prototyping", "UI Design", "UX Design", "User Research",
        "Usability Testing", "Design Thinking", "Canva", "Adobe Photoshop",
        "Adobe Illustrator", "Zeplin", "Material Design", "Accessibility"
    ],
    "Project Management": [
        "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Trello",
        "Asana", "Project Management", "PMP", "Prince2", "Waterfall",
        "Risk Management", "Stakeholder Management", "MS Project",
        "Sprint Planning", "Scrum Master", "Product Owner"
    ],
    "General & Tools": [
        "Git", "GitHub", "GitLab", "Bitbucket", "VS Code", "IntelliJ",
        "Eclipse", "Jupyter", "Postman", "Swagger", "Linux", "Windows Server",
        "MacOS", "Bash", "PowerShell", "Microservices", "SOA",
        "System Design", "Design Patterns", "OOP", "Functional Programming",
        "Technical Writing", "Documentation", "Code Review"
    ],
    "ERP & Enterprise": [
        "SAP", "Oracle ERP", "Salesforce", "ServiceNow", "Workday",
        "Microsoft Dynamics", "SAP HANA", "SAP ABAP", "SAP MM",
        "SAP SD", "SAP FI", "SAP HR", "CRM", "ERP"
    ],
    "Game Development": [
        "Unity", "Unreal Engine", "C#", "C++", "Game Design",
        "3D Modeling", "Blender", "OpenGL", "DirectX", "Godot",
        "Game Physics", "Shader Programming", "AR", "VR"
    ]
}

ALL_SKILLS = [skill for skills in SKILL_DATABASE.values() for skill in skills]

ROLE_SKILLS = {
    # Data & AI
    "Data Analyst": ["SQL", "Python", "Excel", "Power BI", "Tableau", "Pandas", "Statistics", "EDA", "Data Cleaning", "Reporting", "Dashboard"],
    "Data Scientist": ["Python", "Machine Learning", "Deep Learning", "SQL", "Statistics", "TensorFlow", "Scikit-learn", "NLP", "Feature Engineering", "NumPy", "Pandas"],
    "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Docker", "REST API", "AWS", "Git", "Spark", "Kubernetes"],
    "AI/ML Intern": ["Python", "Machine Learning", "Pandas", "NumPy", "Scikit-learn", "Deep Learning", "Git", "Statistics", "Jupyter"],
    "Data Engineer": ["Python", "SQL", "Spark", "Airflow", "Kafka", "AWS", "ETL", "Data Pipeline", "Docker", "Hadoop", "PostgreSQL"],
    "BI Developer": ["Power BI", "Tableau", "SQL", "DAX", "Power Query", "Excel", "Data Warehouse", "ETL", "Dashboard", "Reporting"],
    "Business Analyst": ["SQL", "Excel", "Power BI", "Tableau", "Statistics", "Reporting", "Dashboard", "Agile", "JIRA", "Stakeholder Management"],
    "Research Analyst": ["Python", "R", "Statistics", "Hypothesis Testing", "Excel", "Data Collection", "Reporting", "Matplotlib", "Seaborn"],

    # Software Development
    "Software Developer": ["Python", "Java", "C++", "Git", "OOP", "Data Structures", "REST API", "SQL", "Agile", "Design Patterns"],
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Angular", "Vue.js", "Bootstrap", "Tailwind CSS", "Git", "Figma", "Redux"],
    "Backend Developer": ["Python", "Java", "Node.js", "SQL", "REST API", "Docker", "Git", "PostgreSQL", "MongoDB", "Microservices"],
    "Full Stack Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB", "Git", "Docker", "REST API"],
    "Mobile App Developer": ["Android", "iOS", "React Native", "Flutter", "Swift", "Kotlin", "Firebase", "Git", "REST API"],
    "Python Developer": ["Python", "Django", "Flask", "FastAPI", "REST API", "SQL", "Git", "Docker", "PostgreSQL", "NumPy", "Pandas"],
    "Java Developer": ["Java", "Spring Boot", "Hibernate", "SQL", "Maven", "Git", "REST API", "Microservices", "Docker", "JUnit"],
    "JavaScript Developer": ["JavaScript", "TypeScript", "React", "Node.js", "Express.js", "Git", "REST API", "MongoDB", "HTML", "CSS"],

    # Web
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "Git", "Bootstrap", "REST API", "PHP"],
    "UI/UX Designer": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "UI Design", "UX Design", "User Research", "Design Thinking", "Canva", "Sketch"],

    # Cloud & DevOps
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux", "CI/CD", "Python", "Bash"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible", "AWS", "Linux", "Python", "Bash"],
    "Site Reliability Engineer": ["Linux", "Docker", "Kubernetes", "Python", "Prometheus", "Grafana", "AWS", "CI/CD", "Bash", "Incident Response"],

    # Cybersecurity
    "Cybersecurity Analyst": ["Cybersecurity", "Network Security", "SIEM", "Firewall", "Vulnerability Assessment", "Wireshark", "SOC", "Splunk", "Linux", "Risk Assessment"],
    "Ethical Hacker": ["Ethical Hacking", "Penetration Testing", "Kali Linux", "Metasploit", "Nmap", "Burp Suite", "OWASP", "Networking", "Python", "Cryptography"],
    "Security Engineer": ["Cybersecurity", "IAM", "Zero Trust", "Cryptography", "Network Security", "Cloud Security", "AWS", "Docker", "Python", "Risk Assessment"],

    # Testing
    "QA Engineer": ["Manual Testing", "Automation Testing", "Selenium", "JIRA", "Test Cases", "API Testing", "Regression Testing", "Postman", "Python", "SQL"],
    "Automation Test Engineer": ["Selenium", "Cypress", "Python", "Java", "TestNG", "JUnit", "Pytest", "CI/CD", "Git", "API Testing", "BDD"],
    "Manual Tester": ["Manual Testing", "Test Cases", "JIRA", "Regression Testing", "UAT", "Test Planning", "Bug Reporting", "Agile", "Postman"],

    # Networking
    "Network Engineer": ["Networking", "Cisco", "TCP/IP", "Router", "Switch", "Firewall", "VPN", "CCNA", "BGP", "OSPF", "Network Monitoring"],
    "System Administrator": ["Linux", "Windows Server", "Active Directory", "Networking", "Bash", "PowerShell", "Virtualization", "Backup", "DNS", "DHCP"],
    "IT Support Engineer": ["Networking", "Windows", "Linux", "Hardware", "Troubleshooting", "Active Directory", "ITIL", "DNS", "DHCP", "Ticketing"],

    # Other
    "Database Administrator": ["SQL", "MySQL", "PostgreSQL", "Oracle", "MongoDB", "Database Design", "Query Optimization", "Backup", "Performance Tuning", "Linux"],
    "ERP Consultant": ["SAP", "Oracle ERP", "SAP ABAP", "SAP MM", "SAP SD", "SQL", "Business Analysis", "ERP", "CRM", "Project Management"],
    "IT Project Manager": ["Project Management", "Agile", "Scrum", "JIRA", "Risk Management", "Stakeholder Management", "MS Project", "PMP", "Confluence"],
    "Scrum Master": ["Scrum", "Agile", "JIRA", "Sprint Planning", "Kanban", "Confluence", "Stakeholder Management", "Trello", "Risk Management"],
    "Technical Writer": ["Technical Writing", "Documentation", "Markdown", "Confluence", "Git", "API Documentation", "Swagger", "MS Word", "Communication"],
    "Game Developer": ["Unity", "Unreal Engine", "C#", "C++", "Game Design", "3D Modeling", "Git", "OpenGL", "Blender", "AR", "VR"]
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