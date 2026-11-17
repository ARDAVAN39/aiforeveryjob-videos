"""Episode: AI for Fitness Trainers in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

# Named tools, each confirmed on the vendor's own site (November 2026):
# - ChatGPT, Claude, Gemini (general assistants; drafting replies from pasted notes):
#     https://chatgpt.com/  https://claude.ai/  https://gemini.google.com/
# - Mindbody Messenger[ai] ("24/7 AI front desk"; trained to answer questions and booking requests
#     in your brand voice; replies needing a human are "flagged for follow-up"):
#     https://www.mindbodyonline.com/business/messenger-ai
# - Google Calendar appointment schedules (booking page link, availability, buffer time,
#     maximum bookings per day, minimum notice via scheduling window, booking form fields):
#     https://support.google.com/calendar/answer/10729749
#   Breaks between appointments, per-day limit and booking notice need an eligible plan:
#     https://support.google.com/googleone/answer/12351029
# - Gemini in Gmail "Help me write" (draft a new email from a prompt; eligible plan):
#     https://support.google.com/mail/answer/13955415
# - Gemini in Google Forms (create a form from a prompt, review and edit; eligible plan):
#     https://support.google.com/docs/answer/16346789
# - Descript (edit video by editing the transcript; remove "um", "uh" and other fillers in bulk):
#     https://help.descript.com/getting-started/edit-like-a-doc.md
# - Canva Magic Write (draft, rewrite, shorten text): https://www.canva.com/features/ai-writing-assistant/
# - Gemini Guided Learning (tutor; step-by-step; interactive quizzes): https://support.google.com/gemini/answer/16448384
#     https://blog.google/outreach-initiatives/education/guided-learning/
# - Claude file uploads (PDF): https://support.claude.com/en/articles/8241126-upload-files-to-claude

CHANNEL = "AI for Every Job"
PRESENTER = "fitness_trainer"
VOICE = "am_adam"
EPISODE = "AI for Fitness Trainers in 2026"

SCENES = [
    dict(kind="title", title="AI for Fitness Trainers", year="2026",
         sub="One session: a warm-up, seven sets, a cool-down.",
         beats=[
             dict(say="I'm a personal trainer. I run a small studio and coach clients in person and online. Coaching is the fun part. The messages, bookings and forms around it fill my evenings."),
             dict(say="So this video runs like a session. A quick warm-up, then seven sets that follow one new client, Dana, from her first message to her first month, plus my own learning."),
             dict(tts="One clear line before we lift anything. A I here helps with admin, messages, scheduling, content and learning. It never writes diets or diagnoses pain. Doctors, physios and registered dietitians decide those.",
                  say="One clear line before we lift anything. AI here helps with admin, messages, scheduling, content and learning. It never writes diets or diagnoses pain. Doctors, physios and registered dietitians decide those."),
         ]),
    dict(kind="cards", num="01", title="Set 1: The first enquiry",
         beats=[
             dict(say="Set one. At ten at night Dana messages me. She wants to get stronger, she's nervous about gyms, and she asks what happens next. I'm asleep, but she deserves a quick answer."),
             dict(card=("Answer in your voice", "Paste your notes and ask for a short, warm reply to edit"),
                  tts="In the morning I paste her message and my studio notes into Chat G P T, Claude or Gemini and ask: write a short, friendly reply explaining the free consultation and how to book.",
                  say="In the morning I paste her message and my studio notes into ChatGPT, Claude or Gemini and ask: write a short, friendly reply explaining the free consultation and how to book."),
             dict(card=("Mindbody Messenger[ai]", "An AI front desk for questions and booking requests"),
                  tts="If your studio runs on Mindbody, Messenger A I is an A I front desk. You train it to answer common questions and booking requests in your brand voice, at any hour.",
                  say="If your studio runs on Mindbody, Messenger[ai] is an AI front desk. You train it to answer common questions and booking requests in your brand voice, at any hour."),
             dict(card=("A human hand-off", "Anything personal or unclear comes to you, not the bot"),
                  say="Mindbody says replies that need a person get flagged for follow-up. Use that. Questions about health, injuries or worries come straight to you, and you answer them yourself, carefully."),
         ]),
    dict(kind="cards", num="02", title="Set 2: Book the consult",
         beats=[
             dict(say="Set two. Dana wants a consultation. The old way was five messages about which Tuesday works. Now she picks a slot herself, in one tap, while she still feels brave."),
             dict(card=("Calendar booking page", "Google Calendar appointment schedules: clients pick a slot"),
                  say="Google Calendar has appointment schedules. You set the hours you're free, and it gives you a booking page link. Dana picks a time, and it lands in your calendar."),
             dict(card=("Buffers and limits", "Gaps between bookings, a daily maximum, minimum notice"),
                  say="On an eligible plan, you can add buffer time between appointments, cap bookings per day, and set minimum notice. That protects your lunch break and stops someone booking you an hour from now."),
             dict(card=("The confirmation email", "Gemini in Gmail drafts it; you check time and address"),
                  say="Then the confirmation. On an eligible plan, Help me write in Gmail drafts it from a prompt: confirm Dana's consultation, the address, parking, and what to wear. Check every detail."),
         ]),
    dict(kind="cards", num="03", title="Set 3: The intake forms",
         beats=[
             dict(tts="Set three: paperwork. Before Dana's first session I need contact details, goals, availability, and a health questionnaire. A I can help with the format, but never with the judgement.",
                  say="Set three: paperwork. Before Dana's first session I need contact details, goals, availability, and a health questionnaire. AI can help with the format, but never with the judgement."),
             dict(card=("Draft the form", "Gemini in Google Forms builds a first draft from a prompt"),
                  say="Gemini in Google Forms, on an eligible plan, creates a form from a prompt. Try: a new client form with contact details, goals, preferred times and an emergency contact."),
             dict(card=("Use the approved form", "Use your approved screening form, not an AI rewrite"),
                  say="The health questions are different. Use the screening form your business, insurer or certifying body already approved. Don't let a chatbot invent or reword them, because the wording matters."),
             dict(card=("Keep health data private", "Never paste health answers into unapproved AI tools"),
                  tts="Dana's answers are sensitive health information. Keep them out of public A I tools unless your business has approved one. If any answer is flagged, she sees her doctor before training.",
                  say="Dana's answers are sensitive health information. Keep them out of public AI tools unless your business has approved one. If any answer is flagged, she sees her doctor before training."),
         ]),
    dict(kind="cards", num="04", title="Set 4: Welcome aboard",
         beats=[
             dict(say="Set four: onboarding. Dana is cleared and booked. A good welcome answers nervous questions before she asks them, and makes a one-person studio feel organised."),
             dict(card=("The welcome email", "What to bring, where to park, how to reschedule"),
                  say="Give an assistant your bullet points and ask: write a welcome email for a nervous beginner. Include what to bring, where to park, and how to reschedule. Keep it short."),
             dict(card=("Your rules, plain words", "AI rewrites your own policy clearly; it does not set it"),
                  say="Paste your own cancellation policy and ask for it in plain, friendly words. The policy stays yours. Unsure about terms or contracts? Ask a lawyer, not a chatbot."),
             dict(card=("A reusable checklist", "The same onboarding steps for every new client"),
                  say="Then ask: turn my onboarding steps into a checklist I can reuse. Form received, consultation done, welcome sent, first session booked. Small, but nothing slips through."),
         ]),
    dict(kind="cards", num="05", title="Set 5: The weekly check-in",
         beats=[
             dict(say="Set five. Dana trains with me twice a week and follows a home plan online. Between sessions she sends check-ins, and so do my other online clients. Replies can eat Sunday."),
             dict(card=("A check-in template", "The same few questions each week, in a friendly tone"),
                  say="Ask an assistant to draft a short weekly check-in: how did the sessions feel, what got in the way, what was one win. The same questions make answers easy to compare."),
             dict(card=("Reply faster, still you", "Rough notes in; a clear reply you edit before sending"),
                  say="When replies pile up, type rough notes, like: great consistency, move Thursday, praise the early starts. Ask for a warm reply. Read it, fix it, and send it yourself."),
             dict(card=("Pain is a hand-off", "Pain, injury or diet questions go to a professional"),
                  say="If Dana mentions pain, dizziness or a diet question, I don't ask a chatbot. She sees her doctor, a physio or a registered dietitian. Her training plan comes from my own qualifications."),
         ]),
    dict(kind="cards", num="06", title="Set 6: Content that's true",
         beats=[
             dict(tts="Set six: marketing. A small studio lives on word of mouth and a few honest posts each week. A I can speed up writing and editing, but it must never invent results.",
                  say="Set six: marketing. A small studio lives on word of mouth and a few honest posts each week. AI can speed up writing and editing, but it must never invent results."),
             dict(card=("Descript", "Edit a video by editing its transcript; cut filler words"),
                  say="Film a quick tip on your phone, then open it in Descript. You edit the video by deleting words in the transcript, and it can remove ums and uhs in bulk."),
             dict(card=("Canva Magic Write", "Drafts and shortens captions inside your design"),
                  say="In Canva, Magic Write drafts and shortens text. Try: three caption ideas for a beginner strength class, friendly, no hype. Then rewrite them so they sound like you."),
             dict(card=("Ask before you post", "Written consent for photos, quotes or progress stories"),
                  tts="Dana is proud of her progress. Still, ask in writing before you share her photo, quote or story. And never let A I add promises like guaranteed results.",
                  say="Dana is proud of her progress. Still, ask in writing before you share her photo, quote or story. And never let AI add promises like guaranteed results."),
         ]),
    dict(kind="cards", num="07", title="Set 7: Coach the coach",
         beats=[
             dict(say="Set seven is mine. Good trainers keep learning: courses, certifications, new research, and the business side. An assistant can be a patient study partner, if I check its sources."),
             dict(card=("Gemini Guided Learning", "A tutor mode that explains a topic step by step"),
                  say="Gemini has a Guided Learning mode that works like a tutor. Studying for a certification? Ask it to explain the course terms step by step, then quiz you on them."),
             dict(card=("Read the long paper", "Upload a PDF; ask for main points with page numbers"),
                  tts="Claude and other assistants accept P D F uploads. Upload a course handout or a published study and ask for the main points with page numbers. Then read those pages yourself.",
                  say="Claude and other assistants accept PDF uploads. Upload a course handout or a published study and ask for the main points with page numbers. Then read those pages yourself."),
             dict(card=("Bring better questions", "Turn your notes into questions for a mentor or tutor"),
                  say="Before a mentoring call or workshop, ask: turn my notes into clear questions. The answers come from qualified people and good sources, never from a chatbot alone."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="Before the cool-down, here are three rules for any trainer using A I, whatever app you choose. They protect your clients, your reputation and your small studio.",
                  say="Before the cool-down, here are three rules for any trainer using AI, whatever app you choose. They protect your clients, your reputation and your small studio."),
             dict(card=("1   Stay in your lane", "Health, injury, rehab and diet go to qualified professionals"),
                  tts="Rule one: stay in your lane. Diets, pain, injuries and rehab belong to doctors, physios and registered dietitians. Programming comes from your own qualifications. A I helps with admin and words.",
                  say="Rule one: stay in your lane. Diets, pain, injuries and rehab belong to doctors, physios and registered dietitians. Programming comes from your own qualifications. AI helps with admin and words."),
             dict(card=("2   Guard client data", "Health answers stay out of unapproved AI tools"),
                  say="Rule two: guard client data. Health forms, notes, photos and messages are private. Share only what a task needs, use tools your business approved, and read each app's data terms."),
             dict(card=("3   Your name is on it", "Check every message, date and claim before it goes out"),
                  say="Rule three: your name is on it. Read every draft before you send or post it. Check dates, addresses and claims, and never promise results. Clients trust you, not the software."),
         ]),
    dict(kind="title", title="Cool-down", year="",
         sub="Pick one set and try it with your next client.",
         beats=[
             dict(say="You don't need all seven sets this week. Pick the one that costs you the most time, maybe the booking page or the check-in template, and try it with your next client."),
             dict(tts="This channel is A I for Every Job. Every episode takes one profession and shows what A I can really do for it. Subscribe, and tell us in the comments which job we should cover next.",
                  say="This channel is AI for Every Job. Every episode takes one profession and shows what AI can really do for it. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
