def render(data_frames):
    import base64
    import os
    import time
    from io import BytesIO

    import pandas as pd
    import streamlit as st
    from PIL import Image, ImageDraw, ImageOps
    from utils.ui_components import render_page_title

    def is_cloud():
        return "appuser" in os.getcwd()

    def format_inr(val):
        try:
            return f"₹ {round(val / 100000, 2)} Lakhs"
        except Exception:
            return "-"

    def format_date(val):
        try:
            return pd.to_datetime(val).strftime("%d-%b-%Y")
        except Exception:
            return "-"

    def create_circular_image(path, size=(150, 150)):
        img = Image.open(path).convert("RGBA").resize(size)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        output = ImageOps.fit(img, size, centering=(0.5, 0.5))
        output.putalpha(mask)
        return output

    def get_circular_image_b64(empid):
        for ext in [".png", ".jpg", ".jpeg"]:
            path = f"data/images/{empid}{ext}"
            if os.path.exists(path):
                img = create_circular_image(path)
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
        return ""

    def export_html_to_pdf_using_cdp(html_path, pdf_path):
        if is_cloud():
            st.warning("PDF export is not supported on Streamlit Cloud.")
            return False

        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1280,1696")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("file://" + os.path.abspath(html_path))
        time.sleep(2)

        result = driver.execute_cdp_cmd(
            "Page.printToPDF",
            {
                "landscape": False,
                "printBackground": True,
                "preferCSSPageSize": True,
            },
        )

        with open(pdf_path, "wb") as f:
            f.write(base64.b64decode(result["data"]))

        driver.quit()
        return True

    df = data_frames.get("employee", pd.DataFrame())
    if df.empty:
        st.warning("Employee data not available.")
        return

    today = pd.to_datetime("today")
    df["date_of_exit"] = pd.to_datetime(df["date_of_exit"], errors="coerce")
    df["date_of_joining"] = pd.to_datetime(df["date_of_joining"], errors="coerce")
    df["last_promotion"] = pd.to_datetime(df["last_promotion"], errors="coerce")
    df["last_transfer"] = pd.to_datetime(df["last_transfer"], errors="coerce")
    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")

    df_active = df[df["date_of_exit"].isna() | (df["date_of_exit"] > today)]

    render_page_title("Talent Profile", "Unified employee intelligence card aligned with the global UI system.")
    emp_id = st.text_input("Enter Employee ID", key="pdf_input")
    if not emp_id:
        return

    try:
        emp_id = int(emp_id)
    except Exception:
        st.error("Employee ID must be numeric.")
        return

    row = df_active[df_active["employee_id"] == emp_id]
    if row.empty:
        st.warning("No active employee found.")
        return

    emp = row.iloc[0]
    photo_b64 = get_circular_image_b64(emp["employee_id"])

    age = "-"
    tenure = "-"
    if pd.notna(emp["date_of_birth"]):
        age = f"{int((today - emp['date_of_birth']).days / 365.25)} yrs"
    if pd.notna(emp["date_of_joining"]):
        delta = today - emp["date_of_joining"]
        years = delta.days // 365
        months = (delta.days % 365) // 30
        tenure = f"{years} yrs {months} months" if years > 0 else f"{months} months"

    def section(title, fields):
        merged_skills = ", ".join(
            filter(None, [str(emp.get("skills_1", "")).strip(), str(emp.get("skills_2", "")).strip(), str(emp.get("skills_3", "")).strip()])
        ) or "-"

        merged_competency = "-"
        if emp.get("competency_type") or emp.get("competency_level"):
            merged_competency = " - ".join(
                filter(None, [str(emp.get("competency_type", "")).strip(), str(emp.get("competency_level", "")).strip()])
            ) or "-"

        rows = [f"<div class='talent-section'><h4>{title}</h4>"]
        for label, key in fields:
            val = emp.get(key, "-")
            if key == "merged_skills":
                val = merged_skills
            if key == "merged_competency":
                val = merged_competency
            if "ctc" in key and pd.notna(val):
                val = format_inr(val)
            elif any(x in key for x in ["date", "promotion", "transfer"]) and pd.notna(val):
                val = format_date(val)
            elif "training" in key and pd.notna(val):
                val = f"{val} hrs"
            elif "exp" in key and pd.notna(val) and isinstance(val, (int, float)):
                val = f"{val} yrs"
            rows.append(f"<div class='talent-row'><div class='talent-label'>{label}</div><div class='talent-value'>{val}</div></div>")
        rows.append("</div>")
        return "".join(rows)

    html = f"""
    <html><head><meta charset='utf-8'>
    <style>
    body {{ font-family: 'Inter', sans-serif; font-size: 13px; margin: 8px; background: transparent; color: #eef3ff; }}
    .talent-profile-shell {{ font-size: 13px; color: #eff4ff; padding: 8px 2px; }}
    .talent-header {{ display:flex; align-items:center; justify-content:space-between; gap:16px; background: linear-gradient(120deg, rgba(25, 34, 74, 0.92), rgba(48, 25, 86, 0.88)); border: 1px solid rgba(255,255,255,0.14); border-radius: 16px; padding: 18px; }}
    .talent-avatar {{ width: 112px; height: 112px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.36); object-fit: cover; }}
    .talent-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-top:14px; }}
    .talent-section {{ background: linear-gradient(145deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02)); border:1px solid rgba(255,255,255,0.14); border-radius:12px; padding:12px 14px; }}
    .talent-section h4 {{ margin:0 0 8px; color:#9adfff; font-size:13px; text-transform:uppercase; letter-spacing:0.6px; }}
    .talent-row {{ display:flex; justify-content:space-between; gap:10px; padding:5px 0; border-bottom:1px solid rgba(255,255,255,0.08); }}
    .talent-row:last-child {{ border-bottom:none; }}
    .talent-label {{ color:#b7c8ff; font-weight:600; }}
    .talent-value {{ color:#ffffff; text-align:right; }}
    @media (max-width: 1100px) {{ .talent-grid {{ grid-template-columns: 1fr; }} }}
    </style></head><body>

    <div class='talent-profile-shell'>
    <div class="talent-header">
        <div>
            <h2>{emp['employee_name']}</h2>
            <div>Employee ID: <b>{emp['employee_id']}</b></div>
            <div>{emp['function']} | {emp['department']} | Band: {emp['band']} | Grade: {emp['grade']}</div>
            <div>Age: {age} | Tenure: {tenure}</div>
        </div>
        {f"<img src='{photo_b64}' class='talent-avatar'/>" if photo_b64 else ''}
    </div>
    """

    html += "<div class='talent-grid'>" + section("Organizational Context", [
        ("Company", "company"), ("Business Unit", "business_unit"),
        ("Department", "department"), ("Function", "function"),
        ("Zone", "zone"), ("Cluster", "cluster"), ("Area", "area"), ("Location", "location")
    ]) + section("Tenure & Movement", [
        ("Date of Joining", "date_of_joining"), ("Last Promotion", "last_promotion"),
        ("Last Transfer", "last_transfer"), ("Total Experience", "total_exp_yrs"),
        ("Previous Experience", "prev_exp_in_yrs"), ("Employment Type", "employment_type")
    ]) + "</div>"

    html += "<div class='talent-grid'>" + section("Compensation", [
        ("Fixed CTC", "fixed_ctc_pa"), ("Variable CTC", "variable_ctc_pa"), ("Total CTC", "total_ctc_pa")
    ]) + section("Performance & Potential", [
        ("Satisfaction Score", "satisfaction_score"), ("Engagement Score", "engagement_score"),
        ("Rating 2025", "rating_25"), ("Rating 2024", "rating_24"),
        ("Top Talent", "Top Talent"), ("Succession Ready", "succession_ready")
    ]) + "</div>"

    html += "<div class='talent-grid'>" + section("Development & Learning", [
        ("Learning Program", "learning_program"), ("Training Hours", "training_hours")
    ]) + section("Competency & Skills", [
        ("Competency", "competency"), ("Competency Details", "merged_competency"), ("Skills", "merged_skills")
    ]) + "</div>"

    html += "<div class='talent-grid'>" + section("Education & Background", [
        ("Qualification", "qualification"), ("Highest Qualification", "highest_qualification"),
        ("Qualification Type", "qualification_type"), ("Previous Employers", "previous_employers"),
        ("Last Employer", "last_employer"), ("Employment Sector", "employment_sector")
    ]) + "</div></div></body></html>"

    st.components.v1.html(html, height=1000, scrolling=True)

    os.makedirs("exports", exist_ok=True)
    html_path = os.path.join("exports", f"profile_{emp['employee_id']}.html")
    pdf_path = os.path.join("exports", f"profile_{emp['employee_id']}.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    if not is_cloud():
        pdf_success = export_html_to_pdf_using_cdp(html_path, pdf_path)
        if pdf_success:
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download as PDF", f, file_name=os.path.basename(pdf_path))
    else:
        st.info("PDF export is not available on Streamlit Cloud deployment.")
