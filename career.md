---
title: Career
layout: default
---

# Career

<div class="career-container">
    <div class="career-item" onclick="toggleDetails('corrigo')">
        <img src="{{ '/images/corrigo_logo.png' | relative_url }}" alt="Corrigo Logo" class="company-logo">
        <h3>ML Engineer at Corrigo (now part of JLL-Technologies)</h3>
    </div>
    <div id="corrigo" class="career-details">
        <p>As an ML Engineer at Corrigo, I worked on developing machine learning models to improve operational efficiency and predictive maintenance.</p>
        <ul>
            <li>Developed predictive maintenance models</li>
            <li>Improved operational efficiency through ML solutions</li>
            <li>Collaborated with cross-functional teams</li>
        </ul>
    </div>

    <div class="career-item" onclick="toggleDetails('senior-data-scientist')">
        <img src="{{ '/images/corrigo_logo.png' | relative_url }}" alt="Corrigo Logo" class="company-logo">
        <h3>Senior Data Scientist at Corrigo</h3>
    </div>
    <div id="senior-data-scientist" class="career-details">
        <p>As a Senior Data Scientist, I led data science projects to extract insights from large datasets and drive business decisions.</p>
        <ul>
            <li>Led data science projects</li>
            <li>Extracted insights from large datasets</li>
            <li>Drove business decisions through data analysis</li>
        </ul>
    </div>

    <div class="career-item" onclick="toggleDetails('co-star')">
        <img src="{{ '/images/costar_logo.png' | relative_url }}" alt="Co Star Logo" class="company-logo">
        <h3>Data Scientist at Co Star</h3>
    </div>
    <div id="co-star" class="career-details">
        <p>At Co Star, I focused on building data-driven solutions to enhance real estate market analysis and forecasting.</p>
        <ul>
            <li>Built data-driven solutions for market analysis</li>
            <li>Enhanced real estate market forecasting</li>
            <li>Worked closely with stakeholders to deliver insights</li>
        </ul>
    </div>

    <div class="career-item" onclick="toggleDetails('analytics-consulting')">
        <img src="{{ '/images/musigma.png' | relative_url }}" alt="Consulting Logo" class="company-logo">
        <h3>Mu Sigma - Analytics & Consulting</h3>
    </div>
    <div id="analytics-consulting" class="career-details">
        <p>I started my career in analytics and consulting, helping clients leverage data to solve complex business problems.</p>
        <ul>
            <li>Provided data-driven consulting services</li>
            <li>Helped clients solve complex business problems</li>
            <li>Developed analytical models to support decision-making</li>
        </ul>
    </div>
</div>

<script>
function toggleDetails(id) {
    var element = document.getElementById(id);
    if (element.style.display === "none" || element.style.display === "") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}
</script>