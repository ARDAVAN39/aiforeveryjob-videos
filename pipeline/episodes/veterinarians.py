"""Episode: AI for Veterinarians in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

# Named tools, each confirmed on the vendor's own site (November 2026):
# - PetDesk automated reminders (owner-chosen channel, confirm/cancel link, pre-visit instructions):
#     https://petdesk.com/product/feature/automated-reminders
# - Weave Smart Drafts (suggests replies to inbound messages): https://getweave.com/ai/
# - Gemini "Take notes for me" in Google Meet (notes in a shareable Google Doc):
#     https://support.google.com/meet/answer/14754931
# - ScribbleVet (records visit or dictation, drafts SOAP note; client summary emails; Care Cards
#     handout from discharge instructions): https://scribblevet.com/
# - Scribenote (SOAP and other formats; client summaries; callbacks; free consent form template
#     and recording notice): https://scribenote.com/
# - VetRec (AI veterinary scribe for SOAP notes and records): https://www.vetrec.io/solutions
# - ezyVet AI-Assisted Notes (draft SOAP notes inside ezyVet, clinician reviews and approves; beta):
#     https://www.ezyvet.com/ezyvet-ai-consultation
# - Copilot in Outlook (summarises an email thread; may include citations):
#     https://support.microsoft.com/topic/a79873f2-396b-46dc-b852-7fe5947ab640
# - ChatGPT file uploads (PDFs, summaries, questions): https://help.openai.com/en/articles/8555545-file-uploads-faq
# - Claude file uploads (PDFs): https://support.claude.com/en/articles/8241126-upload-files-to-claude

CHANNEL = "AI for Every Job"
PRESENTER = "veterinarian"
VOICE = "af_heart"
EPISODE = "AI for Veterinarians in 2026"

SCENES = [
    dict(kind="title", title="AI for Veterinarians", year="2026",
         sub="One beagle. One visit. Every page of paperwork.",
         beats=[
             dict(say="Meet Biscuit, a fictional beagle with an itchy ear. His visit takes twenty minutes in the exam room, and far longer in messages, records, and phone calls around it."),
             dict(say="So today we follow Biscuit from the moment his owner books, through the exam and the records, to the follow up call, and see where AI can lighten the paperwork."),
             dict(say="A clear line first. This is about admin, records, and communication. AI does not diagnose, choose treatment, or set doses. Every clinical call and every signature stays with the vet."),
         ]),
    dict(kind="cards", num="01", title="Biscuit gets booked",
         beats=[
             dict(say="Stage one: the booking. Biscuit's owner sends a message late on Sunday. On Monday morning the front desk faces dozens like it, plus reminders that still need to go out."),
             dict(card=("PetDesk reminders", "Automatic reminders with a link to confirm or cancel"),
                  tts="Pet Desk can send automatic reminders before a visit, by email, text, app notification, or postcard. Owners confirm or cancel from a link, and you can add pre visit instructions.",
                  say="PetDesk can send automatic reminders before a visit, by email, text, app notification, or postcard. Owners confirm or cancel from a link, and you can add pre-visit instructions."),
             dict(card=("Weave Smart Drafts", "Suggested replies to incoming client messages"),
                  say="If your clinic uses Weave for phones and texting, it lists a feature called Smart Drafts that suggests replies to incoming messages. A team member still reads and edits each one."),
             dict(card=("Write your templates", "Friendly booking replies the whole team can reuse"),
                  say="With any assistant, try: write five short, friendly replies for booking requests, a new client, a reschedule, and a waitlist. Then your team adjusts them to the clinic's voice."),
         ]),
    dict(kind="cards", num="02", title="The morning huddle",
         beats=[
             dict(say="Stage two: the huddle before doors open. Biscuit is one of many appointments today, and the team needs to know who covers what, without a long meeting."),
             dict(card=("Draft the day plan", "Shifts, breaks and cover from first names and roles"),
                  tts="Give an assistant first names, roles, and shift times, and ask: draft today's cover plan, with lunch breaks staggered so reception and the vet tech station are never empty.",
                  say="Give an assistant first names, roles, and shift times, and ask: draft today's cover plan, with lunch breaks staggered so reception and the vet tech station are never empty."),
             dict(card=("Take notes for me", "Gemini in Google Meet saves notes to a shared doc"),
                  say="For a weekly team meeting on Google Meet, Gemini has a feature called take notes for me. It writes the notes into a Google Doc that you can share with everyone."),
             dict(card=("A checklist, not a memo", "Turn meeting notes into owners and next steps"),
                  say="Then paste the notes and ask: turn this into a checklist with one owner per task. Read it before posting, because summaries sometimes drop the one detail that mattered."),
         ]),
    dict(kind="cards", num="03", title="In the exam room",
         beats=[
             dict(say="Stage three: the exam. Biscuit's owner is talking, Biscuit is wriggling, and the vet is trying to type. This is where veterinary AI scribes come in."),
             dict(card=("ScribbleVet", "Record the visit or dictate, get a draft SOAP note"),
                  tts="Scribble Vet records the appointment, or your dictation, and drafts a formatted S O A P note within minutes. It says off topic chatter is filtered out of the record.",
                  say="ScribbleVet records the appointment, or your dictation, and drafts a formatted SOAP note within minutes. It says off-topic chatter is filtered out of the record."),
             dict(card=("Scribenote", "Draft notes in SOAP and other formats"),
                  tts="Scribenote turns speech into structured notes, in S O A P and other formats, and connects to several practice management systems. Vet Rec is another scribe built for veterinary records.",
                  say="Scribenote turns speech into structured notes, in SOAP and other formats, and connects to several practice management systems. VetRec is another scribe built for veterinary records."),
             dict(card=("Ask before you record", "Tell the owner, get consent, follow clinic policy"),
                  say="Before you press record, tell the owner and get their consent. Scribenote even offers a free consent form template and recording notice. Follow your clinic's policy and local rules."),
             dict(tip="Only use scribes your practice has approved. Client data stays protected.",
                  say="Only use a scribe your practice has approved and checked for data protection. Client names, addresses, and payment details never go into a random free app."),
         ]),
    dict(kind="cards", num="04", title="Biscuit's record",
         beats=[
             dict(say="Stage four: the record. The scribe hands you a draft for Biscuit. It is fast and tidy, but it is still a draft, and the medical record carries your name."),
             dict(card=("ezyVet AI-Assisted Notes", "Draft SOAP notes in ezyVet, approved by the clinician"),
                  tts="If you use ezy Vet, its A I Assisted Notes feature, currently in beta, drafts S O A P notes inside the system. The clinician reviews and approves the draft. Nothing goes in by itself.",
                  say="If you use ezyVet, its AI-Assisted Notes feature, currently in beta, drafts SOAP notes inside the system. The clinician reviews and approves the draft. Nothing goes in by itself."),
             dict(card=("Read every line", "Check what was heard, what was missed, what was added"),
                  say="Read each section as if a colleague wrote it. Did it mishear the owner? Did it add something nobody said? Scribes can sound confident and still be wrong."),
             dict(card=("Your judgement only", "The assessment and plan are yours, not the software's"),
                  say="The assessment and the plan come from your examination and your professional judgement. Never accept wording that suggests a finding or a decision you did not make. Then sign."),
         ]),
    dict(kind="cards", num="05", title="Biscuit goes home",
         beats=[
             dict(say="Stage five: going home. You have already decided Biscuit's care and written the instructions. Now the owner needs to understand them, at the counter and again tonight at home."),
             dict(card=("Client summary emails", "ScribbleVet drafts a friendly visit recap to send"),
                  tts="Scribble Vet can draft a client friendly recap email from the visit, and its Care Cards feature turns your discharge instructions into a printable handout. Read both before they go.",
                  say="ScribbleVet can draft a client-friendly recap email from the visit, and its Care Cards feature turns your discharge instructions into a printable handout. Read both before they go."),
             dict(card=("Plainer words", "Reword instructions you wrote, without changing meaning"),
                  say="With an approved assistant, paste your own instructions with no client details and ask: rewrite this for a worried owner, short steps, no jargon, and change nothing about the care."),
             dict(card=("Another language", "A fluent colleague checks before the owner sees it"),
                  say="If the owner reads Spanish more easily, AI can translate the explanation you wrote. Ask a fluent colleague to check it, because a wrong word in care instructions really matters."),
         ]),
    dict(kind="cards", num="06", title="The follow-up call",
         beats=[
             dict(say="Stage six: three days later, someone calls to ask how Biscuit is doing. Good follow up builds trust, but the calls and emails pile up after a busy week."),
             dict(card=("Scribenote callbacks", "Help with callback notes and client summaries"),
                  say="Scribenote lists callbacks for client communication among its features, alongside client summaries. That helps the team record the call, but the vet decides what happens next."),
             dict(card=("A call checklist", "Questions from your own plan, so nothing is skipped"),
                  tts="Ask an assistant: turn my follow up plan into a short call checklist for a vet tech, with space for the owner's answers, and a line saying when to bring the vet in.",
                  say="Ask an assistant: turn my follow-up plan into a short call checklist for a vet tech, with space for the owner's answers, and a line saying when to bring the vet in."),
             dict(card=("Copilot in Outlook", "Summarises a long email thread at the top"),
                  say="When a referral or a client complaint has turned into a long email chain, Copilot in Outlook can summarise the thread, and may cite the emails it used. Then you reply yourself."),
         ]),
    dict(kind="cards", num="07", title="After Biscuit: you",
         beats=[
             dict(say="Stage seven is you. Biscuit is home, the clinic is quiet, and you still have continuing education to log, journal articles to read, and a body that needs rest."),
             dict(card=("ChatGPT · Claude", "Upload a public PDF and ask for the key points"),
                  tts="Chat G P T and Claude both accept P D F uploads. Try: summarise this association guideline in ten points, with the page number for each, so I can read the right sections first.",
                  say="ChatGPT and Claude both accept PDF uploads. Try: summarise this association guideline in ten points, with the page number for each, so I can read the right sections first."),
             dict(card=("Quiz yourself", "Questions from the document, one at a time"),
                  say="After reading, ask it to quiz you on that document, one question at a time. It turns passive reading into active learning. The original document stays the authority."),
             dict(card=("Guard your evenings", "Batch the admin, then close the laptop"),
                  say="And ask for help with your own load: here are my unfinished tasks, sort them into today, this week, and someone else's job. Then go home. Burnout is not a badge."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(say="To finish, three rules for any vet using AI. They protect your patients, your clients, and your licence, whichever tools your clinic ends up choosing."),
             dict(card=("1   Consent and privacy", "Ask before recording. Approved tools only."),
                  say="Rule one: consent and privacy. Ask owners before you record, keep client data in tools your practice has approved, and follow its policy and your local data laws."),
             dict(card=("2   The vet decides", "No AI for diagnosis, treatment or doses"),
                  say="Rule two: the vet decides. AI drafts words. It does not diagnose, choose treatment, set doses, or triage. Clinical judgement stays with you and your training."),
             dict(card=("3   Review and sign", "Every record and message is checked by you"),
                  say="Rule three: review, then sign. Every note, handout, and message is a draft until you have checked it. Follow your regulator and professional body, because your name is on it."),
         ]),
    dict(kind="title", title="Start with one stage", year="",
         sub="Pick one stage of Biscuit's visit and try it this week.",
         beats=[
             dict(say="You do not need to change the whole visit at once. Choose one stage, perhaps booking replies or the discharge handout, try it this week, and see what it saves."),
             dict(say="This channel is AI for Every Job. Each episode takes one profession and shows what AI can really do for it. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
