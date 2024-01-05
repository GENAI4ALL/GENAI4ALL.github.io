

module.exports = function (eleventyConfig) {

    // copy assets and images folder to _site/ output
    eleventyConfig.addPassthroughCopy("src/assets");
    eleventyConfig.addPassthroughCopy("src/images");

    // minify css
    eleventyConfig.on('afterBuild', () => {
        const CleanCSS = require("clean-css");
        const fs = require('fs');

        // Run me after the build ends
        var inputFile = 'src/assets/css/main.css';
        var input = fs.readFileSync(inputFile, 'utf8');
        var output = new CleanCSS().minify(input);
        fs.writeFile('_site/assets/css/main.css', output.styles, function (err) {
            if (err) return console.log('Error minifying main.css' + err);
            //success
          });
    });

    return {
        dir: {
            input: "src",
            output: "_site",
        },
        templateFormats: ["html", "md", "njk"],
        htmlTemplateEngine: "njk"
    };
};