document.addEventListener('DOMContentLoaded', function () {
    const footer = `
        <article id="footer" class="wrapper style1">
            <footer>
                <ul id="copyright">
                    <li>&copy; 2025 GenAI4All. All rights reserved.</li>
                </ul>
            </footer>
        </article>
    `;
    document.body.insertAdjacentHTML('beforeend', footer);
});