import React, { useState } from 'react';
import styles from './ProjectsTimeline.module.css';

const projects = [
  {
    title: 'RAFT',
    description: 'The RAFT consensus algorithm from scratch',
    details: 'Implemented the RAFT consensus algorithm from scratch using core OS libraries only, which is used for managing a replicated log in distributed systems.',
    link: 'https://github.com/lsprangers/raft-course',
  },
  {
    title: 'BYO Cloud',
    description: 'A project to build your own cloud infrastructure.',
    details: 'Developed a project to build your own cloud infrastructure, providing a scalable and flexible solution for cloud computing.',
    link: 'https://github.com/lsprangers',
  },
  {
    title: 'Pregel & GraphX: Map-Reduce Based Graph Algorithms',
    description: 'Graph traversal and connected components algorithm using MapReduce.',
    details: 'Implemented graph traversal and connected components algorithms using MapReduce, leveraging functional programming constructs in Scala.',
    link: 'https://github.com/lsprangers',
  },
  {
    title: 'Scalable Streaming Entity Resolution Using Commodity Hardware',
    description: 'BYO Inverted Index and Streaming ER Solution on Delta Lake',
    details: 'Terrabyte Sized ER via Spark and Delta Lake - Create an in-memory partitioned inverted index for our Streaming Entity Resolution use case',
    link: 'https://github.com/lsprangers',
  },
];

export default function ProjectsTimeline() {
  const [openIndex, setOpenIndex] = useState(null);

  return (
    <div className={styles.timeline}>
      {projects.map((project, idx) => (
        <div key={idx} className={styles.bubbleContainer}>
          <button
            className={styles.bubble}
            onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
          >
            <div className={styles.title}>{project.title}</div>
            <div className={styles.description}>{project.description}</div>
          </button>
          {openIndex === idx && (
            <div className={styles.excerpt}>
              <p>{project.details}</p>
              <a href={project.link} target="_blank" rel="noopener noreferrer">View Project</a>
            </div>
          )}
        </div>
      ))}
    </div>
  );
} 