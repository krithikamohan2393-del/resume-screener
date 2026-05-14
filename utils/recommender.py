from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

JOB_PROFILES = {
    "Data Analyst":        {"keywords": "python sql excel power bi tableau pandas numpy statistics data visualization data cleaning eda reporting dashboard kpi", "reason": "Strong in SQL, Excel, BI tools & visualization"},
    "Data Scientist":      {"keywords": "python machine learning deep learning nlp scikit-learn tensorflow keras pytorch statistics feature engineering regression classification clustering time series", "reason": "ML/DL knowledge with strong Python analytics"},
    "ML Engineer":         {"keywords": "python machine learning deep learning tensorflow pytorch docker kubernetes aws mlops model deployment rest api fastapi git linux spark", "reason": "ML + engineering skills for production systems"},
    "AI/ML Intern":        {"keywords": "python machine learning deep learning pandas numpy scikit-learn tensorflow keras jupyter git statistics mathematics data preprocessing eda projects", "reason": "Good ML fundamentals for entry-level AI roles"},
    "Data Engineer":       {"keywords": "python sql spark pyspark kafka airflow hadoop aws azure etl data pipeline data warehouse snowflake bigquery docker postgresql", "reason": "Pipeline & infrastructure skills for data engineering"},
    "BI Developer":        {"keywords": "power bi tableau dax power query sql excel data visualization dashboard reporting data warehouse etl business intelligence kpi ssrs", "reason": "Specialized in BI tools & data visualization"},
    "Business Analyst":    {"keywords": "sql excel power bi tableau business intelligence reporting data analysis agile scrum jira dashboard kpi metrics stakeholder requirements", "reason": "Analytical + business communication skills"},
    "Research Analyst":    {"keywords": "python r statistics hypothesis testing regression excel data collection reporting visualization pandas numpy matplotlib seaborn research", "reason": "Research methodology & statistical analysis skills"},
    "Software Developer":  {"keywords": "python java c++ c# git oop data structures rest api sql agile design patterns algorithms problem solving software development", "reason": "Strong programming & software engineering fundamentals"},
    "Frontend Developer":  {"keywords": "html css javascript react angular vue bootstrap tailwind css git figma redux responsive design ui ux typescript", "reason": "Strong HTML/CSS/JS & modern frontend frameworks"},
    "Backend Developer":   {"keywords": "python java node.js sql rest api docker git postgresql mongodb microservices spring boot django flask authentication server", "reason": "Backend frameworks, APIs & database skills"},
    "Full Stack Developer":{"keywords": "html css javascript react node.js python sql mongodb git docker rest api microservices full stack web development", "reason": "Both frontend and backend development skills"},
    "Mobile App Developer":{"keywords": "android ios react native flutter swift kotlin firebase git rest api mobile app development ui design", "reason": "Mobile development frameworks & app building skills"},
    "Python Developer":    {"keywords": "python django flask fastapi rest api sql git docker postgresql numpy pandas automation scripting web development", "reason": "Strong Python with web frameworks & automation"},
    "Java Developer":      {"keywords": "java spring boot hibernate sql maven git rest api microservices docker junit oop design patterns enterprise", "reason": "Java ecosystem & enterprise application development"},
    "JavaScript Developer":{"keywords": "javascript typescript react node.js express.js git rest api mongodb html css angular vue frontend backend", "reason": "JavaScript full-stack development skills"},
    "Web Developer":       {"keywords": "html css javascript react node.js php sql git bootstrap rest api web design responsive cms wordpress", "reason": "Web development skills across frontend & backend"},
    "UI/UX Designer":      {"keywords": "figma adobe xd wireframing prototyping ui design ux design user research design thinking canva sketch usability testing accessibility", "reason": "Design tools & user-centered design skills"},
    "Cloud Engineer":      {"keywords": "aws azure gcp docker kubernetes terraform linux ci/cd python bash cloud architecture s3 ec2 lambda networking", "reason": "Cloud platforms & infrastructure automation skills"},
    "DevOps Engineer":     {"keywords": "docker kubernetes ci/cd jenkins github actions terraform ansible aws linux python bash devops automation monitoring deployment", "reason": "DevOps tools, automation & infrastructure skills"},
    "Site Reliability Engineer": {"keywords": "linux docker kubernetes python prometheus grafana aws ci/cd bash incident response monitoring sre reliability performance", "reason": "Reliability engineering & infrastructure monitoring"},
    "Cybersecurity Analyst":{"keywords": "cybersecurity network security siem firewall vulnerability assessment wireshark soc splunk linux risk assessment incident response threat", "reason": "Security monitoring & threat detection skills"},
    "Ethical Hacker":      {"keywords": "ethical hacking penetration testing kali linux metasploit nmap burp suite owasp networking python cryptography ceh security", "reason": "Penetration testing & offensive security skills"},
    "Security Engineer":   {"keywords": "cybersecurity iam zero trust cryptography network security cloud security aws docker python risk assessment devsecops", "reason": "Security engineering & cloud security skills"},
    "QA Engineer":         {"keywords": "manual testing automation testing selenium jira test cases api testing regression testing postman python sql quality assurance", "reason": "Testing methodologies & QA tools"},
    "Automation Test Engineer": {"keywords": "selenium cypress python java testng junit pytest ci/cd git api testing bdd cucumber automation framework testing", "reason": "Test automation frameworks & scripting skills"},
    "Manual Tester":       {"keywords": "manual testing test cases jira regression testing uat test planning bug reporting agile postman quality software testing", "reason": "Manual testing & quality assurance skills"},
    "Network Engineer":    {"keywords": "networking cisco tcp/ip router switch firewall vpn ccna bgp ospf network monitoring lan wan network administration", "reason": "Network infrastructure & administration skills"},
    "System Administrator":{"keywords": "linux windows server active directory networking bash powershell virtualization backup dns dhcp system administration", "reason": "System & server administration skills"},
    "IT Support Engineer": {"keywords": "networking windows linux hardware troubleshooting active directory itil dns dhcp ticketing support helpdesk customer service", "reason": "IT support & troubleshooting skills"},
    "Database Administrator": {"keywords": "sql mysql postgresql oracle mongodb database design query optimization backup performance tuning linux dba administration", "reason": "Database management & optimization skills"},
    "ERP Consultant":      {"keywords": "sap oracle erp sap abap sap mm sap sd sql business analysis erp crm project management implementation", "reason": "ERP systems & business process skills"},
    "IT Project Manager":  {"keywords": "project management agile scrum jira risk management stakeholder management ms project pmp confluence planning it", "reason": "IT project management & leadership skills"},
    "Scrum Master":        {"keywords": "scrum agile jira sprint planning kanban confluence stakeholder management trello risk management facilitation coaching", "reason": "Agile methodology & scrum facilitation skills"},
    "Technical Writer":    {"keywords": "technical writing documentation markdown confluence git api documentation swagger ms word communication content writing", "reason": "Technical documentation & communication skills"},
    "Game Developer":      {"keywords": "unity unreal engine c# c++ game design 3d modeling git opengl blender ar vr game development physics", "reason": "Game engines & programming skills"}
}

def recommend_jobs(extracted_skills, target_role, top_n=5):
    if not extracted_skills:
        return [{"role": role, "match": 30, "reason": "Upload resume with skills for better matching"} for role in list(JOB_PROFILES.keys())[:top_n]]

    candidate_text = " ".join(extracted_skills).lower()
    all_roles = list(JOB_PROFILES.keys())
    job_texts = [JOB_PROFILES[role]["keywords"] for role in all_roles]
    documents = [candidate_text] + job_texts

    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english", max_features=2000)
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarities = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]

        results = []
        for i, role in enumerate(all_roles):
            boost = 0.15 if role == target_role else 0
            match_pct = min(98, round((similarities[i] + boost) * 100 * 1.5))
            results.append({
                "role": role,
                "match": max(10, match_pct),
                "reason": JOB_PROFILES[role]["reason"]
            })

        results.sort(key=lambda x: x["match"], reverse=True)
        return results[:top_n]

    except Exception:
        return [{"role": role, "match": 40, "reason": JOB_PROFILES[role]["reason"]} for role in all_roles[:top_n]]