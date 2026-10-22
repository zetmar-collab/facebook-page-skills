# config.md - settings for the fb-* skills
# Copy to ~/.claude/facebook/config.md (the installer does this if the file is absent).

page_name:     {{your Page name; /fb-start can fill it from Composio}}
page_id:       {{id from FACEBOOK_LIST_MANAGED_PAGES. The id only, never a token}}
page_url:      {{https://www.facebook.com/your-page/}}
language:      en            # language of the posts you publish: en | pl | (add your own lexicon)
timezone:      {{e.g. Europe/Warsaw, America/New_York}}
publish_mode:  gate          # gate = always ask before publishing (do not change lightly)
link_policy:   in the body   # or: first comment
hashtags_max:  3
