---
title: Contact
layout: default
---

import styles from '../css/ContactBubbles.module.css';

<div className={styles.contactBubbleContainer}>
  <div className={styles.contactBubbleCard}>
    <h2>Get in Touch</h2>
    <p>I'm always interested in hearing about new opportunities and interesting projects. Feel free to reach out!</p>
    <div className={styles.contactMethods}>
      <div className={styles.contactMethod}>
        <i className="fas fa-envelope"></i>
        <h3>Email</h3>
        <p><a href="mailto:sprangersluke@gmail.com">sprangersluke@gmail.com</a></p>
        <p className={styles.contactNote}>I typically respond within 24 hours</p>
      </div>
      <div className={styles.contactMethod}>
        <i className="fab fa-linkedin"></i>
        <h3>LinkedIn</h3>
        <p><a href="https://www.linkedin.com/in/luke-sprangers" target="_blank">linkedin.com/in/luke-sprangers</a></p>
        <p className={styles.contactNote}>Connect with me for professional networking</p>
      </div>
      <div className={styles.contactMethod}>
        <i className="fab fa-github"></i>
        <h3>GitHub</h3>
        <p><a href="https://github.com/lsprangers" target="_blank">github.com/lsprangers</a></p>
        <p className={styles.contactNote}>Check out my open source projects</p>
      </div>
    </div>
  </div>
  <div className={styles.contactBubbleCard}>
    <h2>What I'm Looking For</h2>
    <p className={styles.contactBlurb}>
      Technically I enjoy whatever is in the middle of distributed systems, economic analysis, and data
    </p>
    <p className={styles.contactBlurb}>
    However, I don't like sitting in a corner - so consulting, architecture, and management are my main desires!
    </p>
    <ul className={styles.interestsList}>
      <li>Distributed systems</li>
      <li>Economics / analytics</li>
      <li>ML + data engineering</li>
      <li>Open source contributions and collaborations</li>
      <li>Technical leadership and architecture roles</li>
    </ul>
  </div>
</div>