---
title: Career
layout: default
---

<!-- # Career -->

<div class="career-container">
    <div class="career-item" onclick="toggleDetails('moodys')">
        <img src="{{ '/images/ma_logo.png' | relative_url }}" alt="Moodys Logo" class="company-logo">
        <div class="career-info">
            <h3>ML + Data Tech Lead at Moodys Analytics</h3>
            <p class="career-date">November 2022 - Present</p>
        </div>
    </div>
    <div id="moodys" class="career-details">
        <p>I lead a group under the Data and AI Functional Group in the KYC OU in Moodys Analytics. The main projects I oversee are Data and ML Platforms along with real time feeds and ML inference.</p>
        <ul>
            <li>Data and ML Platforms</li>
            <li>Engineering manager responsibilites for Data Engineering group</li>
            <li>Help communicate and set strategy for SWE, MLE, DE, and Analytics across the org</li>
        </ul>
    </div>

    <div class="career-item" onclick="toggleDetails('corrigo')">
        <img src="{{ '/images/corrigo_logo.png' | relative_url }}" alt="Corrigo Logo" class="company-logo">
        <div class="career-info">
            <h3>ML Engineer at Corrigo (JLL-T)</h3>
            <p class="career-date">January 2022 - November 2022</p>
        </div>
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
        <div class="career-info">
            <h3>Senior Data Scientist at Corrigo (JLL-T)</h3>
            <p class="career-date">March 2020 - January 2022</p>
        </div>
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
        <div class="career-info">
            <h3>Data Scientist at Co Star</h3>
            <p class="career-date">July 2019 - March 2020</p>
        </div>
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
        <div class="career-info">
            <h3>Technical Consultant at Mu Sigma</h3>
            <p class="career-date">August 2018 - July 2019</p>
        </div>
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
    if (!element) {
        return;
    }
    
    var currentDisplay = window.getComputedStyle(element).display;
    
    if (currentDisplay === "none" || currentDisplay === "") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}

// Close all details when page loads
document.addEventListener('DOMContentLoaded', function() {
    var allDetails = document.querySelectorAll('.career-details');
    allDetails.forEach(function(detail) {
        detail.style.display = 'none';
    });
});
</script>