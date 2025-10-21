document.addEventListener('DOMContentLoaded', function () {
    const nav = `
        <nav id="nav">
            <ul class="container">
                <li><a href="index.html"><h3>GenAI4All</h3></a></li>
                <li><a href="book/">Book</a></li>
                <li><a href="course.html">Course</a></li>
                <li><a href="resources.html">Resources</a></li>
                <li><a href="about.html">About</a></li>
            </ul>
        </nav>
    `;
    document.body.insertAdjacentHTML('afterbegin', nav);
});