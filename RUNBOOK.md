# AI for Every Job: daily production and publishing runbook

Channel: https://www.youtube.com/@AIForEveryJob (Studio channel id `UCm6lpFy3y5xQXUUItmwjMXg`).
The owner has asked for this to run fully on its own: do not ask him to review, approve or upload anything.
The owner wants continuous production: runs fire every hour, and each run produces and publishes one video. Never publish anything that failed fact-checking or looks broken.

## 0. Setup (fresh workspace every run)

```bash
cd ~ && git clone --depth 1 https://github.com/ARDAVAN39/aiforeveryjob-videos
pip install --break-system-packages -q kokoro-onnx soundfile cairosvg
mkdir -p ~/tts && cd ~/tts
curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
```
Fonts: Inter must exist at `/usr/share/fonts/opentype/inter/`; check with `fc-list | grep -i inter`.

## 1. Pick the episode (runs can overlap, so claim first)

Read `queue.json`. Runs start hourly and a run can take longer than an hour, so:
- If an item has status `rendered`, publish it first (step 6), then continue to produce the next one in the same run.
- To produce, take the first `todo` item, or an `in_progress` item whose `claimed_at` is more than 3 hours old. Set it to `in_progress` with `claimed_at` (UTC ISO time), then commit and push straight away. If the push is rejected because another run pushed first, run `git pull --rebase`, re-read the queue and pick again.
- If no `todo` items are left, append 10 new professions to the queue, each with a `note` where the topic needs limits. Pick widely useful jobs not yet covered, such as pilots, farmers, police officers, social workers, translators, photographers, video editors, data analysts, product managers, project managers, consultants, event planners, fitness trainers, psychologists, veterinarians, engineers, scientists, librarians, retail workers, logistics and drivers. Mix in some cross-cutting episodes too, for example "AI for Your Job Interview" or "AI for Learning a New Language at Work".

## 2. Research and script (subagent: researcher and scriptwriter)

Write `pipeline/episodes/<slug>.py`, mirroring `pipeline/episodes/managers.py` exactly:
- Module variables: `PRESENTER = "<key>"`, `VOICE = "<kokoro voice>"`, `CHANNEL = "AI for Every Job"`, `EPISODE = "<title>"`, `SCENES`.
- Structure: a title scene (3 beats), 7 or 8 card scenes `01`..`08` (a lead-in beat, then 3 card beats, optional tip beat, max 4 card/tip items, title max 26 characters, card description max 62 characters, tip max 85 characters), a `★` "Three rules" scene, and a closing title scene whose last beat names the channel and asks viewers to subscribe and comment which job to cover next.
- Narration is 950 to 1100 words in plain spoken English, 25 to 45 words per beat, with concrete example prompts and honest limits.
- Add `tts` spellings for abbreviations and product names (for example "Chat G P T", "P D F", "H R").
- Name only tools confirmed on the vendor's own site. No prices, statistics or percentages.
- Honour the queue item's `note`. Health, legal and finance topics cover workflow, admin and learning only, never advice.
- Make it different from the earlier episodes, with its own angle, structure of examples and wording, so the channel does not look mass-produced.

## 3. Fact-check (separate subagent that did not write the script)

Check every named product and legal or factual claim against vendor or official pages. Fix only wrong or overstated lines, with minimal edits, and keep `tts` in sync. If a claim cannot be verified, remove it.

## 4. Presenter (designer)

In `pipeline/character.py`, add a config to `PRESENTERS` for this profession, choosing a `room`, `outfit_style`, `hair_style`, `glasses` and colours. Where the profession needs it, add a new `room` branch in `backdrop()` (for example a clinic, classroom, kitchen or workshop) and a new `outfit_style` branch in `body()` (for example scrubs, apron or overalls). Keep the existing ones working, and vary gender, skin tone and hair across episodes.
Run `python3 pipeline/character.py <key>`, open the PNG it prints, and fix anything wrong: overlaps, items hidden behind the head, odd shapes.
Voices: `af_heart`, `af_bella`, `af_nicole` (female) and `am_michael`, `am_adam` (male). Match the voice to the presenter.

## 5. Render

```bash
cd ~/aiforeveryjob-videos/pipeline
export EP=<slug> TTS_DIR=~/tts WORK_DIR=~/work
python3 build.py preview      # look at ~/work/<slug>/preview_*.png; text must not overflow or overlap the presenter panel
python3 build.py tts
python3 build.py plan         # total should be roughly 6 to 9 minutes
python3 build.py render       # about 6 minutes on 2 CPUs
bash finish.sh "<Title-With-Dashes>.mp4"     # writes videos/<file>
```
Grab two or three frames with ffmpeg and look at them. Then set the queue item to `status: rendered` with `file`, and commit and push:
```bash
git add -A && git commit -m "Add <title>" && git -c push.negotiate=true push
```
A "push negotiation failed" warning is harmless.

## 6. Publish (built-in browser on the owner's computer, signed in to YouTube)

1. Navigate a tab to `https://studio.youtube.com/channel/UCm6lpFy3y5xQXUUItmwjMXg/videos/upload?d=ud`.
2. Run JavaScript in the page to fetch the video from GitHub and hand it to the uploader:
```js
const r = await fetch('https://raw.githubusercontent.com/ARDAVAN39/aiforeveryjob-videos/main/<file>');
const b = await r.blob(); const f = new File([b], '<name>.mp4', {type: 'video/mp4'});
const dt = new DataTransfer(); dt.items.add(f);
const inp = document.querySelector('input[type=file][name=Filedata]'); inp.files = dt.files;
inp.dispatchEvent(new Event('change', {bubbles: true})); b.size
```
3. Studio often shows a "Welcome to YouTube Studio" overlay that swallows clicks. Dismiss it in JS with `[...document.querySelectorAll('button, ytcp-button')].filter(b=>/^\s*Continue\s*$/.test(b.innerText||'')).forEach(b=>b.click())`. Do all form filling with JS, not coordinate clicks:
```js
const d = document.querySelector('ytcp-uploads-dialog');
function setBox(sel, text){ const tb = d.querySelector(sel+' #textbox'); tb.focus(); document.execCommand('selectAll'); document.execCommand('insertText', false, text); }
setBox('#title-textarea', TITLE);         // max 100 chars, keyword-led, e.g. "AI for Teachers in 2026: Lesson Plans, Feedback and Less Admin"
setBox('#description-textarea', DESC);
d.querySelector('tp-yt-paper-radio-button[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').click();
```
4. DESC: two-sentence summary; a `Chapters` list with real timestamps (cumulative scene durations from `build.py plan` or the `rendered` log lines, first one `0:00`); the tools mentioned; the channel line; this disclosure line: "Made with AI tools: the script was researched and written with AI assistance, and the narration and animated presenter are AI-generated."; and three hashtags.
5. Click `#next-button` three times (about 1.8 seconds apart), then click `tp-yt-paper-radio-button[name="PUBLIC"]` and `#done-button`. Upload processing does not need to finish first.
6. Verify in the Studio content list (`ytcp-video-row`, visibility cell says `Public`). Record `youtube_id` (from the `youtu.be` link in the dialog or the row link), the `published` date and `status: published` in `queue.json`; commit and push.

## Pacing

Publish whenever a video is ready. Never upload the same file twice: check `queue.json` and the Studio content list for the title first.

## Failure handling

- If the computer or browser cannot be reached, still produce and push the next video (status `rendered`), so the next run publishes it.
- If an upload step fails, leave the item `rendered`, write what failed in `log.md` with the date, and stop. Do not retry more than once.
- Append one line per run to `log.md`: date, episode, result, YouTube link.
