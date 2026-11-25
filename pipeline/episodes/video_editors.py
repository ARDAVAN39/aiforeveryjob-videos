"""Episode: AI for Video Editors in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

# Sources for tool claims (vendor pages, checked 2026-11-25):
# - Premiere Text-Based Editing: auto transcript with timecodes, cut/rearrange text to edit,
#   detect and bulk-delete filler words:
#   https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/overview-of-text-based-editing.html
# - Premiere Paper Edit: select transcript sentences, preview, create a new sequence:
#   https://helpx.adobe.com/premiere/desktop/edit-projects/edit-video-using-text-based-editing/create-a-sequence-with-paper-edit.html
# - Premiere media intelligence search: describe a shot to find it; analysis runs locally;
#   visual search is English only:
#   https://helpx.adobe.com/premiere/desktop/organize-media/file-organization/search-for-media-using-ai-powered-media-intelligence.html
# - Premiere Enhance Speech: AI dialogue clarity and noise reduction, Enhancement slider:
#   https://helpx.adobe.com/premiere/desktop/add-audio-effects/adjust-volume-and-levels/enhance-speech.html
# - Premiere Speech to Text: generate transcripts and add captions:
#   https://helpx.adobe.com/premiere/desktop/add-text-images/insert-captions/auto-transcribe-video-using-speech-to-text.html
# - Premiere Generative Extend: video up to 2 seconds, ambient audio extended, dialogue not
#   extended, clips with music not eligible:
#   https://helpx.adobe.com/premiere/desktop/edit-projects/edit-with-generative-ai/generative-extend-faq.html
# - DaVinci Resolve IntelliScript: compares script text to transcribed audio and creates a cut:
#   https://www.blackmagicdesign.com/products/davinciresolve/whatsnew
# - DaVinci Resolve Fairlight AI effects such as Voice Isolation:
#   https://www.blackmagicdesign.com/products/davinciresolve
# - Descript: edit video by editing the transcript, Remove Filler Words with review,
#   Studio Sound (noise and echo), captions from transcript:
#   https://www.descript.com/features
# - CapCut auto captions: generated from audio, edit text, timing, font and placement:
#   https://www.capcut.com/tools/auto-caption-app
# - Frame.io comments: timecode comments, range comments, drawing annotations:
#   https://help.frame.io/en/articles/9105251-commenting-on-your-media
# - Frame.io share links: clients comment without an account when commenting is on:
#   https://help.frame.io/en/articles/9105242-share-links-explained-for-clients
# - YouTube disclosure of realistic AI-generated or altered content; captions and audio
#   repair do not need disclosure:
#   https://support.google.com/youtube/answer/14328491
# - ChatGPT, Claude, Gemini accept pasted text and uploaded files:
#   https://help.openai.com/en/articles/8555545-file-uploads-faq
#   https://support.claude.com/en/articles/8241126-upload-files-to-claude
#   https://support.google.com/gemini/answer/14903178

CHANNEL = "AI for Every Job"
PRESENTER = "video_editor"
VOICE = "am_adam"
EPISODE = "AI for Video Editors in 2026"

SCENES = [
    dict(kind="title", title="AI for Video Editors", year="2026",
         sub="Four hours of footage. One three-minute film.",
         beats=[
             dict(say="I edit videos for small organisations. The creative part is the best bit. The slow part is everything around it: logging, transcripts, noisy audio, captions, and client notes."),
             dict(say="So let's follow one invented job. A community bike workshop, Northgate Bike Kitchen, hands me four hours of footage and asks for a three minute film."),
             dict(tts="At each stage: which tools help, the prompts I actually type, and where A I gets it wrong. The client is paying for your judgement, not the software's first guess.",
                  say="At each stage: which tools help, the prompts I actually type, and where AI gets it wrong. The client is paying for your judgement, not the software's first guess."),
         ]),
    dict(kind="cards", num="01", title="Log four hours fast",
         beats=[
             dict(tts="Stage one: logging. Four hours means two interviews, a busy Saturday session, and plenty of B roll. I used to watch it all and type notes.",
                  say="Stage one: logging. Four hours means two interviews, a busy Saturday session, and plenty of b-roll. I used to watch it all and type notes."),
             dict(card=("Transcribe first", "Premiere's Text panel and Descript make timecoded transcripts"),
                  say="First, transcribe the interviews. Premiere Pro's Text panel and Descript both create a transcript linked to timecode, so every sentence jumps straight to its moment in the footage."),
             dict(card=("Search the pictures", "Premiere media intelligence finds shots you describe"),
                  tts="For B roll, Premiere's media intelligence lets me describe a shot: close up of hands fixing a chain. It analyses footage locally, and visual search is English only.",
                  say="For b-roll, Premiere's media intelligence lets me describe a shot: close up of hands fixing a chain. It analyses footage locally, and visual search is English only."),
             dict(card=("Ask for selects", "Paste transcripts, ask for the strongest quotes and timecodes"),
                  tts="Then I paste the transcripts into Claude, Chat G P T or Gemini and ask: list the ten strongest lines about why this workshop matters, with timecodes and who said them.",
                  say="Then I paste the transcripts into Claude, ChatGPT or Gemini and ask: list the ten strongest lines about why this workshop matters, with timecodes and who said them."),
             dict(tip="Client footage and transcripts go only into tools the client has agreed to.",
                  say="This is the client's material, and the people in it trusted them. Only use tools the client has agreed to, and check every quote against the clip."),
         ]),
    dict(kind="cards", num="02", title="Paper edit first",
         beats=[
             dict(say="Stage two: the story. Three minutes is short. Before I touch the timeline, I want a paper edit: a written plan of which lines go where, and why."),
             dict(card=("Ask for three shapes", "Same selects, three openings: a problem, a person, a place"),
                  say="I give the assistant my selects and the brief, then ask: suggest three structures, one opening on a problem, one on a person, one on a place."),
             dict(card=("Premiere Paper Edit", "Pick transcript lines, then create a sequence from them"),
                  say="I build my favourite in Premiere's Paper Edit. Select sentences in the transcript, preview them, and create a new sequence. That's a first assembly without dragging a single clip."),
             dict(card=("Resolve IntelliScript", "Matches a script to transcribed audio and builds a cut"),
                  tts="In Da Vinci Resolve Studio, Intelli Script works the other way round. You give it a script, and it compares the text with the transcribed audio to build a cut.",
                  say="In DaVinci Resolve Studio, IntelliScript works the other way round. You give it a script, and it compares the text with the transcribed audio to build a cut."),
         ]),
    dict(kind="cards", num="03", title="Rough cut by text",
         beats=[
             dict(say="Stage three: the rough cut. My assembly runs nine minutes, so now I cut it down. With text based editing, deleting words in the transcript removes them from the video."),
             dict(card=("Delete words, cut video", "Premiere and Descript trim the timeline as you edit text"),
                  say="In Premiere or Descript, I highlight a rambling sentence and delete it, and the timeline follows. Tightening a long interview answer takes seconds, not minutes."),
             dict(card=("Remove filler words", "Find every um and uh, then review before deleting"),
                  say="Both tools can find filler words like um and uh across a whole interview. Descript lets you review each cut first. Do review, because some pauses carry real feeling."),
             dict(card=("Watch it, don't read it", "A clean transcript can still be a jumpy edit"),
                  say="Then watch it with fresh eyes. A transcript that reads perfectly can still hide jump cuts, clipped breaths, or a mechanic glancing away. The text is a map, not the film."),
         ]),
    dict(kind="cards", num="04", title="Clean up the sound",
         beats=[
             dict(say="Stage four: sound. Our best interview was recorded next to a compressor and a radio. Viewers forgive soft pictures, but they click away from bad audio."),
             dict(card=("Premiere Enhance Speech", "Clearer dialogue, less noise, with an Enhancement slider"),
                  tts="Premiere's Enhance Speech uses A I to make dialogue clearer and reduce background noise. I rarely push its Enhancement slider to maximum. A little room sound feels natural.",
                  say="Premiere's Enhance Speech uses AI to make dialogue clearer and reduce background noise. I rarely push its Enhancement slider to maximum. A little room sound feels natural."),
             dict(card=("Resolve Voice Isolation", "A Studio AI effect in Fairlight, the Resolve audio page"),
                  tts="In Da Vinci Resolve Studio, the paid version, Fairlight's A I effects include Voice Isolation, which pulls voices away from noise. Adjust it by ear, so the speaker still sounds like themselves.",
                  say="In DaVinci Resolve Studio, the paid version, Fairlight's AI effects include Voice Isolation, which pulls voices away from noise. Adjust it by ear, so the speaker still sounds like themselves."),
             dict(card=("Descript Studio Sound", "One click to remove background noise and echo"),
                  say="Descript's Studio Sound does a similar job in one click, removing noise and echo. But push any of these too hard and voices turn robotic, so always compare with the original."),
         ]),
    dict(kind="cards", num="05", title="Captions you can trust",
         beats=[
             dict(say="Stage five: captions. The workshop will post short clips on social media, where lots of people watch with the sound off. Captions are part of delivery, not an extra."),
             dict(card=("Premiere Speech to Text", "Transcribe, then add captions from the transcript"),
                  say="In Premiere, Speech to Text generates a transcript and adds captions from it. We transcribed in stage one, so they come almost free. Descript builds captions from its transcript too."),
             dict(card=("CapCut auto captions", "Quick captions for vertical clips; edit text and timing"),
                  tts="For vertical clips, Cap Cut's auto captions listen to the audio and generate synced captions. Then you can edit the text, the timing, the font, and where they sit.",
                  say="For vertical clips, CapCut's auto captions listen to the audio and generate synced captions. Then you can edit the text, the timing, the font, and where they sit."),
             dict(card=("Proofread every name", "Names, places and jargon are where captions slip"),
                  say="Then proofread. Speech recognition trips on names, local streets, and bike jargon. I ask an assistant: list every word in these captions that looks like a name or technical term."),
         ]),
    dict(kind="cards", num="06", title="One clean review round",
         beats=[
             dict(say="Stage six: client review, where projects usually drag on. Vague notes like, can it feel more energetic, are hard to act on. AI helps me turn feedback into precise changes."),
             dict(card=("Frame.io comments", "Notes pinned to a timecode, with ranges and drawings"),
                  tts="I share the cut on Frame I O. Each comment is pinned to a timecode, a range comment covers a stretch, and reviewers can draw on the frame. With commenting on, clients need no account.",
                  say="I share the cut on Frame.io. Each comment is pinned to a timecode, a range comment covers a stretch, and reviewers can draw on the frame. With commenting on, clients need no account."),
             dict(card=("Turn notes into a list", "Group comments into changes, questions and conflicts"),
                  say="Then I paste the comments and ask: group these notes into clear changes, open questions, and notes that contradict each other. Contradictions go back to the client."),
             dict(card=("Draft the reply", "What changed, what didn't and why, one decision needed"),
                  say="Finally I ask for a reply in my voice: what I changed, what I didn't and why, and the one decision I need from them. Then I rewrite it myself."),
         ]),
    dict(kind="cards", num="07", title="Gaps, rights, disclosure",
         beats=[
             dict(tts="Stage seven: delivery. One shot ends a second too early, and the client wants to know how A I was used. This is where speed meets rights and consent.",
                  say="Stage seven: delivery. One shot ends a second too early, and the client wants to know how AI was used. This is where speed meets rights and consent."),
             dict(card=("Premiere Generative Extend", "Adds up to two seconds; no dialogue, no music clips"),
                  say="Premiere's Generative Extend can add up to two seconds to a clip, and extend room tone. It won't extend dialogue, and clips with music aren't eligible. Use it for breathing room only."),
             dict(card=("Rights and consent", "Releases, music licence and contract, before export"),
                  tts="Before export, check everyone on screen agreed to be filmed, the music licence covers this use, and your contract allows A I tools. I can't interpret the law for you. Ask the client.",
                  say="Before export, check everyone on screen agreed to be filmed, the music licence covers this use, and your contract allows AI tools. I can't interpret the law for you. Ask the client."),
             dict(card=("Disclose what AI made", "Follow each platform's rules for realistic AI content"),
                  tts="Then disclose. YouTube asks creators to label realistic content made or meaningfully changed with A I, but not captions or audio repair. Check each platform's current rules, and tell your client.",
                  say="Then disclose. YouTube asks creators to label realistic content made or meaningfully changed with AI, but not captions or audio repair. Check each platform's current rules, and tell your client."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(say="Before you open your next project, here are three rules. They hold whether you cut weddings, adverts, documentaries, or small community films like this one."),
             dict(card=("1   Rights before render", "Consent, licences and contract checked before delivery"),
                  tts="Rule one: rights before render. Know who agreed to be filmed, what the music licence covers, and what your contract says about A I. When unsure, ask before you export.",
                  say="Rule one: rights before render. Know who agreed to be filmed, what the music licence covers, and what your contract says about AI. When unsure, ask before you export."),
             dict(card=("2   Say what AI made", "Tell the client and viewers about generated or altered shots"),
                  tts="Rule two: say what A I made. If a shot was extended, a voice changed, or anything was generated, tell your client and follow the platform's disclosure rules. Trust is your real product.",
                  say="Rule two: say what AI made. If a shot was extended, a voice changed, or anything was generated, tell your client and follow the platform's disclosure rules. Trust is your real product."),
             dict(card=("3   Watch every frame", "Proof captions, sound and cuts yourself before sign-off"),
                  say="Rule three: watch every frame before sign off. Transcripts mishear, audio tools swallow words, and generated frames can look odd. Your name is on it, so the last check is yours."),
         ]),
    dict(kind="title", title="Cut one stage", year="",
         sub="Pick one stage of the bike workshop film and try it this week.",
         beats=[
             dict(say="You don't need to rebuild your whole workflow. Pick one stage, maybe transcripts or client notes, try it on your next project, and keep only what saves time without costing quality."),
             dict(say="This has been AI for Every Job, where each episode follows one profession and what AI can honestly do for it. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
