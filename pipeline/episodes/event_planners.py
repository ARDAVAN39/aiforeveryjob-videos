"""Episode: AI for Event Planners in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

CHANNEL = "AI for Every Job"
PRESENTER = "event_planner"
VOICE = "am_michael"
EPISODE = "AI for Event Planners in 2026"

SCENES = [
    dict(kind="title", title="AI for Event Planners", year="2026",
         sub="One offsite. Seven documents. From brief to thank-you.",
         beats=[
             dict(tts="I'm an event planner. People picture flowers and stages, but my week is mostly documents: briefs, schedules, emails and forms. In 2026, A I helps me draft most of them.",
                  say="I'm an event planner. People picture flowers and stages, but my week is mostly documents: briefs, schedules, emails and forms. In 2026, AI helps me draft most of them."),
             dict(say="Instead of a tool tour, I'll follow one made up client, Fernhill, and their two day offsite for a hundred and twenty people, through seven documents."),
             dict(tts="Expect real example prompts and honest limits: what A I gets wrong, and what stays my job. Three rules at the end. Let's open the first file.",
                  say="Expect real example prompts and honest limits: what AI gets wrong, and what stays my job. Three rules at the end. Let's open the first file."),
         ]),
    dict(kind="cards", num="01", title="The one-page brief",
         beats=[
             dict(say="Document one: the brief. Dana, Fernhill's office manager, wants a two day offsite for a hundred and twenty people next spring. Her email is warm, but vague."),
             dict(card=("A Claude project", "Brief, venue notes and emails in one workspace"),
                  say="I open a Claude project for Fernhill. Its knowledge holds Dana's email and my call notes. Its instructions say: flag anything unclear, and never invent details."),
             # Verified: https://support.claude.com/en/articles/9517075-what-are-projects
             dict(card=("Draft the brief", "Goals, guests, dates, must-haves and open questions"),
                  say="Then I ask: turn these notes into a one page brief with goals, guest profile, dates, must haves, and open questions. Minutes later, I have a draft."),
             dict(card=("What is missing?", "Ask what an experienced planner would still need"),
                  say="Next: what would an experienced planner still need to know? It notices we have nothing on access needs, or partners. I ask Dana, and she confirms the brief in writing."),
         ]),
    dict(kind="cards", num="02", title="The venue shortlist",
         beats=[
             dict(say="Document two: the venue shortlist. Fernhill wants somewhere by a lake, within two hours of the office, with bedrooms and meeting rooms for the whole group of a hundred and twenty."),
             dict(card=("ChatGPT search", "Current web results with links to the sources"),
                  tts="Chat G P T search answers with links to its sources. I ask: find lakeside venues within two hours of the city that host residential groups of about a hundred and twenty.",
                  say="ChatGPT search answers with links to its sources. I ask: find lakeside venues within two hours of the city that host residential groups of about a hundred and twenty."),
             # Verified: https://help.openai.com/en/articles/9237897-chatgpt-search
             dict(card=("Questions per venue", "Capacity, step-free access, quiet rooms, food"),
                  say="For each one, I ask for the questions to put to the venue: step free access, a quiet room, dietary options, Wi-Fi, and where coaches can stop."),
             dict(card=("Call, then visit", "Web pages go out of date, so confirm directly"),
                  tts="Then I phone them. Web pages go out of date, and A I can mix up two venues. Nothing makes the shortlist until the venue confirms it, ideally on a site visit.",
                  say="Then I phone them. Web pages go out of date, and AI can mix up two venues. Nothing makes the shortlist until the venue confirms it, ideally on a site visit."),
         ]),
    dict(kind="cards", num="03", title="Supplier comparison",
         beats=[
             dict(say="Document three: the supplier comparison. Venue, caterer, coaches, sound and lighting. Every proposal arrives in its own format, which makes comparing them painfully slow work."),
             dict(card=("Request for proposal", "One clear request, so every supplier answers the same"),
                  say="First, I ask the assistant to turn the brief into one request for proposal, with the same questions for every supplier. Matching answers are far easier to compare."),
             dict(card=("Sheets: Help me organize", "Builds a new comparison table from a prompt"),
                  say="In Google Sheets, on eligible plans, Help me organize builds a new table from a prompt: supplier comparison for a company offsite, with inclusions, deadlines, and open questions."),
             # Verified: https://support.google.com/docs/answer/13951830?hl=en
             dict(card=("Contracts stay human", "An AI summary of terms is not legal advice"),
                  say="An assistant can list what a proposal says about cancellation, but that is not legal advice. I read contracts in full, and a lawyer does when it matters."),
             dict(tip="Verify every supplier directly. A chatbot mention is not a reference.",
                  tts="And verify every supplier yourself. Ask for references, confirm their details with them directly, and never trust a company just because an A I chat recommended it.",
                  say="And verify every supplier yourself. Ask for references, confirm their details with them directly, and never trust a company just because an AI chat recommended it."),
         ]),
    dict(kind="cards", num="04", title="The run-of-show",
         beats=[
             dict(say="Document four: the run of show, the minute by minute plan for both days. Who does what, when, and where. My whole crew works from it."),
             dict(card=("Agenda to run sheet", "Times, owners, rooms and cues for every session"),
                  say="In the Fernhill project, I paste Dana's agenda and ask: turn this into a run of show with times, owner, room, and technical cues for every session."),
             dict(card=("Find the pinch points", "Ask where the timings are too tight"),
                  say="Then: where is this schedule too tight? It spots that a hundred and twenty people cannot leave the main room, grab coffee, and reach three workshops in ten minutes."),
             dict(card=("Plan B for rain", "A backup for every outdoor session"),
                  say="Day two has a lakeside walk, so I ask for a wet weather plan using our booked indoor rooms. Then I check every room and time with the venue."),
         ]),
    dict(kind="cards", num="05", title="Invitation and sign-up",
         beats=[
             dict(say="Document five: the invitation and registration. A hundred and twenty people need the same clear information, and I need their answers back in one place."),
             dict(card=("Cvent AI Writing Assistant", "Event descriptions and emails, in the tone you pick"),
                  tts="Teams that register guests in Cvent can use its A I Writing Assistant for event descriptions and marketing emails. It rewrites drafts more formal or playful, shorter or longer.",
                  say="Teams that register guests in Cvent can use its AI Writing Assistant for event descriptions and marketing emails. It rewrites drafts more formal or playful, shorter or longer."),
             # Verified: https://www.cvent.com/en/event-marketing-management/ai-writing-assistant
             dict(card=("Google Forms", "Help me create builds a form from your prompt"),
                  say="Or Google Forms, on eligible plans, can build the registration form from a prompt. I ask for attendance, travel, dietary needs, access needs, and a contact for questions."),
             # Verified: https://support.google.com/docs/answer/16346789
             dict(card=("Ask only what you need", "Dietary and access details are personal data"),
                  say="Dietary and access details are personal data. I ask only what I need, say who will see it, and store it where the client allows. Never in a public chatbot."),
             dict(tip="You pass every need to the venue and caterer, then get it confirmed.",
                  say="And I pass every need to the venue and caterer, and get their confirmation back. A form collects answers. It does not guarantee anything to anyone."),
         ]),
    dict(kind="cards", num="06", title="The on-the-day pack",
         beats=[
             dict(say="Document six: the on the day pack. A crew briefing, a contact list, and session tools that keep a hundred and twenty people involved, not just listening."),
             dict(card=("Crew briefings", "One page per role, built from the run-of-show"),
                  say="From the run of show, I ask for a one page briefing per role: registration desk, room hosts, and coach marshal. Each person sees only what they need."),
             dict(card=("Slido AI", "Suggested polls, and help wording audience questions"),
                  tts="For the sessions, Fernhill uses Slido. Its A I can suggest polls from your meeting goal and audience size, and Question A I helps guests word their questions for the Q and A.",
                  say="For the sessions, Fernhill uses Slido. Its AI can suggest polls from your meeting goal and audience size, and Question AI helps guests word their questions for the Q&A."),
             # Verified: https://www.slido.com/ai
             dict(card=("Print the essentials", "Wi-Fi fails, so keep paper copies"),
                  tts="And I print the essentials: run of show, contacts, and the emergency plan. Wi-Fi fails at lakeside venues. On the day, A I is a helper, never the only copy.",
                  say="And I print the essentials: run of show, contacts, and the emergency plan. Wi-Fi fails at lakeside venues. On the day, AI is a helper, never the only copy."),
         ]),
    dict(kind="cards", num="07", title="Thank-you and survey",
         beats=[
             dict(say="Document seven: the thank you and the survey. The offsite is over, the coaches have gone, and Dana wants to know what worked before she plans next year."),
             dict(card=("Thank-you notes", "Built from real moments that you list yourself"),
                  say="I list real moments from the two days, like the speaker who stayed for questions, and ask for short thank you notes. Then I make each one personal."),
             dict(card=("Forms: summarise answers", "Gemini summarises open-text survey responses"),
                  say="In Google Forms, on eligible plans, Gemini can summarise open text answers once at least three responses are in. I still read the raw answers, especially critical ones."),
             # Verified: https://support.google.com/docs/answer/16231981
             dict(card=("The debrief report", "What worked, what to change, open actions"),
                  say="Finally: draft a debrief for Dana with what worked, what to change, and open actions. I check every line against the survey and my notes before sending."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(tts="Before you try any of this, here are three rules. They protect your guests, your clients, and your reputation, whatever A I tools you end up choosing.",
                  say="Before you try any of this, here are three rules. They protect your guests, your clients, and your reputation, whatever AI tools you end up choosing."),
             dict(card=("1   Protect guest data", "Approved tools only, and leave personal details out"),
                  say="Rule one: protect guest data. Names, dietary and access needs belong only in tools your client or company approved. Leave personal details out of what you paste."),
             dict(card=("2   Confirm at the source", "Venues and suppliers confirm, not chatbots"),
                  tts="Rule two: confirm at the source. Availability, capacity, menus, and access all come from the venue and suppliers directly. A I can be confidently wrong about every one of them.",
                  say="Rule two: confirm at the source. Availability, capacity, menus, and access all come from the venue and suppliers directly. AI can be confidently wrong about every one of them."),
             dict(card=("3   You own the promises", "People read contracts and check every need is met"),
                  tts="Rule three: you own every promise. A I drafts, but people read contracts, and lawyers advise on them. When you tell a guest their needs are covered, make sure they are.",
                  say="Rule three: you own every promise. AI drafts, but people read contracts, and lawyers advise on them. When you tell a guest their needs are covered, make sure they are."),
         ]),
    dict(kind="title", title="Open one document", year="",
         sub="Pick one document from Fernhill's offsite and try it this week.",
         beats=[
             dict(tts="You don't have to change everything at once. Pick one document, maybe your next brief or run of show, try A I on it this week, and build from there.",
                  say="You don't have to change everything at once. Pick one document, maybe your next brief or run of show, try AI on it this week, and build from there."),
             dict(tts="This channel is A I for Every Job. Each episode shows what A I can really do for one profession. Subscribe, and tell us in the comments which job to cover next.",
                  say="This channel is AI for Every Job. Each episode shows what AI can really do for one profession. Subscribe, and tell us in the comments which job to cover next."),
         ]),
]
