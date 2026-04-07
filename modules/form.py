# modules/form.py

import streamlit as st

def get_user_input():
    # ================= SESSION STATE INITIALIZATION =================
    for key in ["education_list", "experience_list", "project_list", "research_list", "language_list"]:
        if key not in st.session_state:
            st.session_state[key] = [{}]

    # ================= MAIN FORM =================
    with st.form("cv_form"):

        # ================= PERSONAL INFO =================
        st.header("👤 Personal Information (Required)")
        name = st.text_input("Full Name *", value=st.session_state.get("name", ""))
        email = st.text_input("Email *", value=st.session_state.get("email", ""))
        phone = st.text_input("Phone *", value=st.session_state.get("phone", ""))

        # ================= PROFILE PHOTO =================
        st.header("🖼 Profile Photo (Optional)")

        profile_photo = st.file_uploader(
            "Upload your photo", type=["png", "jpg", "jpeg"]
        )

        # Save the uploaded file in session_state for later use in PDF
        if profile_photo is not None:
            st.session_state["profile_photo"] = profile_photo
        else:
            st.session_state["profile_photo"] = None

        # ================= ADDITIONAL INFO =================
        st.header("📍 Additional Info (Optional)")
        location = st.text_input("Location", value=st.session_state.get("location", ""))
        linkedin = st.text_input("LinkedIn", value=st.session_state.get("linkedin", ""))
        github = st.text_input("GitHub", value=st.session_state.get("github", ""))
        website = st.text_input("Portfolio Website", value=st.session_state.get("website", ""))

        # ================= SKILLS =================
        st.header("🛠 Skills (Required)")
        skills = st.text_input("Comma-separated skills *", value=st.session_state.get("skills", ""))

        # ================= PROFILE SUMMARY =================
        st.header("🧠 Profile Summary")
        if "ai_profile" not in st.session_state:
            st.session_state["ai_profile"] = ""
        profile = st.text_area(
            "Write your summary or generate one",
            value=st.session_state.get("profile", st.session_state["ai_profile"])
        )

        if st.form_submit_button("✨ Generate AI Summary"):
            if name and skills:
                st.session_state["ai_profile"] = (
                    f"{name} is a motivated professional with skills in {skills}. "
                    f"Passionate about problem-solving, technology, and continuous learning."
                )
                st.success("AI summary generated! Click again to see it.")
            else:
                st.warning("Enter name and skills first")

        # ================= CERTIFICATIONS =================
        st.header("📜 Certifications")

        for i, cert in enumerate(st.session_state.get("certification_list", [{}])):
            st.subheader(f"Certification {i+1}")
            cname = st.text_input(f"Certificate Name {i+1}", value=cert.get("name", ""), key=f"cert_name_{i}")
            clink = st.text_input(f"Certificate Link {i+1}", value=cert.get("link", ""), key=f"cert_link_{i}")

            st.session_state.setdefault("certification_list", [{}])
            st.session_state["certification_list"][i] = {
                "name": cname,
                "link": clink
            }

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_cert", use_container_width=True):
                st.session_state.setdefault("certification_list", [{}])
                st.session_state["certification_list"].append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_cert", use_container_width=True):
                if len(st.session_state.get("certification_list", [{}])) > 1:
                    st.session_state["certification_list"].pop()

        # ================= EDUCATION =================
        st.header("🎓 Education")
        for i, edu in enumerate(st.session_state.education_list):
            st.subheader(f"Education {i+1}")
            degree = st.text_input(f"Degree {i+1}", value=edu.get("degree", ""), key=f"degree_{i}")
            school = st.text_input(f"School {i+1}", value=edu.get("school", ""), key=f"school_{i}")
            year = st.text_input(f"Year {i+1}", value=edu.get("year", ""), key=f"year_{i}")
            st.session_state.education_list[i] = {"degree": degree, "school": school, "year": year}

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_education", use_container_width=True):
                st.session_state.education_list.append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_education", use_container_width=True):
                if len(st.session_state.education_list) > 1:
                    st.session_state.education_list.pop()

        # ================= EXPERIENCE =================
        st.header("💼 Experience")
        for i, exp in enumerate(st.session_state.experience_list):
            st.subheader(f"Experience {i+1}")
            job = st.text_input(f"Job Title {i+1}", value=exp.get("job", ""), key=f"job_{i}")
            company = st.text_input(f"Company {i+1}", value=exp.get("company", ""), key=f"company_{i}")
            duration = st.text_input(f"Duration {i+1}", value=exp.get("duration", ""), key=f"duration_{i}")
            desc = st.text_area(f"Description {i+1}", value=exp.get("description", ""), key=f"desc_{i}")
            st.session_state.experience_list[i] = {"job": job, "company": company, "duration": duration, "description": desc}

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_experience", use_container_width=True):
                st.session_state.experience_list.append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_experience", use_container_width=True):
                if len(st.session_state.experience_list) > 1:
                    st.session_state.experience_list.pop()

        # ================= LANGUAGES =================
        st.header("🌐 Languages")
        for i, lang in enumerate(st.session_state.language_list):
            st.subheader(f"Language {i+1}")
            language_name = st.text_input(f"Language {i+1}", value=lang.get("language", ""), key=f"lang_{i}")
            level = st.selectbox(
                f"Level {i+1}",
                ["Beginner", "Intermediate", "Advanced", "Fluent", "Native"],
                index=["Beginner", "Intermediate", "Advanced", "Fluent", "Native"].index(lang.get("level", "Beginner")),
                key=f"level_{i}"
            )
            st.session_state.language_list[i] = {"language": language_name, "level": level}

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_language", use_container_width=True):
                st.session_state.language_list.append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_language", use_container_width=True):
                if len(st.session_state.language_list) > 1:
                    st.session_state.language_list.pop()

        # ================= PROJECTS =================
        st.header("🌍 Projects")
        for i, proj in enumerate(st.session_state.project_list):
            st.subheader(f"Project {i+1}")
            pname = st.text_input(f"Project Name {i+1}", value=proj.get("name", ""), key=f"pname_{i}")
            pdesc = st.text_area(f"Project Description {i+1}", value=proj.get("description", ""), key=f"pdesc_{i}")
            tech = st.text_input(f"Technologies {i+1}", value=proj.get("technologies", ""), key=f"tech_{i}")
            links = proj.get("links", ["", "", ""])
            link1 = st.text_input("Link 1", value=links[0] if len(links) > 0 else "", key=f"link1_{i}")
            link2 = st.text_input("Link 2", value=links[1] if len(links) > 1 else "", key=f"link2_{i}")
            link3 = st.text_input("Link 3", value=links[2] if len(links) > 2 else "", key=f"link3_{i}")
            st.session_state.project_list[i] = {"name": pname, "description": pdesc, "technologies": tech, "links": [link1, link2, link3]}

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_project", use_container_width=True):
                st.session_state.project_list.append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_project", use_container_width=True):
                if len(st.session_state.project_list) > 1:
                    st.session_state.project_list.pop()

        # ================= RESEARCH =================
        st.header("🔬 Research (Optional)")
        for i, res in enumerate(st.session_state.research_list):
            st.subheader(f"Research {i+1}")
            title = st.text_input(f"Title {i+1}", value=res.get("title", ""), key=f"r_title_{i}")
            desc = st.text_area(f"Description {i+1}", value=res.get("description", ""), key=f"r_desc_{i}")
            authors = st.text_input(f"Authors (optional) {i+1}", value=res.get("authors", ""), key=f"r_auth_{i}")
            publication = st.text_input(f"Publication (optional) {i+1}", value=res.get("publication", ""), key=f"r_pub_{i}")
            year = st.text_input(f"Year (optional) {i+1}", value=res.get("year", ""), key=f"r_year_{i}")
            link = st.text_input(f"Research Link {i+1}", value=res.get("link", ""), key=f"r_link_{i}")
            st.session_state.research_list[i] = {"title": title, "description": desc, "authors": authors, "publication": publication, "year": year, "link": link}

        col1, _, col3 = st.columns([2,6,2])
        with col1:
            if st.form_submit_button("➕ Add", key="add_research", use_container_width=True):
                st.session_state.research_list.append({})
        with col3:
            if st.form_submit_button("➖ Remove", key="remove_research", use_container_width=True):
                if len(st.session_state.research_list) > 1:
                    st.session_state.research_list.pop()

        # ================= DESIGN =================
        st.header("🎨 Design")
        color = st.color_picker("Theme Color", value=st.session_state.get("color", "#000000"))

        # ================= SUBMIT =================
        submit = st.form_submit_button("🚀 Generate CV")

        if submit:
            st.session_state["cv_generated"] = True
            st.success("✅ CV generated! Go to '📄 Preview & Download'")

        # ================= VALIDATION =================
        if submit:
            if not name.strip() or not email.strip() or not phone.strip() or not skills.strip():
                st.error("Please fill all required fields")
                return None

            # Save session_state for later use
            st.session_state["name"] = name
            st.session_state["email"] = email
            st.session_state["phone"] = phone
            st.session_state["location"] = location
            st.session_state["linkedin"] = linkedin
            st.session_state["github"] = github
            st.session_state["website"] = website
            st.session_state["profile"] = profile
            st.session_state["skills"] = skills
            st.session_state["color"] = color

            return {
                "name": name,
                "email": email,
                "phone": phone,
                "profile_photo": profile_photo,
                "location": location,
                "linkedin": linkedin,
                "github": github,
                "website": website,
                "profile": profile,
                "education": st.session_state.education_list,
                "experience": st.session_state.experience_list,
                "skills": skills,
                "certifications": st.session_state.get("certification_list", []),
                "languages": st.session_state.language_list,
                "projects": st.session_state.project_list,
                "research": st.session_state.research_list,
                "color": color
            }

    return None