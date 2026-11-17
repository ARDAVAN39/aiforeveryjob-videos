"""Episode: AI for Farmers in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

# Named tools, each confirmed on the vendor's own site (November 2026):
# - Gemini in Google Sheets (create tables, create formulas, build charts and graphs, data analysis;
#     eligible Workspace or Google AI plan): https://support.google.com/docs/answer/14218565
# - Gemini Apps file uploads (documents, spreadsheets, photos):
#     https://support.google.com/gemini/answer/14903178
# - Gemini Guided Learning (tutor; "breaks down problems step-by-step"): https://support.google.com/gemini/answer/16448384
#     and https://blog.google/outreach-initiatives/education/guided-learning/
# - Claude file uploads (PDF and images): https://support.claude.com/en/articles/8241126-upload-files-to-claude
# - ChatGPT image inputs, incl. iOS/Android app (tap + to add an image):
#     https://help.openai.com/en/articles/8400551-image-inputs-for-chatgpt-faq
# - ChatGPT Voice (spoken conversation, talk through your thoughts): https://chatgpt.com/features/voice/
# - Phone dictation (iPhone: dictate text instead of typing):
#     https://support.apple.com/guide/iphone/dictate-text-iph2c0651d2/ios
# - Google Translate conversation mode (take turns speaking, translations play out loud):
#     https://support.google.com/translate/answer/6142474
# - Google Translate camera (translate signs or handwritten notes):
#     https://support.google.com/translate/answer/6142483
# - Canva Magic Write (draft, rewrite, expand, shorten): https://www.canva.com/features/ai-writing-assistant/
# - Canva Magic Design (turns ideas into designs): https://www.canva.com/newsroom/news/magic-studio/

CHANNEL = "AI for Every Job"
PRESENTER = "farmer"
VOICE = "am_michael"
EPISODE = "AI for Farmers in 2026"

SCENES = [
    dict(kind="title", title="AI for Farmers", year="2026",
         sub="One farming year, season by season.",
         beats=[
             dict(tts="I farm with my family: vegetables, a few beef cattle, and a stand by the road. The work is outside, but planning, paperwork and selling never stop. That is where A I helps.",
                  say="I farm with my family: vegetables, a few beef cattle, and a stand by the road. The work is outside, but planning, paperwork and selling never stop. That is where AI helps."),
             dict(say="So we walk through one farming year, season by season: winter plans and paperwork, spring records and crew, summer notes, harvest selling, and learning in the quiet months."),
             dict(tts="One clear line first. This is about admin, records, planning, learning and marketing. A I gives no spray, feed, animal health or money advice here. Labels and local experts decide those.",
                  say="One clear line first. This is about admin, records, planning, learning and marketing. AI gives no spray, feed, animal health or money advice here. Labels and local experts decide those."),
         ]),
    dict(kind="cards", num="01", title="Winter: plan the year",
         beats=[
             dict(say="Winter, part one: planning. The fields are quiet and the kitchen table is covered in notes. Time to turn last year's lessons into this year's plan."),
             dict(card=("Last year, on one page", "Paste last season's notes; ask what worked and what did not"),
                  tts="Paste last season's notes into Chat G P T, Claude or Gemini and ask: summarise what worked, what went wrong, and which questions I should raise with my adviser this winter.",
                  say="Paste last season's notes into ChatGPT, Claude or Gemini and ask: summarise what worked, what went wrong, and which questions I should raise with my adviser this winter."),
             dict(card=("A year of jobs", "Your own plan turned into a month-by-month job calendar"),
                  say="Then give it the plan you already made and ask: turn this into a month by month calendar of jobs, orders and deadlines, as a table I can print."),
             dict(card=("Gemini in Sheets", "Creates tables and formulas from a plain request"),
                  say="If you use Google Sheets on an eligible plan, Gemini can create tables and formulas from a plain request. Try: make a seed order sheet with supplier, quantity and delivery date."),
         ]),
    dict(kind="cards", num="02", title="Winter: the paper pile",
         beats=[
             dict(say="Winter, part two: paperwork. Scheme letters, inspection forms, contracts, and a box of receipts. Nobody became a farmer for this part, but it must be done before spring."),
             dict(card=("Read the long letter", "Upload a PDF; ask for every deadline and page number"),
                  tts="Claude accepts P D F uploads, and so do other assistants. Upload a long scheme guidance document and ask: list every deadline and every document I must send, with page numbers.",
                  say="Claude accepts PDF uploads, and so do other assistants. Upload a long scheme guidance document and ask: list every deadline and every document I must send, with page numbers."),
             dict(card=("Draft the reply", "Short, polite letters from the points you give it"),
                  say="Writing to a buyer, a landlord, or the council? Give it your points and ask for a short, polite letter. Then check every fact and date."),
             dict(card=("The accountant decides", "AI can explain a term; tax and grants need a professional"),
                  say="An assistant can explain a word on a form, but can be confidently wrong. Tax, grants, loans and contracts go to your accountant or adviser, and the official guidance decides."),
         ]),
    dict(kind="cards", num="03", title="Spring: records that last",
         beats=[
             dict(say="Spring arrives, and so does the rush. Good records make next winter's planning possible, and a buyer or inspector may ask for them. Here an assistant saves real evenings."),
             dict(card=("Photo of the notebook", "Snap a handwritten page; ask for it as a clean table"),
                  tts="Photograph a notebook page and add it to Chat G P T, Claude or the Gemini app. Ask: turn this into a table with date, field, job, and who did it.",
                  say="Photograph a notebook page and add it to ChatGPT, Claude or the Gemini app. Ask: turn this into a table with date, field, job, and who did it."),
             dict(card=("Sheets that answer back", "Gemini in Sheets can build charts from your data"),
                  say="Check each line against the page, then paste it in. Gemini in Sheets can build charts too. Ask: chart our farm stand sales by week, and show the best weeks."),
             dict(card=("Official records first", "Required records follow the rules, not the chatbot"),
                  say="Some records, like animal movements or spray records, follow official rules and formats. Use the forms your authority requires. An assistant can tidy notes, never decide what goes in them."),
         ]),
    dict(kind="cards", num="04", title="Spring: the new crew",
         beats=[
             dict(say="Spring also brings seasonal workers. Clear instructions keep people safe and save you explaining the same job ten times, especially when not everyone shares your first language."),
             dict(card=("Write it once, clearly", "Short numbered steps for the jobs you explain every year"),
                  say="Talk through a job, like washing and packing salad, and ask: turn this into short numbered steps for someone on their first day. Then walk through it together."),
             dict(card=("Google Translate", "Conversation mode for talking; camera for signs"),
                  say="Google Translate has a conversation mode. Two people take turns speaking, and the translation plays out loud. Its camera can also translate signs and handwritten notes."),
             dict(card=("Check the safety words", "A fluent speaker checks before anyone relies on it"),
                  say="But a wrong word in a safety instruction really matters. Machine and chemical rules come from the manufacturer and the label. Have a fluent speaker check it first."),
         ]),
    dict(kind="cards", num="05", title="Summer: notes by voice",
         beats=[
             dict(say="Summer: long days, dirty hands, and no time to type. This is where voice helps most, because you can capture the day while it is still fresh."),
             dict(card=("Talk, then tidy", "Dictate on your phone, then ask for a clean daily log"),
                  say="Standing at the gate, tap the microphone on your phone's keyboard and speak your notes: which field, what you did, what broke. Later, ask for a tidy daily log."),
             dict(card=("ChatGPT Voice", "A spoken conversation to talk through tomorrow"),
                  tts="Chat G P T Voice lets you have a spoken conversation. After work, try: help me plan tomorrow. The baler needs fixing, two people are off, and the stand needs restocking.",
                  say="ChatGPT Voice lets you have a spoken conversation. After work, try: help me plan tomorrow. The baler needs fixing, two people are off, and the stand needs restocking."),
             dict(card=("The Sunday look back", "A week of scraps turned into a short summary"),
                  say="On Sunday evening, paste the week's notes and ask: what happened this week, what is still open, and what should I tell the family at breakfast? Scraps become a plan."),
             dict(tip="Never use a phone or AI while driving a tractor or running machinery. Stop first.",
                  say="One safety line I never bend. Never use a phone or an assistant while driving a tractor or running machinery. Stop, switch off, and step down first. The notes can wait."),
         ]),
    dict(kind="cards", num="06", title="Harvest: the farm stand",
         beats=[
             dict(say="Harvest: the best season, and the busiest. The crops are ready, and now people need to find them. An assistant helps with words and pictures."),
             dict(card=("Canva Magic Studio", "Magic Design builds a layout; Magic Write drafts the text"),
                  say="In Canva, Magic Design turns a typed idea into a design you can edit, and Magic Write drafts and shortens text. Try: a chalkboard style price sign."),
             dict(card=("The weekly newsletter", "What is fresh, a simple recipe idea, and opening hours"),
                  say="For your email newsletter, list what is fresh and ask: write a warm note with this week's harvest, a simple recipe idea, and our opening hours. Add a real photo."),
             dict(card=("Posts that sound like you", "Real photos, your voice, and no invented claims"),
                  say="For social posts, paste two you wrote and ask it to match your voice. Never let it add words like organic or grass fed unless they are true and allowed."),
         ]),
    dict(kind="cards", num="07", title="Off season: keep learning",
         beats=[
             dict(say="Then the year turns again. In the quiet months, farmers learn: new rules, new ideas, new ways to sell. An assistant can be a patient study partner at any hour."),
             dict(card=("Gemini Guided Learning", "A tutor mode that explains a topic step by step"),
                  say="Gemini has a Guided Learning mode that works like a tutor. Ask it to explain how an online farm shop works, step by step, and keep asking until it clicks."),
             dict(card=("Bring better questions", "Prepare for the adviser, the agronomist or the vet"),
                  say="Before you meet an agronomist, extension adviser or vet, ask: help me write clear questions, so I forget nothing. The answers come from them, not from the chatbot."),
             dict(card=("Read the report fast", "Main points of a public report, with page numbers"),
                  say="Upload a public extension report and ask for the main points with page numbers. Then read those pages yourself, because a summary can miss what matters on your farm."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="To close the year, three rules for any farmer using A I. They protect your land, your animals, your workers and your business, whatever app you choose.",
                  say="To close the year, three rules for any farmer using AI. They protect your land, your animals, your workers and your business, whatever app you choose."),
             dict(card=("1   Labels and experts decide", "Sprays, crops, animals and money: ask a professional"),
                  say="Rule one: labels and experts decide. For pesticides, the product label. For crops, your agronomist or extension adviser. For animals, your vet. For money and tax, your accountant."),
             dict(card=("2   Guard your farm data", "Share only what a task needs; read each app's terms"),
                  say="Rule two: guard your farm data. Yields, prices, maps and worker details are valuable. Share only what a task needs, and read each app's data terms before you upload anything."),
             dict(card=("3   Stop, then type", "Engine off before any phone or AI; check every draft"),
                  tts="Rule three: stop, then type. No phone and no A I while driving or operating machinery. And check every draft, number and translation before anyone relies on it.",
                  say="Rule three: stop, then type. No phone and no AI while driving or operating machinery. And check every draft, number and translation before anyone relies on it."),
         ]),
    dict(kind="title", title="Start this season", year="",
         sub="Pick one idea for the season you are in and try it this week.",
         beats=[
             dict(say="You do not need the whole year at once. Pick one idea for the season you are in, maybe the winter plan or summer voice notes, and try it this week."),
             dict(tts="This channel is A I for Every Job. Every episode takes one profession and shows what A I can really do for it. Subscribe, and tell us in the comments which job we should cover next.",
                  say="This channel is AI for Every Job. Every episode takes one profession and shows what AI can really do for it. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
