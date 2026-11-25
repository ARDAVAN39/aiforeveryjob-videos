"""Episode: AI for Consultants in 2026.
Each scene: kind, number, title, beats. Each beat: say (narration), optional tts (pronunciation override),
optional card (name, description) or tip (text) that appears when the beat starts."""

CHANNEL = "AI for Every Job"
PRESENTER = "consultant"
VOICE = "af_heart"
EPISODE = "AI for Consultants in 2026"

# Sources for product claims:
# Copilot in Word, drafts from notes or referenced files: https://support.microsoft.com/en-us/copilot-word
# ChatGPT deep research, cited reports and stated limitations: https://openai.com/index/introducing-deep-research/
# Copilot in Teams meetings, recap, questions, transcription, external meetings: https://support.microsoft.com/en-us/office/use-copilot-in-microsoft-teams-meetings-0bf9dd3c-96f7-44e2-8bb8-790bedf066b1
# Claude projects, files as project knowledge: https://support.claude.com/en/articles/9517075-what-are-projects
# Copilot in PowerPoint, deck from a Word document with a template: https://support.microsoft.com/en-us/copilot-powerpoint
# Copilot in Excel, charts, PivotTables, trends and outliers: https://support.microsoft.com/copilot-excel

SCENES = [
    dict(kind="title", title="AI for Consultants", year="2026",
         sub="Research. Interviews. Storylines. Decks. Client trust.",
         beats=[
             dict(say="Consultants are paid for judgement, yet much of the week goes on reading, notes, and moving boxes on slides. AI can carry that load, if you guard client trust."),
             dict(say="So let's run one made up engagement together. Your client is a regional bakery chain. Bread keeps reaching its shops late, and the operations director wants to know why."),
             dict(say="We go from proposal to final readout: research, interviews, the issue tree, the storyline, the numbers, and the handover. Then three rules for keeping clients safe."),
         ]),
    dict(kind="cards", num="01", title="Scope the engagement",
         beats=[
             dict(say="Stage one: the proposal. After the first call, you have a page of rough notes and a deadline. Before any of it touches an AI tool, check two things."),
             dict(card=("Policy and contract first", "Your firm's AI policy, then the client's contract or NDA"),
                  tts="Read your firm's AI policy, then the client's contract or N D A. If they rule out outside tools, that settles it. Use approved enterprise tools, never a personal account.",
                  say="Read your firm's AI policy, then the client's contract or NDA. If they rule out outside tools, that settles it. Use approved enterprise tools, never a personal account."),
             # https://support.microsoft.com/en-us/copilot-word
             dict(card=("Copilot in Word", "A first draft from your notes, or from files you reference"),
                  say="If your firm uses Copilot in Word, ask: draft a short proposal from these notes, with the problem, objectives, scope, approach, and what is out of scope."),
             dict(card=("Play the sceptical partner", "What is vague, too big, or impossible in the time?"),
                  say="Then say: act as a sceptical partner. What is vague, what is too big for the time we have, and what could the client misread? Fix those lines."),
             dict(tip="Anonymise first: Bakery A, Site 1. No real names, staff or customer details.",
                  say="And anonymise as you go. Call the client Bakery A, and the shops Site one and Site two. The assistant needs the shape of the problem, not real names."),
         ]),
    dict(kind="cards", num="02", title="Desk research, cited",
         beats=[
             dict(say="Stage two: the fact base. Before any interview, learn how bakery distribution usually works. This is public research, so let AI do the legwork first."),
             # https://openai.com/index/introducing-deep-research/
             dict(card=("ChatGPT deep research", "Searches the web and writes a report with citations"),
                  tts="Chat G P T has a mode called deep research. Ask: how do regional bakeries plan early deliveries, and what causes delays? It searches the web and returns a report with citations.",
                  say="ChatGPT has a mode called deep research. Ask: how do regional bakeries plan early deliveries, and what causes delays? It searches the web and returns a report with citations."),
             # https://openai.com/index/introducing-deep-research/ (limitations section)
             dict(card=("Open every citation", "AI can misread a source or overstate what it says"),
                  tts="Now open every source you plan to use. Open A I itself says deep research can get facts wrong, and struggle to tell reliable information from rumour.",
                  say="Now open every source you plan to use. OpenAI itself says deep research can get facts wrong, and struggle to tell reliable information from rumour."),
             dict(card=("Fact, claim or guess", "Sort each finding before it reaches a slide"),
                  say="Then sort your findings into three piles: checked facts, single source claims, and guesses. Only the first pile goes on a client slide without a caveat."),
         ]),
    dict(kind="cards", num="03", title="Client interviews",
         beats=[
             dict(say="Stage three: interviews. You will speak to night bakers, delivery drivers, shop managers, and the operations director. Each group sees a different piece of the problem."),
             dict(card=("A neutral interview guide", "Open questions, nothing that leads the answer"),
                  say="Ask an assistant: write an interview guide for a shop manager about late deliveries, open questions only. Then ask it to flag any question that leads the answer."),
             # https://support.microsoft.com/en-us/office/use-copilot-in-microsoft-teams-meetings-0bf9dd3c-96f7-44e2-8bb8-790bedf066b1
             dict(card=("Copilot in Teams", "Recaps and answers questions when transcription is on"),
                  say="If the call runs in your own Microsoft Teams with transcription on, Copilot can recap it and answer questions. It does not work in meetings another organisation hosts."),
             # https://support.claude.com/en/articles/9517075-what-are-projects
             dict(card=("Themes with quotes", "A Claude project for the notes, a quote behind each theme"),
                  say="Then add anonymised notes to a Claude project for the engagement, if your firm allows it, and ask: what themes come up, which quote supports each, and who disagrees?"),
             dict(tip="Ask permission before you record. Check every quote against your own notes.",
                  say="Always ask permission before you record or transcribe anyone. Then check each quote against your notes, because AI can blend two people's words into one."),
         ]),
    dict(kind="cards", num="04", title="Issue tree, hypotheses",
         beats=[
             dict(say="Stage four: structure. Turn facts and voices into an issue tree: one key question, split into branches that do not overlap and together cover everything."),
             dict(card=("Draft the tree", "One key question, branches that do not overlap"),
                  say="Ask: build an issue tree for the question, why does bread reach the shops late? A useful draft splits it into baking, loading, driving, and receiving. Ask what is missing."),
             dict(card=("Branches become tests", "For each hypothesis: what data would prove it wrong?"),
                  say="Turn each branch into a hypothesis. For example: loading starts late because shop orders arrive after the cut off. Then ask: what data would prove this wrong?"),
             dict(card=("You pick what to test", "AI lists options; your judgement sets the order"),
                  say="The assistant can list ten hypotheses in seconds. Choosing the two worth testing this week is your job, based on the interviews and your experience."),
         ]),
    dict(kind="cards", num="05", title="Storyline, then slides",
         beats=[
             dict(say="Stage five: the storyline. A good consulting habit is writing slide titles before building slides. AI redrafts fast, so throwing away a version costs little."),
             dict(card=("Answer first", "Pyramid principle: the answer, then the support"),
                  say="Use the pyramid principle: answer first, then reasons, then evidence. Ask: here are my findings, draft a storyline that opens with the answer, with three points beneath it."),
             dict(card=("Action titles", "Each title is a sentence that says what it means"),
                  say="Then ask for action titles. Not, delivery times, but: late mornings start in the loading bay, not on the road. Read the titles alone. Do they tell the story?"),
             # https://support.microsoft.com/en-us/copilot-powerpoint
             dict(card=("Copilot in PowerPoint", "A first draft deck from a Word file and your template"),
                  tts="With the storyline in a Word document, Copilot in Power Point can turn it into a first draft deck in your template. Expect to rewrite titles and rebuild charts.",
                  say="With the storyline in a Word document, Copilot in PowerPoint can turn it into a first draft deck in your template. Expect to rewrite titles and rebuild charts."),
         ]),
    dict(kind="cards", num="06", title="Check the numbers",
         beats=[
             dict(say="Stage six: the numbers. The client sends a spreadsheet of delivery times by shop and morning. An assistant can save hours here, and also be quietly wrong."),
             # https://support.microsoft.com/copilot-excel
             dict(card=("Copilot in Excel", "Ask questions; get charts, PivotTables and outliers"),
                  tts="In Excel, Copilot can answer questions with charts, Pivot Tables, and trends. Ask: which shops have the most late mornings, and does it change by weekday?",
                  say="In Excel, Copilot can answer questions with charts, PivotTables, and trends. Ask: which shops have the most late mornings, and does it change by weekday?"),
             dict(card=("Tie it to the source", "Match a total the client already trusts"),
                  say="Before you believe an answer, tie it back. Does the delivery count match the client's own report? Trace a few rows by hand. If anything differs, find out why."),
             dict(card=("Write the caveats", "Say plainly what the data cannot show"),
                  say="Then ask: what can this data not tell us? Perhaps it records when the van left, not when bread reached the shelf. Put limits like that on the slide."),
             dict(tip="Contract or money questions? Bring in qualified legal and finance advisers.",
                  say="If the client asks about supplier contracts or money, AI can help list the questions. But it is not legal or financial advice, and neither is this deck."),
         ]),
    dict(kind="cards", num="07", title="Readout and handover",
         beats=[
             dict(say="Final stage: the readout. The operations director and her team will push back, and they should. Be ready, and leave something the client can use."),
             dict(card=("Rehearse the room", "Let the assistant play the toughest listener"),
                  say="Ask the assistant to play a sceptical operations director: challenge every slide, one question at a time. Answer out loud. The questions you fumble show which slides to fix."),
             dict(card=("A one-page summary", "Answer, reasons, next steps and who owns each"),
                  say="Afterwards, give it your notes and the deck, and ask for a one page summary: the answer, the reasons, next steps, and owners. Then edit it yourself."),
             dict(card=("A clean handover", "Where files live, who owns what, data returned"),
                  say="Last, the handover: where files live, who owns each action, and what happens to client data. Return or delete files as the contract says, including anything in AI tools."),
         ]),
    dict(kind="cards", num="★", title="Three rules",
         beats=[
             dict(say="Before we finish, three rules for every consultant using AI. They protect your client, your firm, and your reputation, which is a big part of what you sell."),
             dict(card=("1   Client rules first", "AI policy, contract and NDA, then approved tools"),
                  tts="Rule one: client rules come first. Check your firm's AI policy and the client's contract or N D A, use only approved enterprise tools, and anonymise whatever you can.",
                  say="Rule one: client rules come first. Check your firm's AI policy and the client's contract or NDA, use only approved enterprise tools, and anonymise whatever you can."),
             dict(card=("2   You own the advice", "AI drafts; the recommendation carries your name"),
                  say="Rule two: you own the advice. AI can draft a proposal, a tree, or a deck. But the recommendation carries your name, so defend every line of it."),
             dict(card=("3   Trace every claim", "Each fact, quote and number back to its source"),
                  say="Rule three: trace every claim. Each fact to a source you opened, each quote to an interview, each number to the client's data. Otherwise, cut it."),
         ]),
    dict(kind="title", title="Start with one storyline", year="",
         sub="Pick one stage of your next engagement and try AI there.",
         beats=[
             dict(say="You do not need AI at every stage. On your next engagement, pick one, maybe the interview guide or the storyline, and see what thinking time it gives back."),
             dict(say="This channel is AI for Every Job. Each episode shows what AI can really do for one profession. Subscribe, and tell us in the comments which job we should cover next."),
         ]),
]
