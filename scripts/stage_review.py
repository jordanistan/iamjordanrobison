from pathlib import Path
import shutil, sys
root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]).resolve()
if out.exists() and any(out.iterdir()): raise SystemExit("Output must be empty")
out.mkdir(parents=True,exist_ok=True)
# Publish only the restored website dependencies, never the repository contents.
for name in ['index.html', 'resume.html', 'threat-detection.html', 'favicon.ico', 'robots.txt', 'sitemap.xml', '.nojekyll', '_headers', 'Jordan_Robison_2026-Resume.pdf', 'assets/bootstrap/css/bootstrap.min.css', 'assets/bootstrap/js/bootstrap.min.js', 'assets/css/font-awesome.min.css', 'assets/css/site.css', 'assets/js/jquery.js', 'assets/images/myphoto-2.jpg', 'assets/images/myphoto.jpg', 'assets/images/home2.jpg', 'assets/images/photos/astrobirdy.space.png', 'assets/images/photos/birdy.jpg', 'assets/bootstrap/fonts/glyphicons-halflings-regular.eot', 'assets/bootstrap/fonts/glyphicons-halflings-regular.svg', 'assets/bootstrap/fonts/glyphicons-halflings-regular.ttf', 'assets/bootstrap/fonts/glyphicons-halflings-regular.woff', 'assets/bootstrap/fonts/glyphicons-halflings-regular.woff2', 'assets/fonts/fontawesome/FontAwesome.otf', 'assets/fonts/fontawesome/fontawesome-webfont.eot', 'assets/fonts/fontawesome/fontawesome-webfont.svg', 'assets/fonts/fontawesome/fontawesome-webfont.ttf', 'assets/fonts/fontawesome/fontawesome-webfont.woff', 'assets/images/ico/apple-touch-icon-114-precomposed.png', 'assets/images/ico/apple-touch-icon-144-precomposed.png', 'assets/images/ico/apple-touch-icon-57-precomposed.png', 'assets/images/ico/apple-touch-icon-72-precomposed.png', 'assets/images/ico/favicon.png']:
    target=out/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(root/name,target)
shutil.copytree(root/"site-assets",out/"site-assets")
