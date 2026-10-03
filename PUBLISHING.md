# Publishing articles to Snail World

Articles in `content/articles/` are published to the Snail World blog (https://snailworld.org/blog) through the Brilliant Directories (BD) **Add Post** form, with Claude Cowork doing the data entry in your logged-in Chrome session.

## Why not the CSV importer?

BD's **Import Post File** rejects any CSV containing a `<table>` tag with "Invalid file, please choose a csv type of file". We confirmed this by uploading test files one feature at a time. Our articles use tables, and the Add Post editor accepts them, so we publish through the form instead.

Other things we learned on snailworld.org (these are observations, not documented BD rules):

| Finding | Effect |
|---|---|
| A downloaded file must be named `*.csv` | Otherwise the upload fails with the same "Invalid file" error |
| Posts need an author | `user_id` 5 ("Admin User - Blog Author") |
| The form has no slug field | The URL is built from the title: `https://snailworld.org/blog/<slugified-title>`, with no trailing slash |
| Tags are limited to 100 characters | The generator keeps whole tags in priority order up to the limit |
| Publish status defaults to "No" | Set it to "Yes" to publish |
| A `&` in a category name breaks its clean URL, redirects and filter links | Write "and" in category names that have posts or landing pages (e.g. "System Design and Pens", "Purging and Cleaning"); the slug becomes `purging-and-cleaning` and the filter URL `/blog?category[]=Purging+and+Cleaning` |
| The editor rewrites numeric codes (`&#8212;`) as named ones (`&mdash;`) | They display the same |

## Steps for each new batch

1. Add the article Markdown to `content/articles/` and its mapping (category, secondary categories, tags, meta title) to `ARTICLES` in `scripts/generate_bd_article_import.py`.
2. Run `python3 scripts/generate_bd_article_import.py` and fix anything it reports. It derives each post's live URL from its title and checks that the article's JSON-LD uses it.
3. Commit and push. Then give Cowork the prompt below, with the branch name filled in.
4. Delete any test posts afterwards. Never delete or re-create published articles without first checking for duplicates.

## Cowork prompt

Replace `<BRANCH>` with the branch you pushed, e.g. `claude/charming-franklin-d235ad`.

```
Please publish new blog articles on my Brilliant Directories website, Snail World (https://snailworld.org), using my already-logged-in Chrome session.

Site:
- Admin panel: https://ww2.managemydirectory.com/admin. Before doing anything, confirm the "Snail World" logo is showing top-left. If not, use "Switch Website" to select Snail World. If you can't confirm it, stop and ask me.
- Post type: "Website Blog Article" (ID 14, /blog).

Source files (download from GitHub; use the GitHub connector if available, otherwise open each page in Chrome and click "Download raw file"; I'm signed in to GitHub):
- https://github.com/carestaffsolutionrecruitment-sudo/heliciculture-content-engine/blob/<BRANCH>/bd_article_import.csv
  Columns: post_title, post_content, post_category, post_tags, user_id.
- https://github.com/carestaffsolutionrecruitment-sudo/heliciculture-content-engine/blob/<BRANCH>/bd_article_reference.csv
  Columns include post_title, Post URL, Meta Title, Meta Description, Schema JSON-LD.
Don't open or re-save either file in Excel or another spreadsheet app.

For each row in bd_article_import.csv:
1. In My Content > Manage Posts, check whether a Website Blog Article with exactly this title already exists. If it does, skip the row and tell me.
2. Add a new Website Blog Article.
3. Title: post_title, exactly.
4. Content: switch the editor to Source/HTML view first, then insert post_content exactly as it is in the file. Don't retype or convert the &#...; codes. Check that headings, tables and lists display correctly in the visual view.
5. Category: post_category. Tags: post_tags (already within the 100-character limit).
6. Author: the member whose ID is user_id ("Admin User - Blog Author", #5).
7. Publish: Yes.
8. Save once. If unsure whether a save worked, check Manage Posts before retrying.
9. Open the live post and confirm its URL matches the "Post URL" for that title in bd_article_reference.csv. If it differs, tell me the actual URL and don't change anything else.

Then, for each post you created, look for per-post SEO fields (meta title, meta description) and any per-post field for custom head code or scripts. If they exist, enter Meta Title, Meta Description and the Schema JSON-LD block from bd_article_reference.csv and save. If a field doesn't exist, don't change any site-wide settings; just tell me which fields were missing.

Rules: work only on Snail World. Don't change passwords, members, billing or site-wide settings. If anything errors, stop and screenshot it.

When done, report each post's title, category, status and live URL, and which SEO/schema fields you filled in.
```
