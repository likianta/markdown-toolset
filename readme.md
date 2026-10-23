# Markdown Toolset

## Markdown Image Base64

Convert image links to base64 encoded html elements.

Run:

```sh
# get help
uvm src.markdown_image_base64.md_img_b64 -h
uvm src.markdown_image_base64.md_img_b64 md2html -h

# convert markdown to html file. the file remains same name as source but ends 
# with '.b64.html'.
uvm src.markdown_image_base64.md_img_b64 md2html ./readme.md

# there is also a GUI to use:
python -m streamlit run --server.port 2163 src/markdown_image_base64/md_img_b64/ui.py
```

```
                       python -m md_img_b64 md2html ...
╭─────────────────────────────────────────────────────────────── PARAMETERS ─╮
│  * 1    file-i  TEXT                                                       │
│         an absolute or relative path.                                      │
│                                                                            │
│    2    file-o  TEXT                                     default = :empty  │
│         optional. if not given, will use the same name as source but ends  │
│         with '.b64.html'.                                                  │
│         you can also give directory instead of file, it generates          │
│         '<the_given_dir>/<source_name>.b64.html'.                          │
╰────────────────────────────────────────────────────────────────────────────╯
                                                       🔥 powered by argsense
```

## Markdown Image Lofter

This is a semi-automatic tool, to convert local image links to "http/https" urls, so that CSDN online editor can read them and convert them into CSDN image hosting urls.

Run:

```sh
# get help
python -m src.markdown_image_lofter.md_img_lofter.app -h
# run gui (port 2166) and local file server (port 2167)
python -m src.markdown_image_lofter.md_img_lofter.app -f
# run gui and custom file server.
python -m src.markdown_image_lofter.md_img_lofter.app -d https://example.com -p 2031
```

```
                              python app.py ...
╭─────────────────────────────────────────────────────────────── PARAMETERS ─╮
│    1    enable-file-server -f FLAG                        default = :true  │
│    2    bore-secret        -s TEXT                       default = :empty  │
│    3    domain             -d TEXT                       default = :empty  │
│         Starting from 'http://' or 'https://'.                             │
│         Note: CSDN image hosting requires https links. You can use         │
│         NAT-DDNS tools (e.g. AweShell, Cpolar) to get a https domain.      │
│                                                                            │
│    4    port               -p NUMBER                       default = 2167  │
╰────────────────────────────────────────────────────────────────────────────╯
                                                       🔥 powered by argsense
```

The ideal way is:

1. Use AweShell/Cpolar/etc. to expose local port to public domain, suggest https protocol.
2. `python -m src.markdown_image_lofter.md_img_lofter.app -d <public_domain> -p <local_port>`, like command above.
3. Open a browser, visit http://localhost:2166, this is user interface for you to choose markdown file, the UI inplaces image links to public ones, then the converted markdown is living in the TextArea.
4. Just copy & paste the converted markdown to CSDN online editor, then CSDN auto converts these urls to CSDN-hosted ones.

PS: Dev.to image hosting is under the way...

Why don't we create a full-automatic tool?

- CSDN doesn't provide API/SDK, we have to use headless browser -- it is not good, not stable, not safe, not long-term valuable.
- It takes time.
- For caution consideration, people prefer to spend time to do platform specific actions by themselves or trusted delegates, like tags, categories, column series, keywords, caption image, pin-to-top...
