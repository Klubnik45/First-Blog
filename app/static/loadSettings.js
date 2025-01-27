let settings = "";
const root = document.documentElement;

fetch("static/theme.json")
.then(response => response.json())

.then(
 
    json => {
        console.log(json);
        settings = json;
        root.style.setProperty("--text-size", settings.settings["--text-size"]);
        root.style.setProperty("--text-color", settings.settings["--text-color"]);
        root.style.setProperty("--text-line-height", settings.settings["--text-line-height"]);
        root.style.setProperty("--blog-title-size", settings.settings["--blog-title-size"]);
        root.style.setProperty("--bg-color", settings.settings["--bg-color"]);
        root.style.setProperty("--box-color", settings.settings["--box-color"]);
        root.style.setProperty("--title-color", settings.settings["--title-color"]);
        root.style.setProperty("--border-color", settings.settings["--border-color"]);
        root.style.setProperty("--footer-color", settings.settings["--footer-color"]);
        root.style.setProperty("--footer_text-color", settings.settings["--footer_text-color"]);
    }
)