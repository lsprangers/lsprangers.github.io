---
title: Projects
layout: default
---

<!-- # Projects -->

<div class="projects-container">
    <div class="project-item" onclick="toggleDetails('raft')">
        <h3>RAFT</h3>
        <p class="project-description">The RAFT consensus algorithm from scratch</p>
        <div id="raft" class="project-details">
            <p>Implemented the RAFT consensus algorithm from scratch using core OS libraries only, which is used for managing a replicated log in distributed systems.</p>
            <a href="https://github.com/lsprangers/raft-course" target="_blank">View Project</a>
        </div>
    </div>

    <div class="project-item" onclick="toggleDetails('byo-cloud')">
        <h3>BYO Cloud</h3>
        <p class="project-description">A project to build your own cloud infrastructure.</p>
        <div id="byo-cloud" class="project-details">
            <p>Developed a project to build your own cloud infrastructure, providing a scalable and flexible solution for cloud computing.</p>
            <a href="https://github.com/lsprangers" target="_blank">View Project</a>
        </div>
    </div>

    <div class="project-item" onclick="toggleDetails('map-reduce-graph-algorithms')">
        <h3>Pregel & GraphX: Map-Reduce Based Graph Algorithms</h3>
        <p class="project-description">Graph traversal and connected components algorithm using MapReduce.</p>
        <div id="map-reduce-graph-algorithms" class="project-details">
            <p>Implemented graph traversal and connected components algorithms using MapReduce, leveraging functional programming constructs in Scala.</p>
            <a href="https://github.com/lsprangers" target="_blank">View Project</a>
        </div>
    </div>

    <div class="project-item" onclick="toggleDetails('spark-inverted-indexes')">
        <h3>Scalable Streaming Entity Resolution Using Commodity Hardware</h3>
        <p class="project-description">BYO Inverted Index and Streaming ER Solution on Delta Lake</p>
        <div id="spark-inverted-indexes" class="project-details">
            <p>Terrabyte Sized ER via Spark and Delta Lake - Create an in-memory partitioned inverted index for our Streaming Entity Resolution use case</p>
            <a href="https://github.com/lsprangers" target="_blank">View Project</a>
        </div>
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