from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

url = "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=Data+engineer&l=Toulouse+31000"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) "
        "Gecko/20100101 Firefox/122.0 (Contact: injechta@gmail.com - Projet"
        " d'apprentissage Data Engineering)"
    )
}

print("Récupération des offres de Data Engineer à Toulouse...")
response = requests.get(url, headers=headers)
jobs_data = []

if response.status_code == 200:
  soup = BeautifulSoup(response.text, "html.parser")
  job_cards = soup.find_all(
      "a", class_=lambda x: x and "no-underline" in x.lower()
  )

  for card in job_cards:
    title_tag = card.find(
        "p", class_=lambda x: x and "typo-1" in x.lower()
    ) or card.find("h3")
    company_tag = card.find("p", class_=lambda x: x and "typo-s" in x.lower())

    if title_tag:
      title = title_tag.get_text(strip=True)
      company = (
          company_tag.get_text(strip=True) if company_tag else "Non spécifié"
      )

      if company in title:
        title = title.replace(company, "").strip()

      href = card.get("href", "")
      link = (
          href if href.startswith("http") else f"https://www.hellowork.com{href}"
      )

      jobs_data.append({"Titre": title, "Entreprise": company, "Lien": link})

  df_search = pd.DataFrame(jobs_data).drop_duplicates(subset=["Lien"])
  detailed_jobs = []

  for index, row in df_search.iterrows():
    print(
        f"Traitement ({index+1}/{len(df_search)}) : {row['Titre']} chez"
        f" {row['Entreprise']}"
    )
    try:
      detail_res = requests.get(row["Lien"], headers=headers)
      if detail_res.status_code == 200:
        detail_soup = BeautifulSoup(detail_res.text, "html.parser")

        # 1. Extraction sécurisée du salaire
        salaire = "Non spécifié"
        salary_span = detail_soup.find(
            "span", class_=lambda x: x and "truncate" in str(x)
        )
        if salary_span and "€" in salary_span.get_text():
          salaire = salary_span.get_text(strip=True)
        else:
          for li in detail_soup.find_all("li"):
            text_li = li.get_text(strip=True)
            if "€" in text_li or "an" in text_li or "mois" in text_li:
              salaire = text_li
              break

        # 2. Extraction des autres infos
        infos = []
        tags_list = detail_soup.find("ul", class_=lambda x: x and "flex-wrap" in str(x))
        if tags_list:
          for li in tags_list.find_all("li"):
            txt = li.get_text(strip=True)
            if txt and txt != salaire and "€" not in txt and len(txt) < 40:
              infos.append(txt)

        # 3. Extraction des technos
        technos = []
        skill_container = detail_soup.find(
            "div", class_=lambda x: x and "candidate-skills" in str(x)
        ) or detail_soup.find(
            "div", id=lambda x: x and "candidate-skills" in str(x)
        )

        if skill_container:
          for el in skill_container.find_all(["li", "span", "button"]):
            t = el.get_text(strip=True)
            if t and len(t) < 25 and t not in technos:
              technos.append(t)

        if not technos:
          common_techs = [
              "Python",
              "SQL",
              "Spark",
              "Kafka",
              "AWS",
              "GCP",
              "Docker",
              "Kubernetes",
              "Airflow",
              "Databricks",
              "Snowflake",
              "Azure",
              "Git",
              "Jira",
              "dbt",
          ]
          page_text = detail_soup.get_text()
          for tech in common_techs:
            if tech.lower() in page_text.lower() and tech not in technos:
              technos.append(tech)

        # 4. Description
        content_blocks = detail_soup.find_all(
            "div", class_=lambda x: x and "typo-long-m" in str(x)
        )
        description = (
            "<br><br>".join([
                block.get_text(separator=" ", strip=True)
                for block in content_blocks
            ])
            if content_blocks
            else "Description non disponible."
        )

        detailed_jobs.append({
            "Titre": row["Titre"],
            "Entreprise": row["Entreprise"],
            "Salaire": salaire,
            "Infos": " • ".join(infos[:5]),
            "Technos": technos if technos else ["Data Engineering"],
            "Lien": row["Lien"],
            "Description": description,
        })
      time.sleep(1)
    except Exception as e:
      print(f"Erreur sur l'offre {row['Titre']} : {e}")

  # Génération de la page HTML optimisée (mode sombre par défaut, bouton épuré)
  html_content = f"""<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Pipeline | Data Radar - Toulouse</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --badge-bg: #0369a1;
            --badge-text: #e0f2fe;
            --salary-bg: #064e3b;
            --salary-text: #6ee7b7;
            --desc-bg: #0f172a;
            --border-color: #334155;
            --btn-toggle-bg: #334155;
            --btn-toggle-text: #f8fafc;
        }}

        [data-theme="light"] {{
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --accent: #0284c7;
            --accent-hover: #0369a1;
            --badge-bg: #e0f2fe;
            --badge-text: #0369a1;
            --salary-bg: #dcfce7;
            --salary-text: #166534;
            --desc-bg: #f8fafc;
            --border-color: #e2e8f0;
            --btn-toggle-bg: #e2e8f0;
            --btn-toggle-text: #334155;
        }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            transition: background-color 0.3s, color 0.3s;
        }}

        .container {{
            max-width: 950px;
            margin: 0 auto;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            background: var(--card-bg);
            padding: 15px 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            border: 1px solid var(--border-color);
            transition: background 0.3s, border-color 0.3s;
        }}

        h1 {{
            font-size: 1.4rem;
            color: var(--accent);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .theme-toggle {{
            background: var(--btn-toggle-bg);
            color: var(--btn-toggle-text);
            border: 1px solid var(--border-color);
            padding: 8px 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.2s, color 0.2s;
        }}

        .theme-toggle:hover {{
            opacity: 0.9;
        }}

        .job-card {{
            background: var(--card-bg);
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            padding: 22px;
            margin-bottom: 20px;
            border: 1px solid var(--border-color);
            transition: transform 0.2s, background 0.3s, border-color 0.3s;
        }}

        .job-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.15);
        }}

        .job-title {{
            font-size: 1.25rem;
            color: var(--text-main);
            margin: 0 0 5px 0;
            font-weight: 700;
        }}

        .company-name {{
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 12px;
            font-size: 0.95rem;
        }}

        .salary {{
            display: inline-block;
            background-color: var(--salary-bg);
            color: var(--salary-text);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 10px;
            margin-right: 8px;
        }}

        .badge {{
            display: inline-block;
            background-color: var(--badge-bg);
            color: var(--badge-text);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8rem;
            margin-right: 6px;
            margin-bottom: 10px;
            font-weight: 600;
        }}

        .infos {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 12px;
            background: var(--desc-bg);
            padding: 6px 12px;
            border-radius: 6px;
            display: inline-block;
            border: 1px solid var(--border-color);
        }}

        .description {{
            font-size: 0.9rem;
            color: var(--text-muted);
            line-height: 1.6;
            max-height: 140px;
            overflow-y: auto;
            background: var(--desc-bg);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid var(--accent);
            margin-bottom: 15px;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }}

        .btn {{
            display: inline-block;
            background-color: var(--accent);
            color: #0f172a;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 700;
            transition: background 0.2s;
        }}

        .btn:hover {{
            background-color: var(--accent-hover);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚡ Nexus Pipeline — ScrapeloWork</h1>
            <button class="theme-toggle" onclick="toggleTheme()">🌓 Basculer le thème</button>
        </header>
"""

  for job in detailed_jobs:
    badges_html = "".join([
        f'<span class="badge">{t}</span>' for t in job["Technos"]
    ])
    salary_html = (
        f'<div class="salary">💰 {job["Salaire"]}</div>'
        if job["Salaire"] != "Non spécifié"
        else '<div class="salary" style="background:#7f1d1d; color:#fca5a5;">💰 Salaire non spécifié</div>'
    )
    infos_html = f'<div class="infos">📋 {job["Infos"]}</div>' if job["Infos"] else ""

    html_content += f"""
        <div class="job-card">
            <h2 class="job-title">{job['Titre']}</h2>
            <div class="company-name">🏢 {job['Entreprise']}</div>
            <div>{salary_html}</div>
            {infos_html}
            <div>{badges_html}</div>
            <div class="description">{job['Description']}</div>
            <a href="{job['Lien']}" target="_blank" class="btn">Voir l'offre originale →</a>
        </div>
    """

  html_content += """
    </div>
    <script>
        function toggleTheme() {
            const html = document.documentElement;
            const currentTheme = html.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";
            html.setAttribute("data-theme", newTheme);
        }
    </script>
</body>
</html>
"""

  with open("offres_toulouse.html", "w", encoding="utf-8") as f:
    f.write(html_content)

  print("\n✨ Page mise à jour avec mode sombre par défaut : 'offres_toulouse.html' 🌐")

else:
  print(f"Erreur HTTP : {response.status_code}")