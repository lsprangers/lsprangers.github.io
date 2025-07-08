import React, { useState } from 'react';
import styles from '../css/CareerTimeline.module.css';

const jobs = [
  {
    title: "ML + Data Tech Lead",
    company: "Moody's Analytics",
    logo: "/img/ma_logo_no_left.png",
    period: "November 2022 - Present",
    excerpt: "I lead a group under the Data and AI Functional Group in the KYC OU in Moodys Analytics. The main projects I oversee are Data and ML Platforms along with real time feeds and ML inference.",
    bullets: [
      "Data and ML Platforms",
      "Engineering manager responsibilites for Data Engineering group",
      "Help communicate and set strategy for SWE, MLE, DE, and Analytics across the org"
    ]
  },
  {
    title: "ML Engineer",
    company: "Corrigo (JLL-T)",
    logo: "/img/corrigo_logo_no_left.png",
    period: "January 2022 - November 2022",
    excerpt: "As an ML Engineer at Corrigo, I worked on developing machine learning models to improve operational efficiency and predictive maintenance.",
    bullets: [
      "Developed predictive maintenance models",
      "Improved operational efficiency through ML solutions",
      "Collaborated with cross-functional teams"
    ]
  },
  {
    title: "Senior Data Scientist",
    company: "Corrigo (JLL-T)",
    logo: "/img/corrigo_logo.png",
    period: "March 2020 - January 2022",
    excerpt: "As a Senior Data Scientist, I led data science projects to extract insights from large datasets and drive business decisions.",
    bullets: [
      "Led data science projects",
      "Extracted insights from large datasets",
      "Drove business decisions through data analysis"
    ]
  },
  {
    title: "Data Scientist",
    company: "Co Star",
    logo: "/img/costar_logo_no_left.png",
    period: "July 2019 - March 2020",
    excerpt: "At Co Star, I focused on building data-driven solutions to enhance real estate market analysis and forecasting.",
    bullets: [
      "Built data-driven solutions for market analysis",
      "Enhanced real estate market forecasting",
      "Worked closely with stakeholders to deliver insights"
    ]
  },
  {
    title: "Technical Consultant",
    company: "Mu Sigma",
    logo: "/img/musigma_no_left.png",
    period: "August 2018 - July 2019",
    excerpt: "I started my career in analytics and consulting, helping clients leverage data to solve complex business problems.",
    bullets: [
      "Provided data-driven consulting services",
      "Helped clients solve complex business problems",
      "Developed analytical models to support decision-making"
    ]
  }
];

export default function CareerTimeline() {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <div className={styles.timeline}>
      {jobs.map((job, idx) => (
        <div key={idx} className={styles.bubbleContainer}>
          <button
            className={styles.bubble}
            onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
          >
            <img src={job.logo} alt={`${job.company} Logo`} className={styles.logo} />
            <div>
              <div className={styles.title}>{job.title}</div>
              <div className={styles.company}>{job.company}</div>
              <div className={styles.period}>{job.period}</div>
            </div>
          </button>
          {openIndex === idx && (
            <div className={styles.excerpt}>
              <p>{job.excerpt}</p>
              <ul>
                {job.bullets.map((b, i) => <li key={i}>{b}</li>)}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
