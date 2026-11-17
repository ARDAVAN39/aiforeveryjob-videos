"""Episode: AI for Logistics and Delivery Drivers in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

# Angle: one parcel's journey, dispatch desk -> dock -> van -> doorstep -> return -> learning.
# Named tools, each confirmed on the vendor's own site (November 2026):
# - Onfleet route optimization ("AI route optimization software"; constraints incl. delivery windows
#     and vehicle capacity; "Build the most efficient routes in minutes, not hours"):
#     https://onfleet.com/route-optimization  https://onfleet.com/features
# - Onfleet predictive ETAs ("AI-powered ETAs update dynamically throughout the day and flag deliveries
#     at risk of running late"); customizable branded SMS notifications at every delivery stage;
#     proof of delivery (photos and signatures): https://onfleet.com/features
# - Google Translate conversation mode (take turns speaking; translations play out loud):
#     https://support.google.com/translate/answer/6142474
# - Google Translate camera (signs, handwritten notes; small/unclear text may not be accurate):
#     https://support.google.com/translate/answer/6142483
# - Claude file uploads (PDF, images): https://support.claude.com/en/articles/8241126-upload-files-to-claude
# - Gemini in Google Sheets (analyze data, identify trends, build charts; eligible plan;
#     "Outputs may be inaccurate"): https://support.google.com/docs/answer/14218565
# No legal, customs or hours-of-service rules are stated; viewers are referred to company, broker, regulator.

CHANNEL = "AI for Every Job"
PRESENTER = "logistics"
VOICE = "am_michael"
EPISODE = "AI for Logistics and Delivery Drivers in 2026"

SCENES = [
    dict(kind="title", title="AI for Logistics", year="2026",
         sub="One parcel: dock, van, doorstep, and back again.",
         beats=[
             dict(tts="A parcel looks simple: a box, a label, an address. Behind it are planners, warehouse crews and drivers, and piles of messages and paperwork. A I helps there.",
                  say="A parcel looks simple: a box, a label, an address. Behind it are planners, warehouse crews and drivers, and piles of messages and paperwork. AI helps there."),
             dict(say="So today we follow one parcel, a box of blue kitchen tiles, from the dispatch desk to the dock, the van, the doorstep, and back again."),
             dict(tts="One rule rides along the whole way. Never use a phone or A I while driving. Park with the engine off first, and follow your company's rules.",
                  say="One rule rides along the whole way. Never use a phone or AI while driving. Park with the engine off first, and follow your company's rules."),
         ]),
    dict(kind="cards", num="01", title="The order lands",
         beats=[
             dict(say="Stop one: the dispatch desk. The tile order arrives with hundreds of others, each with an address, a delivery window and a size. Someone turns that into routes."),
             # source: https://onfleet.com/route-optimization
             dict(card=("Onfleet route optimization", "AI builds routes around delivery windows and van capacity"),
                  tts="Delivery platforms like Onfleet offer A I route optimization. Planners set limits like delivery windows and vehicle capacity, and the software builds the routes for them.",
                  say="Delivery platforms like Onfleet offer AI route optimization. Planners set limits like delivery windows and vehicle capacity, and the software builds the routes for them."),
             dict(card=("Question the plan", "Paste a stop list, no names; ask what looks unrealistic"),
                  say="A general assistant can be a second pair of eyes. Paste a route summary without customer names and ask: which stops look tight, and why?"),
             dict(card=("Drivers know the street", "Loading bays, gates, stairs: local notes beat the map"),
                  say="But software may not know the tile shop's loading bay is blocked on Tuesday mornings. Drivers do. Add their notes, and the planner makes the final call."),
         ]),
    dict(kind="cards", num="02", title="On the dock",
         beats=[
             dict(say="Stop two: the warehouse. Our box is picked, scanned and staged for the van. The dock crew speaks four languages, and the night shift hands over at dawn."),
             dict(card=("Shift handover notes", "Messy notes into three lists: done, waiting, watch out"),
                  say="At the end of a shift, dictate quick notes, then ask an assistant: turn this into a handover with three headings, done, still waiting, and watch out."),
             # source: https://support.google.com/translate/answer/6142474
             dict(card=("Translate a conversation", "Google Translate: take turns speaking, hear it aloud"),
                  say="For a quick chat across languages, Google Translate has conversation mode. Each person takes a turn speaking, and the translation plays out loud on the phone."),
             # source: https://support.google.com/translate/answer/6142483
             dict(card=("Translate the sign", "Point the Translate camera at a sign or a written note"),
                  say="Its camera translates signs and handwritten notes too. Google warns small or unclear text may come out wrong, so safety instructions come from a trained colleague."),
         ]),
    dict(kind="cards", num="03", title="Papers that travel",
         beats=[
             dict(say="Stop three: paperwork. Our tiles cross a border, so they travel with a bill of lading and customs documents. Those papers are dense and full of jargon."),
             # source: https://support.claude.com/en/articles/8241126-upload-files-to-claude
             dict(card=("Explain this form", "Upload a blank sample; ask what each box and term means"),
                  tts="Claude accepts P D F uploads, and so do other assistants. Upload a blank sample and ask: explain each box on this bill of lading in plain words.",
                  say="Claude accepts PDF uploads, and so do other assistants. Upload a blank sample and ask: explain each box on this bill of lading in plain words."),
             dict(card=("Build a glossary", "Your own list: shipper, consignee, declared value"),
                  say="Then ask for a short glossary of the words you keep meeting, like shipper, consignee and declared value. Pin it by the desk for new starters."),
             dict(card=("The broker decides", "Codes, duties and rules come from brokers and officials"),
                  tts="The honest limit: A I can explain a word, but it can be confidently wrong. Customs codes, duties and rules come from your broker, your company and official sources.",
                  say="The honest limit: AI can explain a word, but it can be confidently wrong. Customs codes, duties and rules come from your broker, your company and official sources."),
         ]),
    dict(kind="cards", num="04", title="Behind the wheel",
         beats=[
             dict(say="Stop four: the van. Our driver loads the tiles and checks the route first. From then on, it is eyes on the road, hands on the wheel."),
             dict(card=("Parked, engine off", "Prompts and messages only when stopped, or off shift"),
                  say="Typing, prompting and reading happen parked with the engine off, or before and after the shift. A message that arrives while driving waits. No exceptions."),
             dict(card=("Approved apps only", "Company driver app; hours rules from company or regulator"),
                  say="Use the driver app your company approved, as trained. Questions about driving hours or breaks go to your company or the regulator's official guidance, never a chatbot."),
             # source: https://onfleet.com/features
             dict(card=("Late-stop warnings", "Onfleet's AI ETAs flag deliveries at risk of running late"),
                  tts="Meanwhile, dispatch watches the day. Onfleet says its A I powered E T As update throughout the day and flag deliveries at risk of running late, so the office can act early.",
                  say="Meanwhile, dispatch watches the day. Onfleet says its AI powered ETAs update throughout the day and flag deliveries at risk of running late, so the office can act early."),
         ]),
    dict(kind="cards", num="05", title="Nobody home",
         beats=[
             dict(say="Stop five: the doorstep. The driver rings twice. Nobody answers, and there is no safe place to leave heavy tiles. It is a failed delivery."),
             dict(card=("Missed-delivery templates", "Short, kind texts that say what happens next"),
                  say="In the office, ask an assistant: write three short, friendly messages for a missed delivery, saying what happens next and how to rebook. A manager approves the wording."),
             # source: https://onfleet.com/features
             dict(card=("Automatic text updates", "Onfleet: customizable SMS at every delivery stage"),
                  tts="Platforms can also send updates automatically. Onfleet, for example, sends customizable, branded S M S notifications at every delivery stage, so customers know what is happening.",
                  say="Platforms can also send updates automatically. Onfleet, for example, sends customizable, branded SMS notifications at every delivery stage, so customers know what is happening."),
             dict(card=("In their language", "Translate the template, then have a fluent speaker check"),
                  say="If the customer prefers another language, an assistant or Google Translate can draft a version. Before reusing it, ask a fluent colleague to check it."),
         ]),
    dict(kind="cards", num="06", title="A crushed corner",
         beats=[
             dict(say="Stop six: a scare. At the next stop the driver opens the van and finds a crushed corner on another box. Engine off, photos taken, as the process says."),
             # source: https://onfleet.com/features
             dict(card=("Proof in the app", "Photos and signatures captured in the delivery app"),
                  say="Delivery apps can capture proof. Onfleet's, for example, lets drivers take photos and collect signatures. Use your company's app, so evidence lands in the right place."),
             dict(card=("Notes into a report", "Dictate what you saw; ask for your company's headings"),
                  say="Still parked, dictate what you saw. Then ask: turn these notes into a short report with these headings: time, place, what I found, what I did."),
             dict(card=("Facts, not fault", "Describe what happened; your company handles the rest"),
                  tts="Keep it to facts you saw. Don't let A I add details or guess the cause. Questions about fault, claims and insurance go to your company, not a chatbot.",
                  say="Keep it to facts you saw. Don't let AI add details or guess the cause. Questions about fault, claims and insurance go to your company, not a chatbot."),
         ]),
    dict(kind="cards", num="07", title="The way back",
         beats=[
             dict(say="Stop seven: the return. Our customer ordered one box too many. The tiles head back to the warehouse, and returns bring their own messages and data."),
             dict(card=("Clear return steps", "Turn the returns policy into simple customer steps"),
                  say="Give an assistant your company's returns policy and ask: rewrite this as five simple steps a customer can follow. Then check it promises nothing extra."),
             # source: https://support.google.com/docs/answer/14218565
             dict(card=("Gemini in Sheets", "Ask a returns log for trends and a chart"),
                  say="If your returns log is in Google Sheets on an eligible plan, Gemini can find trends and build charts. Try: chart this month's most common return reasons."),
             dict(card=("Check the numbers", "Spot-check a few rows against the original records"),
                  say="Before that chart reaches your manager, spot check a few rows against the original records. Google itself says the output may be inaccurate, so checking stays your job."),
         ]),
    dict(kind="cards", num="08", title="New scanner, new skills",
         beats=[
             dict(say="Final stop: learning. The warehouse just rolled out new handheld scanners and a new system screen. Training was one rushed hour, and the manual is long."),
             # source: https://support.claude.com/en/articles/8241126-upload-files-to-claude
             dict(card=("Manual to quick-start", "Upload the manual; ask for a one-page cheat sheet"),
                  say="If your company allows it, upload the manual to an assistant like Claude and ask: make a one page quick start on logging in, scanning, and common errors."),
             dict(card=("Quiz me on it", "Five questions at a time, with the page to reread"),
                  say="Then ask: quiz me with five questions, and tell me which page to reread when I get one wrong. Ten minutes on a break beats guessing."),
             dict(card=("Ask a person too", "Your trainer and supervisor have the final word"),
                  say="When the screen does something strange, ask your supervisor or trainer. The manual and your workplace's process have the final word, not the assistant's guess."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="Our parcel is home. Before we finish, three rules for anyone in logistics who uses A I, on the dock, at the dispatch desk, or in the cab.",
                  say="Our parcel is home. Before we finish, three rules for anyone in logistics who uses AI, on the dock, at the dispatch desk, or in the cab."),
             dict(card=("1   Park, then prompt", "No phone or AI while driving; engine off, or off shift"),
                  tts="Rule one: park, then prompt. Never use a phone or A I while driving. Engine off, or before and after your shift, and always follow the road rules.",
                  say="Rule one: park, then prompt. Never use a phone or AI while driving. Engine off, or before and after your shift, and always follow the road rules."),
             dict(card=("2   Company rules first", "Approved apps; hours, customs and law from official sources"),
                  say="Rule two: company rules come first. Use approved apps. Driving hours, customs and legal questions go to your company, a broker, or the regulator, never a chatbot."),
             dict(card=("3   Guard customer data", "No names, addresses or numbers in unapproved tools"),
                  say="Rule three: guard customer data and check everything. Keep names, addresses and phone numbers out of unapproved tools, and read every draft before it goes out."),
         ]),
    dict(kind="title", title="Start with one stop", year="",
         sub="Pick one stop on this parcel's journey and try it this week.",
         beats=[
             dict(say="You don't need the whole journey at once. Pick one stop, maybe the shift handover or the missed delivery message, and try it this week. Parked, of course."),
             dict(tts="This channel is A I for Every Job. Every episode takes one profession and shows what A I can really do. Subscribe, and tell us in the comments which job we should cover next.",
                  say="This channel is AI for Every Job. Every episode takes one profession and shows what AI can really do. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
