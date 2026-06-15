UMRMKD_ / EDITORIAL STUDIO PLATFORM
====================================

DEPLOY (Netlify)
----------------
Drag the whole 'umrmkd-site' folder onto app.netlify.com/drop, or connect it to a Git repo.
Netlify serves each folder's index.html at a clean URL (e.g. /studies/copenhagen/).

STRUCTURE
---------
index.html              Home
observations/           Observations (Places / Hospitality / Experience / Craft)
studies/                Editorial Studies index
studies/qatar-gp/       Study 01
studies/the-ned-doha/   Study 02
studies/copenhagen/     Study 03
studies/_template/      Copy this to publish a new study
partnerships/           Collaborations, How We Work, Services
journal/                Living archive
contact/                Commission enquiries
css/style.css           One shared stylesheet (the master visual language)
images/                 All imagery, optimised

ADD A NEW STUDY
---------------
1. Copy studies/_template  ->  studies/your-slug
2. Drop new images in /images (~1500px long edge, JPEG)
3. Edit the title, theme, copy and the six image paths in your new index.html
4. Update the Previous/Next links at the foot
5. Add a card to studies/index.html
Done. Home, portfolio and nav stay untouched.

NOTES
-----
- Local preview needs a small server (paths are site-root relative): run
  'npx serve' inside the folder, or just deploy to Netlify.
- Premium Experiences expands with the FIFA World Cup 2022 and Silverstone archives.
- Founder letter is locked. Contact is email + TikTok only.
